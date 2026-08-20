"""Small, P4-compatible Qwen3 embedding service.

This intentionally uses Transformers instead of vLLM: Tesla P4 is compute
capability 6.1 and current vLLM/FlashAttention wheels generally require a
newer GPU. Requests are dynamically micro-batched so concurrent clients share
one forward pass without loading multiple copies of the model.
"""

from __future__ import annotations

import argparse
import asyncio
import os
import threading
import time
from dataclasses import dataclass
from typing import Any

import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from transformers import AutoModel, AutoTokenizer


DEFAULT_MODEL = "Qwen/Qwen3-Embedding-0.6B"


class EmbeddingRequest(BaseModel):
    model: str | None = None
    input: str | list[str]
    encoding_format: str = "float"
    dimensions: int | None = None


class SimpleEmbeddingRequest(BaseModel):
    texts: list[str] = Field(min_length=1)


@dataclass
class WorkItem:
    texts: list[str]
    future: asyncio.Future[list[list[float]]]


class EmbeddingEngine:
    def __init__(
        self,
        model_name: str,
        *,
        revision: str | None = None,
        max_batch_size: int = 16,
        max_batch_tokens: int = 8192,
        max_length: int = 8192,
        batch_wait_ms: float = 3.0,
    ) -> None:
        self.model_name = model_name
        self.max_batch_size = max_batch_size
        self.max_batch_tokens = max_batch_tokens
        self.max_length = max_length
        self.batch_wait_ms = batch_wait_ms
        self.queue: asyncio.Queue[WorkItem] = asyncio.Queue()
        self._worker_task: asyncio.Task[None] | None = None
        self._infer_lock = threading.Lock()

        if not torch.cuda.is_available():
            raise RuntimeError("未检测到 CUDA；此服务要求在装有 NVIDIA 驱动的服务器上运行")
        self.device = torch.device("cuda")
        # P4 supports FP16 but not BF16/Tensor Cores. Eager attention is the
        # compatible path and avoids flash-attn wheels compiled for newer GPUs.
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
        self.model = AutoModel.from_pretrained(
            model_name,
            torch_dtype=torch.float16,
            attn_implementation="eager",
            trust_remote_code=True,
        ).eval().to(self.device)
        self.dimension = int(getattr(self.model.config, "hidden_size", 1024))
        self.revision = revision or str(getattr(self.model.config, "_commit_hash", "") or "unknown")

    async def start(self) -> None:
        self._worker_task = asyncio.create_task(self._worker())

    async def stop(self) -> None:
        if self._worker_task:
            self._worker_task.cancel()
            await asyncio.gather(self._worker_task, return_exceptions=True)

    async def submit(self, texts: list[str]) -> list[list[float]]:
        if not texts or any(not isinstance(text, str) or not text.strip() for text in texts):
            raise ValueError("input 必须是非空字符串数组")
        if len(texts) > self.max_batch_size:
            raise ValueError(f"单次最多 {self.max_batch_size} 条文本")
        # One API request can contain long documents. Split it by an estimated
        # token budget before queueing, while keeping all sub-batches concurrent
        # so the worker can still merge them with other clients.
        groups: list[list[str]] = []
        current: list[str] = []
        current_tokens = 0
        for text in texts:
            estimate = self._estimate_tokens(text)
            if current and (
                len(current) >= self.max_batch_size
                or current_tokens + estimate > self.max_batch_tokens
            ):
                groups.append(current)
                current = []
                current_tokens = 0
            current.append(text)
            current_tokens += estimate
        if current:
            groups.append(current)

        loop = asyncio.get_running_loop()
        futures: list[asyncio.Future[list[list[float]]]] = []
        for group in groups:
            future: asyncio.Future[list[list[float]]] = loop.create_future()
            futures.append(future)
            await self.queue.put(WorkItem(texts=group, future=future))
        results = await asyncio.gather(*futures)
        return [vector for group in results for vector in group]

    async def _worker(self) -> None:
        while True:
            first = await self.queue.get()
            items = [first]
            total = len(first.texts)
            total_tokens = sum(self._estimate_tokens(text) for text in first.texts)
            deadline = time.monotonic() + self.batch_wait_ms / 1000.0
            while (
                total < self.max_batch_size
                and total_tokens < self.max_batch_tokens
                and time.monotonic() < deadline
            ):
                timeout = max(0.0, deadline - time.monotonic())
                try:
                    item = await asyncio.wait_for(self.queue.get(), timeout)
                except asyncio.TimeoutError:
                    break
                item_tokens = sum(self._estimate_tokens(text) for text in item.texts)
                if (
                    total + len(item.texts) > self.max_batch_size
                    or total_tokens + item_tokens > self.max_batch_tokens
                ):
                    # Keep ordering and let the next iteration handle it.
                    await self.queue.put(item)
                    break
                items.append(item)
                total += len(item.texts)
                total_tokens += item_tokens
            texts = [text for item in items for text in item.texts]
            try:
                vectors = await asyncio.to_thread(self._encode, texts)
                offset = 0
                for item in items:
                    count = len(item.texts)
                    item.future.set_result(vectors[offset : offset + count])
                    offset += count
            except Exception as exc:  # propagate model errors to every waiter
                for item in items:
                    if not item.future.done():
                        item.future.set_exception(exc)

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        # Conservative estimate used only by the micro-batcher. The tokenizer
        # still applies the exact max_length limit during the forward pass.
        return max(1, len(text.encode("utf-8")) // 2 + 8)

    def _encode(self, texts: list[str]) -> list[list[float]]:
        with self._infer_lock, torch.inference_mode():
            encoded = self.tokenizer(
                texts,
                padding=True,
                # Keep one extra token so over-limit input is rejected below
                # without materializing arbitrarily long sequences.
                truncation=True,
                max_length=self.max_length + 1,
                return_tensors="pt",
            )
            sequence_lengths = encoded["attention_mask"].sum(dim=1)
            if bool(sequence_lengths.max().item() > self.max_length):
                actual = int(sequence_lengths.max().item())
                raise ValueError(
                    f"输入 token 数 {actual} 超过服务端 max_length={self.max_length}；"
                    "请降低客户端 max_chunk_tokens 或提高服务端 max-length"
                )
            encoded = {key: value.to(self.device, non_blocking=True) for key, value in encoded.items()}
            outputs = self.model(**encoded)
            hidden = outputs.last_hidden_state
            # Qwen3-Embedding uses last-token pooling for causal embeddings.
            last_indices = encoded["attention_mask"].sum(dim=1) - 1
            pooled = hidden[torch.arange(hidden.size(0), device=self.device), last_indices]
            pooled = F.normalize(pooled.float(), p=2, dim=1)
            return pooled.cpu().tolist()


def create_app(engine: EmbeddingEngine) -> FastAPI:
    app = FastAPI(title="Qwen3 Embedding", version="1.0")

    @app.on_event("startup")
    async def _startup() -> None:
        await engine.start()

    @app.on_event("shutdown")
    async def _shutdown() -> None:
        await engine.stop()

    @app.get("/health")
    async def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "model": engine.model_name,
            "dimension": engine.dimension,
            "max_length": engine.max_length,
            "max_batch_size": engine.max_batch_size,
            "max_batch_tokens": engine.max_batch_tokens,
        }

    @app.get("/v1/models")
    async def models() -> dict[str, Any]:
        return {
            "data": [
                {
                    "id": engine.model_name,
                    "model_revision": engine.revision,
                    "owned_by": "local",
                    "max_input_tokens": engine.max_length,
                }
            ]
        }

    @app.post("/embed")
    async def simple_embed(request: SimpleEmbeddingRequest) -> dict[str, Any]:
        try:
            return {"embeddings": await engine.submit(request.texts)}
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

    @app.post("/v1/embeddings")
    async def openai_embed(request: EmbeddingRequest) -> dict[str, Any]:
        texts = [request.input] if isinstance(request.input, str) else request.input
        if request.model and request.model != engine.model_name:
            raise HTTPException(status_code=400, detail=f"只加载了模型 {engine.model_name}")
        if request.encoding_format != "float":
            raise HTTPException(status_code=400, detail="仅支持 encoding_format=float")
        if request.dimensions not in (None, engine.dimension):
            raise HTTPException(status_code=400, detail=f"仅支持 dimensions={engine.dimension}")
        try:
            vectors = await engine.submit(texts)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return {
            "object": "list",
            "model": engine.model_name,
            "data": [{"object": "embedding", "index": i, "embedding": vector} for i, vector in enumerate(vectors)],
            "usage": {"prompt_tokens": 0, "total_tokens": 0},
        }

    @app.post("/tokenize")
    @app.post("/v1/tokenize")
    async def tokenize(payload: dict[str, Any]) -> dict[str, Any]:
        prompt = payload.get("prompt", "")
        if not isinstance(prompt, str):
            raise HTTPException(status_code=400, detail="prompt 必须是字符串")
        tokens = engine.tokenizer(prompt, add_special_tokens=True)["input_ids"]
        return {"count": len(tokens)}

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="P4-compatible Qwen3 embedding server")
    parser.add_argument("--model", default=os.getenv("QWEN_EMBEDDING_MODEL", DEFAULT_MODEL))
    parser.add_argument("--revision", default=os.getenv("QWEN_EMBEDDING_REVISION"))
    parser.add_argument("--host", default=os.getenv("QWEN_EMBEDDING_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("QWEN_EMBEDDING_PORT", "8000")))
    parser.add_argument("--max-batch-size", type=int, default=int(os.getenv("QWEN_MAX_BATCH_SIZE", "16")))
    parser.add_argument("--max-batch-tokens", type=int, default=int(os.getenv("QWEN_MAX_BATCH_TOKENS", "8192")))
    parser.add_argument("--max-length", type=int, default=int(os.getenv("QWEN_MAX_LENGTH", "8192")))
    parser.add_argument("--batch-wait-ms", type=float, default=float(os.getenv("QWEN_BATCH_WAIT_MS", "3")))
    args = parser.parse_args()
    torch.set_float32_matmul_precision("high")
    engine = EmbeddingEngine(
        args.model,
        revision=args.revision,
        max_batch_size=args.max_batch_size,
        max_batch_tokens=args.max_batch_tokens,
        max_length=args.max_length,
        batch_wait_ms=args.batch_wait_ms,
    )
    import uvicorn

    uvicorn.run(create_app(engine), host=args.host, port=args.port, workers=1, log_level="info")


if __name__ == "__main__":
    main()


"""

python3 -m venv .venv-server
.venv-server/bin/pip install -r requirements-server.txt

export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_DOWNLOAD_TIMEOUT=120
export HF_HUB_ETAG_TIMEOUT=30

.venv-server/bin/python server.py \
  --model Qwen/Qwen3-Embedding-0.6B \
  --host 0.0.0.0 \
  --port 8000 \
  --max-batch-size 16 \
  --max-batch-tokens 8192 \
  --max-length 2048 \
  --batch-wait-ms 3

"""

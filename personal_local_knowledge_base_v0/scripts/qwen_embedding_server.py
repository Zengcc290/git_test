"""Standalone, P4-compatible Qwen3 embedding service.

Upload this one file to a Linux GPU server and run
``python3 qwen_embedding_server.py``. Missing non-PyTorch dependencies are
installed automatically; the pre-installed PyTorch/CUDA runtime is never
replaced. The service binds to ``0.0.0.0`` and makes a best-effort attempt to
allow the port in an active UFW/firewalld firewall.

Transformers is used instead of vLLM because Tesla P4 (compute capability
6.1) is not compatible with many current FlashAttention wheels. Concurrent
requests are merged into length-aware micro-batches so one model copy serves
all clients.
"""

from __future__ import annotations

import argparse
import asyncio
import importlib.util
import os
import shutil
import subprocess
import sys
import threading
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "Qwen/Qwen3-Embedding-0.6B"
_PYTHON_REQUIREMENTS = (
    "transformers>=4.51,<5.0",
    "fastapi>=0.110,<1.0",
    "uvicorn[standard]>=0.29,<1.0",
    "orjson>=3.9",
)
_MODULE_TO_REQUIREMENT = {
    "transformers": _PYTHON_REQUIREMENTS[0],
    "fastapi": _PYTHON_REQUIREMENTS[1],
    "uvicorn": _PYTHON_REQUIREMENTS[2],
    "orjson": _PYTHON_REQUIREMENTS[3],
}


def _switch_to_torch_interpreter() -> None:
    """Re-exec with the active Conda/PATH Python when /bin/python lacks torch."""

    if importlib.util.find_spec("torch") is not None:
        return
    candidates: list[str] = []
    conda_prefix = os.getenv("CONDA_PREFIX")
    if conda_prefix:
        candidates.extend(
            [
                str(Path(conda_prefix) / "bin" / "python"),
                str(Path(conda_prefix) / "bin" / "python3"),
            ]
        )
    for command in ("python", "python3"):
        resolved = shutil.which(command)
        if resolved:
            candidates.append(resolved)
    current = os.path.realpath(sys.executable)
    for candidate in candidates:
        candidate_path = os.path.realpath(candidate)
        if candidate_path == current or not os.path.isfile(candidate_path):
            continue
        probe = subprocess.run(
            [candidate_path, "-c", "import torch"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        if probe.returncode == 0:
            print(f"当前解释器没有 torch，切换到：{candidate_path}", flush=True)
            os.execv(candidate_path, [candidate_path, *sys.argv])


def _ensure_runtime_dependencies() -> None:
    """Install the server dependency set without touching torch."""

    if importlib.util.find_spec("torch") is None:
        raise SystemExit(
            "未检测到 torch。此脚本不会安装或替换 PyTorch，请先使用租用镜像提供的 "
            "PyTorch 2.7.1 + CUDA 12.6 环境。"
        )
    missing = [
        requirement
        for module, requirement in _MODULE_TO_REQUIREMENT.items()
        if importlib.util.find_spec(module) is None
    ]
    if not missing:
        return
    print("正在安装服务依赖（不会安装/替换 torch）：" + ", ".join(missing), flush=True)
    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "pip",
            "install",
            "--disable-pip-version-check",
            *missing,
        ]
    )


# Direct execution is the one-file deployment path. Importing this module
# from server.py remains side-effect free and expects dependencies installed.
if __name__ == "__main__":
    _switch_to_torch_interpreter()
    if "--no-install" not in sys.argv:
        _ensure_runtime_dependencies()

# Preserve the original deployment's China-friendly model download defaults.
# Every value remains overrideable through the server environment.
os.environ.setdefault("HF_ENDPOINT", "https://hf-mirror.com")
os.environ.setdefault("HF_HUB_DOWNLOAD_TIMEOUT", "120")
os.environ.setdefault("HF_HUB_ETAG_TIMEOUT", "30")

import torch
import torch.nn.functional as F
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from transformers import AutoModel, AutoTokenizer

try:
    import orjson as _orjson  # noqa: F401
    from fastapi.responses import ORJSONResponse

    _DEFAULT_RESPONSE_CLASS = ORJSONResponse
except ImportError:  # pragma: no cover - optional fast serialization
    _DEFAULT_RESPONSE_CLASS = JSONResponse


class EmbeddingRequest(BaseModel):
    model: str | None = None
    input: str | list[str]
    encoding_format: str = "float"
    dimensions: int | None = None


class SimpleEmbeddingRequest(BaseModel):
    texts: list[str] = Field(min_length=1)


@dataclass(slots=True)
class WorkItem:
    texts: list[str]
    token_estimates: list[int]
    future: asyncio.Future[list[list[float]]]

    @property
    def max_estimated_tokens(self) -> int:
        return max(self.token_estimates, default=1)


class EmbeddingEngine:
    def __init__(
        self,
        model_name: str,
        *,
        revision: str | None = None,
        max_batch_size: int = 32,
        max_batch_tokens: int = 16384,
        max_length: int = 16384,
        max_request_size: int = 256,
        batch_wait_ms: float = 3.0,
        attention: str = "auto",
        warmup: bool = True,
    ) -> None:
        if max_batch_size < 1 or max_batch_tokens < 1 or max_length < 1:
            raise ValueError("批次和 max_length 参数必须为正数")
        if max_request_size < max_batch_size:
            raise ValueError("max_request_size 不能小于 max_batch_size")
        self.model_name = model_name
        self.max_batch_size = max_batch_size
        # Padded length * batch size tracks attention work and memory better
        # than summing lengths when texts differ greatly in size.
        self.max_batch_tokens = max_batch_tokens
        self.max_length = max_length
        self.max_request_size = max_request_size
        self.batch_wait_ms = max(0.0, batch_wait_ms)
        self.queue: asyncio.Queue[WorkItem] = asyncio.Queue()
        self._worker_task: asyncio.Task[None] | None = None
        self._infer_lock = threading.Lock()

        if not torch.cuda.is_available():
            raise RuntimeError("未检测到 CUDA；此服务要求在装有 NVIDIA 驱动的服务器上运行")
        self.device = torch.device("cuda:0")
        self.attention = self._resolve_attention(attention)

        # P4 supports FP16 but not BF16/Tensor Cores. Eager attention is kept
        # for Pascal; newer GPUs can use PyTorch SDPA without flash-attn.
        model_kwargs: dict[str, Any] = {
            "torch_dtype": torch.float16,
            "attn_implementation": self.attention,
            "trust_remote_code": True,
        }
        tokenizer_kwargs: dict[str, Any] = {"trust_remote_code": True}
        if revision:
            model_kwargs["revision"] = revision
            tokenizer_kwargs["revision"] = revision
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, **tokenizer_kwargs)
        if self.tokenizer.pad_token is None:
            self.tokenizer.pad_token = self.tokenizer.eos_token
        # Left padding makes the final non-padding token index constant.
        self.tokenizer.padding_side = "left"
        self.model = AutoModel.from_pretrained(model_name, **model_kwargs).eval().to(self.device)
        self.model.requires_grad_(False)
        self.model.config.use_cache = False
        self.dimension = int(getattr(self.model.config, "hidden_size", 1024))
        self.revision = revision or str(getattr(self.model.config, "_commit_hash", "") or "unknown")
        if warmup:
            self._encode(["warmup"])

    @staticmethod
    def _resolve_attention(requested: str) -> str:
        if requested in {"eager", "sdpa"}:
            return requested
        if requested != "auto":
            raise ValueError("attention 必须是 auto、eager 或 sdpa")
        major, _minor = torch.cuda.get_device_capability()
        return "sdpa" if major >= 7 else "eager"

    async def start(self) -> None:
        self._worker_task = asyncio.create_task(self._worker())

    async def stop(self) -> None:
        if self._worker_task:
            self._worker_task.cancel()
            await asyncio.gather(self._worker_task, return_exceptions=True)
            self._worker_task = None

    async def submit(self, texts: list[str]) -> list[list[float]]:
        if not texts or any(not isinstance(text, str) or not text.strip() for text in texts):
            raise ValueError("input 必须是非空字符串数组")
        if len(texts) > self.max_request_size:
            raise ValueError(f"单次最多 {self.max_request_size} 条文本")

        groups: list[tuple[list[str], list[int]]] = []
        current: list[str] = []
        estimates: list[int] = []
        current_max = 1
        for text in texts:
            estimate = self._estimate_tokens(text)
            next_max = max(current_max, estimate)
            over_token_budget = current and next_max * (len(current) + 1) > self.max_batch_tokens
            if current and (len(current) >= self.max_batch_size or over_token_budget):
                groups.append((current, estimates))
                current, estimates, current_max = [], [], 1
            current.append(text)
            estimates.append(estimate)
            current_max = max(current_max, estimate)
        if current:
            groups.append((current, estimates))

        loop = asyncio.get_running_loop()
        futures: list[asyncio.Future[list[list[float]]]] = []
        for group, token_estimates in groups:
            future: asyncio.Future[list[list[float]]] = loop.create_future()
            futures.append(future)
            await self.queue.put(WorkItem(group, token_estimates, future))
        results = await asyncio.gather(*futures)
        return [vector for group in results for vector in group]

    async def _worker(self) -> None:
        pending: WorkItem | None = None
        while True:
            first = pending or await self.queue.get()
            pending = None
            items = [first]
            total = len(first.texts)
            longest = first.max_estimated_tokens
            deadline = time.monotonic() + self.batch_wait_ms / 1000.0
            while total < self.max_batch_size and time.monotonic() < deadline:
                timeout = max(0.0, deadline - time.monotonic())
                try:
                    item = await asyncio.wait_for(self.queue.get(), timeout)
                except asyncio.TimeoutError:
                    break
                item_longest = max(longest, item.max_estimated_tokens)
                next_size = total + len(item.texts)
                if (
                    next_size > self.max_batch_size
                    or item_longest * next_size > self.max_batch_tokens
                ):
                    # Hold this item for the next pass rather than re-queueing
                    # it, which avoids starvation under sustained traffic.
                    pending = item
                    break
                items.append(item)
                total = next_size
                longest = item_longest

            active_items = [item for item in items if not item.future.cancelled()]
            if not active_items:
                continue
            texts = [text for item in active_items for text in item.texts]
            try:
                vectors = await asyncio.to_thread(self._encode, texts)
                offset = 0
                for item in active_items:
                    count = len(item.texts)
                    if not item.future.done():
                        item.future.set_result(vectors[offset : offset + count])
                    offset += count
            except Exception as exc:  # propagate model errors to every waiter
                for item in active_items:
                    if not item.future.done():
                        item.future.set_exception(exc)

    @staticmethod
    def _estimate_tokens(text: str) -> int:
        # Conservative scheduler estimate; exact tokenization enforces limits.
        return max(1, len(text.encode("utf-8")) // 2 + 8)

    def _encode(self, texts: list[str]) -> list[list[float]]:
        with self._infer_lock, torch.inference_mode():
            encoded = self.tokenizer(
                texts,
                padding=True,
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
            encoded = {
                key: value.to(self.device, non_blocking=True)
                for key, value in encoded.items()
            }
            outputs = self.model(**encoded, use_cache=False, return_dict=True)
            pooled = outputs.last_hidden_state[:, -1]
            pooled = F.normalize(pooled.float(), p=2, dim=1)
            return pooled.cpu().tolist()


def create_app(engine: EmbeddingEngine) -> FastAPI:
    app = FastAPI(
        title="Qwen3 Embedding",
        version="1.1",
        default_response_class=_DEFAULT_RESPONSE_CLASS,
    )

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
            "device": str(engine.device),
            "attention": engine.attention,
            "revision": engine.revision,
            "max_length": engine.max_length,
            "max_batch_size": engine.max_batch_size,
            "max_batch_tokens": engine.max_batch_tokens,
            "queue_size": engine.queue.qsize(),
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
            "data": [
                {"object": "embedding", "index": i, "embedding": vector}
                for i, vector in enumerate(vectors)
            ],
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


def _open_firewall(port: int) -> None:
    """Allow TCP port when a local Linux firewall is active.

    Cloud security-group rules are outside the guest OS and cannot be changed
    by this script; binding to 0.0.0.0 is still required for those platforms.
    """

    if os.name != "posix" or (not shutil.which("sudo") and os.geteuid() != 0):
        print(f"服务将监听 0.0.0.0:{port}；请在云平台安全组放行 TCP/{port}。", flush=True)
        return
    prefix = [] if os.geteuid() == 0 else ["sudo", "-n"]
    if shutil.which("ufw"):
        status = subprocess.run([*prefix, "ufw", "status"], capture_output=True, text=True)
        if status.returncode == 0 and "Status: active" in status.stdout:
            result = subprocess.run(
                [*prefix, "ufw", "allow", f"{port}/tcp"], capture_output=True, text=True
            )
            if result.returncode == 0:
                print(f"已通过 UFW 放行 TCP/{port}。", flush=True)
                return
    if shutil.which("firewall-cmd"):
        active = subprocess.run(
            [*prefix, "firewall-cmd", "--state"], capture_output=True, text=True
        )
        if active.returncode == 0 and active.stdout.strip() == "running":
            result = subprocess.run(
                [*prefix, "firewall-cmd", "--permanent", "--add-port", f"{port}/tcp"],
                capture_output=True,
                text=True,
            )
            if result.returncode == 0:
                subprocess.run([*prefix, "firewall-cmd", "--reload"], check=False)
                print(f"已通过 firewalld 放行 TCP/{port}。", flush=True)
                return
    print(f"未发现可自动配置的活动防火墙；服务将监听 0.0.0.0:{port}。", flush=True)
    print(f"如需公网访问，还需在云平台安全组放行 TCP/{port}。", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description="P4-compatible Qwen3 embedding server")
    parser.add_argument("--model", default=os.getenv("QWEN_EMBEDDING_MODEL", DEFAULT_MODEL))
    parser.add_argument("--revision", default=os.getenv("QWEN_EMBEDDING_REVISION"))
    parser.add_argument("--host", default=os.getenv("QWEN_EMBEDDING_HOST", "0.0.0.0"))
    parser.add_argument("--port", type=int, default=int(os.getenv("QWEN_EMBEDDING_PORT", "8000")))
    parser.add_argument(
        "--max-batch-size",
        type=int,
        default=int(os.getenv("QWEN_MAX_BATCH_SIZE", "16")),
    )
    parser.add_argument(
        "--max-batch-tokens",
        type=int,
        default=int(os.getenv("QWEN_MAX_BATCH_TOKENS", "8192")),
    )
    parser.add_argument("--max-length", type=int, default=int(os.getenv("QWEN_MAX_LENGTH", "8192")))
    parser.add_argument(
        "--max-request-size",
        type=int,
        default=int(os.getenv("QWEN_MAX_REQUEST_SIZE", "256")),
    )
    parser.add_argument(
        "--batch-wait-ms",
        type=float,
        default=float(os.getenv("QWEN_BATCH_WAIT_MS", "3")),
    )
    parser.add_argument(
        "--attention",
        choices=("auto", "eager", "sdpa"),
        default=os.getenv("QWEN_ATTENTION", "auto"),
    )
    parser.add_argument("--no-warmup", action="store_false", dest="warmup", help="跳过 GPU warmup")
    parser.add_argument("--skip-firewall", action="store_true", help="不配置 UFW/firewalld")
    parser.add_argument("--install-only", action="store_true", help="只安装依赖，不启动模型")
    parser.add_argument("--no-install", action="store_true", help="不自动安装缺失依赖")
    parser.add_argument("--access-log", action="store_true", help="开启每请求访问日志")
    args = parser.parse_args()

    if args.install_only:
        print("依赖检查完成。PyTorch/CUDA 按预装环境使用。", flush=True)
        return
    if not 1 <= args.port <= 65535:
        parser.error("--port 必须在 1 到 65535 之间")
    if not args.skip_firewall:
        _open_firewall(args.port)
    torch.set_float32_matmul_precision("high")
    engine = EmbeddingEngine(
        args.model,
        revision=args.revision,
        max_batch_size=args.max_batch_size,
        max_batch_tokens=args.max_batch_tokens,
        max_length=args.max_length,
        max_request_size=args.max_request_size,
        batch_wait_ms=args.batch_wait_ms,
        attention=args.attention,
        warmup=args.warmup,
    )
    import uvicorn

    uvicorn.run(
        create_app(engine),
        host=args.host,
        port=args.port,
        workers=1,
        access_log=args.access_log,
        log_level="info",
    )


if __name__ == "__main__":
    main()

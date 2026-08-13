"""Minimal OpenAI-compatible chat-completions HTTP client."""

from __future__ import annotations

import json
import os
import socket
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from dotenv import find_dotenv, load_dotenv


class LLMClientError(RuntimeError):
    """A user-facing, sanitized LLM configuration or request error."""


@dataclass(frozen=True)
class TokenUsage:
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0


@dataclass(frozen=True)
class LLMResponse:
    content: str
    usage: TokenUsage = TokenUsage()


class LLMClient:
    """Call an OpenAI-compatible ``/chat/completions`` endpoint."""

    def __init__(
        self,
        *,
        api_key: str,
        base_url: str,
        model: str,
        timeout_seconds: float = 60.0,
    ) -> None:
        if not api_key:
            raise LLMClientError("未配置 LLM_API_KEY。")
        if not base_url:
            raise LLMClientError("未配置 LLM_BASE_URL。")
        if not model:
            raise LLMClientError("未配置 LLM_MODEL。")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds 必须大于 0")

        parsed_url = urllib.parse.urlsplit(base_url)
        if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
            raise LLMClientError("LLM_BASE_URL 必须是有效的 HTTP(S) 地址。")

        self._api_key = api_key
        self._base_url = base_url.rstrip("/")
        self.model = model
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_env(cls, environ: Mapping[str, str] | None = None) -> "LLMClient":
        if environ is None:
            cls.load_dotenv()
            values = os.environ
        else:
            # An explicit mapping keeps tests and embedded callers deterministic.
            values = environ
        return cls(
            api_key=values.get("LLM_API_KEY", "").strip(),
            base_url=values.get("LLM_BASE_URL", "").strip(),
            model=values.get("LLM_MODEL", "").strip(),
        )

    @staticmethod
    def load_dotenv() -> None:
        """Load the nearest project .env without overriding real environment vars."""

        dotenv_path = find_dotenv(usecwd=True)
        if not dotenv_path:
            project_dotenv = Path(__file__).resolve().parents[2] / ".env"
            if project_dotenv.is_file():
                dotenv_path = str(project_dotenv)
        if dotenv_path:
            load_dotenv(dotenv_path=dotenv_path, override=False)

    @property
    def endpoint(self) -> str:
        if self._base_url.endswith("/chat/completions"):
            return self._base_url
        return f"{self._base_url}/chat/completions"

    def _sanitize(self, message: str) -> str:
        sanitized = message.replace(self._api_key, "[REDACTED]")
        return sanitized.replace(self._base_url, "[REDACTED_URL]")

    def complete(
        self,
        messages: Sequence[Mapping[str, str]],
        *,
        temperature: float = 0.0,
    ) -> LLMResponse:
        payload = json.dumps(
            {
                "model": self.model,
                "messages": list(messages),
                "temperature": temperature,
            },
            ensure_ascii=False,
        ).encode("utf-8")
        try:
            request = urllib.request.Request(
                self.endpoint,
                data=payload,
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )
            with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                response_data = json.loads(response.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            detail = self._http_error_detail(exc)
            raise LLMClientError(
                self._sanitize(f"大模型请求失败（HTTP {exc.code}）：{detail}")
            ) from exc
        except (urllib.error.URLError, TimeoutError, socket.timeout) as exc:
            raise LLMClientError(
                "无法连接到大模型服务，请检查 LLM_BASE_URL、网络连接和服务状态。"
            ) from exc
        except OSError as exc:
            raise LLMClientError(
                "无法连接到大模型服务，请检查 LLM_BASE_URL、网络连接和服务状态。"
            ) from exc
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise LLMClientError("大模型服务返回了无法解析的响应。") from exc
        except ValueError as exc:
            raise LLMClientError("LLM_BASE_URL 无效，无法创建大模型请求。") from exc

        return self._parse_response(response_data)

    def _http_error_detail(self, exc: urllib.error.HTTPError) -> str:
        try:
            body = exc.read(16_384).decode("utf-8", errors="replace")
            data = json.loads(body)
            message = data.get("error", {}).get("message", "")
            if isinstance(message, str) and message.strip():
                return message.strip()
        except (AttributeError, json.JSONDecodeError, OSError):
            pass
        return "请检查模型配置、额度和服务状态。"

    def _parse_response(self, data: Any) -> LLMResponse:
        try:
            content = data["choices"][0]["message"]["content"]
            usage_data = data.get("usage") or {}
            usage = TokenUsage(
                prompt_tokens=int(usage_data.get("prompt_tokens", 0)),
                completion_tokens=int(usage_data.get("completion_tokens", 0)),
                total_tokens=int(usage_data.get("total_tokens", 0)),
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMClientError("大模型服务响应缺少答案或 token 使用量格式无效。") from exc
        if not isinstance(content, str) or not content.strip():
            raise LLMClientError("大模型服务返回了空答案。")
        return LLMResponse(content=content.strip(), usage=usage)

"""Run the real ask CLI against a local model response with no citation."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from knowledge_search.database import KnowledgeBase
from knowledge_search.indexer import index_paths


class _NoCitationHandler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:  # noqa: N802 - BaseHTTPRequestHandler API
        content_length = int(self.headers.get("Content-Length", "0"))
        self.rfile.read(content_length)
        payload = json.dumps(
            {
                "choices": [
                    {"message": {"content": "This answer has no citation."}}
                ],
                "usage": {
                    "prompt_tokens": 20,
                    "completion_tokens": 6,
                    "total_tokens": 26,
                },
            }
        ).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        return


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--log-output", type=Path)
    parser.add_argument("--result-output", type=Path)
    args = parser.parse_args()

    secret = "citation-probe-secret"
    with tempfile.TemporaryDirectory() as temp_dir:
        root = Path(temp_dir)
        source = root / f"{secret}.md"
        source.write_text("项目代号是晨星。", encoding="utf-8")
        database = root / "knowledge.db"
        log_file = root / "app.log"
        with KnowledgeBase(database) as knowledge_base:
            index_paths(knowledge_base, [source])

        server = ThreadingHTTPServer(("127.0.0.1", 0), _NoCitationHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        env = os.environ.copy()
        env.update(
            {
                "LLM_API_KEY": secret,
                "LLM_BASE_URL": f"http://127.0.0.1:{server.server_port}/v1",
                "LLM_MODEL": "citation-probe-model",
            }
        )
        try:
            completed = subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "knowledge_search",
                    "ask",
                    "项目代号是什么？",
                    "--db",
                    str(database),
                    "--log-file",
                    str(log_file),
                ],
                cwd=Path(__file__).resolve().parents[1],
                env=env,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=30,
                check=False,
            )
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

        log_text = log_file.read_text(encoding="utf-8")
        checks = {
            "cli_exit_code": completed.returncode,
            "rag_error_present": '"event": "rag_error"' in log_text,
            "rag_answer_absent": '"event": "rag_answer"' not in log_text,
            "citation_error_present": "CitationValidationError" in log_text,
            "token_usage_preserved": '"total_tokens": 26' in log_text,
            "api_key_redacted": secret not in log_text,
        }
        passed = (
            checks["cli_exit_code"] == 1
            and all(value for key, value in checks.items() if key != "cli_exit_code")
        )
        result_text = json.dumps(
            {"passed": passed, **checks}, ensure_ascii=False, indent=2
        )
        print(result_text)
        if args.log_output is not None:
            args.log_output.parent.mkdir(parents=True, exist_ok=True)
            args.log_output.write_text(log_text, encoding="utf-8")
        if args.result_output is not None:
            args.result_output.parent.mkdir(parents=True, exist_ok=True)
            args.result_output.write_text(result_text + "\n", encoding="utf-8")
        return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())

import contextlib
import io
import json
import logging
import socket
import tempfile
import unittest
from pathlib import Path

from knowledge_search.cli import build_parser, main


def _reset_logging_handlers() -> None:
    root_logger = logging.getLogger()
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
        handler.close()


class CLIIntegrationTests(unittest.TestCase):
    def test_web_port_defaults_to_8000_and_accepts_override(self):
        parser = build_parser()

        self.assertEqual(parser.parse_args(["web"]).port, 8000)
        self.assertEqual(parser.parse_args(["web", "--port", "9000"]).port, 9000)

    def test_web_command_reports_occupied_port_and_exits(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as occupied:
                occupied.bind(("127.0.0.1", 0))
                occupied.listen()
                port = occupied.getsockname()[1]
                errors = io.StringIO()
                try:
                    with contextlib.redirect_stderr(errors):
                        status = main(
                            [
                                "web",
                                "--port",
                                str(port),
                                "--db",
                                str(root / "knowledge.db"),
                                "--upload-dir",
                                str(root / "uploads"),
                                "--log-file",
                                str(root / "app.log"),
                            ]
                        )
                finally:
                    _reset_logging_handlers()

            self.assertEqual(status, 1)
            self.assertIn(f"端口 {port} 已被占用", errors.getvalue())

    def test_size_options_accept_human_readable_units(self):
        args = build_parser().parse_args(
            [
                "index",
                "items.json",
                "--max-json-size",
                "1GB",
                "--json-record-probe-size",
                "512MB",
            ]
        )

        self.assertEqual(args.max_json_size, 1024**3)
        self.assertEqual(args.json_record_probe_size, 512 * 1024**2)

    def test_json_structure_command_reports_streamed_schema(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            path = root / "items.json"
            path.write_text(
                "\n".join(
                    json.dumps(item, ensure_ascii=False)
                    for item in (
                        {"id": 1, "title": "one"},
                        {"id": 2, "title": "two"},
                    )
                ),
                encoding="utf-8",
            )

            output = io.StringIO()
            try:
                with contextlib.redirect_stdout(output):
                    status = main(
                        [
                            "json-structure",
                            str(path),
                            "--max-records",
                            "1",
                            "--read-size",
                            "3",
                            "--log-file",
                            str(root / "app.log"),
                        ]
                    )
            finally:
                _reset_logging_handlers()

            self.assertEqual(status, 0)
            self.assertIn("扫描记录：1", output.getvalue())
            self.assertIn("$.id", output.getvalue())
            self.assertIn("$.title", output.getvalue())

    def test_json_index_command_uses_configured_stream(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            data_path = root / "items.json"
            config_path = root / "config.json"
            data_path.write_text(
                "\n".join(
                    json.dumps(item, ensure_ascii=False)
                    for item in (
                        {"id": 1, "text": "first searchable record"},
                        {"id": 2, "text": "second searchable record"},
                    )
                ),
                encoding="utf-8",
            )
            config_path.write_text(
                json.dumps(
                    {
                        "name": "items",
                        "record_path": "$",
                        "fields": ["id", "text"],
                    },
                    ensure_ascii=False,
                ),
                encoding="utf-8",
            )

            output = io.StringIO()
            try:
                with contextlib.redirect_stdout(output):
                    status = main(
                        [
                            "index",
                            str(data_path),
                            "--json-config",
                            str(config_path),
                            "--db",
                            str(root / "knowledge.db"),
                            "--log-file",
                            str(root / "app.log"),
                        ]
                    )
            finally:
                _reset_logging_handlers()

            self.assertEqual(status, 0)
            self.assertIn("本次索引未启用 Embedding", output.getvalue())
            self.assertIn("新增/更新 1", output.getvalue())


if __name__ == "__main__":
    unittest.main()

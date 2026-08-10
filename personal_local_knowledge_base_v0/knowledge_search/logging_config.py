"""统一日志配置。"""

from __future__ import annotations

import logging
import sys
from pathlib import Path


def configure_logging(level: str = "INFO", log_file: Path | None = None) -> None:
    # 控制台日志使用 stderr，避免污染 CLI 的正常结果输出。
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stderr)]
    if log_file is not None:
        # 日志目录可能还不存在，因此先创建父目录。
        log_file.parent.mkdir(parents=True, exist_ok=True)
        # 使用 UTF-8 写入文件，保证中文日志可读。
        handlers.append(logging.FileHandler(log_file, encoding="utf-8"))

    # force=True 可以覆盖 unittest 或重复调用遗留的旧日志配置。
    logging.basicConfig(
        # 将字符串级别转换成 logging 模块使用的整数级别。
        level=getattr(logging, level.upper(), logging.INFO),
        # 每条日志都包含时间、级别、模块名和消息正文。
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=handlers,
        force=True,
    )

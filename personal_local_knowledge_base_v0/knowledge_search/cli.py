"""命令行入口。"""

from __future__ import annotations

# argparse 负责生成子命令、参数校验和 --help 文档。
import argparse
# logging 用于记录命令执行过程中的错误。
import logging
# sqlite3.Error 用于捕获数据库层异常并转换为 CLI 失败状态。
import sqlite3
# Path 让数据库、日志和索引输入参数支持跨平台路径。
from pathlib import Path
# Sequence 允许 main 接收 list、tuple 等不同形式的参数集合。
from typing import Sequence

# CLI 只负责参数和输出，具体能力由下层模块完成。
from .database import KnowledgeBase
from .highlighting import highlight_text
from .indexer import index_paths
from .logging_config import configure_logging


logger = logging.getLogger(__name__)


def _add_runtime_options(parser: argparse.ArgumentParser) -> None:
    # 这些运行时选项同时提供给 index、search、stats 和 init-db。
    parser.add_argument(
        "--db",
        type=Path,
        default=Path("data/knowledge.db"),
        help="SQLite 数据库路径（默认：data/knowledge.db）",
    )
    parser.add_argument(
        "--log-file",
        type=Path,
        default=Path("logs/app.log"),
        help="日志文件路径（默认：logs/app.log）",
    )
    parser.add_argument(
        "--log-level",
        choices=("DEBUG", "INFO", "WARNING", "ERROR"),
        default="INFO",
        help="日志级别",
    )


def build_parser() -> argparse.ArgumentParser:
    # 创建顶层解析器，子命令负责各自的业务参数。
    parser = argparse.ArgumentParser(
        prog="knowledge-search",
        description="个人本地知识库搜索工具 V0：导入文档并使用 SQLite FTS5 搜索。",
    )
    # required=True 可以在用户忘记子命令时给出明确用法提示。
    subparsers = parser.add_subparsers(dest="command", required=True)

    # index 命令接受一个或多个文件/目录，并提供分段参数。
    index_parser = subparsers.add_parser("index", help="导入并索引 TXT、Markdown、PDF 文件")
    index_parser.add_argument("paths", nargs="+", type=Path, help="文件或目录，可重复传入")
    index_parser.add_argument("--chunk-size", type=int, default=800, help="分段目标字符数")
    index_parser.add_argument("--overlap", type=int, default=100, help="超长段落的重叠字符数")
    index_parser.add_argument("--force", action="store_true", help="忽略哈希，强制重新索引")
    _add_runtime_options(index_parser)

    # search 命令接收一个查询字符串，并限制返回条数。
    search_parser = subparsers.add_parser("search", help="搜索已索引内容")
    search_parser.add_argument("query", help="关键词，可输入多个词，默认 AND 匹配")
    search_parser.add_argument("--limit", type=int, default=10, help="最多返回条数（默认：10）")
    search_parser.add_argument("--no-color", action="store_true", help="不使用 ANSI 颜色，改用 [[...]] 标记")
    _add_runtime_options(search_parser)

    # stats 只读取数据库统计信息，不执行索引或搜索。
    stats_parser = subparsers.add_parser("stats", help="查看数据库统计信息")
    _add_runtime_options(stats_parser)

    # init-db 用于显式创建数据库结构；index 也会自动初始化。
    init_parser = subparsers.add_parser("init-db", help="初始化数据库")
    _add_runtime_options(init_parser)
    return parser


def _print_index_stats(stats) -> None:
    # 将 IndexStats 转换成适合终端阅读的一行摘要。
    print(
        "索引完成："
        f"发现 {stats.files_found}，新增/更新 {stats.indexed}，"
        f"跳过 {stats.skipped}，空文本 {stats.empty}，失败 {stats.failed}"
    )


def _run(args: argparse.Namespace) -> int:
    # 先配置日志，再创建数据库连接，保证初始化错误也有记录。
    configure_logging(args.log_level, args.log_file)

    # with 负责在任何子命令结束后关闭 SQLite 连接。
    with KnowledgeBase(args.db) as knowledge_base:
        if args.command == "init-db":
            # KnowledgeBase 构造时已经执行 schema 初始化。
            print(f"数据库已初始化：{knowledge_base.db_path}")
            return 0

        if args.command == "index":
            # 对输入路径执行抽取、清洗、分段、增量判断和数据库写入。
            stats = index_paths(
                knowledge_base,
                args.paths,
                chunk_size=args.chunk_size,
                overlap=args.overlap,
                force=args.force,
            )
            _print_index_stats(stats)
            # 只有全部文件都失败且没有任何成功索引时，才返回失败状态。
            return 1 if stats.failed and not stats.indexed else 0

        if args.command == "stats":
            # 输出数据库位置和两类核心数量指标。
            print(f"数据库：{knowledge_base.db_path}")
            print(f"文档数：{knowledge_base.document_count()}")
            print(f"分段数：{knowledge_base.chunk_count()}")
            return 0

        if args.command == "search":
            # 搜索模块返回已排序的结果对象。
            results = knowledge_base.search(args.query, limit=args.limit)
            if not results:
                # 空结果不是命令错误，因此仍返回 0。
                print("没有找到匹配内容。")
                return 0

            for number, result in enumerate(results, start=1):
                # 每条结果显示来源、分段编号和排序分数，方便定位原文。
                print(f"[{number}] {result.filename} ({result.file_type})")
                print(f"    路径：{result.document_path}")
                print(f"    分段：{result.chunk_index}  score：{result.score:.4f}")
                if args.no_color:
                    # 无颜色模式使用可见的 [[...]] 标记，适合重定向到文件。
                    content = highlight_text(result.content, args.query, "[[", "]]")
                else:
                    # 默认使用 ANSI 黄色高亮，适合直接在终端阅读。
                    content = highlight_text(result.content, args.query, "\033[1;33m", "\033[0m")
                print(f"    {content}")
            return 0

    return 0


def main(argv: Sequence[str] | None = None) -> int:
    # argv=None 时由 argparse 从 sys.argv 读取；测试时可传入列表避免启动子进程。
    args = build_parser().parse_args(argv)
    try:
        # 业务错误统一转换为 1，避免打印 Python traceback 给普通 CLI 用户。
        return _run(args)
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as exc:
        # argparse 自己的参数错误会返回 2；这里处理的是运行时异常。
        logging.basicConfig(level=logging.ERROR)
        logger.error("命令执行失败：%s", exc)
        return 1

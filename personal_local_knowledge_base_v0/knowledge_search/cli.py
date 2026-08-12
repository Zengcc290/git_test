"""命令行入口。"""

from __future__ import annotations

# argparse 负责生成子命令、参数校验和 --help 文档。
import argparse
# logging 用于记录命令执行过程中的错误。
import logging
# sqlite3.Error 用于捕获数据库层异常并转换为 CLI 失败状态。
import sqlite3
# sys 用于调整 Windows 控制台的标准输出编码。
import sys
# Path 让数据库、日志和索引输入参数支持跨平台路径。
from pathlib import Path
# Sequence 允许 main 接收 list、tuple 等不同形式的参数集合。
from typing import Sequence

# CLI 只负责参数和输出，具体能力由下层模块完成。
from .database import KnowledgeBase
from .highlighting import highlight_text
from .indexer import index_paths
from .json_parser import (
    DEFAULT_MAX_JSON_SIZE,
    JsonProfile,
    inspect_json_structure,
    parse_json_preview,
)
from .logging_config import configure_logging
from .models import IndexProgress


logger = logging.getLogger(__name__)


def _configure_console_encoding() -> None:
    """保留终端原有编码，并避免特殊字符导致 Windows CLI 打印失败。"""

    # Python 3.7+ 的文本流支持 reconfigure，可以在不替换流对象的情况下调整编码。
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is None:
            # 测试中的自定义流可能没有 reconfigure，保持原流不变即可。
            continue
        try:
            # 保留当前编码以兼容 PowerShell，同时替换编码无法表示的字符。
            reconfigure(errors="replace")
        except (OSError, ValueError):
            # 某些被重定向或已关闭的流不能重新配置，忽略即可。
            continue


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
        description="个人本地知识库搜索工具 V1：导入、管理文档并使用 SQLite FTS5 搜索。",
    )
    # required=True 可以在用户忘记子命令时给出明确用法提示。
    subparsers = parser.add_subparsers(dest="command", required=True)

    # index 命令接受一个或多个文件/目录，并提供分段参数。
    index_parser = subparsers.add_parser(
        "index",
        help="导入并索引 TXT、Markdown、PDF、PPTX、JSON 文件",
    )
    index_parser.add_argument("paths", nargs="+", type=Path, help="文件或目录，可重复传入")
    index_parser.add_argument("--chunk-size", type=int, default=800, help="分段目标字符数")
    index_parser.add_argument("--overlap", type=int, default=100, help="超长段落的重叠字符数")
    index_parser.add_argument("--force", action="store_true", help="忽略哈希，强制重新索引")
    index_parser.add_argument(
        "--json-config",
        type=Path,
        help="JSON 解析配置文件；索引 JSON 时必须提供",
    )
    index_parser.add_argument(
        "--exclude-dir",
        action="append",
        dest="exclude_dirs",
        metavar="RULE",
        help="排除目录名、通配符或相对路径；可重复传入",
    )
    index_parser.add_argument(
        "--max-files",
        type=int,
        default=0,
        help="最多索引文件数；0 表示不限制（默认：0）",
    )
    index_parser.add_argument(
        "--max-json-size",
        type=int,
        default=DEFAULT_MAX_JSON_SIZE,
        help=(
            "JSON 最大字节数；0 表示不限制，默认："
            f"{DEFAULT_MAX_JSON_SIZE}"
        ),
    )
    _add_runtime_options(index_parser)

    # json-preview 用于正式索引前检查配置抽取出的文本。
    preview_parser = subparsers.add_parser(
        "json-preview",
        help="预览 JSON 配置解析结果",
    )
    preview_parser.add_argument("path", type=Path, help="待预览的 JSON 文件")
    preview_parser.add_argument(
        "--json-config",
        required=True,
        type=Path,
        help="JSON 解析配置文件",
    )
    preview_parser.add_argument(
        "--limit",
        type=int,
        default=5,
        help="最多预览的记录数（默认：5）",
    )
    preview_parser.add_argument(
        "--max-json-size",
        type=int,
        default=DEFAULT_MAX_JSON_SIZE,
        help="JSON 最大字节数；0 表示不限制",
    )
    _add_runtime_options(preview_parser)

    structure_parser = subparsers.add_parser(
        "json-structure",
        help="流式读取 JSON 并输出字段目录结构",
    )
    structure_parser.add_argument("path", type=Path, help="待扫描的 JSON/JSON Lines 文件")
    structure_parser.add_argument(
        "--max-records",
        type=int,
        default=100,
        help="最多扫描的记录数；0 表示扫描到文件末尾（默认：100）",
    )
    structure_parser.add_argument(
        "--read-size",
        type=int,
        default=64 * 1024,
        help="每次读取的字符数（默认：65536）",
    )
    structure_parser.add_argument(
        "--max-depth",
        type=int,
        default=20,
        help="最多展开的嵌套层级（默认：20）",
    )
    structure_parser.add_argument(
        "--max-paths",
        type=int,
        default=10_000,
        help="最多保留的字段路径数（默认：10000）",
    )
    structure_parser.add_argument(
        "--max-json-size",
        type=int,
        default=DEFAULT_MAX_JSON_SIZE,
        help="JSON 最大字节数；0 表示不限制",
    )
    _add_runtime_options(structure_parser)

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
    search_parser.add_argument(
        "--type",
        dest="file_type",
        choices=("txt", "md", "pdf", "pptx", "json"),
        help="只搜索指定文件类型",
    )
    search_parser.add_argument(
        "--path",
        type=Path,
        help="只搜索指定文件或目录下的已索引文档",
    )

    list_parser = subparsers.add_parser("list", help="列出已索引文档")
    _add_runtime_options(list_parser)

    remove_parser = subparsers.add_parser("remove", help="删除指定的已索引文档")
    remove_parser.add_argument("path", type=Path, help="文档路径")
    _add_runtime_options(remove_parser)

    prune_parser = subparsers.add_parser(
        "prune", help="清理源文件已经不存在的索引文档"
    )
    _add_runtime_options(prune_parser)

    check_parser = subparsers.add_parser(
        "check-db", help="检查数据库和 FTS5 索引健康状态"
    )
    _add_runtime_options(check_parser)
    return parser


def _print_index_stats(stats) -> None:
    # 将 IndexStats 转换成适合终端阅读的一行摘要。
    print(
        "索引完成："
        f"发现 {stats.files_found}，新增/更新 {stats.indexed}，"
        f"跳过 {stats.skipped}，空文本 {stats.empty}，"
        f"超大 JSON {stats.oversized}，失败 {stats.failed}"
    )


def _print_index_progress(progress: IndexProgress) -> None:
    """以单行状态输出索引进度，适合终端和重定向日志。"""

    status_names = {
        "indexed": "完成",
        "skipped": "跳过（未变化）",
        "empty": "空文本",
        "oversized": "跳过（JSON 超大）",
        "failed": "失败",
    }
    if progress.status == "processing":
        print(
            f"索引进度 [{progress.current}/{progress.total}]："
            f"处理中 {progress.path}",
            end="",
            flush=True,
        )
        return
    print(f" -> {status_names.get(progress.status, progress.status)}", flush=True)


def _print_documents(documents) -> None:
    if not documents:
        print("没有已索引文档。")
        return

    print("已索引文档：")
    for document in documents:
        print(f"- {document.filename} ({document.file_type})")
        print(f"  路径：{document.path}")
        print(
            f"  大小：{document.size} 字节；分段数：{document.chunk_count}；"
            f"索引时间：{document.indexed_at}"
        )


def _print_health(report) -> None:
    status = "通过" if report.healthy else "发现问题"
    print(f"数据库健康检查：{status}")
    print(f"文档数：{report.document_count}")
    print(f"分段数：{report.chunk_count}")
    print(f"chunks FTS5 数：{report.chunks_fts_count}")
    print(f"chunk_tokens 数：{report.chunk_tokens_count}")
    print(f"中文 FTS5 数：{report.chunks_fts_jieba_count}")
    for issue in report.issues:
        print(f"问题：{issue}")


def _print_json_structure(report) -> None:
    status = "完整扫描" if report.complete else "达到记录上限，未扫描文件末尾"
    print(f"JSON 文件：{report.path}")
    print(f"扫描记录：{report.records_scanned}（{status}）")
    print("字段结构：")
    for entry in report.entries:
        type_text = ", ".join(
            f"{value} x{count}" for value, count in entry.types
        )
        print(f"{entry.path} [{type_text}]，出现 {entry.count} 次")


def _run(args: argparse.Namespace) -> int:
    # 先配置日志，再创建数据库连接，保证初始化错误也有记录。
    configure_logging(args.log_level, args.log_file)

    if args.command == "json-preview":
        profile = JsonProfile.from_file(args.json_config)
        previews = parse_json_preview(
            args.path,
            profile,
            args.limit,
            max_size=args.max_json_size,
        )
        if not previews:
            print("没有解析出可索引内容。")
            return 0
        for number, content in enumerate(previews, start=1):
            print(f"--- 记录 {number} ---")
            print(content)
        return 0

    if args.command == "json-structure":
        report = inspect_json_structure(
            args.path,
            max_records=args.max_records,
            read_size=args.read_size,
            max_depth=args.max_depth,
            max_paths=args.max_paths,
            max_size=args.max_json_size,
        )
        _print_json_structure(report)
        return 0

    # with 负责在任何子命令结束后关闭 SQLite 连接。
    with KnowledgeBase(args.db) as knowledge_base:
        if args.command == "init-db":
            # KnowledgeBase 构造时已经执行 schema 初始化。
            print(f"数据库已初始化：{knowledge_base.db_path}")
            return 0

        if args.command == "list":
            _print_documents(knowledge_base.list_documents())
            return 0

        if args.command == "remove":
            removed = knowledge_base.remove_document(args.path)
            if removed:
                print(f"已删除索引文档：{args.path}")
                return 0
            print(f"未找到已索引文档：{args.path}")
            return 1

        if args.command == "prune":
            removed_documents = knowledge_base.prune_missing_documents()
            if removed_documents:
                print(f"已清理 {len(removed_documents)} 个源文件不存在的文档：")
                for document in removed_documents:
                    print(f"- {document.path}")
            else:
                print("没有需要清理的文档。")
            return 0

        if args.command == "check-db":
            report = knowledge_base.check_health()
            _print_health(report)
            return 0 if report.healthy else 1

        if args.command == "index":
            # 对输入路径执行抽取、清洗、分段、增量判断和数据库写入。
            json_profile = (
                JsonProfile.from_file(args.json_config)
                if args.json_config is not None
                else None
            )
            stats = index_paths(
                knowledge_base,
                args.paths,
                chunk_size=args.chunk_size,
                overlap=args.overlap,
                force=args.force,
                json_profile=json_profile,
                exclude_dirs=args.exclude_dirs,
                max_files=args.max_files,
                max_json_size=args.max_json_size,
                progress_callback=_print_index_progress,
            )
            _print_index_stats(stats)
            # 只有全部文件都失败/被大小保护且没有任何成功索引时，才返回失败状态。
            unsuccessful = stats.failed + stats.oversized
            return 1 if unsuccessful and not stats.indexed else 0

        if args.command == "stats":
            # 输出数据库位置和两类核心数量指标。
            print(f"数据库：{knowledge_base.db_path}")
            print(f"文档数：{knowledge_base.document_count()}")
            print(f"分段数：{knowledge_base.chunk_count()}")
            return 0

        if args.command == "search":
            # 搜索模块返回已排序的结果对象。
            results = knowledge_base.search(
                args.query,
                limit=args.limit,
                file_type=args.file_type,
                path=args.path,
            )
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
    # 先处理输出编码，再解析参数和执行命令，覆盖帮助、索引和搜索输出。
    _configure_console_encoding()
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

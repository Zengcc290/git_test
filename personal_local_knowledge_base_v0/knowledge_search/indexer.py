"""文件发现、增量索引和异常隔离。"""

from __future__ import annotations

# logging 用于记录发现、跳过、完成和失败的文件。
import logging
# Iterable/Iterator 让文件发现函数可以惰性地产生路径。
from collections.abc import Iterable, Iterator
# Path 负责跨平台的目录递归和扩展名判断。
from pathlib import Path

# 索引流水线依次调用流式清洗、流式分段和数据库写入模块。
from .chunking import iter_chunk_text
from .cleaning import iter_clean_text
from .database import KnowledgeBase
from .extractors import SUPPORTED_SUFFIXES, extract_document, iter_document_text
from .models import IndexStats


logger = logging.getLogger(__name__)


def discover_files(inputs: Iterable[Path]) -> Iterator[Path]:
    """递归发现支持的文件；目录中的不可支持文件会被忽略。"""

    # 逐个处理 CLI 传入的文件或目录参数。
    for raw_input in inputs:
        # 展开用户目录符号，但保留相对路径以便根据当前工作目录解析。
        path = Path(raw_input).expanduser()
        if path.is_file():
            # 单文件输入只接受支持的扩展名。
            if path.suffix.lower() in SUPPORTED_SUFFIXES:
                yield path.resolve()
            else:
                logger.warning("忽略不支持的文件：%s", path)
            continue
        if path.is_dir():
            # 目录输入递归遍历所有子项，并保持排序保证索引顺序稳定。
            for child in sorted(path.rglob("*")):
                if child.is_file() and child.suffix.lower() in SUPPORTED_SUFFIXES:
                    yield child.resolve()
            continue
        # 不存在的输入只记录警告，不影响其他输入继续处理。
        logger.warning("索引输入不存在：%s", path)


def index_paths(
    knowledge_base: KnowledgeBase,
    inputs: Iterable[Path],
    *,
    chunk_size: int = 800,
    overlap: int = 100,
    force: bool = False,
) -> IndexStats:
    # stats 汇总本次索引结果，供日志和 CLI 摘要使用。
    stats = IndexStats()
    # 先物化路径列表，便于同时统计总数和逐个处理。
    paths = list(discover_files(inputs))
    stats.files_found = len(paths)
    logger.info("发现 %s 个待处理文件", stats.files_found)

    for path in paths:
        try:
            # 根据后缀读取文件、计算哈希并抽取文本。
            document = extract_document(path)
            if not force and knowledge_base.is_unchanged(document):
                # 内容哈希不变时不重复清洗、分段和写数据库。
                stats.skipped += 1
                logger.info("跳过未变化文件：%s", path)
                continue

            # 抽取器、清洗器和分段器全部返回迭代器，不在索引器中保存全文。
            source_text = iter_document_text(document)
            cleaned_text = iter_clean_text(source_text)
            chunks = iter_chunk_text(cleaned_text, chunk_size=chunk_size, overlap=overlap)

            # 用计数器包装分段流，只记录数量，不保存已经写入数据库的分段。
            chunk_count = 0

            def counted_chunks():
                nonlocal chunk_count
                for chunk in chunks:
                    chunk_count += 1
                    yield chunk

            # 在事务中替换旧文档，并由数据库层逐个消费分段生成器。
            knowledge_base.replace_document(document, counted_chunks())
            if chunk_count == 0:
                # 文件可能从有内容变成空文件，清理刚写入的空记录和旧索引。
                knowledge_base.remove_document(document.path)
                stats.empty += 1
                logger.warning("文件没有可索引文本：%s", path)
                continue

            stats.indexed += 1
            logger.info("完成索引：%s（%s 个分段）", path, chunk_count)
        except Exception:
            # 单个文件失败不应中断整个目录；记录堆栈并累加失败数。
            stats.failed += 1
            logger.exception("处理文件失败：%s", path)

    # 返回完整汇总，让 CLI 决定显示和退出状态码。
    return stats

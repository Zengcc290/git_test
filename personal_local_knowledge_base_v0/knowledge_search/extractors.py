"""TXT、Markdown 和 PDF 文本抽取。"""

from __future__ import annotations

# hashlib 用于计算源文件指纹，实现增量索引。
import hashlib
# logging 负责记录编码降级、PDF 页失败等可诊断信息。
import logging
# Path 提供跨平台的文件系统访问。
from pathlib import Path

# 抽取结果统一使用这个数据模型传递给清洗和索引模块。
from .models import ExtractedDocument


# 目前 V0 只接受纯文本、Markdown 和带文本层的 PDF。
SUPPORTED_SUFFIXES = {".txt", ".md", ".pdf"}
# 为当前模块创建独立 logger，便于按模块筛选日志。
logger = logging.getLogger(__name__)


def _read_text_bytes(data: bytes, path: Path) -> str:
    try:
        # 优先处理 UTF-8，同时自动去掉可能存在的 BOM。
        return data.decode("utf-8-sig")
    except UnicodeDecodeError:
        try:
            # 兼容部分中文 Windows 文档常见的 GB18030 编码。
            logger.warning("文件 %s 不是 UTF-8，尝试使用 GB18030 解码", path)
            return data.decode("gb18030")
        except UnicodeDecodeError:
            # 最后的兜底策略是不让单个坏文件阻塞整个目录索引。
            logger.warning("文件 %s 无法可靠解码，将使用 UTF-8 replacement", path)
            return data.decode("utf-8", errors="replace")


def _extract_pdf_text(path: Path) -> str:
    try:
        # 延迟导入，保证只使用 TXT/Markdown 时仍能清晰报告 PDF 依赖问题。
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - requirements 会安装 pypdf
        raise RuntimeError("PDF 抽取需要 pypdf，请先安装 requirements.txt") from exc

    # PdfReader 负责解析 PDF 文件结构和页面对象。
    reader = PdfReader(str(path))
    # 每页文本单独收集，最后用空行连接，避免相邻页内容粘连。
    pages: list[str] = []
    for page_number, page in enumerate(reader.pages, start=1):
        try:
            # 某些 PDF 页面没有文本层，extract_text 会返回 None。
            pages.append(page.extract_text() or "")
        except Exception:
            # 单页失败时记录堆栈并继续读取其余页面。
            logger.exception("抽取 PDF %s 的第 %s 页失败", path, page_number)
    return "\n\n".join(pages)


def extract_document(path: Path) -> ExtractedDocument:
    """读取一个支持的文件，并计算内容哈希用于增量索引。"""

    # 展开用户目录符号并转成绝对路径，确保数据库键稳定。
    path = path.expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"文件不存在：{path}")
    # 统一使用小写后缀，兼容 .TXT、.Md 等大小写变体。
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_SUFFIXES:
        raise ValueError(f"不支持的文件类型：{path.suffix or '<无扩展名>'}")

    # 一次读取原始字节，既用于计算哈希，也用于 TXT/Markdown 解码。
    data = path.read_bytes()
    stat = path.stat()
    file_hash = hashlib.sha256(data).hexdigest()
    if suffix == ".pdf":
        # PDF 文本由 pypdf 根据页面结构抽取，不能直接把二进制内容 decode 成文本。
        text = _extract_pdf_text(path)
    else:
        # TXT 和 Markdown 直接走带编码降级策略的文本读取。
        text = _read_text_bytes(data, path)

    # 返回统一的文档对象，供清洗器和索引器继续处理。
    return ExtractedDocument(
        path=path,
        file_type=suffix[1:],
        text=text,
        sha256=file_hash,
        size=stat.st_size,
        modified_ns=stat.st_mtime_ns,
    )

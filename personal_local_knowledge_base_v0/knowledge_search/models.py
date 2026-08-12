# dataclass 用来定义轻量的数据对象，避免手写初始化和比较逻辑。
from dataclasses import dataclass
# Path 用于表达源文件路径，并提供跨平台的路径操作。
from pathlib import Path


@dataclass(frozen=True)
class ExtractedDocument:
    """已从文件中读取出的原始文档及其文件元数据。"""

    # 文件的规范化绝对路径，也是数据库中的唯一标识。
    path: Path
    # 文件类型，例如 ``txt``、``md`` 或 ``pdf``。
    file_type: str
    # 兼容旧接口的全文字段；实际文件抽取时为 None，索引使用流式迭代器。
    text: str | None
    # 原始文件内容的 SHA-256，用于判断是否需要增量重建索引。
    sha256: str
    # 文件字节大小，用于保存文档元数据。
    size: int
    # 文件最后修改时间的纳秒表示，用于保存文档元数据。
    modified_ns: int
    # 解析配置指纹；普通文档为空，JSON 配置变化时用于触发重新索引。
    parser_fingerprint: str = ""


@dataclass(frozen=True)
class Chunk:
    """文档被切分后的一个可检索片段。"""

    # 一个文档内部的连续分段编号，从 0 开始。
    index: int
    # 实际写入 SQLite 和 FTS5 的文本内容。
    content: str
    # 分段在原文中的起始偏移；V0 暂时保留字段，默认值为 0。
    start_offset: int = 0


@dataclass(frozen=True)
class SearchResult:
    """一条搜索命中。score 使用 SQLite FTS5 的 bm25 分数。"""

    # SQLite chunks 表中的分段主键。
    chunk_id: int
    # 命中文档的绝对路径。
    document_path: str
    # 文档显示名称，不包含目录。
    filename: str
    # 文档扩展名对应的类型。
    file_type: str
    # 分段在源文档中的编号。
    chunk_index: int
    # 未添加标记的原始分段文本。
    content: str
    # SQLite FTS5 bm25 排序分数；分数越小通常越相关。
    score: float
    # 使用 HTML-like mark 标签处理后的文本，供程序或测试使用。
    highlighted_content: str


@dataclass(frozen=True)
class DocumentInfo:
    """已索引文档及其可管理的统计信息。"""

    document_id: int
    path: str
    filename: str
    file_type: str
    size: int
    chunk_count: int
    indexed_at: str


@dataclass(frozen=True)
class DatabaseHealth:
    """数据库一致性检查结果。"""

    document_count: int
    chunk_count: int
    chunks_fts_count: int
    chunk_tokens_count: int
    chunks_fts_jieba_count: int
    issues: tuple[str, ...] = ()

    @property
    def healthy(self) -> bool:
        return not self.issues


@dataclass(frozen=True)
class IndexProgress:
    """索引器发出的单文件进度事件。"""

    # 当前文件在本次索引任务中的序号，从 1 开始。
    current: int
    # 本次实际纳入处理的文件总数。
    total: int
    # 正在处理或刚处理完的文件路径。
    path: Path
    # ``processing``、``indexed``、``skipped``、``empty``、``oversized`` 或 ``failed``。
    status: str


@dataclass
class IndexStats:
    # 本次发现的支持类型文件数量。
    files_found: int = 0
    # 成功新增或更新的文档数量。
    indexed: int = 0
    # 因哈希未变化而跳过的文档数量。
    skipped: int = 0
    # 读取成功但没有可索引文本的文件数量。
    empty: int = 0
    # 处理过程中发生异常的文件数量。
    failed: int = 0
    # 因超过 JSON 大小上限而拒绝处理的文件数量。
    oversized: int = 0

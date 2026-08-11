"""SQLite 持久化、jieba 中文索引和 FTS5 混合搜索。"""

from __future__ import annotations

# logging 用于记录数据库初始化和 FTS5 查询异常。
import logging
# sqlite3 是 Python 标准库中的 SQLite 驱动。
import sqlite3
# Path 用于创建数据库目录并稳定处理文件路径。
from pathlib import Path
# Iterable 允许 replace_document 接收列表、生成器等任意分段集合。
from typing import Iterable

# 搜索模块同时复用查询转义和高亮逻辑。
from .highlighting import highlight_text, query_terms, to_fts_query
# 这些数据模型让数据库层不直接暴露裸元组。
from .models import Chunk, ExtractedDocument, SearchResult
# jieba 词项用于构建第二套中文搜索索引。
from .tokenization import tokenize_for_search, to_token_fts_query


logger = logging.getLogger(__name__)

# 统一初始化脚本：普通表保存源数据，FTS5 虚拟表保存可检索索引。
SCHEMA = """
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY,
    path TEXT NOT NULL UNIQUE,
    filename TEXT NOT NULL,
    file_type TEXT NOT NULL,
    sha256 TEXT NOT NULL,
    size INTEGER NOT NULL,
    modified_ns INTEGER NOT NULL,
    indexed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS chunks (
    id INTEGER PRIMARY KEY,
    document_id INTEGER NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    start_offset INTEGER NOT NULL DEFAULT 0,
    UNIQUE(document_id, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_chunks_document_id ON chunks(document_id);

-- external-content FTS5 表只保存索引，正文仍以 chunks 表为准。
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
    content,
    content='chunks',
    content_rowid='id',
    tokenize='unicode61'
);

-- 插入分段时同步写入 FTS5 索引。
CREATE TRIGGER IF NOT EXISTS chunks_ai AFTER INSERT ON chunks BEGIN
    INSERT INTO chunks_fts(rowid, content) VALUES (new.id, new.content);
END;

-- 删除分段时发送 FTS5 的特殊 delete 指令，移除旧索引内容。
CREATE TRIGGER IF NOT EXISTS chunks_ad AFTER DELETE ON chunks BEGIN
    INSERT INTO chunks_fts(chunks_fts, rowid, content)
    VALUES ('delete', old.id, old.content);
END;

-- 更新正文时先删除旧索引，再插入新正文。
CREATE TRIGGER IF NOT EXISTS chunks_au AFTER UPDATE OF content ON chunks BEGIN
    INSERT INTO chunks_fts(chunks_fts, rowid, content)
    VALUES ('delete', old.id, old.content);
    INSERT INTO chunks_fts(rowid, content) VALUES (new.id, new.content);
END;

-- 保存每个分段的 jieba 词序列，作为中文 FTS5 的外部内容表。
CREATE TABLE IF NOT EXISTS chunk_tokens (
    chunk_id INTEGER PRIMARY KEY REFERENCES chunks(id) ON DELETE CASCADE,
    tokens TEXT NOT NULL
);

-- 中文索引使用空格分隔的 jieba 词，仍由 SQLite FTS5 负责倒排和 BM25 排序。
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts_jieba USING fts5(
    tokens,
    content='chunk_tokens',
    content_rowid='chunk_id',
    tokenize='unicode61'
);

-- 新增词序列时同步写入中文 FTS5 索引。
CREATE TRIGGER IF NOT EXISTS chunk_tokens_ai AFTER INSERT ON chunk_tokens BEGIN
    INSERT INTO chunks_fts_jieba(rowid, tokens) VALUES (new.chunk_id, new.tokens);
END;

-- 删除词序列时同步删除中文 FTS5 索引。
CREATE TRIGGER IF NOT EXISTS chunk_tokens_ad AFTER DELETE ON chunk_tokens BEGIN
    INSERT INTO chunks_fts_jieba(chunks_fts_jieba, rowid, tokens)
    VALUES ('delete', old.chunk_id, old.tokens);
END;

-- 更新词序列时先删除旧索引，再写入新索引。
CREATE TRIGGER IF NOT EXISTS chunk_tokens_au AFTER UPDATE OF tokens ON chunk_tokens BEGIN
    INSERT INTO chunks_fts_jieba(chunks_fts_jieba, rowid, tokens)
    VALUES ('delete', old.chunk_id, old.tokens);
    INSERT INTO chunks_fts_jieba(rowid, tokens) VALUES (new.chunk_id, new.tokens);
END;
"""


class KnowledgeBase:
    """一个 SQLite 知识库实例，负责连接生命周期和数据操作。"""

    def __init__(self, db_path: Path):
        # 记录规范化后的数据库路径，避免同一文件被不同相对路径打开。
        self.db_path = Path(db_path).expanduser().resolve()
        # 默认数据库目录可能不存在，先创建目录。
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        # 建立 SQLite 连接，并让查询结果可以通过列名访问。
        self.connection = sqlite3.connect(self.db_path)
        self.connection.row_factory = sqlite3.Row
        # 开启外键级联，删除文档时自动删除其分段。
        self.connection.execute("PRAGMA foreign_keys = ON")
        # WAL 提升读写并发性，NORMAL 同步级别适合这个本地 V0 工具。
        self.connection.execute("PRAGMA journal_mode = WAL")
        self.connection.execute("PRAGMA synchronous = NORMAL")
        # 连接创建后立即保证表、虚拟表和触发器存在。
        self.initialize()

    def __enter__(self) -> "KnowledgeBase":
        # 支持 ``with KnowledgeBase(...)``，让调用方自动关闭连接。
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        # 无论 with 代码块是否抛出异常，都释放 SQLite 连接。
        self.close()

    def initialize(self) -> None:
        try:
            # executescript 可以一次创建所有表、索引和触发器。
            self.connection.executescript(SCHEMA)
            # 显式提交初始化结果，确保后续查询立即可见。
            self.connection.commit()
            # 旧版本数据库没有 jieba 词表，需要按分段逐条补建中文索引。
            self._backfill_token_index()
        except sqlite3.DatabaseError:
            # 记录完整堆栈后继续抛出，让 CLI 返回失败状态码。
            logger.exception("初始化 SQLite 数据库失败：%s", self.db_path)
            raise

    def _backfill_token_index(self) -> None:
        """为已有 chunks 增量补建 jieba 词表，避免升级后中文索引为空。"""

        chunk_count = self.connection.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        token_count = self.connection.execute("SELECT COUNT(*) FROM chunk_tokens").fetchone()[0]
        if chunk_count == token_count:
            # 数量一致时认为词表已经同步，避免每次启动都重复分词。
            return

        logger.info("正在补建 jieba 中文索引：%s 个分段", chunk_count)
        with self.connection:
            # 先清空旧词表，触发器会同步清理对应的 FTS5 内容。
            self.connection.execute("DELETE FROM chunk_tokens")
            rows = self.connection.execute("SELECT id, content FROM chunks ORDER BY id")
            # 逐行分词并写入，避免把所有旧分段一次性加载到 Python 列表。
            self.connection.executemany(
                "INSERT INTO chunk_tokens(chunk_id, tokens) VALUES (?, ?)",
                (
                    (row["id"], " ".join(tokenize_for_search(row["content"])))
                    for row in rows
                ),
            )

    def close(self) -> None:
        # 关闭连接，释放文件句柄和 WAL 相关资源。
        self.connection.close()

    def is_unchanged(self, document: ExtractedDocument) -> bool:
        # 只比较内容哈希；文件时间变化但内容未变时仍可安全跳过。
        row = self.connection.execute(
            "SELECT sha256 FROM documents WHERE path = ?", (str(document.path),)
        ).fetchone()
        # 没有旧记录，或哈希不同，都意味着需要重新索引。
        return row is not None and row["sha256"] == document.sha256

    def replace_document(self, document: ExtractedDocument, chunks: Iterable[Chunk]) -> int:
        """原子替换同路径文档；FTS5 通过触发器同步。"""

        with self.connection:
            # 找到同路径旧文档后先删除，外键和触发器会同步清理旧分段/索引。
            old = self.connection.execute(
                "SELECT id FROM documents WHERE path = ?", (str(document.path),)
            ).fetchone()
            if old is not None:
                self.connection.execute("DELETE FROM documents WHERE id = ?", (old["id"],))

            # 插入新的文档元数据，并取得自增主键。
            cursor = self.connection.execute(
                """
                INSERT INTO documents(path, filename, file_type, sha256, size, modified_ns)
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    str(document.path),
                    document.path.name,
                    document.file_type,
                    document.sha256,
                    document.size,
                    document.modified_ns,
                ),
            )
            document_id = int(cursor.lastrowid)
            # 批量消费分段迭代器；不会先把整个文档的 chunks 转成 list。
            # chunks_ai 触发器会在每次插入后同步到 FTS5。
            self.connection.executemany(
                """
                INSERT INTO chunks(document_id, chunk_index, content, start_offset)
                VALUES (?, ?, ?, ?)
                """,
                (
                    (document_id, chunk.index, chunk.content, chunk.start_offset)
                    for chunk in chunks
                ),
            )
            # chunks 已经写入后，按分段逐条生成 jieba 词序列并同步中文索引。
            new_chunks = self.connection.execute(
                "SELECT id, content FROM chunks WHERE document_id = ? ORDER BY chunk_index",
                (document_id,),
            )
            self.connection.executemany(
                "INSERT INTO chunk_tokens(chunk_id, tokens) VALUES (?, ?)",
                (
                    (row["id"], " ".join(tokenize_for_search(row["content"])))
                    for row in new_chunks
                ),
            )
        # with self.connection 成功退出后事务已经提交，返回文档 ID 供调用方使用。
        return document_id

    def remove_document(self, path: Path) -> None:
        """删除指定路径的文档及其 FTS5 内容。"""

        # 删除 documents 行会通过 ON DELETE CASCADE 删除 chunks，触发器再清除 FTS5。
        with self.connection:
            self.connection.execute("DELETE FROM documents WHERE path = ?", (str(path),))

    def _search_fts_rows(
        self,
        table_name: str,
        match_query: str,
        limit: int,
    ) -> list[sqlite3.Row]:
        """在指定 FTS5 表中执行一次安全的关键词查询。"""

        # table_name 只由本模块内部传入，不能直接使用用户输入，避免 SQL 注入。
        if table_name not in {"chunks_fts", "chunks_fts_jieba"}:
            raise ValueError(f"未知的 FTS5 表：{table_name}")

        # 两套 FTS 表都通过 rowid 关联到同一份 chunks 正文和 documents 元数据。
        return self.connection.execute(
            f"""
            SELECT
                c.id AS chunk_id,
                d.path AS document_path,
                d.filename AS filename,
                d.file_type AS file_type,
                c.chunk_index AS chunk_index,
                c.content AS content,
                bm25({table_name}) AS score
            FROM {table_name}
            JOIN chunks AS c ON c.id = {table_name}.rowid
            JOIN documents AS d ON d.id = c.document_id
            WHERE {table_name} MATCH ?
            ORDER BY score ASC, d.path ASC, c.chunk_index ASC
            LIMIT ?
            """,
            (match_query, limit),
        ).fetchall()

    def search(self, query: str, limit: int = 10) -> list[SearchResult]:
        """先用 jieba 词索引搜索，再按顺序回退到原始 FTS5 和 LIKE。"""

        # 限制必须为正数，否则 LIMIT 的语义不符合 CLI 预期。
        if limit <= 0:
            raise ValueError("limit 必须大于 0")

        # 普通查询保留给原始 FTS5 作为回退路径。
        raw_query = to_fts_query(query)
        token_query = to_token_fts_query(query)
        rows: list[sqlite3.Row] = []

        try:
            if token_query:
                # 第一优先级：jieba 词序列 + FTS5 BM25，中文词边界更准确。
                rows = self._search_fts_rows("chunks_fts_jieba", token_query, limit)
            if not rows:
                # 第二优先级：原始文本 FTS5，兼容 jieba 词切分不理想的查询。
                rows = self._search_fts_rows("chunks_fts", raw_query, limit)
        except sqlite3.OperationalError as exc:
            # 将底层 SQLite 异常转换为 CLI 能理解的 ValueError。
            logger.exception("FTS5 搜索失败，查询=%r", query)
            raise ValueError(f"搜索失败：{exc}") from exc

        # unicode61 对连续中文的分词能力有限。两套 FTS5 都没命中时，
        # 最后才使用参数化 LIKE 兜底，保证老数据库或特殊词仍有机会召回。
        contains_cjk = any(
            any("\u4e00" <= char <= "\u9fff" for char in term)
            for term in query_terms(query)
        )
        if not rows and contains_cjk:
            # LIKE 词项与 FTS5 使用相同的 AND 语义，避免无关结果过多。
            like_terms = query_terms(query)
            # 条件模板只由程序生成，真正的用户词仍通过参数绑定传入。
            where_clause = " AND ".join("c.content LIKE ?" for _ in like_terms)
            # 兜底结果没有 FTS5 bm25 分数，使用 0.0 作为显示值。
            rows = self.connection.execute(
                f"""
                SELECT
                    c.id AS chunk_id,
                    d.path AS document_path,
                    d.filename AS filename,
                    d.file_type AS file_type,
                    c.chunk_index AS chunk_index,
                    c.content AS content,
                    0.0 AS score
                FROM chunks AS c
                JOIN documents AS d ON d.id = c.document_id
                WHERE {where_clause}
                ORDER BY d.path ASC, c.chunk_index ASC
                LIMIT ?
                """,
                [*(f"%{term}%" for term in like_terms), limit],
            ).fetchall()

        # 将 SQLite 行转换为稳定的 SearchResult，并计算程序侧高亮文本。
        return [
            SearchResult(
                chunk_id=int(row["chunk_id"]),
                document_path=row["document_path"],
                filename=row["filename"],
                file_type=row["file_type"],
                chunk_index=int(row["chunk_index"]),
                content=row["content"],
                score=float(row["score"]),
                highlighted_content=highlight_text(row["content"], query),
            )
            for row in rows
        ]

    def document_count(self) -> int:
        # 统计文档表中的源文件数量。
        row = self.connection.execute("SELECT COUNT(*) AS count FROM documents").fetchone()
        return int(row["count"])

    def chunk_count(self) -> int:
        # 统计所有文档分段数量，用于 stats 命令和实验观察。
        row = self.connection.execute("SELECT COUNT(*) AS count FROM chunks").fetchone()
        return int(row["count"])

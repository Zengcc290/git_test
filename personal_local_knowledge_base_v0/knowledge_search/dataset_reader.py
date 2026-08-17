"""统一读取 Hugging Face 数据集和本地数据集文件的适配层。

物理格式由 ``datasets`` 负责解码；本模块只负责选择数据集适配器，
并把不同字段布局归一为稳定的记录字典。导入 ``datasets`` 是惰性的，
因此不安装可选依赖时，V0 原有的本地文档索引仍可以正常使用。
"""

from __future__ import annotations

import gc
import hashlib
from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path
from typing import Any, Callable

from .models import DocumentBlock


DATASET_RECORD_KEYS = ("id", "title", "text", "query", "answers", "meta")
DatasetAdapter = Callable[[Mapping[str, Any], int], dict[str, Any]]


class DatasetReaderError(RuntimeError):
    """数据集读取或适配失败。"""


def _load_dataset(*args: Any, **kwargs: Any):
    """Load ``datasets`` lazily so the base application has no hard import cost."""

    try:
        from datasets import load_dataset
    except ImportError as exc:  # pragma: no cover - exercised without optional dep
        raise DatasetReaderError(
            "数据集读取需要可选依赖，请安装：pip install datasets pyarrow"
        ) from exc
    return load_dataset(*args, **kwargs)


def _value(row: Mapping[str, Any], key: str, default: Any = None) -> Any:
    value = row.get(key, default)
    return default if value is None else value


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _base_record(index: int) -> dict[str, Any]:
    return {
        "id": str(index),
        "title": None,
        "text": None,
        "query": None,
        "answers": [],
        "meta": {},
    }


def _nested(row: Mapping[str, Any], *keys: str) -> Any:
    value: Any = row
    for key in keys:
        if not isinstance(value, Mapping):
            return None
        value = value.get(key)
    return value


def _normalize_dureader(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    record = _base_record(index)
    record["query"] = _text(_value(row, "anchor"))
    record["text"] = _text(_value(row, "positive"))
    record["meta"]["negatives"] = [
        text
        for position in range(1, 16)
        if (text := _text(_value(row, f"negative_{position}")))
    ]
    return record


def _normalize_github_code(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    record = _base_record(index)
    repository = _text(_value(row, "repo_name"))
    path = _text(_value(row, "path"))
    record["id"] = f"{repository or ''}:{path or index}"
    record["title"] = path
    record["text"] = _text(_value(row, "code"))
    record["meta"] = {
        "repository": repository,
        "language": _value(row, "language"),
        "license": _value(row, "license"),
    }
    return record


def _normalize_codesearchnet(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    record = _base_record(index)
    record["id"] = _text(_value(row, "url")) or str(index)
    record["title"] = _text(_value(row, "func_name"))
    record["text"] = _text(_value(row, "whole_func_string"))
    record["query"] = _text(_value(row, "docstring"))
    record["meta"] = {
        "repository": _value(row, "repository_name"),
        "path": _value(row, "func_path_in_repository"),
    }
    return record


def _normalize_narrativeqa(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    record = _base_record(index)
    document_id = _nested(row, "document", "id")
    record["id"] = str(document_id) if document_id is not None else str(index)
    record["title"] = _text(_nested(row, "document", "summary", "title"))
    record["text"] = _text(_nested(row, "document", "text"))
    record["query"] = _text(_nested(row, "question", "text"))
    answers = _value(row, "answers", [])
    if isinstance(answers, Iterable) and not isinstance(answers, (str, bytes, Mapping)):
        record["answers"] = [
            text
            for answer in answers
            if isinstance(answer, Mapping)
            and (text := _text(answer.get("text")))
        ]
    return record


def _normalize_natural_questions(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    record = _base_record(index)
    document = _value(row, "document", {})
    tokens = _value(document, "tokens", {}) if isinstance(document, Mapping) else {}
    token_values = _value(tokens, "token", []) if isinstance(tokens, Mapping) else []
    html_values = _value(tokens, "is_html", []) if isinstance(tokens, Mapping) else []
    if isinstance(token_values, Iterable) and not isinstance(token_values, (str, bytes)):
        if not isinstance(html_values, Iterable) or isinstance(html_values, (str, bytes)):
            html_values = []
        html_flags = list(html_values)
        record["text"] = " ".join(
            str(token)
            for position, token in enumerate(token_values)
            if position >= len(html_flags) or not bool(html_flags[position])
        ).strip() or None
    record["id"] = str(_value(row, "id", index))
    record["title"] = _text(_value(document, "title")) if isinstance(document, Mapping) else None
    record["query"] = _text(_nested(row, "question", "text"))
    record["meta"]["annotations"] = _value(row, "annotations", [])
    return record


def _normalize_text_record(row: Mapping[str, Any], index: int) -> dict[str, Any]:
    record = _base_record(index)
    record["id"] = str(_value(row, "_id", index))
    record["title"] = _text(_value(row, "title"))
    record["text"] = _text(_value(row, "text"))
    return record


_ADAPTERS: dict[str, DatasetAdapter] = {
    "dureader": _normalize_dureader,
    "github_code": _normalize_github_code,
    "codesearchnet": _normalize_codesearchnet,
    "narrativeqa": _normalize_narrativeqa,
    "natural_questions": _normalize_natural_questions,
    "msmarco": _normalize_text_record,
    "hotpotqa": _normalize_text_record,
}


def register_adapter(
    dataset_name: str,
    adapter: DatasetAdapter,
    *,
    replace: bool = False,
) -> None:
    """Register a dataset field adapter without changing physical readers."""

    name = str(dataset_name).strip().lower()
    if not name:
        raise ValueError("dataset_name 不能为空")
    if not callable(adapter):
        raise TypeError("adapter 必须可调用")
    if name in _ADAPTERS and not replace:
        raise ValueError(f"数据集适配器已存在：{name}")
    _ADAPTERS[name] = adapter


def available_adapters() -> tuple[str, ...]:
    """Return registered adapter names in deterministic order."""

    return tuple(sorted(_ADAPTERS))


def normalize(
    dataset_name: str,
    row: Mapping[str, Any],
    index: int,
) -> dict[str, Any]:
    """Normalize one dataset row to ``id/title/text/query/answers/meta``."""

    if not isinstance(row, Mapping):
        raise DatasetReaderError(
            f"数据集记录必须是映射对象，实际类型：{type(row).__name__}"
        )
    adapter_name = str(dataset_name).strip().lower()
    adapter = _ADAPTERS.get(adapter_name)
    if adapter is None:
        raise ValueError(f"Unsupported dataset: {dataset_name}")
    record = adapter(row, index)
    if tuple(record) != DATASET_RECORD_KEYS:
        record = {key: record.get(key) for key in DATASET_RECORD_KEYS}
    record["id"] = str(record["id"])
    if not isinstance(record["answers"], list):
        record["answers"] = list(record["answers"] or [])
    if not isinstance(record["meta"], dict):
        record["meta"] = {"value": record["meta"]}
    return record


def _dataset_kwargs(config: str | None, split: str) -> dict[str, Any]:
    kwargs: dict[str, Any] = {"split": split, "streaming": True}
    if config is not None:
        kwargs["name"] = config
    return kwargs


def _iter_normalized_rows(
    dataset: Iterable[Mapping[str, Any]],
    adapter: str,
) -> Iterator[dict[str, Any]]:
    """Normalize rows and explicitly release local streaming file handles."""

    iterator = iter(dataset)
    try:
        for index, row in enumerate(iterator):
            yield normalize(adapter, row, index)
    finally:
        close_iterator = getattr(iterator, "close", None)
        if callable(close_iterator):
            close_iterator()
        close_dataset = getattr(dataset, "close", None)
        if callable(close_dataset):
            close_dataset()
        iterator = None
        dataset = None
        # Some datasets/fsspec compression wrappers release Windows file
        # handles only from finalizers, even after the stream is exhausted.
        gc.collect()


def iter_huggingface(
    repo: str,
    config: str | None,
    split: str,
    adapter: str,
) -> Iterator[dict[str, Any]]:
    """Stream a Hugging Face dataset and normalize each row lazily."""

    try:
        dataset = _load_dataset(repo, **_dataset_kwargs(config, split))
        try:
            yield from _iter_normalized_rows(dataset, adapter)
        finally:
            dataset = None
            gc.collect()
    except DatasetReaderError:
        raise
    except Exception as exc:
        raise DatasetReaderError(
            f"读取 Hugging Face 数据集失败：{repo}/{config or '<default>'}:{split}：{exc}"
        ) from exc


def infer_local_format(path: Path) -> str:
    """Infer a ``datasets`` builder name from Parquet/JSONL/GZIP suffixes."""

    suffixes = [suffix.lower() for suffix in Path(path).suffixes]
    if suffixes and suffixes[-1] == ".gz":
        suffixes.pop()
    if suffixes and suffixes[-1] in {".jsonl", ".json"}:
        return "json"
    if suffixes and suffixes[-1] == ".parquet":
        return "parquet"
    raise ValueError(
        f"无法从文件后缀推断数据集格式：{path}；目前支持 Parquet、JSONL 和 GZIP"
    )


def iter_local_dataset(
    path: Path,
    dataset_name: str,
    *,
    split: str = "train",
    file_format: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Stream a local Parquet/JSONL/GZIP file through ``datasets``."""

    local_path = Path(path).expanduser().resolve()
    if not local_path.is_file():
        raise FileNotFoundError(f"数据集文件不存在：{local_path}")
    builder = file_format or infer_local_format(local_path)
    try:
        dataset = _load_dataset(
            builder,
            data_files={split: str(local_path)},
            **_dataset_kwargs(None, split),
        )
        try:
            yield from _iter_normalized_rows(dataset, dataset_name)
        finally:
            dataset = None
            gc.collect()
    except DatasetReaderError:
        raise
    except Exception as exc:
        raise DatasetReaderError(f"读取本地数据集失败：{local_path}：{exc}") from exc


def iter_local_dureader(path: Path) -> Iterator[dict[str, Any]]:
    """Convenience wrapper for a downloaded DuReader Parquet shard."""

    yield from iter_local_dataset(path, "dureader")


def iter_dataset_blocks(
    records: Iterable[Mapping[str, Any]],
    *,
    source_name: str,
) -> Iterator[DocumentBlock]:
    """Convert normalized records into independent structural blocks.

    Only ``record['text']`` becomes canonical source content. Titles and record
    ids are structural context; queries, answers and meta remain available on
    the normalized records for evaluation or caller-specific storage.
    """

    for index, record in enumerate(records):
        missing = [key for key in DATASET_RECORD_KEYS if key not in record]
        if missing:
            raise DatasetReaderError(
                f"统一记录缺少字段：{', '.join(missing)}（记录 {index}）"
            )
        content = _text(record["text"])
        if not content:
            continue
        record_id = str(record["id"])
        title = _text(record["title"])
        meta = record["meta"] if isinstance(record["meta"], Mapping) else {}
        language = _text(meta.get("language"))
        identity = f"{source_name}\0{record_id}\0{index}"
        block_id = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]
        yield DocumentBlock(
            block_id=block_id,
            path=f"dataset:{source_name}",
            block_type="dataset-record",
            language=language,
            heading_path=(title,) if title else (),
            symbol_path=(),
            content=content,
            start_line=None,
            end_line=None,
            page_number=None,
            hard_boundary_before=True,
            hard_boundary_after=True,
            record_path=f"{source_name}[{record_id}]",
            parser="huggingface-datasets",
        )


def iter_dataset(
    source: str | Path,
    dataset_name: str,
    *,
    config: str | None = None,
    split: str = "train",
    file_format: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Unified entry point for a local dataset file or HF repository."""

    candidate = Path(str(source)).expanduser()
    suffixes = {suffix.lower() for suffix in candidate.suffixes}
    looks_local = (
        isinstance(source, Path)
        or candidate.is_absolute()
        or candidate.is_file()
        or bool(suffixes & {".parquet", ".json", ".jsonl", ".gz"})
    )
    if looks_local:
        yield from iter_local_dataset(
            candidate,
            dataset_name,
            split=split,
            file_format=file_format,
        )
        return
    yield from iter_huggingface(str(source), config, split, dataset_name)

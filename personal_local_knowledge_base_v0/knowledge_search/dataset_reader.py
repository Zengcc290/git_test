"""统一读取 Hugging Face 数据集和本地数据集文件的适配层。

物理格式由 ``datasets`` 负责解码；本模块只负责选择数据集适配器，
并把不同字段布局归一为稳定的记录字典。导入 ``datasets`` 是惰性的，
因此不安装可选依赖时，V0 原有的本地文档索引仍可以正常使用。
"""

from __future__ import annotations

import gc
import gzip
import hashlib
import io
import zipfile
from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path
from typing import Any, Callable

from .models import DocumentBlock


DATASET_RECORD_KEYS = ("id", "title", "text", "query", "answers", "meta")
DatasetAdapter = Callable[[Mapping[str, Any], int], dict[str, Any]]

_NO_FIRST_ROW = object()
_AUTO_FORMATS = ("parquet", "json", "csv", "text")


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
    record["id"] = str(_value(row, "_id", _value(row, "id", index)))
    record["title"] = _text(_value(row, "title"))
    record["text"] = _text(
        _value(row, "text", _value(row, "content", _value(row, "body", _value(row, "passage"))))
    )
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


def infer_dataset_name(row: Mapping[str, Any]) -> str:
    """Infer a built-in adapter from one dataset row's field names.

    Only the first streamed row is inspected by callers, so this remains a
    constant-time startup check relative to dataset size. ``hotpotqa`` is the
    stable default for the generic ``_id/title/text`` layout shared by several
    passage datasets; callers can still override it explicitly when metadata
    semantics matter.
    """

    if not isinstance(row, Mapping):
        raise DatasetReaderError(
            f"无法自动识别数据集字段：记录必须是映射对象，实际类型：{type(row).__name__}"
        )
    fields = set(row)
    if {"anchor", "positive"}.issubset(fields):
        return "dureader"
    if {"repo_name", "path", "code"}.issubset(fields):
        return "github_code"
    if {"func_name", "whole_func_string", "docstring"}.issubset(fields):
        return "codesearchnet"
    document = row.get("document")
    if isinstance(document, Mapping):
        if isinstance(document.get("tokens"), Mapping) and {
            "question",
            "annotations",
        }.issubset(fields):
            return "natural_questions"
        if (
            isinstance(document.get("summary"), Mapping)
            and "question" in fields
            and "answers" in fields
        ):
            return "narrativeqa"
    if fields & {"text", "content", "body", "passage"}:
        return "hotpotqa"
    raise DatasetReaderError(
        "无法自动识别数据集字段；请指定 --dataset-name。"
        f" 首条记录字段：{', '.join(sorted(str(field) for field in fields)) or '<空>'}"
    )


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
    adapter: str | None,
    *,
    iterator: Iterator[Mapping[str, Any]] | None = None,
    first_row: Any = _NO_FIRST_ROW,
) -> Iterator[dict[str, Any]]:
    """Normalize rows and explicitly release local streaming file handles."""

    if iterator is None:
        iterator = iter(dataset)
    try:
        if first_row is not _NO_FIRST_ROW:
            selected_adapter = adapter or infer_dataset_name(first_row)
            yield normalize(selected_adapter, first_row, 0)
            start_index = 1
        else:
            if adapter is None:
                raise DatasetReaderError(
                    "无法自动识别空数据集；请指定 dataset_name 或确认 split 有数据"
                )
            selected_adapter = adapter
            start_index = 0
        for index, row in enumerate(iterator, start=start_index):
            yield normalize(selected_adapter, row, index)
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
    adapter: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Stream a Hugging Face dataset and normalize each row lazily."""

    if isinstance(adapter, str) and adapter.strip().lower() in {"", "auto", "infer"}:
        adapter = None
    try:
        dataset = _load_dataset(repo, **_dataset_kwargs(config, split))
        try:
            iterator = iter(dataset)
            try:
                first_row = next(iterator)
            except StopIteration:
                first_row = _NO_FIRST_ROW
            yield from _iter_normalized_rows(
                dataset,
                adapter,
                iterator=iterator,
                first_row=first_row,
            )
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


def _read_format_probe(path: Path, *, read_size: int = 8192) -> bytes:
    """Read a small decompressed sample without loading the dataset."""

    with path.open("rb") as stream:
        prefix = stream.read(4)
    if prefix == b"\x1f\x8b":
        with gzip.open(path, "rb") as stream:
            return stream.read(read_size)
    if prefix[:2] == b"PK" and zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for member in archive.infolist():
                if member.is_dir():
                    continue
                with archive.open(member) as stream:
                    return stream.read(read_size)
        return b""
    with path.open("rb") as stream:
        return stream.read(read_size)


def _auto_local_formats(path: Path) -> tuple[str, ...]:
    """Return likely ``datasets`` builders for a file with an unknown suffix.

    The suffix remains the fastest and least surprising signal. For arbitrary
    names, a short content probe only orders the candidate builders; the
    selected builder still validates the stream before any normalized row is
    emitted.
    """

    try:
        preferred = infer_local_format(path)
        return (preferred,) + tuple(
            builder for builder in _AUTO_FORMATS if builder != preferred
        )
    except ValueError:
        pass

    candidates = list(_AUTO_FORMATS)
    try:
        with path.open("rb") as stream:
            header = stream.read(8)
            stream.seek(-8, io.SEEK_END)
            footer = stream.read(8)
        if header.startswith(b"PAR1") and b"PAR1" in footer:
            return ("parquet",)
    except (OSError, ValueError):
        pass

    try:
        sample = _read_format_probe(path)
    except (OSError, EOFError, gzip.BadGzipFile, zipfile.BadZipFile):
        sample = b""
    if sample.startswith(b"PAR1"):
        # A compressed or archived Parquet file has no usable footer at the
        # outer path, but the decompressed probe still identifies its builder.
        return ("parquet",)
    text = sample.decode("utf-8-sig", errors="ignore").lstrip()
    if text.startswith(("{", "[")):
        candidates.remove("json")
        candidates.insert(0, "json")
    elif text and "," in text.splitlines()[0]:
        candidates.remove("csv")
        candidates.insert(0, "csv")
    elif text:
        candidates.remove("text")
        candidates.insert(0, "text")
    return tuple(candidates)


def _close_stream(dataset: Any, iterator: Any) -> None:
    close_iterator = getattr(iterator, "close", None)
    if callable(close_iterator):
        close_iterator()
    close_dataset = getattr(dataset, "close", None)
    if callable(close_dataset):
        close_dataset()


def _iter_local_auto(
    path: Path,
    dataset_name: str | None,
    split: str,
) -> Iterator[dict[str, Any]]:
    """Try dataset builders lazily when a local file has no known suffix."""

    errors: list[str] = []
    kwargs = {
        "data_files": {split: str(path)},
        **_dataset_kwargs(None, split),
    }
    for builder in _auto_local_formats(path):
        dataset: Any = None
        iterator: Any = None
        try:
            dataset = _load_dataset(builder, **kwargs)
            iterator = iter(dataset)
            try:
                first_row = next(iterator)
            except StopIteration:
                first_row = _NO_FIRST_ROW
        except DatasetReaderError:
            raise
        except Exception as exc:
            errors.append(f"{builder}: {exc}")
            _close_stream(dataset, iterator)
            gc.collect()
            continue

        try:
            yield from _iter_normalized_rows(
                dataset,
                dataset_name,
                iterator=iterator,
                first_row=first_row,
            )
        except DatasetReaderError:
            raise
        except Exception as exc:
            raise DatasetReaderError(
                f"读取本地数据集失败：{path}（builder={builder}）：{exc}"
            ) from exc
        return

    detail = "; ".join(errors) or "没有可用的 datasets builder"
    raise DatasetReaderError(
        f"读取本地数据集失败：{path}；无法识别物理格式：{detail}"
    )


def iter_local_dataset(
    path: Path,
    dataset_name: str | None = None,
    *,
    split: str = "train",
    file_format: str | None = None,
) -> Iterator[dict[str, Any]]:
    """Stream a local dataset through ``datasets``, independent of its suffix.

    ``file_format`` may be any builder accepted by ``datasets`` (for example
    ``"json"`` or ``"parquet"``). When omitted, known suffixes are used first;
    arbitrary names are content-probed and lazily tried with common builders.
    """

    local_path = Path(path).expanduser().resolve()
    if not local_path.is_file():
        raise FileNotFoundError(f"数据集文件不存在：{local_path}")
    requested_format = (
        file_format.strip().lower()
        if isinstance(file_format, str)
        else file_format
    )
    if requested_format in {"", "auto", "infer"}:
        requested_format = None
    if isinstance(dataset_name, str) and dataset_name.strip().lower() in {
        "",
        "auto",
        "infer",
    }:
        dataset_name = None
    if requested_format is None:
        yield from _iter_local_auto(local_path, dataset_name, split)
        return
    builder = requested_format
    try:
        dataset = _load_dataset(
            builder,
            data_files={split: str(local_path)},
            **_dataset_kwargs(None, split),
        )
        try:
            iterator = iter(dataset)
            try:
                first_row = next(iterator)
            except StopIteration:
                first_row = _NO_FIRST_ROW
            yield from _iter_normalized_rows(
                dataset,
                dataset_name,
                iterator=iterator,
                first_row=first_row,
            )
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
    dataset_name: str | None = None,
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

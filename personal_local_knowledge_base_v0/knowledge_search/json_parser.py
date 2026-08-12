"""配置驱动的 JSON 记录解析。"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any


_PATH_TOKEN = re.compile(r"(?:([^.[\]]+)|\[(\*|\d+)\])")
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
DEFAULT_JSON_READ_SIZE = 64 * 1024
DEFAULT_MAX_JSON_SIZE = 512 * 1024 * 1024


class JsonSizeLimitError(ValueError):
    """JSON 文件超过安全处理上限。"""


class _JsonEndOfStream(Exception):
    """Internal marker used when a streaming reader reaches clean EOF."""


@dataclass(frozen=True)
class JsonField:
    """一条待写入索引的 JSON 字段规则。"""

    path: str
    name: str | None = None
    join: str = "、"


@dataclass(frozen=True)
class JsonFilter:
    """一条记录过滤规则。"""

    path: str
    operator: str
    expected: Any = None


@dataclass(frozen=True)
class JsonProfile:
    """JSON 解析和索引配置。"""

    name: str
    record_path: str
    index_mode: str
    fields: tuple[JsonField, ...]
    separator: str
    filters: tuple[JsonFilter, ...]
    fingerprint: str
    config_path: Path | None = None

    @classmethod
    def from_file(cls, path: Path) -> "JsonProfile":
        """读取并校验 JSON 配置文件。"""

        config_path = Path(path).expanduser().resolve()
        if not config_path.is_file():
            raise FileNotFoundError(f"JSON 配置文件不存在：{config_path}")

        try:
            with config_path.open("r", encoding="utf-8-sig") as stream:
                raw_config = json.load(stream)
        except json.JSONDecodeError as exc:
            raise ValueError(f"JSON 配置格式错误：{config_path}：{exc}") from exc

        if not isinstance(raw_config, dict):
            raise ValueError("JSON 配置的根节点必须是对象")

        name = raw_config.get("name", config_path.stem)
        if not isinstance(name, str) or not name.strip():
            raise ValueError("JSON 配置的 name 必须是非空字符串")

        record_path = raw_config.get("record_path", "$")
        if not isinstance(record_path, str) or not record_path.strip():
            raise ValueError("JSON 配置的 record_path 必须是非空字符串")
        _parse_path(record_path)

        index_mode = raw_config.get("index_mode", "record")
        if not isinstance(index_mode, str) or index_mode not in {"record", "file"}:
            raise ValueError("JSON 配置的 index_mode 只能是 record 或 file")

        raw_fields = raw_config.get("fields")
        if not isinstance(raw_fields, list) or not raw_fields:
            raise ValueError("JSON 配置的 fields 必须是非空数组")

        fields: list[JsonField] = []
        for position, raw_field in enumerate(raw_fields, start=1):
            if isinstance(raw_field, str):
                raw_field = {"path": raw_field}
            if not isinstance(raw_field, dict):
                raise ValueError(f"fields[{position}] 必须是字符串或对象")

            field_path = raw_field.get("path")
            if not isinstance(field_path, str) or not field_path.strip():
                raise ValueError(f"fields[{position}].path 必须是非空字符串")
            _parse_path(field_path)

            field_name = raw_field.get("name")
            if field_name is not None and (
                not isinstance(field_name, str) or not field_name.strip()
            ):
                raise ValueError(f"fields[{position}].name 必须是非空字符串")

            join = raw_field.get("join", "、")
            if not isinstance(join, str):
                raise ValueError(f"fields[{position}].join 必须是字符串")
            fields.append(JsonField(path=field_path, name=field_name, join=join))

        filters = _parse_filters(raw_config.get("filter"))
        separator = raw_config.get("separator", "\n")
        if not isinstance(separator, str):
            raise ValueError("JSON 配置的 separator 必须是字符串")

        canonical_config = json.dumps(
            raw_config,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        )
        fingerprint = hashlib.sha256(canonical_config.encode("utf-8")).hexdigest()
        return cls(
            name=name.strip(),
            record_path=record_path,
            index_mode=index_mode,
            fields=tuple(fields),
            separator=separator,
            filters=filters,
            fingerprint=fingerprint,
            config_path=config_path,
        )


def ensure_json_size(path: Path, max_size: int = DEFAULT_MAX_JSON_SIZE) -> None:
    """在打开 JSON 前检查字节大小，避免意外处理超大数据文件。

    ``max_size=0`` 表示显式关闭限制；默认值仍然提供保护。检查使用文件
    元数据，不会读取正文，也不会改变流式解析的内存特性。
    """

    if max_size < 0:
        raise ValueError("JSON 最大文件大小不能小于 0")
    if max_size == 0:
        return

    json_path = Path(path).expanduser().resolve()
    size = json_path.stat().st_size
    if size > max_size:
        raise JsonSizeLimitError(
            f"JSON 文件超过大小上限：{json_path}（{size} 字节 > {max_size} 字节）"
        )


def _parse_filters(raw_filter: Any) -> tuple[JsonFilter, ...]:
    if raw_filter is None:
        return ()
    raw_filters = raw_filter if isinstance(raw_filter, list) else [raw_filter]
    filters: list[JsonFilter] = []
    supported_operators = {"equals", "not_equals", "in", "exists"}

    for position, item in enumerate(raw_filters, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"filter[{position}] 必须是对象")
        path = item.get("path")
        if not isinstance(path, str) or not path.strip():
            raise ValueError(f"filter[{position}].path 必须是非空字符串")
        _parse_path(path)

        operators = [key for key in supported_operators if key in item]
        if len(operators) != 1:
            raise ValueError(
                f"filter[{position}] 必须且只能设置一个条件："
                "equals、not_equals、in 或 exists"
            )
        operator = operators[0]
        expected = item[operator]
        if operator == "in" and (
            not isinstance(expected, list) or not expected
        ):
            raise ValueError(f"filter[{position}].in 必须是非空数组")
        if operator == "exists" and not isinstance(expected, bool):
            raise ValueError(f"filter[{position}].exists 必须是布尔值")
        filters.append(JsonFilter(path=path, operator=operator, expected=expected))
    return tuple(filters)


def _parse_path(path: str) -> tuple[str | int, ...]:
    """解析一个有限 JSONPath，支持点号字段和 [*]/[数字]。"""

    path = path.strip()
    if path == "$":
        return ()
    if path.startswith("$"):
        path = path[1:]
        if path.startswith("."):
            path = path[1:]
    if not path:
        return ()

    tokens: list[str | int] = []
    position = 0
    while position < len(path):
        if path[position] == ".":
            position += 1
            if position == len(path):
                raise ValueError("JSON 路径不能以 . 结尾")
        match = _PATH_TOKEN.match(path, position)
        if match is None:
            raise ValueError(f"不支持的 JSON 路径：{path}")
        field_name, array_index = match.groups()
        if field_name is not None:
            tokens.append(field_name)
        elif array_index == "*":
            tokens.append("*")
        else:
            tokens.append(int(array_index))
        position = match.end()
        if position < len(path) and path[position] not in ".[":
            raise ValueError(f"不支持的 JSON 路径：{path}")
    return tuple(tokens)


def _resolve(value: Any, path: str) -> list[Any]:
    """从 value 中读取路径对应的所有值。"""

    values = [value]
    for token in _parse_path(path):
        next_values: list[Any] = []
        for current in values:
            if token == "*":
                if isinstance(current, list):
                    next_values.extend(current)
                elif isinstance(current, dict):
                    next_values.extend(current.values())
                continue
            if isinstance(token, int):
                if isinstance(current, list) and token < len(current):
                    next_values.append(current[token])
                continue
            if isinstance(current, dict) and token in current:
                next_values.append(current[token])
        values = next_values
        if not values:
            break
    return values


def _scalar_text(value: Any, join: str) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (dict, list)):
        if isinstance(value, list):
            return join.join(
                text
                for item in value
                if (text := _scalar_text(item, join))
            )
        return json.dumps(value, ensure_ascii=False, sort_keys=True)
    return str(value)


def _field_text(record: Any, field: JsonField, root: Any) -> str:
    source = root if field.path.strip().startswith("$") else record
    values = _resolve(source, field.path)
    text = field.join.join(
        value_text
        for value in values
        if (value_text := _scalar_text(value, field.join))
    )
    if field.name and text:
        return f"{field.name}: {text}"
    return text


def _matches_filter(record: Any, rule: JsonFilter, root: Any) -> bool:
    source = root if rule.path.strip().startswith("$") else record
    values = _resolve(source, rule.path)
    if rule.operator == "exists":
        return bool(values) is rule.expected
    if rule.operator == "equals":
        return any(value == rule.expected for value in values)
    if rule.operator == "not_equals":
        return bool(values) and all(value != rule.expected for value in values)
    return any(value in rule.expected for value in values)


def _format_record(record: Any, profile: JsonProfile, root: Any) -> str:
    field_texts = [
        text
        for field in profile.fields
        if (text := _field_text(record, field, root))
    ]
    return profile.separator.join(field_texts)


class _JsonChunkReader:
    """Read JSON values from a bounded text buffer.

    ``json.JSONDecoder.raw_decode`` is deliberately used one value at a time.
    This handles JSON Lines and avoids the unbounded memory use of ``json.load``.
    A single JSON record still needs to fit in memory, but the file does not.
    """

    def __init__(self, path: Path, read_size: int) -> None:
        if read_size <= 0:
            raise ValueError("JSON read_size 必须大于 0")
        self.path = Path(path)
        self.stream = self.path.open("r", encoding="utf-8-sig", newline="")
        self.read_size = read_size
        self.decoder = json.JSONDecoder()
        self.buffer = ""
        self.position = 0
        self.eof = False

    def close(self) -> None:
        self.stream.close()

    def _fill(self) -> bool:
        if self.eof:
            return False
        chunk = self.stream.read(self.read_size)
        if not chunk:
            self.eof = True
            return False
        self.buffer += chunk
        return True

    def _compact(self) -> None:
        # Keep a small unread tail so parsing a large record does not repeatedly
        # copy the whole buffer after every delimiter.
        if self.position >= self.read_size:
            self.buffer = self.buffer[self.position :]
            self.position = 0

    def skip_whitespace(self) -> bool:
        while True:
            while self.position < len(self.buffer) and self.buffer[self.position].isspace():
                self.position += 1
            if self.position < len(self.buffer):
                return True
            if not self._fill():
                return False

    def peek(self) -> str:
        if not self.skip_whitespace():
            raise _JsonEndOfStream
        return self.buffer[self.position]

    def take(self) -> str:
        if not self.skip_whitespace():
            raise _JsonEndOfStream
        character = self.buffer[self.position]
        self.position += 1
        self._compact()
        return character

    def read_value(self) -> Any:
        while True:
            if not self.skip_whitespace():
                raise _JsonEndOfStream
            try:
                value, end = self.decoder.raw_decode(self.buffer, self.position)
            except json.JSONDecodeError:
                if self.eof or not self._fill():
                    raise
                continue
            self.position = end
            self._compact()
            return value


def _iter_json_values(
    path: Path,
    read_size: int = DEFAULT_JSON_READ_SIZE,
    max_size: int = DEFAULT_MAX_JSON_SIZE,
) -> Iterator[Any]:
    """Yield top-level JSON values without loading the complete file.

    A JSON Lines file produces one object per iteration.  A top-level JSON
    array produces one array element per iteration.  Other valid top-level
    values (including one object) are also supported.
    """

    path = Path(path).expanduser().resolve()
    ensure_json_size(path, max_size)
    reader = _JsonChunkReader(path, read_size)
    try:
        try:
            first = reader.peek()
        except _JsonEndOfStream:
            return
        if first == "[":
            reader.take()
            try:
                while True:
                    delimiter = reader.peek()
                    if delimiter == "]":
                        reader.take()
                        break
                    yield reader.read_value()
                    delimiter = reader.take()
                    if delimiter == "]":
                        break
                    if delimiter != ",":
                        raise ValueError(f"JSON 数组缺少逗号或结束符：{path}")
            except _JsonEndOfStream as exc:
                raise ValueError(f"JSON 数组缺少结束符：{path}") from exc
            if reader.skip_whitespace():
                raise ValueError(f"JSON 文件存在多余内容：{path}")
        else:
            while True:
                try:
                    yield reader.read_value()
                except _JsonEndOfStream:
                    break
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 文件格式错误：{path}：{exc}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"JSON 文件不是有效的 UTF-8：{Path(path)}：{exc}") from exc
    finally:
        reader.close()


def _iter_formatted_records(
    path: Path,
    profile: JsonProfile,
    *,
    read_size: int = DEFAULT_JSON_READ_SIZE,
    max_size: int = DEFAULT_MAX_JSON_SIZE,
) -> Iterator[str]:
    """Yield configured records while keeping only one root value in memory."""

    for root in _iter_json_values(path, read_size, max_size):
        records = [root] if profile.record_path.strip() == "$" else _resolve(
            root, profile.record_path
        )
        for record in records:
            if not all(_matches_filter(record, rule, root) for rule in profile.filters):
                continue
            text = _format_record(record, profile, root)
            if text:
                yield text


def iter_json_text(
    path: Path,
    profile: JsonProfile,
    *,
    read_size: int = DEFAULT_JSON_READ_SIZE,
    max_size: int = DEFAULT_MAX_JSON_SIZE,
) -> Iterator[str]:
    """按配置产生 JSON 文本；整个文件不会一次性载入内存。

    ``record`` 模式每次产生一条记录。``file`` 模式仍然把所有记录交给
    同一个下游分块器，但以多个文本块流过，避免拼接成一个超大字符串。
    """

    records = _iter_formatted_records(
        path,
        profile,
        read_size=read_size,
        max_size=max_size,
    )
    if profile.index_mode == "record":
        yield from records
        return

    first = True
    for text in records:
        if not first:
            yield profile.separator
        yield text
        first = False


@dataclass(frozen=True)
class JsonStructureEntry:
    """One path in a JSON structure summary."""

    path: str
    count: int
    types: tuple[tuple[str, int], ...]


@dataclass(frozen=True)
class JsonStructureReport:
    """Bounded-memory report returned by :func:`inspect_json_structure`."""

    path: Path
    records_scanned: int
    complete: bool
    entries: tuple[JsonStructureEntry, ...]


def _json_type(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _child_path(parent: str, key: str | int) -> str:
    if key == "*":
        return f"{parent}[*]"
    if isinstance(key, int):
        return f"{parent}[{key}]"
    if _IDENTIFIER.fullmatch(key):
        return f"{parent}.{key}"
    return f"{parent}[{json.dumps(key, ensure_ascii=False)}]"


def inspect_json_structure(
    path: Path,
    *,
    max_records: int = 100,
    read_size: int = DEFAULT_JSON_READ_SIZE,
    max_depth: int = 20,
    max_paths: int = 10_000,
    max_size: int = DEFAULT_MAX_JSON_SIZE,
) -> JsonStructureReport:
    """Scan JSON Lines/array records and return paths, types and counts.

    ``max_records=0`` scans until EOF.  The default samples the first 100
    records, which is usually enough to discover a schema without waiting for
    a multi-gigabyte file.  Only one parsed record and the path counters are
    retained.
    """

    if max_records < 0:
        raise ValueError("max_records 不能小于 0")
    if max_depth < 0:
        raise ValueError("max_depth 不能小于 0")
    if max_paths <= 0:
        raise ValueError("max_paths 必须大于 0")

    path = Path(path).expanduser().resolve()
    entries: dict[str, tuple[int, Counter[str]]] = {}
    records_scanned = 0
    truncated = False

    def visit(value: Any, current_path: str, depth: int) -> None:
        if current_path not in entries and len(entries) >= max_paths:
            return
        count, types = entries.setdefault(current_path, (0, Counter()))
        types[_json_type(value)] += 1
        entries[current_path] = (count + 1, types)
        if depth >= max_depth:
            return
        if isinstance(value, dict):
            for key, child in value.items():
                visit(child, _child_path(current_path, key), depth + 1)
        elif isinstance(value, list):
            for child in value:
                visit(child, _child_path(current_path, "*"), depth + 1)

    values = iter(_iter_json_values(path, read_size, max_size))
    while True:
        if max_records and records_scanned >= max_records:
            truncated = True
            break
        try:
            value = next(values)
        except StopIteration:
            break
        visit(value, "$", 0)
        records_scanned += 1

    structure_entries = tuple(
        JsonStructureEntry(
            path=entry_path,
            count=count,
            types=tuple(sorted(type_counts.items())),
        )
        for entry_path, (count, type_counts) in sorted(entries.items())
    )
    return JsonStructureReport(
        path=path,
        records_scanned=records_scanned,
        complete=not truncated,
        entries=structure_entries,
    )


def parse_json_preview(
    path: Path,
    profile: JsonProfile,
    limit: int,
    *,
    max_size: int = DEFAULT_MAX_JSON_SIZE,
) -> list[str]:
    """返回供 CLI 预览的已格式化记录。"""

    if limit <= 0:
        raise ValueError("preview limit 必须大于 0")
    records: list[str] = []
    for record in _iter_formatted_records(path, profile, max_size=max_size):
        records.append(record)
        if len(records) >= limit:
            break
    if profile.index_mode == "file":
        return [profile.separator.join(records)] if records else []
    return records

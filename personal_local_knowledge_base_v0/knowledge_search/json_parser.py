"""配置驱动的 JSON 记录解析。"""

from __future__ import annotations

import hashlib
import json
import logging
import re
from collections import Counter
from collections.abc import Iterator
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation
from pathlib import Path
import tempfile
from typing import Any


_PATH_TOKEN = re.compile(r"(?:([^.[\]]+)|\[(\*|\d+)\])")
_IDENTIFIER = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")
DEFAULT_JSON_READ_SIZE = 64 * 1024
# 文件上限由调用方按数据源配置；记录级探测另有独立的 512 MiB 逻辑窗口。
DEFAULT_MAX_JSON_SIZE = 512 * 1024 * 1024
DEFAULT_JSON_RECORD_PROBE_SIZE = 512 * 1024 * 1024
_SIZE_PATTERN = re.compile(
    r"^\s*(?P<number>\d+(?:\.\d+)?)\s*"
    r"(?P<unit>B|KB|KIB|MB|MIB|GB|GIB|TB|TIB)?\s*$",
    re.IGNORECASE,
)
_SIZE_FACTORS = {
    "B": 1,
    "KB": 1024,
    "KIB": 1024,
    "MB": 1024**2,
    "MIB": 1024**2,
    "GB": 1024**3,
    "GIB": 1024**3,
    "TB": 1024**4,
    "TIB": 1024**4,
}


logger = logging.getLogger(__name__)


def parse_size(value: str | int) -> int:
    """将 ``1GB``、``512MB`` 等人类可读大小转换为字节数。

    未带单位的数字仍按字节处理，以兼容原有 CLI 用法；MB/GB 使用
    1024 进制，和项目现有的 512 MiB 默认保护保持一致。也接受显式的
    ``KiB``、``MiB``、``GiB`` 和 ``TiB`` 写法，以及小数大小如 ``1.5GB``。
    """

    if isinstance(value, bool):
        raise ValueError("文件大小不能是布尔值")
    if isinstance(value, int):
        if value < 0:
            raise ValueError("文件大小不能小于 0")
        return value
    if not isinstance(value, str):
        raise ValueError("文件大小必须是数字或带单位的字符串，例如 512MB")

    match = _SIZE_PATTERN.fullmatch(value)
    if match is None:
        raise ValueError(
            f"无法识别文件大小：{value!r}；示例：512MB、1GB、0"
        )

    try:
        amount = Decimal(match.group("number"))
    except InvalidOperation as exc:  # pragma: no cover - 正则已过滤正常输入
        raise ValueError(f"无法识别文件大小：{value!r}") from exc

    unit = (match.group("unit") or "B").upper()
    size = amount * _SIZE_FACTORS[unit]
    if size != size.to_integral_value():
        raise ValueError(f"文件大小换算后不是完整字节数：{value!r}")
    return int(size)


class JsonSizeLimitError(ValueError):
    """JSON 文件超过安全处理上限。"""


class _JsonEndOfStream(Exception):
    """Internal marker used when a streaming reader reaches clean EOF."""


class _LargeJsonRecord:
    """A JSON record whose raw text must remain streamed instead of parsed."""

    def __init__(self, scanner: "_RawValueScanner") -> None:
        self._scanner = scanner

    def iter_chunks(self) -> Iterator[str]:
        """Yield the complete raw record in bounded text chunks."""

        try:
            yield from self._scanner.iter_large_chunks()
        finally:
            self.close()

    def close(self) -> None:
        self._scanner.close()


class JsonTextBlock(str):
    """Text block carrying record-boundary metadata through the pipeline."""

    def __new__(
        cls,
        text: str,
        *,
        record_start: bool,
        record_end: bool,
    ) -> "JsonTextBlock":
        value = super().__new__(cls, text)
        value.record_start = record_start
        value.record_end = record_end
        return value


class JsonRecordTooLargeError(ValueError):
    """记录超过探测窗口，当前操作需要完整 JSON 对象。"""


def _raise_large_record_for_materialized_consumer(
    record: _LargeJsonRecord,
) -> None:
    record.close()
    raise JsonRecordTooLargeError(
        "JSON 单条记录超过探测窗口，无法执行需要完整对象的操作"
    )


class _RawValueScanner:
    """扫描一个 JSON 值，并在超过探测窗口后转为原始文本流。"""

    def __init__(self, reader: "_JsonChunkReader", probe_size: int) -> None:
        self.reader = reader
        self.probe_size = probe_size
        self.bytes_seen = 0
        self.stack: list[str] = []
        self.mode = "normal"
        self.escape = False
        self.complete = False
        self.large = False
        self.store = tempfile.TemporaryFile(
            mode="w+", encoding="utf-8", newline=""
        )
        self.prefix_buffer: list[str] = []
        self.prefix_buffer_size = 0
        self.output_buffer: list[str] = []
        self.output_buffer_size = 0
        self.output_started = False
        self.reader._active_scanners.add(self)

    def close(self) -> None:
        if not self.store.closed:
            self.store.close()
        self.reader._active_scanners.discard(self)

    def _flush_prefix(self) -> None:
        if self.prefix_buffer:
            self.store.write("".join(self.prefix_buffer))
            self.prefix_buffer.clear()
            self.prefix_buffer_size = 0

    def _capture(self, character: str) -> None:
        if not self.large:
            self.prefix_buffer.append(character)
            self.prefix_buffer_size += len(character)
        self.bytes_seen += len(character.encode("utf-8"))
        if self.prefix_buffer_size >= self.reader.read_size:
            self._flush_prefix()
        if self.bytes_seen > self.probe_size:
            self._flush_prefix()
            self.store.flush()
            self.large = True

    def _advance(self, character: str) -> None:
        if self.mode == "string":
            if self.escape:
                self.escape = False
            elif character == "\\":
                self.escape = True
            elif character == '"':
                self.mode = "normal"
                if not self.stack:
                    self.complete = True
            return

        if self.mode == "scalar":
            return

        if character == '"':
            self.mode = "string"
            return
        if character == "{":
            self.stack.append("}")
            return
        if character == "[":
            self.stack.append("]")
            return
        if character in "}]":
            if not self.stack or self.stack[-1] != character:
                raise ValueError(f"JSON 记录括号不匹配：{self.reader.path}")
            self.stack.pop()
            if not self.stack:
                self.complete = True

    def _consume_first(self) -> str:
        self.reader.skip_whitespace()
        first = self.reader.take_raw_character()
        self._capture(first)
        if first not in "[{\"":
            self.mode = "scalar"
        else:
            self._advance(first)
        return first

    def _consume_next(self) -> str:
        character = self.reader.take_raw_character()
        self._capture(character)
        self._advance(character)
        return character

    def _is_scalar_boundary(self) -> bool:
        if self.mode != "scalar":
            return False
        try:
            character = self.reader.peek_raw_character()
        except _JsonEndOfStream:
            self.complete = True
            return True
        if character.isspace() or character in ",]}":
            self.complete = True
            return True
        return False

    def _scan_until_large_or_complete(self) -> None:
        self._consume_first()
        while not self.complete:
            if self._is_scalar_boundary():
                break
            self._consume_next()
            if self.large:
                return

    def _load_small_value(self) -> Any:
        self._flush_prefix()
        self.store.flush()
        self.store.seek(0)
        try:
            return json.load(self.store)
        finally:
            self.close()

    def iter_large_chunks(self) -> Iterator[str]:
        """先吐出探测窗口，再继续读取当前记录的后续文本。"""

        first_block = True
        self._flush_prefix()
        self.store.flush()
        self.store.seek(0)
        while True:
            text = self.store.read(self.reader.read_size)
            if not text:
                break
            yield JsonTextBlock(
                text,
                record_start=first_block,
                record_end=False,
            )
            first_block = False

        if self.output_buffer:
            yield JsonTextBlock(
                "".join(self.output_buffer),
                record_start=first_block,
                record_end=False,
            )
            self.output_buffer.clear()
            self.output_buffer_size = 0
            first_block = False

        while not self.complete:
            if self._is_scalar_boundary():
                break
            try:
                character = self._consume_next()
            except _JsonEndOfStream as exc:
                raise ValueError(
                    f"JSON 超大记录缺少结束符：{self.reader.path}"
                ) from exc
            self.output_buffer.append(character)
            self.output_buffer_size += len(character)
            if self.output_buffer_size >= self.reader.read_size:
                text = "".join(self.output_buffer)
                self.output_buffer.clear()
                self.output_buffer_size = 0
                yield JsonTextBlock(text, record_start=first_block, record_end=False)
                first_block = False

        text = "".join(self.output_buffer)
        self.output_buffer.clear()
        self.output_buffer_size = 0
        if text or first_block:
            yield JsonTextBlock(text, record_start=first_block, record_end=True)
        else:
            yield JsonTextBlock("", record_start=False, record_end=True)

    def read_or_large(self) -> Any | _LargeJsonRecord:
        """解析小记录，或返回延迟执行的超大记录流。"""

        self._scan_until_large_or_complete()
        if self.large:
            return _LargeJsonRecord(self)
        return self._load_small_value()


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
    """Read JSON syntax from a bounded text buffer.

    ``json.JSONDecoder.raw_decode`` is deliberately used one value at a time.
    Navigation methods skip unrelated values without materializing them. Only
    the selected record is decoded into a Python object.
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
        # 如果下游提前停止消费，关闭 reader 时也要回收尚未输出完的超大记录
        # 临时文件，避免长时间索引任务积累文件句柄和磁盘临时空间。
        self._active_scanners: set[_RawValueScanner] = set()

    def close(self) -> None:
        for scanner in tuple(self._active_scanners):
            scanner.close()
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

    def peek_raw_character(self) -> str:
        """查看下一个字符，但不跳过 JSON 值内部的空白。"""

        if self.position >= len(self.buffer) and not self._fill():
            raise _JsonEndOfStream
        return self.buffer[self.position]

    def take_raw_character(self) -> str:
        """消费下一个字符，但不跳过 JSON 值内部的空白。"""

        character = self.peek_raw_character()
        self.position += 1
        self._compact()
        return character

    def expect(self, expected: str) -> None:
        """Consume one syntax character and validate it."""

        actual = self.take()
        if actual != expected:
            raise ValueError(
                f"JSON 语法错误：期望 {expected!r}，实际为 {actual!r}：{self.path}"
            )

    def skip_string(self) -> None:
        """跳过字符串值，不把无关的大字符串读入内存。"""

        self.expect('"')
        escaped = False
        while True:
            if self.position >= len(self.buffer) and not self._fill():
                raise ValueError(f"JSON 字符串缺少结束引号：{self.path}")
            character = self.buffer[self.position]
            self.position += 1
            if escaped:
                escaped = False
            elif character == "\\":
                escaped = True
            elif character == '"':
                self._compact()
                return
            elif ord(character) < 0x20:
                raise ValueError(f"JSON 字符串包含未转义控制字符：{self.path}")
            self._compact()

    def skip_value(self) -> None:
        """递归跳过一个 JSON 值，保留近似读取块大小的缓存。"""

        first = self.peek()
        if first == '"':
            self.skip_string()
            return
        if first == "{":
            self.take()
            if self.peek() == "}":
                self.take()
                return
            while True:
                if self.peek() != '"':
                    raise ValueError(f"JSON 对象键必须是字符串：{self.path}")
                self.skip_string()
                self.expect(":")
                self.skip_value()
                delimiter = self.take()
                if delimiter == "}":
                    return
                if delimiter != ",":
                    raise ValueError(f"JSON 对象缺少逗号或结束符：{self.path}")
                if self.peek() == "}":
                    raise ValueError(f"JSON 对象不允许尾逗号：{self.path}")
        if first == "[":
            self.take()
            if self.peek() == "]":
                self.take()
                return
            while True:
                self.skip_value()
                delimiter = self.take()
                if delimiter == "]":
                    return
                if delimiter != ",":
                    raise ValueError(f"JSON 数组缺少逗号或结束符：{self.path}")
                if self.peek() == "]":
                    raise ValueError(f"JSON 数组不允许尾逗号：{self.path}")
        # 对数字、true、false、null 使用 JSON 解码器验证并消费。
        self.read_value()

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

    def read_value_streaming(
        self,
        probe_size: int = DEFAULT_JSON_RECORD_PROBE_SIZE,
    ) -> Any | _LargeJsonRecord:
        """读取一个值；过大时切换为原始记录分块流。

        ``probe_size`` 是逻辑探测窗口，不会一次性申请同等大小的内存。
        小记录通过标准 JSON 解码保持对象完整性；超过窗口仍未闭合的
        记录由 `_LargeJsonRecord` 继续以原始文本块输出。
        """

        if probe_size <= 0:
            raise ValueError("JSON record_probe_size 必须大于 0")
        scanner = _RawValueScanner(self, probe_size)
        try:
            return scanner.read_or_large()
        except Exception:
            scanner.close()
            raise


def _iter_json_values(
    path: Path,
    read_size: int = DEFAULT_JSON_READ_SIZE,
    max_size: int = DEFAULT_MAX_JSON_SIZE,
    record_probe_size: int = DEFAULT_JSON_RECORD_PROBE_SIZE,
) -> Iterator[Any | _LargeJsonRecord]:
    """Yield top-level JSON values without loading the complete file.

    A JSON Lines file produces one object per iteration.  A top-level JSON
    array produces one array element per iteration.  Other valid top-level
    values (including one object) are also supported.
    """

    yield from _iter_streamed_records(
        path,
        "$",
        read_size=read_size,
        max_size=max_size,
        record_probe_size=record_probe_size,
    )


def _iter_values_at_path(
    reader: _JsonChunkReader,
    tokens: tuple[str | int, ...],
    *,
    record_probe_size: int = DEFAULT_JSON_RECORD_PROBE_SIZE,
) -> Iterator[Any | _LargeJsonRecord]:
    """从当前位置导航到 JSONPath，并只 materialize 命中的值。"""

    if not tokens:
        yield reader.read_value_streaming(record_probe_size)
        return

    token = tokens[0]
    rest = tokens[1:]
    first = reader.peek()

    if first == "{" and (isinstance(token, str)):
        reader.take()
        if reader.peek() == "}":
            reader.take()
            return
        while True:
            if reader.peek() != '"':
                raise ValueError(f"JSON 对象键必须是字符串：{reader.path}")
            key = reader.read_value()
            if not isinstance(key, str):
                raise ValueError(f"JSON 对象键必须是字符串：{reader.path}")
            reader.expect(":")
            if token == "*" or key == token:
                yield from _iter_values_at_path(
                    reader,
                    rest,
                    record_probe_size=record_probe_size,
                )
            else:
                reader.skip_value()
            delimiter = reader.take()
            if delimiter == "}":
                return
            if delimiter != ",":
                raise ValueError(f"JSON 对象缺少逗号或结束符：{reader.path}")
            if reader.peek() == "}":
                raise ValueError(f"JSON 对象不允许尾逗号：{reader.path}")

    if first == "[":
        reader.take()
        if reader.peek() == "]":
            reader.take()
            return
        index = 0
        while True:
            selected = token == "*" or token == index
            if selected:
                yield from _iter_values_at_path(
                    reader,
                    rest,
                    record_probe_size=record_probe_size,
                )
            else:
                reader.skip_value()
            delimiter = reader.take()
            if delimiter == "]":
                return
            if delimiter != ",":
                raise ValueError(f"JSON 数组缺少逗号或结束符：{reader.path}")
            if reader.peek() == "]":
                raise ValueError(f"JSON 数组不允许尾逗号：{reader.path}")
            index += 1

    # 路径要求的容器类型与实际 JSON 值不匹配。消费当前值让异常上下文
    # 保持一致，并明确告诉调用方配置路径无法命中。
    reader.skip_value()
    raise ValueError(f"JSON 路径无法匹配容器：{reader.path}")


def _iter_streamed_records(
    path: Path,
    record_path: str,
    *,
    read_size: int = DEFAULT_JSON_READ_SIZE,
    max_size: int = DEFAULT_MAX_JSON_SIZE,
    record_probe_size: int = DEFAULT_JSON_RECORD_PROBE_SIZE,
) -> Iterator[Any | _LargeJsonRecord]:
    """按配置路径逐条读取记录，不先解析完整顶层对象。"""

    path = Path(path).expanduser().resolve()
    ensure_json_size(path, max_size)
    reader = _JsonChunkReader(path, read_size)
    tokens = _parse_path(record_path)
    try:
        try:
            first = reader.peek()
        except _JsonEndOfStream:
            return

        # 顶层数组的元素作为根记录；有 record_path 时，在每个元素内部导航。
        if first == "[":
            reader.take()
            if reader.peek() == "]":
                reader.take()
            else:
                while True:
                    if tokens:
                        yield from _iter_values_at_path(
                            reader,
                            tokens,
                            record_probe_size=record_probe_size,
                        )
                    else:
                        yield reader.read_value_streaming(record_probe_size)
                    delimiter = reader.take()
                    if delimiter == "]":
                        break
                    if delimiter != ",":
                        raise ValueError(f"JSON 数组缺少逗号或结束符：{path}")
                    if reader.peek() == "]":
                        raise ValueError(f"JSON 数组不允许尾逗号：{path}")
            if reader.skip_whitespace():
                raise ValueError(f"JSON 文件存在多余内容：{path}")
            return

        # JSON Lines 或单个 JSON 根对象：每个顶层 JSON 值都作为导航起点。
        while True:
            if not reader.skip_whitespace():
                break
            if tokens:
                yield from _iter_values_at_path(
                    reader,
                    tokens,
                    record_probe_size=record_probe_size,
                )
            else:
                yield reader.read_value_streaming(record_probe_size)
    except _JsonEndOfStream as exc:
        raise ValueError(f"JSON 记录缺少结束符：{path}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"JSON 文件格式错误：{path}：{exc}") from exc
    except UnicodeDecodeError as exc:
        raise ValueError(f"JSON 文件不是有效的 UTF-8：{path}：{exc}") from exc
    finally:
        reader.close()


def _iter_formatted_records(
    path: Path,
    profile: JsonProfile,
    *,
    read_size: int = DEFAULT_JSON_READ_SIZE,
    max_size: int = DEFAULT_MAX_JSON_SIZE,
    record_probe_size: int = DEFAULT_JSON_RECORD_PROBE_SIZE,
    allow_large_records: bool = True,
) -> Iterator[str | JsonTextBlock]:
    """Yield configured records one by one without materializing the root object."""

    if any(field.path.strip().startswith("$") for field in profile.fields) or any(
        rule.path.strip().startswith("$") for rule in profile.filters
    ):
        if profile.record_path.strip() != "$":
            raise ValueError(
                "record_path 不是 $ 时，fields/filter 不能使用以 $ 开头的根节点路径"
            )

    for record in _iter_streamed_records(
        path,
        profile.record_path,
        read_size=read_size,
        max_size=max_size,
        record_probe_size=record_probe_size,
    ):
        if isinstance(record, _LargeJsonRecord):
            if not allow_large_records:
                _raise_large_record_for_materialized_consumer(record)
            logger.warning(
                "JSON 单条记录超过 %s 字节，改用原始记录分块流：%s",
                record_probe_size,
                path,
            )
            # 超大记录无法安全地 materialize，因此无法应用字段选择和
            # filter；保留完整原始 JSON 记录，确保数据不被截断或拼接。
            yield from record.iter_chunks()
            continue
        if not all(_matches_filter(record, rule, record) for rule in profile.filters):
            continue
        text = _format_record(record, profile, record)
        if text:
            yield text


def iter_json_text(
    path: Path,
    profile: JsonProfile,
    *,
    read_size: int = DEFAULT_JSON_READ_SIZE,
    max_size: int = DEFAULT_MAX_JSON_SIZE,
    record_probe_size: int = DEFAULT_JSON_RECORD_PROBE_SIZE,
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
        record_probe_size=record_probe_size,
    )
    if profile.index_mode == "record":
        yield from records
        return

    first = True
    for text in records:
        if not first and getattr(text, "record_start", True):
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
    max_size: int = 0,
    record_probe_size: int = DEFAULT_JSON_RECORD_PROBE_SIZE,
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

    values = iter(
        _iter_json_values(
            path,
            read_size,
            max_size,
            record_probe_size=record_probe_size,
        )
    )
    while True:
        if max_records and records_scanned >= max_records:
            truncated = True
            break
        try:
            value = next(values)
        except StopIteration:
            break
        if isinstance(value, _LargeJsonRecord):
            # 结构扫描需要解析对象结构；超大单条记录不能被完整 materialize，
            # 因此报告为不可展开，并继续保持文件读取器可关闭。
            value.close()
            raise JsonRecordTooLargeError(
                "JSON 单条记录超过结构扫描可解析大小："
                f"{path}（{record_probe_size} 字节）"
            )
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
    max_size: int = 0,
    record_probe_size: int = DEFAULT_JSON_RECORD_PROBE_SIZE,
) -> list[str]:
    """返回供 CLI 预览的已格式化记录。"""

    if limit <= 0:
        raise ValueError("preview limit 必须大于 0")
    records: list[str] = []
    for record in _iter_formatted_records(
        path,
        profile,
        max_size=max_size,
        record_probe_size=record_probe_size,
        allow_large_records=False,
    ):
        records.append(record)
        if len(records) >= limit:
            break
    if profile.index_mode == "file":
        return [profile.separator.join(records)] if records else []
    return records

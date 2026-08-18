# 代码文件与函数语义索引

> 本文件由 `scripts/generate_code_index.py` 从当前源码生成。每个文件、类、命名函数和 JavaScript 匿名箭头回调都有独立记录；行号以生成时源码为准。
> JSONL 版本适合导入知识库：`docs/code-function-index.jsonl`。检索建议使用 `文件路径`、`symbol`、`关键词`、`调用`、`副作用` 和 `行号`。

覆盖文件：52；实体记录：706。

## personal_local_knowledge_base_v0/experiments/rag-grounding-eval/ablation_no_context.py

**文件作用：** 执行不提供检索上下文的消融实验，用于对比模型是否会凭空回答受控事实。

**语言/关键词：** 消融实验, 无上下文, grounding, Python, py

**函数/类/脚本记录数：** 1

### `main` (function, L12-L34)

**签名：** `def main() -> int`

**作用：** 执行模块主流程，编排参数、业务调用、输出和进程退出码。

**详细语义：** 所属模块职责：执行不提供检索上下文的消融实验，用于对比模型是否会凭空回答受控事实。；输入参数：；声明返回：int；直接/间接调用：LLMClient.from_env, client.complete, print；返回表达式：0；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 消融实验, 无上下文, grounding, main, LLMClient.from_env, client.complete, print

**调用：** LLMClient.from_env, client.complete, print；**返回：** 0；**异常：** 未发现显式 raise；**副作用：** 日志输出。

## personal_local_knowledge_base_v0/knowledge_search/__init__.py

**文件作用：** 知识库核心 Python 包的版本与公开包级说明。

**语言/关键词：** 包入口, 版本, Python package, Python, py

**函数/类/脚本记录数：** 0

## personal_local_knowledge_base_v0/knowledge_search/__main__.py

**文件作用：** 支持 `python -m knowledge_search` 的命令行模块入口，把退出码转交给 CLI。

**语言/关键词：** 模块入口, CLI, SystemExit, Python, py

**函数/类/脚本记录数：** 0

## personal_local_knowledge_base_v0/knowledge_search/block_parsing.py

**文件作用：** 把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。

**语言/关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, Python, py

**函数/类/脚本记录数：** 25

### `_BlockBuilder` (class, L39-L95)

**签名：** `class _BlockBuilder`

**作用：** Create stable, unique block ids in source order.

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；类体包含 2 个直接方法。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, Block, Builder

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_BlockBuilder.__init__` (function, L42-L44)

**签名：** `def __init__(self, path: Path) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：self, path: Path；声明返回：None；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, Block, Builder, init

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_BlockBuilder.make` (function, L46-L95)

**签名：** `def make(self, block_type: str, content: str, *, language: str | None=None, heading_path: tuple[str, ...]=(), symbol_path: tuple[str, ...]=(), start_line: int | None=None, end_line: int | None=None, page_number: int | None=None, hard_boundary_before: bool=False, hard_boundary_after: bool=False, record_path: str | None=None, slide_number: int | None=None, shape_index: int | None=None, module_name: str | None=None, parameters: tuple[str, ...]=(), docstring: str | None=None, comments: tuple[str, ...]=(), parser: str='') -> DocumentBlock`

**作用：** 根据正文和定位元数据创建稳定唯一的 DocumentBlock。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：self, block_type: str, content: str, *, language: str | None=None, heading_path: tuple[str, ...]=(), symbol_path: tuple[str, ...]=(), start_line: int | None=None, end_line: int | None=None, page_number: int | None=None, hard_boundary_before: bool=False, hard_boundary_after: bool=False, record_path: str | None=None, slide_number: int | None=None, shape_index: int | None=None, module_name: str | None=None, parameters: tuple[str, ...]=(), docstring: str | None=None, comments: tuple[str, ...]=(), parser: str=''；声明返回：DocumentBlock；直接/间接调用：DocumentBlock, hashlib.sha256.hexdigest, str, hashlib.sha256, identity.encode；返回表达式：DocumentBlock(block_id=block_id, path=str(self.path), block_type=block_type, language=language, heading_path=heading_path, symbol_path=symbol_path, content=content, start_line=sta…；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, Block, Builder, make, hashlib.sha256.hexdigest, str, hashlib.sha256, identity.encode

**调用：** DocumentBlock, hashlib.sha256.hexdigest, str, hashlib.sha256, identity.encode；**返回：** DocumentBlock(block_id=block_id, path=str(self.path), block_type=block_type, language=language, heading_path=heading_path, symbol_path=symbol_path, content=content, start_line=sta…；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_numbered_lines` (function, L98-L100)

**签名：** `def _numbered_lines(parts: Iterable[str]) -> list[tuple[int, str]]`

**作用：** 执行  numbered lines，涉及 Constant.join.replace.replace, list, enumerate, Constant.join.replace, text.splitlines。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：parts: Iterable[str]；声明返回：list[tuple[int, str]]；直接/间接调用：Constant.join.replace.replace, list, enumerate, Constant.join.replace, text.splitlines, Constant.join；返回表达式：list(enumerate(text.splitlines(), start=1))；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, numbered, lines, Constant.join.replace.replace, list, enumerate, Constant.join.replace, text.splitlines, Constant.join

**调用：** Constant.join.replace.replace, list, enumerate, Constant.join.replace, text.splitlines, Constant.join；**返回：** list(enumerate(text.splitlines(), start=1))；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_markdown_node_kind` (function, L110-L125)

**签名：** `def _markdown_node_kind(lines: list[tuple[int, str]], index: int) -> str`

**作用：** 执行  markdown node kind，涉及 line.lstrip, stripped.startswith, _MD_LIST.match, _MD_TABLE_RULE.match, len。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：lines: list[tuple[int, str]], index: int；声明返回：str；直接/间接调用：line.lstrip, stripped.startswith, _MD_LIST.match, _MD_TABLE_RULE.match, len；返回表达式：'paragraph'; 'code'; 'list'; 'quote'; 'table'；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, markdown, node, kind, line.lstrip, stripped.startswith, _MD_LIST.match, _MD_TABLE_RULE.match, len, 条件分支

**调用：** line.lstrip, stripped.startswith, _MD_LIST.match, _MD_TABLE_RULE.match, len；**返回：** 'paragraph'; 'code'; 'list'; 'quote'; 'table'；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_take_markdown_node` (function, L128-L161)

**签名：** `def _take_markdown_node(lines: list[tuple[int, str]], index: int) -> tuple[str, str, int, int, int]`

**作用：** Return kind, content, first line, last line and next cursor.

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：lines: list[tuple[int, str]], index: int；声明返回：tuple[str, str, int, int, int]；直接/间接调用：_markdown_node_kind, Constant.join.strip, first.lstrip, len, collected.append, Subscript.lstrip.startswith, current.startswith, Constant.join, Subscript.lstrip, _MD_HEADING.match, current.strip；返回表达式：(kind, '\n'.join(collected).strip(), start_line, lines[cursor - 1][0], cursor)；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, take, markdown, node, _markdown_node_kind, Constant.join.strip, first.lstrip, len, collected.append, Subscript.lstrip.startswith, current.startswith, Constant.join, Subscript.lstrip, _MD_HEADING.match, current.strip, 条件分支, 循环

**调用：** _markdown_node_kind, Constant.join.strip, first.lstrip, len, collected.append, Subscript.lstrip.startswith, current.startswith, Constant.join, Subscript.lstrip, _MD_HEADING.match, current.strip；**返回：** (kind, '\n'.join(collected).strip(), start_line, lines[cursor - 1][0], cursor)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_parse_markdown` (function, L164-L225)

**签名：** `def _parse_markdown(document: ExtractedDocument) -> Iterator[DocumentBlock]`

**作用：** 解析并转换markdown；内部调用 _BlockBuilder, _numbered_lines, iter_document_text, len, _MD_HEADING.match。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument；声明返回：Iterator[DocumentBlock]；直接/间接调用：_BlockBuilder, _numbered_lines, iter_document_text, len, _MD_HEADING.match, _take_markdown_node, headings.append, line.strip, builder.make, heading.group, heading.group.strip, tuple；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, parse, markdown, _BlockBuilder, _numbered_lines, iter_document_text, len, _MD_HEADING.match, _take_markdown_node, headings.append, line.strip, builder.make, heading.group, heading.group.strip, tuple, 条件分支, 循环, 生成器 yield

**调用：** _BlockBuilder, _numbered_lines, iter_document_text, len, _MD_HEADING.match, _take_markdown_node, headings.append, line.strip, builder.make, heading.group, heading.group.strip, tuple；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_parse_text` (function, L228-L250)

**签名：** `def _parse_text(document: ExtractedDocument) -> Iterator[DocumentBlock]`

**作用：** 解析并转换text；内部调用 _BlockBuilder, _numbered_lines, iter_document_text, len, clean_text。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument；声明返回：Iterator[DocumentBlock]；直接/间接调用：_BlockBuilder, _numbered_lines, iter_document_text, len, clean_text, Subscript.strip, body.append, Constant.join, builder.make；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, parse, text, _BlockBuilder, _numbered_lines, iter_document_text, len, clean_text, Subscript.strip, body.append, Constant.join, builder.make, 条件分支, 循环, 生成器 yield

**调用：** _BlockBuilder, _numbered_lines, iter_document_text, len, clean_text, Subscript.strip, body.append, Constant.join, builder.make；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_parse_json` (function, L253-L300)

**签名：** `def _parse_json(document: ExtractedDocument, profile: JsonProfile, *, max_json_size: int, record_probe_size: int) -> Iterator[DocumentBlock]`

**作用：** 解析并转换json；内部调用 _BlockBuilder, iter_json_record_text, clean_text, builder.make, record_parts.append。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument, profile: JsonProfile, *, max_json_size: int, record_probe_size: int；声明返回：Iterator[DocumentBlock]；直接/间接调用：_BlockBuilder, iter_json_record_text, clean_text, builder.make, record_parts.append, emit_record, Constant.join, str；返回表达式：builder.make('json-record', content, record_path=locator, hard_boundary_before=True, hard_boundary_after=True, parser='json-stream'); None；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, parse, json, _BlockBuilder, iter_json_record_text, clean_text, builder.make, record_parts.append, emit_record, Constant.join, str, 条件分支, 循环, 生成器 yield

**调用：** _BlockBuilder, iter_json_record_text, clean_text, builder.make, record_parts.append, emit_record, Constant.join, str；**返回：** builder.make('json-record', content, record_path=locator, hard_boundary_before=True, hard_boundary_after=True, parser='json-stream'); None；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_parse_json.emit_record` (function, L264-L275)

**签名：** `def emit_record() -> DocumentBlock | None`

**作用：** 执行 emit record，涉及 clean_text, builder.make, Constant.join。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：；声明返回：DocumentBlock | None；直接/间接调用：clean_text, builder.make, Constant.join；返回表达式：builder.make('json-record', content, record_path=locator, hard_boundary_before=True, hard_boundary_after=True, parser='json-stream'); None；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, parse, json, emit, record, clean_text, builder.make, Constant.join, 条件分支

**调用：** clean_text, builder.make, Constant.join；**返回：** builder.make('json-record', content, record_path=locator, hard_boundary_before=True, hard_boundary_after=True, parser='json-stream'); None；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_parse_pdf` (function, L303-L330)

**签名：** `def _parse_pdf(document: ExtractedDocument) -> Iterator[DocumentBlock]`

**作用：** 解析并转换pdf；内部调用 _BlockBuilder, PdfReader, enumerate, str, RuntimeError。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument；声明返回：Iterator[DocumentBlock]；直接/间接调用：_BlockBuilder, PdfReader, enumerate, str, RuntimeError, clean_text, page.extract_text, logger.exception, re.split, value.strip, builder.make, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：RuntimeError('PDF 抽取需要 pypdf，请先安装 requirements.txt')；控制流：循环, 异常处理, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, parse, pdf, _BlockBuilder, PdfReader, enumerate, str, RuntimeError, clean_text, page.extract_text, logger.exception, re.split, value.strip, builder.make, len, 循环, 异常处理, 生成器 yield

**调用：** _BlockBuilder, PdfReader, enumerate, str, RuntimeError, clean_text, page.extract_text, logger.exception, re.split, value.strip, builder.make, len；**返回：** 未记录；**异常：** RuntimeError('PDF 抽取需要 pypdf，请先安装 requirements.txt')；**副作用：** 日志输出。

### `_shape_text` (function, L333-L348)

**签名：** `def _shape_text(shape, group_type) -> tuple[str, str]`

**作用：** 执行  shape text，涉及 getattr, shape.text.strip, values.append, clean_text, _shape_text。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：shape, group_type；声明返回：tuple[str, str]；直接/间接调用：getattr, shape.text.strip, values.append, clean_text, _shape_text, Constant.join, cell.text.strip；返回表达式：(clean_text('\n'.join(values)), kind)；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, shape, text, getattr, shape.text.strip, values.append, clean_text, _shape_text, Constant.join, cell.text.strip, 条件分支, 循环

**调用：** getattr, shape.text.strip, values.append, clean_text, _shape_text, Constant.join, cell.text.strip；**返回：** (clean_text('\n'.join(values)), kind)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_parse_pptx` (function, L351-L398)

**签名：** `def _parse_pptx(document: ExtractedDocument) -> Iterator[DocumentBlock]`

**作用：** 解析并转换pptx；内部调用 _BlockBuilder, Presentation, enumerate, str, RuntimeError。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument；声明返回：Iterator[DocumentBlock]；直接/间接调用：_BlockBuilder, Presentation, enumerate, str, RuntimeError, _shape_text, slide_blocks.append, clean_text, builder.make, replace, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：RuntimeError('PPTX 抽取需要 python-pptx，请先安装 requirements.txt')；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, parse, pptx, _BlockBuilder, Presentation, enumerate, str, RuntimeError, _shape_text, slide_blocks.append, clean_text, builder.make, replace, len, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** _BlockBuilder, Presentation, enumerate, str, RuntimeError, _shape_text, slide_blocks.append, clean_text, builder.make, replace, len；**返回：** 未记录；**异常：** RuntimeError('PPTX 抽取需要 python-pptx，请先安装 requirements.txt')；**副作用：** 未发现明显外部副作用。

### `_source_text` (function, L401-L410)

**签名：** `def _source_text(document: ExtractedDocument) -> str`

**作用：** 获取代码文档的完整源文本并处理缺失正文情况。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument；声明返回：str；直接/间接调用：Constant.join, iter_document_text, tokenize.open, source.read；返回表达式：''.join(iter_document_text(document)); document.text; source.read()；显式异常：未发现显式 raise；控制流：条件分支, 异常处理, 上下文管理。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, source, text, Constant.join, iter_document_text, tokenize.open, source.read, 条件分支, 异常处理, 上下文管理

**调用：** Constant.join, iter_document_text, tokenize.open, source.read；**返回：** ''.join(iter_document_text(document)); document.text; source.read()；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_source_lines` (function, L413-L414)

**签名：** `def _source_lines(source: str, start: int, end: int) -> str`

**作用：** 截取指定行号范围的源码，供结构块 canonical 内容使用。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：source: str, start: int, end: int；声明返回：str；直接/间接调用：Constant.join.rstrip, Constant.join, source.splitlines；返回表达式：''.join(source.splitlines(keepends=True)[start - 1:end]).rstrip()；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, source, lines, Constant.join.rstrip, Constant.join, source.splitlines

**调用：** Constant.join.rstrip, Constant.join, source.splitlines；**返回：** ''.join(source.splitlines(keepends=True)[start - 1:end]).rstrip()；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_source_comments` (function, L417-L426)

**签名：** `def _source_comments(source: str, start: int, end: int) -> tuple[str, ...]`

**作用：** 提取源码行范围内的注释，作为函数或类的辅助语义。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：source: str, start: int, end: int；声明返回：tuple[str, ...]；直接/间接调用：tuple, tokenize.generate_tokens, io.StringIO, found.append；返回表达式：tuple(found)；显式异常：未发现显式 raise；控制流：条件分支, 循环, 异常处理。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, source, comments, tuple, tokenize.generate_tokens, io.StringIO, found.append, 条件分支, 循环, 异常处理

**调用：** tuple, tokenize.generate_tokens, io.StringIO, found.append；**返回：** tuple(found)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_arguments` (function, L429-L438)

**签名：** `def _arguments(node: ast.FunctionDef | ast.AsyncFunctionDef) -> tuple[str, ...]`

**作用：** 从 Python AST 函数节点展开位置参数、关键字参数和默认值信息。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：node: ast.FunctionDef | ast.AsyncFunctionDef；声明返回：tuple[str, ...]；直接/间接调用：result.extend, tuple, result.append；返回表达式：tuple(result)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, arguments, result.extend, tuple, result.append, 条件分支

**调用：** result.extend, tuple, result.append；**返回：** tuple(result)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_python_items` (function, L441-L455)

**签名：** `def _python_items(statements: list[ast.stmt], parents: tuple[str, ...]=()) -> Iterator[tuple[ast.AST, str, tuple[str, ...]]]`

**作用：** 递归遍历 Python AST，产出模块、类、函数和方法的结构元数据。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：statements: list[ast.stmt], parents: tuple[str, ...]=()；声明返回：Iterator[tuple[ast.AST, str, tuple[str, ...]]]；直接/间接调用：isinstance, _python_items；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, python, items, isinstance, _python_items, 条件分支, 循环, 生成器 yield

**调用：** isinstance, _python_items；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_fallback_lines` (function, L458-L480)

**签名：** `def _fallback_lines(document: ExtractedDocument, source: str, *, language: str, builder: _BlockBuilder, parser: str='fallback-line') -> Iterator[DocumentBlock]`

**作用：** 执行  fallback lines，涉及 source.splitlines, range, len, Constant.join.rstrip, content.strip。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument, source: str, *, language: str, builder: _BlockBuilder, parser: str='fallback-line'；声明返回：Iterator[DocumentBlock]；直接/间接调用：source.splitlines, range, len, Constant.join.rstrip, content.strip, Constant.join, builder.make, min；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, fallback, lines, source.splitlines, range, len, Constant.join.rstrip, content.strip, Constant.join, builder.make, min, 条件分支, 循环, 生成器 yield

**调用：** source.splitlines, range, len, Constant.join.rstrip, content.strip, Constant.join, builder.make, min；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_parse_python` (function, L483-L539)

**签名：** `def _parse_python(document: ExtractedDocument) -> Iterator[DocumentBlock]`

**作用：** 解析并转换python；内部调用 _BlockBuilder, _source_text, ast.get_docstring, _python_items, ast.parse。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument；声明返回：Iterator[DocumentBlock]；直接/间接调用：_BlockBuilder, _source_text, ast.get_docstring, _python_items, ast.parse, getattr, min, _source_lines, logger.warning, builder.make, isinstance, str, _fallback_lines, ast.get_source_segment, _source_comments, _arguments；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, parse, python, _BlockBuilder, _source_text, ast.get_docstring, _python_items, ast.parse, getattr, min, _source_lines, logger.warning, builder.make, isinstance, str, _fallback_lines, ast.get_source_segment, _source_comments, _arguments, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** _BlockBuilder, _source_text, ast.get_docstring, _python_items, ast.parse, getattr, min, _source_lines, logger.warning, builder.make, isinstance, str, _fallback_lines, ast.get_source_segment, _source_comments, _arguments；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 日志输出。

### `_brace_change` (function, L542-L547)

**签名：** `def _brace_change(line: str) -> int`

**作用：** 执行  brace change，涉及 re.sub, without_literals.split, without_comment.count。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：line: str；声明返回：int；直接/间接调用：re.sub, without_literals.split, without_comment.count；返回表达式：without_comment.count('{') - without_comment.count('}')；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, brace, change, re.sub, without_literals.split, without_comment.count

**调用：** re.sub, without_literals.split, without_comment.count；**返回：** without_comment.count('{') - without_comment.count('}')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_closing_line` (function, L550-L559)

**签名：** `def _closing_line(lines: list[str], start: int) -> int`

**作用：** 执行  closing line，涉及 range, len, _brace_change, Subscript.split。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：lines: list[str], start: int；声明返回：int；直接/间接调用：range, len, _brace_change, Subscript.split；返回表达式：len(lines) - 1; position；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, closing, line, range, len, _brace_change, Subscript.split, 条件分支, 循环

**调用：** range, len, _brace_change, Subscript.split；**返回：** len(lines) - 1; position；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_parse_cpp` (function, L571-L676)

**签名：** `def _parse_cpp(document: ExtractedDocument) -> Iterator[DocumentBlock]`

**作用：** 解析并转换cpp；内部调用 _BlockBuilder, _source_text, source.splitlines, set, range。

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument；声明返回：Iterator[DocumentBlock]；直接/间接调用：_BlockBuilder, _source_text, source.splitlines, set, range, sorted, enumerate, emitted.add, Constant.join.rstrip, raw_line.strip, stripped.startswith, _CPP_CONTAINER.search, _CPP_FUNCTION.search, tuple, list, _closing_line, candidates.append, covered.update, _brace_change, logger.exception, len, Subscript.strip, covered.add, container_match.groups；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, parse, cpp, _BlockBuilder, _source_text, source.splitlines, set, range, sorted, enumerate, emitted.add, Constant.join.rstrip, raw_line.strip, stripped.startswith, _CPP_CONTAINER.search, _CPP_FUNCTION.search, tuple, list, _closing_line, candidates.append, covered.update, _brace_change, logger.exception, len, Subscript.strip, covered.add, container_match.groups, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** _BlockBuilder, _source_text, source.splitlines, set, range, sorted, enumerate, emitted.add, Constant.join.rstrip, raw_line.strip, stripped.startswith, _CPP_CONTAINER.search, _CPP_FUNCTION.search, tuple, list, _closing_line, candidates.append, covered.update, _brace_change, logger.exception, len, Subscript.strip, covered.add, container_match.groups；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `build_embedding_content` (function, L679-L694)

**签名：** `def build_embedding_content(block: DocumentBlock, canonical: str | None=None) -> str`

**作用：** Build the stable natural-text document input used by Qwen3 Embedding.

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：block: DocumentBlock, canonical: str | None=None；声明返回：str；直接/间接调用：build_document_embedding_input；返回表达式：build_document_embedding_input(content=block.content if canonical is None else canonical, path=block.path, block_type=block.block_type, language=block.language, heading_path=block…；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, build, embedding, content, build_document_embedding_input, 条件分支

**调用：** build_document_embedding_input；**返回：** build_document_embedding_input(content=block.content if canonical is None else canonical, path=block.path, block_type=block.block_type, language=block.language, heading_path=block…；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `iter_document_blocks` (function, L697-L729)

**签名：** `def iter_document_blocks(document: ExtractedDocument, *, json_profile: JsonProfile | None=None, max_json_size: int=DEFAULT_MAX_JSON_SIZE, json_record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> Iterator[DocumentBlock]`

**作用：** Parse one extracted document without executing source code.

**详细语义：** 所属模块职责：把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。；输入参数：document: ExtractedDocument, *, json_profile: JsonProfile | None=None, max_json_size: int=DEFAULT_MAX_JSON_SIZE, json_record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：Iterator[DocumentBlock]；直接/间接调用：parsers.get, ValueError, parser, _parse_json, _parse_cpp；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError(f'不支持的文档类型：{document.file_type}'); ValueError('索引 JSON 文件必须提供 --json-config 配置文件')；控制流：条件分支, 生成器 yield。

**关键词：** 结构化解析, DocumentBlock, 符号路径, 硬边界, canonical_content, embedding_content, iter, document, blocks, parsers.get, ValueError, parser, _parse_json, _parse_cpp, 条件分支, 生成器 yield

**调用：** parsers.get, ValueError, parser, _parse_json, _parse_cpp；**返回：** 未记录；**异常：** ValueError(f'不支持的文档类型：{document.file_type}'); ValueError('索引 JSON 文件必须提供 --json-config 配置文件')；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/chunking.py

**文件作用：** 在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。

**语言/关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Python, py

**函数/类/脚本记录数：** 22

### `ChunkingConfig` (class, L18-L66)

**签名：** `class ChunkingConfig`

**作用：** Stable V5 chunking parameters; its fingerprint participates in caching.

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；类体包含 3 个直接方法。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Chunking, Config

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkingConfig.__post_init__` (function, L28-L40)

**签名：** `def __post_init__(self) -> None`

**作用：** 执行 dataclass 配置校验，拒绝不满足范围、格式或不变量的参数。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self；声明返回：None；直接/间接调用：ValueError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('core_chunk_chars 必须大于 0'); ValueError('overlap_chars 必须满足 0 <= overlap < max_chunk_chars'); ValueError('min_chunk_chars 必须在 1 到 core_chunk_chars 之间'); ValueError('max_chunk_chars 不能小于 core_chunk_chars'); ValueError('semantic_merge_threshold 必须在 -1 到 1 之间'); ValueError('max_chunk_tokens 必须大于 0')；控制流：条件分支。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Chunking, Config, post, init, ValueError, 条件分支

**调用：** ValueError；**返回：** 未记录；**异常：** ValueError('core_chunk_chars 必须大于 0'); ValueError('overlap_chars 必须满足 0 <= overlap < max_chunk_chars'); ValueError('min_chunk_chars 必须在 1 到 core_chunk_chars 之间'); ValueError('max_chunk_chars 不能小于 core_chunk_chars'); ValueError('semantic_merge_threshold 必须在 -1 到 1 之间'); ValueError('max_chunk_tokens 必须大于 0')；**副作用：** 未发现明显外部副作用。

### `ChunkingConfig.fingerprint` (function, L43-L44)

**签名：** `def fingerprint(self) -> str`

**作用：** 根据当前配置内容计算可比较、可缓存的哈希指纹。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self；声明返回：str；直接/间接调用：self.fingerprint_for；返回表达式：self.fingerprint_for(None)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Chunking, Config, fingerprint, self.fingerprint_for

**调用：** self.fingerprint_for；**返回：** self.fingerprint_for(None)；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `ChunkingConfig.fingerprint_for` (function, L46-L66)

**签名：** `def fingerprint_for(self, backend: EmbeddingBackend | None) -> str`

**作用：** 把分块参数与 Embedding 后端配置组合为索引缓存指纹。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self, backend: EmbeddingBackend | None；声明返回：str；直接/间接调用：fingerprint_payload, payload.update；返回表达式：fingerprint_payload(payload)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Chunking, Config, fingerprint, for, fingerprint_payload, payload.update, 条件分支

**调用：** fingerprint_payload, payload.update；**返回：** fingerprint_payload(payload)；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `_find_stream_split_end` (function, L69-L88)

**签名：** `def _find_stream_split_end(text: str, chunk_size: int) -> int`

**作用：** 在流式缓存的前 chunk_size 个字符中寻找较自然的切分点。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：text: str, chunk_size: int；声明返回：int；直接/间接调用：min, max, text.rfind, len, int；返回表达式：whitespace if whitespace > 0 else hard_end; hard_end; boundary + 1；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, find, stream, split, end, min, max, text.rfind, len, int, 条件分支

**调用：** min, max, text.rfind, len, int；**返回：** whitespace if whitespace > 0 else hard_end; hard_end; boundary + 1；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `iter_chunk_text` (function, L91-L126)

**签名：** `def iter_chunk_text(text_chunks: Iterable[str], chunk_size: int=800, overlap: int=200) -> Iterator[Chunk]`

**作用：** 把文本块流式切分为 Chunk，内存中最多保留一个窗口及其重叠部分。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：text_chunks: Iterable[str], chunk_size: int=800, overlap: int=200；声明返回：Iterator[Chunk]；直接/间接调用：buffer.strip, ValueError, len, _find_stream_split_end, Subscript.strip, max, Chunk；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('chunk_size 必须大于 0'); ValueError('overlap 必须满足 0 <= overlap < chunk_size')；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, iter, chunk, text, buffer.strip, ValueError, len, _find_stream_split_end, Subscript.strip, max, Chunk, 条件分支, 循环, 生成器 yield

**调用：** buffer.strip, ValueError, len, _find_stream_split_end, Subscript.strip, max, Chunk；**返回：** 未记录；**异常：** ValueError('chunk_size 必须大于 0'); ValueError('overlap 必须满足 0 <= overlap < chunk_size')；**副作用：** 未发现明显外部副作用。

### `chunk_text` (function, L129-L133)

**签名：** `def chunk_text(text: str, chunk_size: int=800, overlap: int=200) -> list[Chunk]`

**作用：** 兼容小文本调用，并复用流式实现保证相邻分段始终保留重叠。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：text: str, chunk_size: int=800, overlap: int=200；声明返回：list[Chunk]；直接/间接调用：list, iter_chunk_text；返回表达式：list(iter_chunk_text([text], chunk_size=chunk_size, overlap=overlap))；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, chunk, text, list, iter_chunk_text

**调用：** list, iter_chunk_text；**返回：** list(iter_chunk_text([text], chunk_size=chunk_size, overlap=overlap))；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `iter_chunk_blocks` (function, L136-L258)

**签名：** `def iter_chunk_blocks(blocks: Iterable[DocumentBlock], chunk_size: int=800, overlap: int=200, *, min_chunk_chars: int=200, max_chunk_chars: int=1600, semantic_merge_threshold: float=0.8, max_chunk_tokens: int=8192, embedding_backend: EmbeddingBackend | None=None) -> Iterator[Chunk]`

**作用：** Chunk on non-overlapping cores, merge semantically, then add context.

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：blocks: Iterable[DocumentBlock], chunk_size: int=800, overlap: int=200, *, min_chunk_chars: int=200, max_chunk_chars: int=1600, semantic_merge_threshold: float=0.8, max_chunk_tokens: int=8192, embedding_backend: EmbeddingBackend | None=None；声明返回：Iterator[Chunk]；直接/间接调用：ChunkingConfig, _MergedCore.from_core, enumerate, groups.append, validate_vectors, _add_final_overlap, build_embedding_content, zip, _located_block, min, block.content.strip, _make_core_chunks, embedding_backend.embed_documents, cosine_similarity, _same_structure, _within_token_limit, current.append, range, Chunk, len, _crosses_hard_boundary, _group_block_id, tuple, float；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, iter, chunk, blocks, ChunkingConfig, _MergedCore.from_core, enumerate, groups.append, validate_vectors, _add_final_overlap, build_embedding_content, zip, _located_block, min, block.content.strip, _make_core_chunks, embedding_backend.embed_documents, cosine_similarity, _same_structure, _within_token_limit, current.append, range, Chunk, len, _crosses_hard_boundary, _group_block_id, tuple, float, 条件分支, 循环, 生成器 yield

**调用：** ChunkingConfig, _MergedCore.from_core, enumerate, groups.append, validate_vectors, _add_final_overlap, build_embedding_content, zip, _located_block, min, block.content.strip, _make_core_chunks, embedding_backend.embed_documents, cosine_similarity, _same_structure, _within_token_limit, current.append, range, Chunk, len, _crosses_hard_boundary, _group_block_id, tuple, float；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `_CoreChunk` (class, L262-L270)

**签名：** `class _CoreChunk`

**作用：** 定义 _CoreChunk 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；类体包含 0 个直接方法。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Core, Chunk

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_MergedCore` (class, L274-L291)

**签名：** `class _MergedCore`

**作用：** 定义 _MergedCore 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；类体包含 4 个直接方法。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Merged, Core

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_MergedCore.from_core` (function, L279-L280)

**签名：** `def from_core(cls, core: _CoreChunk) -> '_MergedCore'`

**作用：** 执行 from core，涉及 cls。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：cls, core: _CoreChunk；声明返回：'_MergedCore'；直接/间接调用：cls；返回表达式：cls((core,), core.content)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Merged, Core, from, core, cls

**调用：** cls；**返回：** cls((core,), core.content)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_MergedCore.first` (function, L283-L284)

**签名：** `def first(self) -> _CoreChunk`

**作用：** 返回合并组中的第一个核心块，用于读取起始结构定位。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self；声明返回：_CoreChunk；直接/间接调用：无明显函数调用；返回表达式：self.cores[0]；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Merged, Core, first

**调用：** 无明显调用；**返回：** self.cores[0]；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_MergedCore.last` (function, L287-L288)

**签名：** `def last(self) -> _CoreChunk`

**作用：** 返回合并组中的最后一个核心块，用于读取结束结构定位。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self；声明返回：_CoreChunk；直接/间接调用：无明显函数调用；返回表达式：self.cores[-1]；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Merged, Core, last

**调用：** 无明显调用；**返回：** self.cores[-1]；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_MergedCore.append` (function, L290-L291)

**签名：** `def append(self, core: _CoreChunk, separator: str) -> '_MergedCore'`

**作用：** 把相邻核心分块按分隔符合并，并更新合并块的边界和内容。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self, core: _CoreChunk, separator: str；声明返回：'_MergedCore'；直接/间接调用：_MergedCore；返回表达式：_MergedCore((*self.cores, core), f'{self.content}{separator}{core.content}')；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, Merged, Core, append, _MergedCore

**调用：** _MergedCore；**返回：** _MergedCore((*self.cores, core), f'{self.content}{separator}{core.content}')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_make_core_chunks` (function, L294-L351)

**签名：** `def _make_core_chunks(block: DocumentBlock, config: ChunkingConfig, backend: EmbeddingBackend | None) -> list[_CoreChunk]`

**作用：** Split one structural unit without overlap; rebalance only a short tail.

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：block: DocumentBlock, config: ChunkingConfig, backend: EmbeddingBackend | None；声明返回：list[_CoreChunk]；直接/间接调用：block.content.strip, enumerate, len, _find_stream_split_end, _fit_core_to_token_limit, raw.strip, max, _within_token_limit, result.append, positions.append, Subscript.strip, Subscript.count, _CoreChunk, raw.lstrip, content.count；返回表达式：result；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, make, core, chunks, block.content.strip, enumerate, len, _find_stream_split_end, _fit_core_to_token_limit, raw.strip, max, _within_token_limit, result.append, positions.append, Subscript.strip, Subscript.count, _CoreChunk, raw.lstrip, content.count, 条件分支, 循环

**调用：** block.content.strip, enumerate, len, _find_stream_split_end, _fit_core_to_token_limit, raw.strip, max, _within_token_limit, result.append, positions.append, Subscript.strip, Subscript.count, _CoreChunk, raw.lstrip, content.count；**返回：** result；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `_fit_core_to_token_limit` (function, L354-L378)

**签名：** `def _fit_core_to_token_limit(block: DocumentBlock, text: str, proposed_end: int, config: ChunkingConfig, backend: EmbeddingBackend | None) -> int`

**作用：** 执行  fit core to token limit，涉及 _find_stream_split_end, _within_token_limit, ValueError, Subscript.strip。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：block: DocumentBlock, text: str, proposed_end: int, config: ChunkingConfig, backend: EmbeddingBackend | None；声明返回：int；直接/间接调用：_find_stream_split_end, _within_token_limit, ValueError, Subscript.strip；返回表达式：_find_stream_split_end(text, best); proposed_end；显式异常：ValueError('Embedding 元数据本身已超过 max_chunk_tokens，无法生成有效 Chunk')；控制流：条件分支, 循环。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, fit, core, to, token, limit, _find_stream_split_end, _within_token_limit, ValueError, Subscript.strip, 条件分支, 循环

**调用：** _find_stream_split_end, _within_token_limit, ValueError, Subscript.strip；**返回：** _find_stream_split_end(text, best); proposed_end；**异常：** ValueError('Embedding 元数据本身已超过 max_chunk_tokens，无法生成有效 Chunk')；**副作用：** 模型/向量计算。

### `_same_structure` (function, L381-L390)

**签名：** `def _same_structure(left: _CoreChunk, right: _CoreChunk) -> bool`

**作用：** 比较两个核心块的标题、符号、记录或页面结构是否兼容。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：left: _CoreChunk, right: _CoreChunk；声明返回：bool；直接/间接调用：无明显函数调用；返回表达式：left.block.block_type == right.block.block_type and left.block.heading_path == right.block.heading_path and (left.block.symbol_path == right.block.symbol_path) and (left.block.lan…；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, same, structure

**调用：** 无明显调用；**返回：** left.block.block_type == right.block.block_type and left.block.heading_path == right.block.heading_path and (left.block.symbol_path == right.block.symbol_path) and (left.block.lan…；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_crosses_hard_boundary` (function, L393-L394)

**签名：** `def _crosses_hard_boundary(left: _CoreChunk, right: _CoreChunk) -> bool`

**作用：** 判断合并是否会跨越代码、记录、页面或幻灯片硬边界。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：left: _CoreChunk, right: _CoreChunk；声明返回：bool；直接/间接调用：无明显函数调用；返回表达式：left.hard_boundary_after or right.hard_boundary_before；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, crosses, hard, boundary

**调用：** 无明显调用；**返回：** left.hard_boundary_after or right.hard_boundary_before；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_located_block` (function, L397-L402)

**签名：** `def _located_block(group: _MergedCore) -> DocumentBlock`

**作用：** 从合并核心组恢复带完整来源定位信息的结构块。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：group: _MergedCore；声明返回：DocumentBlock；直接/间接调用：replace；返回表达式：replace(group.first.block, start_line=group.first.start_line, end_line=group.last.end_line)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, located, block, replace

**调用：** replace；**返回：** replace(group.first.block, start_line=group.first.start_line, end_line=group.last.end_line)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_within_token_limit` (function, L405-L416)

**签名：** `def _within_token_limit(content: str, block: DocumentBlock, config: ChunkingConfig, backend: EmbeddingBackend | None) -> bool`

**作用：** 检查候选文本经 Embedding tokenizer 计算后是否不超过 Token 上限。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：content: str, block: DocumentBlock, config: ChunkingConfig, backend: EmbeddingBackend | None；声明返回：bool；直接/间接调用：getattr, callable, bool, backend.token_count, fits_token_limit, build_embedding_content；返回表达式：backend.token_count(build_embedding_content(block, content)) <= config.max_chunk_tokens; True; bool(fits_token_limit(build_embedding_content(block, content), config.max_chunk_tokens))；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, within, token, limit, getattr, callable, bool, backend.token_count, fits_token_limit, build_embedding_content, 条件分支

**调用：** getattr, callable, bool, backend.token_count, fits_token_limit, build_embedding_content；**返回：** backend.token_count(build_embedding_content(block, content)) <= config.max_chunk_tokens; True; bool(fits_token_limit(build_embedding_content(block, content), config.max_chunk_tokens))；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `_add_final_overlap` (function, L419-L446)

**签名：** `def _add_final_overlap(groups: list[_MergedCore], index: int, config: ChunkingConfig, backend: EmbeddingBackend | None) -> str`

**作用：** 执行  add final overlap，涉及 min, _crosses_hard_boundary, len, max, _same_structure。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：groups: list[_MergedCore], index: int, config: ChunkingConfig, backend: EmbeddingBackend | None；声明返回：str；直接/间接调用：min, _crosses_hard_boundary, len, max, _same_structure, _within_token_limit；返回表达式：group.content; candidate；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, add, final, overlap, min, _crosses_hard_boundary, len, max, _same_structure, _within_token_limit, 条件分支, 循环

**调用：** min, _crosses_hard_boundary, len, max, _same_structure, _within_token_limit；**返回：** group.content; candidate；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `_group_block_id` (function, L449-L454)

**签名：** `def _group_block_id(group: _MergedCore) -> str`

**作用：** 根据合并组中的块 ID 生成稳定的最终分组标识。

**详细语义：** 所属模块职责：在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：group: _MergedCore；声明返回：str；直接/间接调用：无明显函数调用；返回表达式：f'{first.block.block_id}.{first.part_number}+{last.block.block_id}.{last.part_number}'; f'{first.block.block_id}.{first.part_number}-{last.part_number}'；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, group, block, id, 条件分支

**调用：** 无明显调用；**返回：** f'{first.block.block_id}.{first.part_number}+{last.block.block_id}.{last.part_number}'; f'{first.block.block_id}.{first.part_number}-{last.part_number}'；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/cleaning.py

**文件作用：** 对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。

**语言/关键词：** 文本清洗, 流式, Unicode, 换行, 空白, Python, py

**函数/类/脚本记录数：** 3

### `_clean_line` (function, L10-L19)

**签名：** `def _clean_line(raw_line: str, previous_blank: bool) -> tuple[str, bool]`

**作用：** 清洗一行文字，并返回清洗结果和新的空行状态。

**详细语义：** 所属模块职责：对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。；输入参数：raw_line: str, previous_blank: bool；声明返回：tuple[str, bool]；直接/间接调用：re.sub.strip, re.sub；返回表达式：(line + '\n', False); ('' if previous_blank else '\n', True)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 文本清洗, 流式, Unicode, 换行, 空白, clean, line, re.sub.strip, re.sub, 条件分支

**调用：** re.sub.strip, re.sub；**返回：** (line + '\n', False); ('' if previous_blank else '\n', True)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `iter_clean_text` (function, L22-L69)

**签名：** `def iter_clean_text(text_chunks: Iterable[str], *, max_pending: int=64 * 1024) -> Iterator[str]`

**作用：** 逐块清洗文本，保证待处理缓存不会随文件总大小增长。

**详细语义：** 所属模块职责：对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。；输入参数：text_chunks: Iterable[str], *, max_pending: int=64 * 1024；声明返回：Iterator[str]；直接/间接调用：unicodedata.normalize, normalized.replace.replace, line_buffer.split, lines.pop, _clean_line, len, line_buffer.rfind, re.sub.strip, normalized.replace, re.sub；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 文本清洗, 流式, Unicode, 换行, 空白, iter, clean, text, unicodedata.normalize, normalized.replace.replace, line_buffer.split, lines.pop, _clean_line, len, line_buffer.rfind, re.sub.strip, normalized.replace, re.sub, 条件分支, 循环, 生成器 yield

**调用：** unicodedata.normalize, normalized.replace.replace, line_buffer.split, lines.pop, _clean_line, len, line_buffer.rfind, re.sub.strip, normalized.replace, re.sub；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `clean_text` (function, L72-L81)

**签名：** `def clean_text(text: str) -> str`

**作用：** 规范换行、空白和不可见字符，同时保留 Markdown 标题等语义文字。

**详细语义：** 所属模块职责：对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。；输入参数：text: str；声明返回：str；直接/间接调用：Constant.join.strip, Constant.join, iter_clean_text；返回表达式：''.join(iter_clean_text([text])).strip(); ''；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 文本清洗, 流式, Unicode, 换行, 空白, clean, text, Constant.join.strip, Constant.join, iter_clean_text, 条件分支

**调用：** Constant.join.strip, Constant.join, iter_clean_text；**返回：** ''.join(iter_clean_text([text])).strip(); ''；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/cli.py

**文件作用：** 定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。

**语言/关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, Python, py

**函数/类/脚本记录数：** 14

### `_configure_console_encoding` (function, L44-L58)

**签名：** `def _configure_console_encoding() -> None`

**作用：** 保留终端原有编码，并避免特殊字符导致 Windows CLI 打印失败。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：；声明返回：None；直接/间接调用：getattr, reconfigure；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 异常处理。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, configure, console, encoding, getattr, reconfigure, 条件分支, 循环, 异常处理

**调用：** getattr, reconfigure；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_add_runtime_options` (function, L61-L80)

**签名：** `def _add_runtime_options(parser: argparse.ArgumentParser) -> None`

**作用：** 执行  add runtime options，涉及 parser.add_argument, Path。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：parser: argparse.ArgumentParser；声明返回：None；直接/间接调用：parser.add_argument, Path；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, add, runtime, options, parser.add_argument, Path

**调用：** parser.add_argument, Path；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `_add_embedding_options` (function, L83-L106)

**签名：** `def _add_embedding_options(parser: argparse.ArgumentParser) -> None`

**作用：** 执行  add embedding options，涉及 parser.add_argument。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：parser: argparse.ArgumentParser；声明返回：None；直接/间接调用：parser.add_argument；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, add, embedding, options, parser.add_argument

**调用：** parser.add_argument；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `_embedding_backend` (function, L109-L126)

**签名：** `def _embedding_backend(args) -> RemoteQwen3EmbeddingModel`

**作用：** 执行  embedding backend，涉及 LLMClient.load_dotenv, RemoteQwen3EmbeddingModel, EmbeddingSettings, os.getenv。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：args；声明返回：RemoteQwen3EmbeddingModel；直接/间接调用：LLMClient.load_dotenv, RemoteQwen3EmbeddingModel, EmbeddingSettings, os.getenv；返回表达式：RemoteQwen3EmbeddingModel(EmbeddingSettings(model_revision=args.embedding_revision or os.getenv('EMBEDDING_MODEL_REVISION'), dimension=args.embedding_dimension, batch_size=args.em…；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, embedding, backend, LLMClient.load_dotenv, RemoteQwen3EmbeddingModel, EmbeddingSettings, os.getenv

**调用：** LLMClient.load_dotenv, RemoteQwen3EmbeddingModel, EmbeddingSettings, os.getenv；**返回：** RemoteQwen3EmbeddingModel(EmbeddingSettings(model_revision=args.embedding_revision or os.getenv('EMBEDDING_MODEL_REVISION'), dimension=args.embedding_dimension, batch_size=args.em…；**异常：** 未发现显式 raise；**副作用：** 环境变量读取, 模型/向量计算。

### `build_parser` (function, L129-L371)

**签名：** `def build_parser() -> argparse.ArgumentParser`

**作用：** 构造并返回parser；内部调用 argparse.ArgumentParser, parser.add_subparsers, subparsers.add_parser, index_parser.add_argument, _add_embedding_options。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：；声明返回：argparse.ArgumentParser；直接/间接调用：argparse.ArgumentParser, parser.add_subparsers, subparsers.add_parser, index_parser.add_argument, _add_embedding_options, _add_runtime_options, preview_parser.add_argument, structure_parser.add_argument, search_parser.add_argument, ask_parser.add_argument, remove_parser.add_argument, web_parser.add_argument, Path；返回表达式：parser；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, build, parser, argparse.ArgumentParser, parser.add_subparsers, subparsers.add_parser, index_parser.add_argument, _add_embedding_options, _add_runtime_options, preview_parser.add_argument, structure_parser.add_argument, search_parser.add_argument, ask_parser.add_argument, remove_parser.add_argument, web_parser.add_argument, Path

**调用：** argparse.ArgumentParser, parser.add_subparsers, subparsers.add_parser, index_parser.add_argument, _add_embedding_options, _add_runtime_options, preview_parser.add_argument, structure_parser.add_argument, search_parser.add_argument, ask_parser.add_argument, remove_parser.add_argument, web_parser.add_argument, Path；**返回：** parser；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `_print_index_stats` (function, L374-L382)

**签名：** `def _print_index_stats(stats) -> None`

**作用：** 执行  print index stats，涉及 print。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：stats；声明返回：None；直接/间接调用：print；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, print, index, stats

**调用：** print；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出, 模型/向量计算。

### `_print_index_progress` (function, L385-L403)

**签名：** `def _print_index_progress(progress: IndexProgress) -> None`

**作用：** 以单行状态输出索引进度，适合终端和重定向日志。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：progress: IndexProgress；声明返回：None；直接/间接调用：print, status_names.get；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, print, index, progress, status_names.get, 条件分支

**调用：** print, status_names.get；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `_print_documents` (function, L406-L419)

**签名：** `def _print_documents(documents) -> None`

**作用：** 执行  print documents，涉及 print。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：documents；声明返回：None；直接/间接调用：print；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, print, documents, 条件分支, 循环

**调用：** print；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `_print_health` (function, L422-L432)

**签名：** `def _print_health(report) -> None`

**作用：** 执行  print health，涉及 print。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：report；声明返回：None；直接/间接调用：print；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, print, health, 条件分支, 循环

**调用：** print；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 日志输出, 模型/向量计算。

### `_print_json_structure` (function, L435-L444)

**签名：** `def _print_json_structure(report) -> None`

**作用：** 执行  print json structure，涉及 print, Constant.join。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：report；声明返回：None；直接/间接调用：print, Constant.join；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, print, json, structure, Constant.join, 条件分支, 循环

**调用：** print, Constant.join；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `_load_rag_config` (function, L447-L465)

**签名：** `def _load_rag_config(args: argparse.Namespace) -> RagConfig`

**作用：** 加载并校验rag config；内部调用 RagConfig, Path, RagConfig.from_file, default_path.exists。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：args: argparse.Namespace；声明返回：RagConfig；直接/间接调用：RagConfig, Path, RagConfig.from_file, default_path.exists；返回表达式：RagConfig(top_k=args.top_k if args.top_k is not None else config.top_k, max_context_chars=args.max_context_chars if args.max_context_chars is not None else config.max_context_char…；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, load, rag, config, RagConfig, Path, RagConfig.from_file, default_path.exists, 条件分支

**调用：** RagConfig, Path, RagConfig.from_file, default_path.exists；**返回：** RagConfig(top_k=args.top_k if args.top_k is not None else config.top_k, max_context_chars=args.max_context_chars if args.max_context_chars is not None else config.max_context_char…；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_print_answer` (function, L468-L482)

**签名：** `def _print_answer(result) -> None`

**作用：** 执行  print answer，涉及 print。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：result；声明返回：None；直接/间接调用：print；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, print, answer, 条件分支, 循环

**调用：** print；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `_run` (function, L485-L706)

**签名：** `def _run(args: argparse.Namespace) -> int`

**作用：** 执行  run，涉及 configure_logging, JsonProfile.from_file, parse_json_preview, enumerate, inspect_json_structure。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：args: argparse.Namespace；声明返回：int；直接/间接调用：configure_logging, JsonProfile.from_file, parse_json_preview, enumerate, inspect_json_structure, _print_json_structure, run_web, KnowledgeBase, print, _print_documents, knowledge_base.remove_document, knowledge_base.prune_missing_documents, knowledge_base.check_health, _print_health, index_paths, _print_index_stats, _embedding_backend, knowledge_base.list_documents, _load_rag_config, RagAnswerer, _print_answer, knowledge_base.ensure_document_embeddings, VectorRetriever, ChunkRetriever；返回表达式：0; 1; 0 if report.healthy else 1; 1 if unsuccessful and (not stats.indexed) else 0；显式异常：未发现显式 raise；控制流：条件分支, 循环, 上下文管理。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, run, configure_logging, JsonProfile.from_file, parse_json_preview, enumerate, inspect_json_structure, _print_json_structure, run_web, KnowledgeBase, print, _print_documents, knowledge_base.remove_document, knowledge_base.prune_missing_documents, knowledge_base.check_health, _print_health, index_paths, _print_index_stats, _embedding_backend, knowledge_base.list_documents, _load_rag_config, RagAnswerer, _print_answer, knowledge_base.ensure_document_embeddings, VectorRetriever, ChunkRetriever, 条件分支, 循环, 上下文管理

**调用：** configure_logging, JsonProfile.from_file, parse_json_preview, enumerate, inspect_json_structure, _print_json_structure, run_web, KnowledgeBase, print, _print_documents, knowledge_base.remove_document, knowledge_base.prune_missing_documents, knowledge_base.check_health, _print_health, index_paths, _print_index_stats, _embedding_backend, knowledge_base.list_documents, _load_rag_config, RagAnswerer, _print_answer, knowledge_base.ensure_document_embeddings, VectorRetriever, ChunkRetriever；**返回：** 0; 1; 0 if report.healthy else 1; 1 if unsuccessful and (not stats.indexed) else 0；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 日志输出, 模型/向量计算。

### `main` (function, L709-L721)

**签名：** `def main(argv: Sequence[str] | None=None) -> int`

**作用：** 执行模块主流程，编排参数、业务调用、输出和进程退出码。

**详细语义：** 所属模块职责：定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。；输入参数：argv: Sequence[str] | None=None；声明返回：int；直接/间接调用：_configure_console_encoding, build_parser.parse_args, _run, build_parser, logging.basicConfig, logger.error；返回表达式：_run(args); 1；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** CLI, argparse, 索引, 搜索, 问答, 退出码, main, _configure_console_encoding, build_parser.parse_args, _run, build_parser, logging.basicConfig, logger.error, 异常处理

**调用：** _configure_console_encoding, build_parser.parse_args, _run, build_parser, logging.basicConfig, logger.error；**返回：** _run(args); 1；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 日志输出。

## personal_local_knowledge_base_v0/knowledge_search/database.py

**文件作用：** 封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。

**语言/关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Python, py

**函数/类/脚本记录数：** 36

### `_json_tuple` (function, L232-L243)

**签名：** `def _json_tuple(value: str | None) -> tuple[str, ...]`

**作用：** Decode tuple metadata while tolerating malformed legacy values.

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：value: str | None；声明返回：tuple[str, ...]；直接/间接调用：tuple, json.loads, isinstance, str；返回表达式：tuple((str(item) for item in parsed)); ()；显式异常：未发现显式 raise；控制流：条件分支, 异常处理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, json, tuple, json.loads, isinstance, str, 条件分支, 异常处理

**调用：** tuple, json.loads, isinstance, str；**返回：** tuple((str(item) for item in parsed)); ()；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_compact_match_text` (function, L246-L250)

**签名：** `def _compact_match_text(text: str) -> str`

**作用：** Normalize text for chunk matching without performing word segmentation.

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：text: str；声明返回：str；直接/间接调用：unicodedata.normalize.casefold, Constant.join, unicodedata.normalize, character.isalnum；返回表达式：''.join((character for character in normalized if character.isalnum()))；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, compact, match, text, unicodedata.normalize.casefold, Constant.join, unicodedata.normalize, character.isalnum

**调用：** unicodedata.normalize.casefold, Constant.join, unicodedata.normalize, character.isalnum；**返回：** ''.join((character for character in normalized if character.isalnum()))；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_character_ngrams` (function, L253-L268)

**签名：** `def _character_ngrams(text: str, *, size: int=2, limit: int=64) -> list[str]`

**作用：** Return bounded character n-grams while preserving their original order.

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：text: str, *, size: int=2, limit: int=64；声明返回：list[str]；直接/间接调用：list, len, dict.fromkeys, range；返回表达式：[grams[index * len(grams) // limit] for index in range(limit)]; []; [text]; grams；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, character, ngrams, list, len, dict.fromkeys, range, 条件分支

**调用：** list, len, dict.fromkeys, range；**返回：** [grams[index * len(grams) // limit] for index in range(limit)]; []; [text]; grams；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeBase` (class, L271-L1512)

**签名：** `class KnowledgeBase`

**作用：** 一个 SQLite 知识库实例，负责连接生命周期和数据操作。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；类体包含 30 个直接方法。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeBase.__init__` (function, L274-L288)

**签名：** `def __init__(self, db_path: Path) -> 未声明`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, db_path: Path；声明返回：未声明；直接/间接调用：Path.expanduser.resolve, self.db_path.parent.mkdir, sqlite3.connect, self.connection.execute, self.initialize, Path.expanduser, Path；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, init, Path.expanduser.resolve, self.db_path.parent.mkdir, sqlite3.connect, self.connection.execute, self.initialize, Path.expanduser, Path

**调用：** Path.expanduser.resolve, self.db_path.parent.mkdir, sqlite3.connect, self.connection.execute, self.initialize, Path.expanduser, Path；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `KnowledgeBase.__enter__` (function, L290-L292)

**签名：** `def __enter__(self) -> 'KnowledgeBase'`

**作用：** 进入上下文管理器并返回可用的资源对象。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：'KnowledgeBase'；直接/间接调用：无明显函数调用；返回表达式：self；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, enter

**调用：** 无明显调用；**返回：** self；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeBase.__exit__` (function, L294-L296)

**签名：** `def __exit__(self, exc_type, exc_value, traceback) -> None`

**作用：** 退出上下文管理器，提交或关闭资源并按约定处理异常。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, exc_type, exc_value, traceback；声明返回：None；直接/间接调用：self.close；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, exit, self.close

**调用：** self.close；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeBase.initialize` (function, L298-L321)

**签名：** `def initialize(self) -> None`

**作用：** 执行 initialize，涉及 self.connection.executescript, self._ensure_schema_compatibility, self.connection.commit, self._backfill_token_index, self.connection.execute.fetchone。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：None；直接/间接调用：self.connection.executescript, self._ensure_schema_compatibility, self.connection.commit, self._backfill_token_index, self.connection.execute.fetchone, self.connection.execute, logger.exception；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：裸 raise；控制流：条件分支, 异常处理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, initialize, self.connection.executescript, self._ensure_schema_compatibility, self.connection.commit, self._backfill_token_index, self.connection.execute.fetchone, self.connection.execute, logger.exception, 条件分支, 异常处理

**调用：** self.connection.executescript, self._ensure_schema_compatibility, self.connection.commit, self._backfill_token_index, self.connection.execute.fetchone, self.connection.execute, logger.exception；**返回：** 未记录；**异常：** 裸 raise；**副作用：** SQLite/数据库写入或查询, 日志输出, 模型/向量计算。

### `KnowledgeBase._ensure_schema_compatibility` (function, L323-L391)

**签名：** `def _ensure_schema_compatibility(self) -> bool`

**作用：** 增量升级已有 V0 表，并用旧正文回填双内容字段。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：bool；直接/间接调用：additions.items, self.connection.execute；返回表达式：migrated；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, ensure, schema, compatibility, additions.items, self.connection.execute, 条件分支, 循环

**调用：** additions.items, self.connection.execute；**返回：** migrated；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase._backfill_token_index` (function, L393-L419)

**签名：** `def _backfill_token_index(self) -> None`

**作用：** 为已有 chunks 增量补建 jieba 词表，避免升级后中文索引为空。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：None；直接/间接调用：logger.info, self.connection.execute.fetchone, self.connection.execute, self.connection.executemany, Constant.join, tokenize_for_search；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 上下文管理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, backfill, token, index, logger.info, self.connection.execute.fetchone, self.connection.execute, self.connection.executemany, Constant.join, tokenize_for_search, 条件分支, 上下文管理

**调用：** logger.info, self.connection.execute.fetchone, self.connection.execute, self.connection.executemany, Constant.join, tokenize_for_search；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 日志输出, 模型/向量计算。

### `KnowledgeBase.close` (function, L421-L423)

**签名：** `def close(self) -> None`

**作用：** 关闭并释放内部资源；内部调用 self.connection.close。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：None；直接/间接调用：self.connection.close；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, close, self.connection.close

**调用：** self.connection.close；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeBase.embedding_model_id` (function, L425-L464)

**签名：** `def embedding_model_id(self, backend: EmbeddingBackend) -> int`

**作用：** Return the exact model/config row, creating it when necessary.

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, backend: EmbeddingBackend；声明返回：int；直接/间接调用：datetime.now.isoformat, self.connection.execute, self.connection.execute.fetchone, int, RuntimeError, datetime.now；返回表达式：int(row['id'])；显式异常：RuntimeError('无法创建 Embedding 模型配置')；控制流：条件分支。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, embedding, model, id, datetime.now.isoformat, self.connection.execute, self.connection.execute.fetchone, int, RuntimeError, datetime.now, 条件分支

**调用：** datetime.now.isoformat, self.connection.execute, self.connection.execute.fetchone, int, RuntimeError, datetime.now；**返回：** int(row['id'])；**异常：** RuntimeError('无法创建 Embedding 模型配置')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase._normalize_source_path` (function, L467-L470)

**签名：** `def _normalize_source_path(path: Path) -> Path`

**作用：** 使用与索引器相同的绝对路径格式识别源文档。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：path: Path；声明返回：Path；直接/间接调用：Path.expanduser.resolve, Path.expanduser, Path；返回表达式：Path(path).expanduser().resolve()；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, normalize, source, path, Path.expanduser.resolve, Path.expanduser, Path

**调用：** Path.expanduser.resolve, Path.expanduser, Path；**返回：** Path(path).expanduser().resolve()；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `KnowledgeBase.is_unchanged` (function, L472-L497)

**签名：** `def is_unchanged(self, document: ExtractedDocument, *, chunker_fingerprint: str | None=None) -> bool`

**作用：** 执行 is unchanged，涉及 self.connection.execute.fetchone, self.connection.execute, str, self._normalize_source_path。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, document: ExtractedDocument, *, chunker_fingerprint: str | None=None；声明返回：bool；直接/间接调用：self.connection.execute.fetchone, self.connection.execute, str, self._normalize_source_path；返回表达式：row is not None and row['sha256'] == document.sha256 and (row['parser_fingerprint'] == document.parser_fingerprint) and (row['parser'] == document.parser) and (chunker_fingerprint…；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, is, unchanged, self.connection.execute.fetchone, self.connection.execute, str, self._normalize_source_path

**调用：** self.connection.execute.fetchone, self.connection.execute, str, self._normalize_source_path；**返回：** row is not None and row['sha256'] == document.sha256 and (row['parser_fingerprint'] == document.parser_fingerprint) and (row['parser'] == document.parser) and (chunker_fingerprint…；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeBase.replace_document` (function, L499-L658)

**签名：** `def replace_document(self, document: ExtractedDocument, chunks: Iterable[Chunk], *, embedding_backend: EmbeddingBackend | None=None, chunker_fingerprint: str='') -> int`

**作用：** Atomically replace a document and persist validated final vectors.

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, document: ExtractedDocument, chunks: Iterable[Chunk], *, embedding_backend: EmbeddingBackend | None=None, chunker_fingerprint: str=''；声明返回：int；直接/间接调用：self._normalize_source_path, self.connection.execute.fetchone, self.connection.execute, int, self.connection.executemany, chunk_rows, self.embedding_model_id, datetime.now.isoformat, str, pending_vectors.append, datetime.now, Constant.join, ValueError, validate_vectors, json.dumps, sqlite3.Binary, tokenize_for_search, content_sha256, vector.tobytes；返回表达式：document_id；显式异常：ValueError('Chunk 含向量但未提供 embedding_backend')；控制流：条件分支, 循环, 上下文管理, 生成器 yield。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, replace, document, self._normalize_source_path, self.connection.execute.fetchone, self.connection.execute, int, self.connection.executemany, chunk_rows, self.embedding_model_id, datetime.now.isoformat, str, pending_vectors.append, datetime.now, Constant.join, ValueError, validate_vectors, json.dumps, sqlite3.Binary, tokenize_for_search, content_sha256, vector.tobytes, 条件分支, 循环, 上下文管理, 生成器 yield

**调用：** self._normalize_source_path, self.connection.execute.fetchone, self.connection.execute, int, self.connection.executemany, chunk_rows, self.embedding_model_id, datetime.now.isoformat, str, pending_vectors.append, datetime.now, Constant.join, ValueError, validate_vectors, json.dumps, sqlite3.Binary, tokenize_for_search, content_sha256, vector.tobytes；**返回：** document_id；**异常：** ValueError('Chunk 含向量但未提供 embedding_backend')；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 模型/向量计算。

### `KnowledgeBase.replace_document.chunk_rows` (function, L544-L586)

**签名：** `def chunk_rows() -> 未声明`

**作用：** 执行 chunk rows，涉及 pending_vectors.append, ValueError, validate_vectors, json.dumps, int。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：；声明返回：未声明；直接/间接调用：pending_vectors.append, ValueError, validate_vectors, json.dumps, int, content_sha256, vector.tobytes；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('Chunk 含向量但未提供 embedding_backend')；控制流：条件分支, 循环, 生成器 yield。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, replace, document, chunk, rows, pending_vectors.append, ValueError, validate_vectors, json.dumps, int, content_sha256, vector.tobytes, 条件分支, 循环, 生成器 yield

**调用：** pending_vectors.append, ValueError, validate_vectors, json.dumps, int, content_sha256, vector.tobytes；**返回：** 未记录；**异常：** ValueError('Chunk 含向量但未提供 embedding_backend')；**副作用：** 模型/向量计算。

### `KnowledgeBase.remove_document` (function, L660-L669)

**签名：** `def remove_document(self, path: Path) -> bool`

**作用：** 删除指定路径的文档及其 FTS5 内容。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, path: Path；声明返回：bool；直接/间接调用：self.connection.execute, str, self._normalize_source_path；返回表达式：cursor.rowcount > 0；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, remove, document, self.connection.execute, str, self._normalize_source_path, 上下文管理

**调用：** self.connection.execute, str, self._normalize_source_path；**返回：** cursor.rowcount > 0；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeBase.ensure_document_embeddings` (function, L671-L750)

**签名：** `def ensure_document_embeddings(self, path: Path, backend: EmbeddingBackend, *, chunker_fingerprint: str) -> int`

**作用：** Regenerate only missing or invalid vectors from stored chunks.

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, path: Path, backend: EmbeddingBackend, *, chunker_fingerprint: str；声明返回：int；直接/间接调用：self._normalize_source_path, len, self.embedding_model_id, self.connection.execute.fetchall, datetime.now.isoformat, range, content_sha256, backend.embed_documents, validate_vectors, self.connection.executemany, self.connection.execute, self._valid_vector_blob, stale.append, datetime.now, str, int, sqlite3.Binary, zip, vector.tobytes；返回表达式：len(stale)；显式异常：未发现显式 raise；控制流：条件分支, 循环, 上下文管理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, ensure, document, embeddings, self._normalize_source_path, len, self.embedding_model_id, self.connection.execute.fetchall, datetime.now.isoformat, range, content_sha256, backend.embed_documents, validate_vectors, self.connection.executemany, self.connection.execute, self._valid_vector_blob, stale.append, datetime.now, str, int, sqlite3.Binary, zip, vector.tobytes, 条件分支, 循环, 上下文管理

**调用：** self._normalize_source_path, len, self.embedding_model_id, self.connection.execute.fetchall, datetime.now.isoformat, range, content_sha256, backend.embed_documents, validate_vectors, self.connection.executemany, self.connection.execute, self._valid_vector_blob, stale.append, datetime.now, str, int, sqlite3.Binary, zip, vector.tobytes；**返回：** len(stale)；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase._valid_vector_blob` (function, L753-L763)

**签名：** `def _valid_vector_blob(blob: bytes | None, backend: EmbeddingBackend) -> bool`

**作用：** 执行  valid vector blob，涉及 np.frombuffer, len, bool, np.isfinite.all, np.isclose。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：blob: bytes | None, backend: EmbeddingBackend；声明返回：bool；直接/间接调用：np.frombuffer, len, bool, np.isfinite.all, np.isclose, np.dtype, np.linalg.norm, np.isfinite；返回表达式：True; False; bool(np.isclose(np.linalg.norm(vector), 1.0, rtol=0.0001, atol=1e-05))；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, valid, vector, blob, np.frombuffer, len, bool, np.isfinite.all, np.isclose, np.dtype, np.linalg.norm, np.isfinite, 条件分支

**调用：** np.frombuffer, len, bool, np.isfinite.all, np.isclose, np.dtype, np.linalg.norm, np.isfinite；**返回：** True; False; bool(np.isclose(np.linalg.norm(vector), 1.0, rtol=0.0001, atol=1e-05))；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `KnowledgeBase.embedding_cache_signature` (function, L765-L776)

**签名：** `def embedding_cache_signature(self, backend: EmbeddingBackend) -> tuple[int, int, str]`

**作用：** 执行 embedding cache signature，涉及 self.embedding_model_id, self.connection.execute.fetchone, int, str, self.connection.execute。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, backend: EmbeddingBackend；声明返回：tuple[int, int, str]；直接/间接调用：self.embedding_model_id, self.connection.execute.fetchone, int, str, self.connection.execute；返回表达式：(model_id, int(row['count']), str(row['latest']))；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, embedding, cache, signature, self.embedding_model_id, self.connection.execute.fetchone, int, str, self.connection.execute

**调用：** self.embedding_model_id, self.connection.execute.fetchone, int, str, self.connection.execute；**返回：** (model_id, int(row['count']), str(row['latest']))；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase.load_embedding_matrix` (function, L778-L803)

**签名：** `def load_embedding_matrix(self, backend: EmbeddingBackend) -> tuple[np.ndarray, np.ndarray]`

**作用：** Load one exact model configuration into aligned ids/vector arrays.

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, backend: EmbeddingBackend；声明返回：tuple[np.ndarray, np.ndarray]；直接/间接调用：self.embedding_model_id, self.connection.execute.fetchall, np.asarray, vectors.append, np.ascontiguousarray, self.connection.execute, int, np.empty, ValueError, np.frombuffer, np.vstack, self._valid_vector_blob；返回表达式：(chunk_ids, np.ascontiguousarray(np.vstack(vectors), dtype=np.float32)); (chunk_ids, np.empty((0, backend.settings.dimension), dtype=np.float32))；显式异常：ValueError(f'Chunk {row['chunk_id']} 的 Embedding 数据无效')；控制流：条件分支, 循环。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, load, embedding, matrix, self.embedding_model_id, self.connection.execute.fetchall, np.asarray, vectors.append, np.ascontiguousarray, self.connection.execute, int, np.empty, ValueError, np.frombuffer, np.vstack, self._valid_vector_blob, 条件分支, 循环

**调用：** self.embedding_model_id, self.connection.execute.fetchall, np.asarray, vectors.append, np.ascontiguousarray, self.connection.execute, int, np.empty, ValueError, np.frombuffer, np.vstack, self._valid_vector_blob；**返回：** (chunk_ids, np.ascontiguousarray(np.vstack(vectors), dtype=np.float32)); (chunk_ids, np.empty((0, backend.settings.dimension), dtype=np.float32))；**异常：** ValueError(f'Chunk {row['chunk_id']} 的 Embedding 数据无效')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase.results_for_vector_scores` (function, L805-L866)

**签名：** `def results_for_vector_scores(self, chunk_ids: list[int], scores: list[float], query: str) -> list[SearchResult]`

**作用：** 执行 results for vector scores，涉及 Constant.join, self.connection.execute.fetchall, zip, int, by_id.get。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, chunk_ids: list[int], scores: list[float], query: str；声明返回：list[SearchResult]；直接/间接调用：Constant.join, self.connection.execute.fetchall, zip, int, by_id.get, results.append, self.connection.execute, SearchResult, float, highlight_text, _json_tuple, bool；返回表达式：results; []；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, results, for, vector, scores, Constant.join, self.connection.execute.fetchall, zip, int, by_id.get, results.append, self.connection.execute, SearchResult, float, highlight_text, _json_tuple, bool, 条件分支, 循环

**调用：** Constant.join, self.connection.execute.fetchall, zip, int, by_id.get, results.append, self.connection.execute, SearchResult, float, highlight_text, _json_tuple, bool；**返回：** results; []；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase.vector_candidate_chunk_ids` (function, L868-L886)

**签名：** `def vector_candidate_chunk_ids(self, *, file_type: str | None=None, path: Path | None=None) -> set[int] | None`

**作用：** 执行 vector candidate chunk ids，涉及 self._document_filters, self.connection.execute, int, Constant.join。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, *, file_type: str | None=None, path: Path | None=None；声明返回：set[int] | None；直接/间接调用：self._document_filters, self.connection.execute, int, Constant.join；返回表达式：{int(row['id']) for row in rows}; None；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, vector, candidate, chunk, ids, self._document_filters, self.connection.execute, int, Constant.join, 条件分支

**调用：** self._document_filters, self.connection.execute, int, Constant.join；**返回：** {int(row['id']) for row in rows}; None；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeBase.list_documents` (function, L888-L922)

**签名：** `def list_documents(self) -> list[DocumentInfo]`

**作用：** 列出文档元数据以及每个文档的分段数量。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：list[DocumentInfo]；直接/间接调用：self.connection.execute.fetchall, DocumentInfo, self.connection.execute, int；返回表达式：[DocumentInfo(document_id=int(row['document_id']), path=row['path'], filename=row['filename'], file_type=row['file_type'], size=int(row['size']), chunk_count=int(row['chunk_count'…；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, list, documents, self.connection.execute.fetchall, DocumentInfo, self.connection.execute, int

**调用：** self.connection.execute.fetchall, DocumentInfo, self.connection.execute, int；**返回：** [DocumentInfo(document_id=int(row['document_id']), path=row['path'], filename=row['filename'], file_type=row['file_type'], size=int(row['size']), chunk_count=int(row['chunk_count'…；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeBase.prune_missing_documents` (function, L924-L940)

**签名：** `def prune_missing_documents(self) -> list[DocumentInfo]`

**作用：** 删除数据库中源文件已不存在的文档，并返回被删除的记录。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：list[DocumentInfo]；直接/间接调用：self.connection.executemany, self.list_documents, Path.is_file, Path；返回表达式：missing; []；显式异常：未发现显式 raise；控制流：条件分支, 上下文管理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, prune, missing, documents, self.connection.executemany, self.list_documents, Path.is_file, Path, 条件分支, 上下文管理

**调用：** self.connection.executemany, self.list_documents, Path.is_file, Path；**返回：** missing; []；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `KnowledgeBase._document_filters` (function, L943-L973)

**签名：** `def _document_filters(file_type: str | None, path: Path | None, *, alias: str='d') -> tuple[list[str], list[str]]`

**作用：** 构造搜索使用的文档过滤条件和绑定参数。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：file_type: str | None, path: Path | None, *, alias: str='d'；声明返回：tuple[list[str], list[str]]；直接/间接调用：conditions.append, parameters.append, KnowledgeBase._normalize_source_path, str, tuple, file_type.lower.lstrip, normalized_path.is_dir, raw_path.endswith, str.replace, prefix.replace.replace, file_type.lower, prefix.replace；返回表达式：(conditions, parameters)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, document, filters, conditions.append, parameters.append, KnowledgeBase._normalize_source_path, str, tuple, file_type.lower.lstrip, normalized_path.is_dir, raw_path.endswith, str.replace, prefix.replace.replace, file_type.lower, prefix.replace, 条件分支

**调用：** conditions.append, parameters.append, KnowledgeBase._normalize_source_path, str, tuple, file_type.lower.lstrip, normalized_path.is_dir, raw_path.endswith, str.replace, prefix.replace.replace, file_type.lower, prefix.replace；**返回：** (conditions, parameters)；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `KnowledgeBase._search_fts_rows` (function, L975-L1018)

**签名：** `def _search_fts_rows(self, table_name: str, match_query: str, limit: int, *, file_type: str | None=None, path: Path | None=None) -> list[sqlite3.Row]`

**作用：** 在指定 FTS5 表中执行一次安全的关键词查询。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, table_name: str, match_query: str, limit: int, *, file_type: str | None=None, path: Path | None=None；声明返回：list[sqlite3.Row]；直接/间接调用：self._document_filters, Constant.join, self.connection.execute.fetchall, ValueError, self.connection.execute；返回表达式：self.connection.execute(f'\n            SELECT\n                c.id AS chunk_id,\n                d.path AS document_path,\n                d.filename AS filename,\n             …；显式异常：ValueError(f'未知的 FTS5 表：{table_name}')；控制流：条件分支。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, search, fts, rows, self._document_filters, Constant.join, self.connection.execute.fetchall, ValueError, self.connection.execute, 条件分支

**调用：** self._document_filters, Constant.join, self.connection.execute.fetchall, ValueError, self.connection.execute；**返回：** self.connection.execute(f'\n            SELECT\n                c.id AS chunk_id,\n                d.path AS document_path,\n                d.filename AS filename,\n             …；**异常：** ValueError(f'未知的 FTS5 表：{table_name}')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase.search` (function, L1020-L1146)

**签名：** `def search(self, query: str, limit: int=10, *, file_type: str | None=None, path: Path | None=None) -> list[SearchResult]`

**作用：** 依次查询结构词索引、结构 FTS、原文 FTS 和参数化 LIKE。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, query: str, limit: int=10, *, file_type: str | None=None, path: Path | None=None；声明返回：list[SearchResult]；直接/间接调用：to_fts_query, to_token_fts_query, any, ValueError, query_terms, Constant.join, self._document_filters, self.connection.execute.fetchall, SearchResult, self._search_fts_rows, logger.exception, self.connection.execute, int, float, highlight_text, _json_tuple, bool；返回表达式：[SearchResult(chunk_id=int(row['chunk_id']), document_path=row['document_path'], filename=row['filename'], file_type=row['file_type'], chunk_index=int(row['chunk_index']), content…；显式异常：ValueError('limit 必须大于 0'); ValueError(f'搜索失败：{exc}')；控制流：条件分支, 异常处理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, search, to_fts_query, to_token_fts_query, any, ValueError, query_terms, Constant.join, self._document_filters, self.connection.execute.fetchall, SearchResult, self._search_fts_rows, logger.exception, self.connection.execute, int, float, highlight_text, _json_tuple, bool, 条件分支, 异常处理

**调用：** to_fts_query, to_token_fts_query, any, ValueError, query_terms, Constant.join, self._document_filters, self.connection.execute.fetchall, SearchResult, self._search_fts_rows, logger.exception, self.connection.execute, int, float, highlight_text, _json_tuple, bool；**返回：** [SearchResult(chunk_id=int(row['chunk_id']), document_path=row['document_path'], filename=row['filename'], file_type=row['file_type'], chunk_index=int(row['chunk_index']), content…；**异常：** ValueError('limit 必须大于 0'); ValueError(f'搜索失败：{exc}')；**副作用：** SQLite/数据库写入或查询, 日志输出, 模型/向量计算。

### `KnowledgeBase.search_chunk_matches` (function, L1148-L1217)

**签名：** `def search_chunk_matches(self, query_chunk: str, limit: int=10) -> list[SearchResult]`

**作用：** Match one question chunk against structured chunks without jieba.

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, query_chunk: str, limit: int=10；声明返回：list[SearchResult]；直接/间接调用：_compact_match_text, _character_ngrams, Constant.join, max, self.connection.execute.fetchall, ranked.sort, self.results_for_vector_scores, ValueError, min, range, int, float, ranked.append, self.connection.execute, len, any, gram.replace.replace.replace, gram.replace.replace, gram.replace；返回表达式：self.results_for_vector_scores([chunk_id for chunk_id, _length, _score in selected], [-score for _chunk_id, _length, score in selected], query_chunk); []；显式异常：ValueError('limit 必须大于 0')；控制流：条件分支, 循环。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, search, chunk, matches, _compact_match_text, _character_ngrams, Constant.join, max, self.connection.execute.fetchall, ranked.sort, self.results_for_vector_scores, ValueError, min, range, int, float, ranked.append, self.connection.execute, len, any, gram.replace.replace.replace, gram.replace.replace, gram.replace, 条件分支, 循环

**调用：** _compact_match_text, _character_ngrams, Constant.join, max, self.connection.execute.fetchall, ranked.sort, self.results_for_vector_scores, ValueError, min, range, int, float, ranked.append, self.connection.execute, len, any, gram.replace.replace.replace, gram.replace.replace, gram.replace；**返回：** self.results_for_vector_scores([chunk_id for chunk_id, _length, _score in selected], [-score for _chunk_id, _length, score in selected], query_chunk); []；**异常：** ValueError('limit 必须大于 0')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase.search_chunk_matches.lambda@1211` (function, L1211-L1211)

**签名：** `lambda item`

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；这是匿名 lambda，输入参数：item；返回表达式：(-item[2], item[1], item[0])；调用：无明显函数调用；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, lambda

**调用：** 无明显调用；**返回：** (-item[2], item[1], item[0])；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeBase.chunk_window` (function, L1219-L1316)

**签名：** `def chunk_window(self, chunk_id: int, radius: int=1) -> list[Chunk]`

**作用：** Return neighbors without crossing page, record, slide, or code boundaries.

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self, chunk_id: int, radius: int=1；声明返回：list[Chunk]；直接/间接调用：self.connection.execute.fetchone, self.connection.execute.fetchall, next, ValueError, Chunk, len, self.connection.execute, int, _json_tuple, bool, enumerate；返回表达式：candidates[left:right + 1]; []；显式异常：ValueError('radius 不能小于 0')；控制流：条件分支, 循环。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, chunk, window, self.connection.execute.fetchone, self.connection.execute.fetchall, next, ValueError, Chunk, len, self.connection.execute, int, _json_tuple, bool, enumerate, 条件分支, 循环

**调用：** self.connection.execute.fetchone, self.connection.execute.fetchall, next, ValueError, Chunk, len, self.connection.execute, int, _json_tuple, bool, enumerate；**返回：** candidates[left:right + 1]; []；**异常：** ValueError('radius 不能小于 0')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase.document_count` (function, L1318-L1321)

**签名：** `def document_count(self) -> int`

**作用：** 执行 document count，涉及 self.connection.execute.fetchone, int, self.connection.execute。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：int；直接/间接调用：self.connection.execute.fetchone, int, self.connection.execute；返回表达式：int(row['count'])；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, document, count, self.connection.execute.fetchone, int, self.connection.execute

**调用：** self.connection.execute.fetchone, int, self.connection.execute；**返回：** int(row['count'])；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeBase.check_health` (function, L1323-L1495)

**签名：** `def check_health(self) -> DatabaseHealth`

**作用：** 检查关系表、三套 FTS5 索引及文档/分段关系的一致性。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：DatabaseHealth；直接/间接调用：self.document_count, self.chunk_count, int, DatabaseHealth, issues.append, self.connection.execute.fetchone, self.connection.execute, tuple；返回表达式：DatabaseHealth(document_count=document_count, chunk_count=chunk_count, chunks_fts_count=chunks_fts_count, chunk_tokens_count=chunk_tokens_count, chunks_fts_jieba_count=chunks_fts_…；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, check, health, self.document_count, self.chunk_count, int, DatabaseHealth, issues.append, self.connection.execute.fetchone, self.connection.execute, tuple, 条件分支

**调用：** self.document_count, self.chunk_count, int, DatabaseHealth, issues.append, self.connection.execute.fetchone, self.connection.execute, tuple；**返回：** DatabaseHealth(document_count=document_count, chunk_count=chunk_count, chunks_fts_count=chunks_fts_count, chunk_tokens_count=chunk_tokens_count, chunks_fts_jieba_count=chunks_fts_…；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase.chunk_count` (function, L1497-L1500)

**签名：** `def chunk_count(self) -> int`

**作用：** 执行 chunk count，涉及 self.connection.execute.fetchone, int, self.connection.execute。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：int；直接/间接调用：self.connection.execute.fetchone, int, self.connection.execute；返回表达式：int(row['count'])；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, chunk, count, self.connection.execute.fetchone, int, self.connection.execute

**调用：** self.connection.execute.fetchone, int, self.connection.execute；**返回：** int(row['count'])；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeBase.embedding_count` (function, L1502-L1506)

**签名：** `def embedding_count(self) -> int`

**作用：** 执行 embedding count，涉及 self.connection.execute.fetchone, int, self.connection.execute。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：int；直接/间接调用：self.connection.execute.fetchone, int, self.connection.execute；返回表达式：int(row['count'])；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, embedding, count, self.connection.execute.fetchone, int, self.connection.execute

**调用：** self.connection.execute.fetchone, int, self.connection.execute；**返回：** int(row['count'])；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeBase.embedding_model_count` (function, L1508-L1512)

**签名：** `def embedding_model_count(self) -> int`

**作用：** 执行 embedding model count，涉及 self.connection.execute.fetchone, int, self.connection.execute。

**详细语义：** 所属模块职责：封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：int；直接/间接调用：self.connection.execute.fetchone, int, self.connection.execute；返回表达式：int(row['count'])；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, Knowledge, Base, embedding, model, count, self.connection.execute.fetchone, int, self.connection.execute

**调用：** self.connection.execute.fetchone, int, self.connection.execute；**返回：** int(row['count'])；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

## personal_local_knowledge_base_v0/knowledge_search/dataset_reader.py

**文件作用：** 将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。

**语言/关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, Python, py

**函数/类/脚本记录数：** 23

### `DatasetReaderError` (class, L23-L24)

**签名：** `class DatasetReaderError`

**作用：** 数据集读取或适配失败。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；类体包含 0 个直接方法。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, Dataset, Reader, Error

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_load_dataset` (function, L27-L36)

**签名：** `def _load_dataset(*args: Any, **kwargs: Any) -> 未声明`

**作用：** Load ``datasets`` lazily so the base application has no hard import cost.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：*args: Any, **kwargs: Any；声明返回：未声明；直接/间接调用：load_dataset, DatasetReaderError；返回表达式：load_dataset(*args, **kwargs)；显式异常：DatasetReaderError('数据集读取需要可选依赖，请安装：pip install datasets pyarrow')；控制流：异常处理。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, load, dataset, load_dataset, DatasetReaderError, 异常处理

**调用：** load_dataset, DatasetReaderError；**返回：** load_dataset(*args, **kwargs)；**异常：** DatasetReaderError('数据集读取需要可选依赖，请安装：pip install datasets pyarrow')；**副作用：** 未发现明显外部副作用。

### `_value` (function, L39-L41)

**签名：** `def _value(row: Mapping[str, Any], key: str, default: Any=None) -> Any`

**作用：** 执行  value，涉及 row.get。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：row: Mapping[str, Any], key: str, default: Any=None；声明返回：Any；直接/间接调用：row.get；返回表达式：default if value is None else value；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, value, row.get, 条件分支

**调用：** row.get；**返回：** default if value is None else value；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_text` (function, L44-L48)

**签名：** `def _text(value: Any) -> str | None`

**作用：** 执行  text，涉及 str.strip, str。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：value: Any；声明返回：str | None；直接/间接调用：str.strip, str；返回表达式：text or None; None；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, text, str.strip, str, 条件分支

**调用：** str.strip, str；**返回：** text or None; None；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_base_record` (function, L51-L59)

**签名：** `def _base_record(index: int) -> dict[str, Any]`

**作用：** 执行  base record，涉及 str。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：index: int；声明返回：dict[str, Any]；直接/间接调用：str；返回表达式：{'id': str(index), 'title': None, 'text': None, 'query': None, 'answers': [], 'meta': {}}；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, base, record, str

**调用：** str；**返回：** {'id': str(index), 'title': None, 'text': None, 'query': None, 'answers': [], 'meta': {}}；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_nested` (function, L62-L68)

**签名：** `def _nested(row: Mapping[str, Any], *keys: str) -> Any`

**作用：** 执行  nested，涉及 value.get, isinstance。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：row: Mapping[str, Any], *keys: str；声明返回：Any；直接/间接调用：value.get, isinstance；返回表达式：value; None；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, nested, value.get, isinstance, 条件分支, 循环

**调用：** value.get, isinstance；**返回：** value; None；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_normalize_dureader` (function, L71-L80)

**签名：** `def _normalize_dureader(row: Mapping[str, Any], index: int) -> dict[str, Any]`

**作用：** 规范化并适配 dureader；内部调用 _base_record, _text, _value, range。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：row: Mapping[str, Any], index: int；声明返回：dict[str, Any]；直接/间接调用：_base_record, _text, _value, range；返回表达式：record；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, normalize, dureader, _base_record, _text, _value, range

**调用：** _base_record, _text, _value, range；**返回：** record；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_normalize_github_code` (function, L83-L95)

**签名：** `def _normalize_github_code(row: Mapping[str, Any], index: int) -> dict[str, Any]`

**作用：** 规范化并适配 github code；内部调用 _base_record, _text, _value。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：row: Mapping[str, Any], index: int；声明返回：dict[str, Any]；直接/间接调用：_base_record, _text, _value；返回表达式：record；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, normalize, github, code, _base_record, _text, _value

**调用：** _base_record, _text, _value；**返回：** record；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_normalize_codesearchnet` (function, L98-L108)

**签名：** `def _normalize_codesearchnet(row: Mapping[str, Any], index: int) -> dict[str, Any]`

**作用：** 规范化并适配 codesearchnet；内部调用 _base_record, _text, str, _value。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：row: Mapping[str, Any], index: int；声明返回：dict[str, Any]；直接/间接调用：_base_record, _text, str, _value；返回表达式：record；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, normalize, codesearchnet, _base_record, _text, str, _value

**调用：** _base_record, _text, str, _value；**返回：** record；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_normalize_narrativeqa` (function, L111-L126)

**签名：** `def _normalize_narrativeqa(row: Mapping[str, Any], index: int) -> dict[str, Any]`

**作用：** 规范化并适配 narrativeqa；内部调用 _base_record, _nested, _text, _value, str。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：row: Mapping[str, Any], index: int；声明返回：dict[str, Any]；直接/间接调用：_base_record, _nested, _text, _value, str, isinstance, answer.get；返回表达式：record；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, normalize, narrativeqa, _base_record, _nested, _text, _value, str, isinstance, answer.get, 条件分支

**调用：** _base_record, _nested, _text, _value, str, isinstance, answer.get；**返回：** record；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_normalize_natural_questions` (function, L129-L148)

**签名：** `def _normalize_natural_questions(row: Mapping[str, Any], index: int) -> dict[str, Any]`

**作用：** 规范化并适配 natural questions；内部调用 _base_record, _value, str, _text, isinstance。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：row: Mapping[str, Any], index: int；声明返回：dict[str, Any]；直接/间接调用：_base_record, _value, str, _text, isinstance, list, _nested, Constant.join.strip, Constant.join, enumerate, len, bool；返回表达式：record；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, normalize, natural, questions, _base_record, _value, str, _text, isinstance, list, _nested, Constant.join.strip, Constant.join, enumerate, len, bool, 条件分支

**调用：** _base_record, _value, str, _text, isinstance, list, _nested, Constant.join.strip, Constant.join, enumerate, len, bool；**返回：** record；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_normalize_text_record` (function, L151-L156)

**签名：** `def _normalize_text_record(row: Mapping[str, Any], index: int) -> dict[str, Any]`

**作用：** 规范化并适配 text record；内部调用 _base_record, str, _text, _value。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：row: Mapping[str, Any], index: int；声明返回：dict[str, Any]；直接/间接调用：_base_record, str, _text, _value；返回表达式：record；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, normalize, text, record, _base_record, str, _text, _value

**调用：** _base_record, str, _text, _value；**返回：** record；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `register_adapter` (function, L170-L185)

**签名：** `def register_adapter(dataset_name: str, adapter: DatasetAdapter, *, replace: bool=False) -> None`

**作用：** Register a dataset field adapter without changing physical readers.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：dataset_name: str, adapter: DatasetAdapter, *, replace: bool=False；声明返回：None；直接/间接调用：str.strip.lower, ValueError, callable, TypeError, str.strip, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('dataset_name 不能为空'); TypeError('adapter 必须可调用'); ValueError(f'数据集适配器已存在：{name}')；控制流：条件分支。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, register, adapter, str.strip.lower, ValueError, callable, TypeError, str.strip, str, 条件分支

**调用：** str.strip.lower, ValueError, callable, TypeError, str.strip, str；**返回：** 未记录；**异常：** ValueError('dataset_name 不能为空'); TypeError('adapter 必须可调用'); ValueError(f'数据集适配器已存在：{name}')；**副作用：** 未发现明显外部副作用。

### `available_adapters` (function, L188-L191)

**签名：** `def available_adapters() -> tuple[str, ...]`

**作用：** Return registered adapter names in deterministic order.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：；声明返回：tuple[str, ...]；直接/间接调用：tuple, sorted；返回表达式：tuple(sorted(_ADAPTERS))；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, available, adapters, tuple, sorted

**调用：** tuple, sorted；**返回：** tuple(sorted(_ADAPTERS))；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `normalize` (function, L194-L217)

**签名：** `def normalize(dataset_name: str, row: Mapping[str, Any], index: int) -> dict[str, Any]`

**作用：** Normalize one dataset row to ``id/title/text/query/answers/meta``.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：dataset_name: str, row: Mapping[str, Any], index: int；声明返回：dict[str, Any]；直接/间接调用：str.strip.lower, _ADAPTERS.get, adapter, str, isinstance, DatasetReaderError, ValueError, tuple, list, str.strip, record.get, type；返回表达式：record；显式异常：DatasetReaderError(f'数据集记录必须是映射对象，实际类型：{type(row).__name__}'); ValueError(f'Unsupported dataset: {dataset_name}')；控制流：条件分支。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, normalize, str.strip.lower, _ADAPTERS.get, adapter, str, isinstance, DatasetReaderError, ValueError, tuple, list, str.strip, record.get, type, 条件分支

**调用：** str.strip.lower, _ADAPTERS.get, adapter, str, isinstance, DatasetReaderError, ValueError, tuple, list, str.strip, record.get, type；**返回：** record；**异常：** DatasetReaderError(f'数据集记录必须是映射对象，实际类型：{type(row).__name__}'); ValueError(f'Unsupported dataset: {dataset_name}')；**副作用：** 未发现明显外部副作用。

### `_dataset_kwargs` (function, L220-L224)

**签名：** `def _dataset_kwargs(config: str | None, split: str) -> dict[str, Any]`

**作用：** 执行  dataset kwargs。

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：config: str | None, split: str；声明返回：dict[str, Any]；直接/间接调用：无明显函数调用；返回表达式：kwargs；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, dataset, kwargs, 条件分支

**调用：** 无明显调用；**返回：** kwargs；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_iter_normalized_rows` (function, L227-L248)

**签名：** `def _iter_normalized_rows(dataset: Iterable[Mapping[str, Any]], adapter: str) -> Iterator[dict[str, Any]]`

**作用：** Normalize rows and explicitly release local streaming file handles.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：dataset: Iterable[Mapping[str, Any]], adapter: str；声明返回：Iterator[dict[str, Any]]；直接/间接调用：iter, enumerate, getattr, callable, gc.collect, close_iterator, close_dataset, normalize；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, iter, normalized, rows, enumerate, getattr, callable, gc.collect, close_iterator, close_dataset, normalize, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** iter, enumerate, getattr, callable, gc.collect, close_iterator, close_dataset, normalize；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `iter_huggingface` (function, L251-L271)

**签名：** `def iter_huggingface(repo: str, config: str | None, split: str, adapter: str) -> Iterator[dict[str, Any]]`

**作用：** Stream a Hugging Face dataset and normalize each row lazily.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：repo: str, config: str | None, split: str, adapter: str；声明返回：Iterator[dict[str, Any]]；直接/间接调用：_load_dataset, gc.collect, DatasetReaderError, _dataset_kwargs, _iter_normalized_rows；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：裸 raise; DatasetReaderError(f'读取 Hugging Face 数据集失败：{repo}/{config or '<default>'}:{split}：{exc}')；控制流：异常处理, 生成器 yield。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, iter, huggingface, _load_dataset, gc.collect, DatasetReaderError, _dataset_kwargs, _iter_normalized_rows, 异常处理, 生成器 yield

**调用：** _load_dataset, gc.collect, DatasetReaderError, _dataset_kwargs, _iter_normalized_rows；**返回：** 未记录；**异常：** 裸 raise; DatasetReaderError(f'读取 Hugging Face 数据集失败：{repo}/{config or '<default>'}:{split}：{exc}')；**副作用：** 未发现明显外部副作用。

### `infer_local_format` (function, L274-L286)

**签名：** `def infer_local_format(path: Path) -> str`

**作用：** Infer a ``datasets`` builder name from Parquet/JSONL/GZIP suffixes.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：path: Path；声明返回：str；直接/间接调用：ValueError, suffix.lower, suffixes.pop, Path；返回表达式：'json'; 'parquet'；显式异常：ValueError(f'无法从文件后缀推断数据集格式：{path}；目前支持 Parquet、JSONL 和 GZIP')；控制流：条件分支。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, infer, local, format, ValueError, suffix.lower, suffixes.pop, Path, 条件分支

**调用：** ValueError, suffix.lower, suffixes.pop, Path；**返回：** 'json'; 'parquet'；**异常：** ValueError(f'无法从文件后缀推断数据集格式：{path}；目前支持 Parquet、JSONL 和 GZIP')；**副作用：** 未发现明显外部副作用。

### `iter_local_dataset` (function, L289-L316)

**签名：** `def iter_local_dataset(path: Path, dataset_name: str, *, split: str='train', file_format: str | None=None) -> Iterator[dict[str, Any]]`

**作用：** Stream a local Parquet/JSONL/GZIP file through ``datasets``.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：path: Path, dataset_name: str, *, split: str='train', file_format: str | None=None；声明返回：Iterator[dict[str, Any]]；直接/间接调用：Path.expanduser.resolve, local_path.is_file, FileNotFoundError, infer_local_format, _load_dataset, Path.expanduser, gc.collect, DatasetReaderError, _dataset_kwargs, _iter_normalized_rows, Path, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：FileNotFoundError(f'数据集文件不存在：{local_path}'); 裸 raise; DatasetReaderError(f'读取本地数据集失败：{local_path}：{exc}')；控制流：条件分支, 异常处理, 生成器 yield。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, iter, local, dataset, Path.expanduser.resolve, local_path.is_file, FileNotFoundError, infer_local_format, _load_dataset, Path.expanduser, gc.collect, DatasetReaderError, _dataset_kwargs, _iter_normalized_rows, Path, str, 条件分支, 异常处理, 生成器 yield

**调用：** Path.expanduser.resolve, local_path.is_file, FileNotFoundError, infer_local_format, _load_dataset, Path.expanduser, gc.collect, DatasetReaderError, _dataset_kwargs, _iter_normalized_rows, Path, str；**返回：** 未记录；**异常：** FileNotFoundError(f'数据集文件不存在：{local_path}'); 裸 raise; DatasetReaderError(f'读取本地数据集失败：{local_path}：{exc}')；**副作用：** 文件系统读写。

### `iter_local_dureader` (function, L319-L322)

**签名：** `def iter_local_dureader(path: Path) -> Iterator[dict[str, Any]]`

**作用：** Convenience wrapper for a downloaded DuReader Parquet shard.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：path: Path；声明返回：Iterator[dict[str, Any]]；直接/间接调用：iter_local_dataset；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：生成器 yield。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, iter, local, dureader, iter_local_dataset, 生成器 yield

**调用：** iter_local_dataset；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `iter_dataset_blocks` (function, L325-L367)

**签名：** `def iter_dataset_blocks(records: Iterable[Mapping[str, Any]], *, source_name: str) -> Iterator[DocumentBlock]`

**作用：** Convert normalized records into independent structural blocks.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：records: Iterable[Mapping[str, Any]], *, source_name: str；声明返回：Iterator[DocumentBlock]；直接/间接调用：enumerate, _text, str, DatasetReaderError, isinstance, meta.get, hashlib.sha256.hexdigest, DocumentBlock, hashlib.sha256, Constant.join, identity.encode；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：DatasetReaderError(f'统一记录缺少字段：{', '.join(missing)}（记录 {index}）')；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, iter, dataset, blocks, enumerate, _text, str, DatasetReaderError, isinstance, meta.get, hashlib.sha256.hexdigest, DocumentBlock, hashlib.sha256, Constant.join, identity.encode, 条件分支, 循环, 生成器 yield

**调用：** enumerate, _text, str, DatasetReaderError, isinstance, meta.get, hashlib.sha256.hexdigest, DocumentBlock, hashlib.sha256, Constant.join, identity.encode；**返回：** 未记录；**异常：** DatasetReaderError(f'统一记录缺少字段：{', '.join(missing)}（记录 {index}）')；**副作用：** 未发现明显外部副作用。

### `iter_dataset` (function, L370-L396)

**签名：** `def iter_dataset(source: str | Path, dataset_name: str, *, config: str | None=None, split: str='train', file_format: str | None=None) -> Iterator[dict[str, Any]]`

**作用：** Unified entry point for a local dataset file or HF repository.

**详细语义：** 所属模块职责：将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：source: str | Path, dataset_name: str, *, config: str | None=None, split: str='train', file_format: str | None=None；声明返回：Iterator[dict[str, Any]]；直接/间接调用：Path.expanduser, suffix.lower, isinstance, candidate.is_absolute, candidate.is_file, bool, iter_huggingface, Path, iter_local_dataset, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 生成器 yield。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, iter, dataset, Path.expanduser, suffix.lower, isinstance, candidate.is_absolute, candidate.is_file, bool, iter_huggingface, Path, iter_local_dataset, str, 条件分支, 生成器 yield

**调用：** Path.expanduser, suffix.lower, isinstance, candidate.is_absolute, candidate.is_file, bool, iter_huggingface, Path, iter_local_dataset, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

## personal_local_knowledge_base_v0/knowledge_search/embedding.py

**文件作用：** 定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。

**语言/关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Python, py

**函数/类/脚本记录数：** 26

### `EmbeddingSettings` (class, L30-L59)

**签名：** `class EmbeddingSettings`

**作用：** All values that affect generated vectors or cache identity.

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 2 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Settings

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingSettings.__post_init__` (function, L40-L50)

**签名：** `def __post_init__(self) -> None`

**作用：** 执行 dataclass 配置校验，拒绝不满足范围、格式或不变量的参数。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：None；直接/间接调用：self.model_name.strip, ValueError, self.query_instruction.strip；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('embedding_model 不能为空'); ValueError('embedding_dimension 必须在 1 到 1024 之间'); ValueError('当前向量链路要求 normalize_embeddings=true'); ValueError('batch_size 必须大于 0'); ValueError('query_instruction 不能为空')；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Settings, post, init, self.model_name.strip, ValueError, self.query_instruction.strip, 条件分支

**调用：** self.model_name.strip, ValueError, self.query_instruction.strip；**返回：** 未记录；**异常：** ValueError('embedding_model 不能为空'); ValueError('embedding_dimension 必须在 1 到 1024 之间'); ValueError('当前向量链路要求 normalize_embeddings=true'); ValueError('batch_size 必须大于 0'); ValueError('query_instruction 不能为空')；**副作用：** 模型/向量计算。

### `EmbeddingSettings.input_fingerprint` (function, L53-L59)

**签名：** `def input_fingerprint(self) -> str`

**作用：** 执行 input fingerprint，涉及 json.dumps.encode, hashlib.sha256.hexdigest, json.dumps, hashlib.sha256。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：str；直接/间接调用：json.dumps.encode, hashlib.sha256.hexdigest, json.dumps, hashlib.sha256；返回表达式：hashlib.sha256(encoded).hexdigest()；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Settings, input, fingerprint, json.dumps.encode, hashlib.sha256.hexdigest, json.dumps, hashlib.sha256

**调用：** json.dumps.encode, hashlib.sha256.hexdigest, json.dumps, hashlib.sha256；**返回：** hashlib.sha256(encoded).hexdigest()；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `EmbeddingBackend` (class, L62-L74)

**签名：** `class EmbeddingBackend`

**作用：** Small injectable surface used by chunking, indexing, and retrieval.

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 4 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Backend

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingBackend.model_revision` (function, L68-L68)

**签名：** `def model_revision(self) -> str`

**作用：** 执行 model revision。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：str；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Backend, model

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingBackend.embed_documents` (function, L70-L70)

**签名：** `def embed_documents(self, texts: Sequence[str]) -> np.ndarray`

**作用：** 执行 embed documents。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, texts: Sequence[str]；声明返回：np.ndarray；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Backend, embed, documents

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `EmbeddingBackend.embed_query` (function, L72-L72)

**签名：** `def embed_query(self, query: str, *, code: bool=False) -> np.ndarray`

**作用：** 执行 embed query。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, query: str, *, code: bool=False；声明返回：np.ndarray；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Backend, embed, query

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `EmbeddingBackend.token_count` (function, L74-L74)

**签名：** `def token_count(self, text: str) -> int`

**作用：** 执行 token count。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, text: str；声明返回：int；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Backend, token, count

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `content_sha256` (function, L77-L78)

**签名：** `def content_sha256(content: str) -> str`

**作用：** 执行 content sha256，涉及 hashlib.sha256.hexdigest, hashlib.sha256, content.encode。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：content: str；声明返回：str；直接/间接调用：hashlib.sha256.hexdigest, hashlib.sha256, content.encode；返回表达式：hashlib.sha256(content.encode('utf-8')).hexdigest()；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, content, sha256, hashlib.sha256.hexdigest, hashlib.sha256, content.encode

**调用：** hashlib.sha256.hexdigest, hashlib.sha256, content.encode；**返回：** hashlib.sha256(content.encode('utf-8')).hexdigest()；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `fingerprint_payload` (function, L81-L83)

**签名：** `def fingerprint_payload(payload: dict[str, object]) -> str`

**作用：** 执行 fingerprint payload，涉及 json.dumps.encode, hashlib.sha256.hexdigest, json.dumps, hashlib.sha256。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：payload: dict[str, object]；声明返回：str；直接/间接调用：json.dumps.encode, hashlib.sha256.hexdigest, json.dumps, hashlib.sha256；返回表达式：hashlib.sha256(encoded).hexdigest()；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, fingerprint, payload, json.dumps.encode, hashlib.sha256.hexdigest, json.dumps, hashlib.sha256

**调用：** json.dumps.encode, hashlib.sha256.hexdigest, json.dumps, hashlib.sha256；**返回：** hashlib.sha256(encoded).hexdigest()；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `build_document_embedding_input` (function, L86-L121)

**签名：** `def build_document_embedding_input(*, content: str, path: str, block_type: str, language: str | None=None, heading_path: tuple[str, ...]=(), symbol_path: tuple[str, ...]=(), start_line: int | None=None, end_line: int | None=None, page_number: int | None=None, record_path: str | None=None, slide_number: int | None=None) -> str`

**作用：** Build the one stable natural-text representation embedded for a chunk.

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：*, content: str, path: str, block_type: str, language: str | None=None, heading_path: tuple[str, ...]=(), symbol_path: tuple[str, ...]=(), start_line: int | None=None, end_line: int | None=None, page_number: int | None=None, record_path: str | None=None, slide_number: int | None=None；声明返回：str；直接/间接调用：Constant.join, Path.suffix.lstrip.upper, metadata.append, str, Path.suffix.lstrip, Path；返回表达式：f'{metadata_text}\n\n原文内容：\n{content}'；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, build, document, embedding, input, Constant.join, Path.suffix.lstrip.upper, metadata.append, str, Path.suffix.lstrip, Path, 条件分支

**调用：** Constant.join, Path.suffix.lstrip.upper, metadata.append, str, Path.suffix.lstrip, Path；**返回：** f'{metadata_text}\n\n原文内容：\n{content}'；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 模型/向量计算。

### `build_query_embedding_input` (function, L124-L131)

**签名：** `def build_query_embedding_input(query: str, instruction: str=DEFAULT_QUERY_INSTRUCTION) -> str`

**作用：** 构造并返回query embedding input；内部调用 query.strip, ValueError。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：query: str, instruction: str=DEFAULT_QUERY_INSTRUCTION；声明返回：str；直接/间接调用：query.strip, ValueError；返回表达式：f'Instruct: {instruction}\nQuery: {query}'；显式异常：ValueError('查询不能为空')；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, build, query, embedding, input, query.strip, ValueError, 条件分支

**调用：** query.strip, ValueError；**返回：** f'Instruct: {instruction}\nQuery: {query}'；**异常：** ValueError('查询不能为空')；**副作用：** 模型/向量计算。

### `validate_vectors` (function, L134-L155)

**签名：** `def validate_vectors(vectors: object, *, expected_count: int, dimension: int, normalized: bool) -> np.ndarray`

**作用：** Return contiguous float32 vectors after enforcing storage invariants.

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：vectors: object, *, expected_count: int, dimension: int, normalized: bool；声明返回：np.ndarray；直接/间接调用：np.asarray, np.ascontiguousarray, ValueError, np.isfinite.all, np.linalg.norm, np.allclose, np.isfinite；返回表达式：np.ascontiguousarray(array, dtype=np.float32)；显式异常：ValueError(f'Embedding dimension mismatch: expected {(expected_count, dimension)}, got {array.shape}'); ValueError('Embedding 包含 NaN 或 Inf'); ValueError('归一化 Embedding 的范数不接近 1.0')；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, validate, vectors, np.asarray, np.ascontiguousarray, ValueError, np.isfinite.all, np.linalg.norm, np.allclose, np.isfinite, 条件分支

**调用：** np.asarray, np.ascontiguousarray, ValueError, np.isfinite.all, np.linalg.norm, np.allclose, np.isfinite；**返回：** np.ascontiguousarray(array, dtype=np.float32)；**异常：** ValueError(f'Embedding dimension mismatch: expected {(expected_count, dimension)}, got {array.shape}'); ValueError('Embedding 包含 NaN 或 Inf'); ValueError('归一化 Embedding 的范数不接近 1.0')；**副作用：** 模型/向量计算。

### `RemoteEmbeddingError` (class, L158-L159)

**签名：** `class RemoteEmbeddingError`

**作用：** The SSH-forwarded embedding service could not satisfy a request.

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 0 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Error

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RemoteQwen3EmbeddingModel` (class, L162-L385)

**签名：** `class RemoteQwen3EmbeddingModel`

**作用：** Batch Qwen3 requests through an OpenAI/vLLM-compatible HTTP service.

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 9 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RemoteQwen3EmbeddingModel.__init__` (function, L165-L187)

**签名：** `def __init__(self, settings: EmbeddingSettings | None=None, *, base_url: str='http://127.0.0.1:8000', api_key: str | None=None, timeout: float=120.0, protocol: str='auto') -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, settings: EmbeddingSettings | None=None, *, base_url: str='http://127.0.0.1:8000', api_key: str | None=None, timeout: float=120.0, protocol: str='auto'；声明返回：None；直接/间接调用：base_url.strip.rstrip, EmbeddingSettings, base_url.strip, ValueError, root.endswith, os.getenv；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('embedding_base_url 不能为空'); ValueError('embedding_timeout 必须大于 0'); ValueError('embedding_protocol 必须是 auto、openai 或 simple')；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model, init, base_url.strip.rstrip, EmbeddingSettings, base_url.strip, ValueError, root.endswith, os.getenv, 条件分支

**调用：** base_url.strip.rstrip, EmbeddingSettings, base_url.strip, ValueError, root.endswith, os.getenv；**返回：** 未记录；**异常：** ValueError('embedding_base_url 不能为空'); ValueError('embedding_timeout 必须大于 0'); ValueError('embedding_protocol 必须是 auto、openai 或 simple')；**副作用：** 环境变量读取, 模型/向量计算。

### `RemoteQwen3EmbeddingModel._service_protocol` (function, L189-L204)

**签名：** `def _service_protocol(self) -> str`

**作用：** 执行  service protocol，涉及 self._request_json, openapi.get, isinstance。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：str；直接/间接调用：self._request_json, openapi.get, isinstance；返回表达式：self._resolved_protocol；显式异常：未发现显式 raise；控制流：条件分支, 异常处理。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model, service, protocol, self._request_json, openapi.get, isinstance, 条件分支, 异常处理

**调用：** self._request_json, openapi.get, isinstance；**返回：** self._resolved_protocol；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `RemoteQwen3EmbeddingModel._request_json` (function, L206-L245)

**签名：** `def _request_json(self, path: str, *, payload: dict[str, object] | None=None) -> dict[str, object]`

**作用：** 执行  request json，涉及 Request, json.dumps.encode, json.loads, isinstance, RemoteEmbeddingError。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, path: str, *, payload: dict[str, object] | None=None；声明返回：dict[str, object]；直接/间接调用：Request, json.dumps.encode, json.loads, isinstance, RemoteEmbeddingError, urlopen, response.read.decode, json.dumps, exc.read.decode, detail.replace, response.read, exc.read；返回表达式：parsed；显式异常：RemoteEmbeddingError('Embedding 服务响应必须是 JSON 对象'); RemoteEmbeddingError(f'Embedding 服务返回 HTTP {exc.code}：{detail}'); RemoteEmbeddingError(f'无法连接 Embedding 服务 {self.base_url}：{exc}'); RemoteEmbeddingError('Embedding 服务返回了无效 JSON')；控制流：条件分支, 异常处理, 上下文管理。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model, request, json, Request, json.dumps.encode, json.loads, isinstance, RemoteEmbeddingError, urlopen, response.read.decode, json.dumps, exc.read.decode, detail.replace, response.read, exc.read, 条件分支, 异常处理, 上下文管理

**调用：** Request, json.dumps.encode, json.loads, isinstance, RemoteEmbeddingError, urlopen, response.read.decode, json.dumps, exc.read.decode, detail.replace, response.read, exc.read；**返回：** parsed；**异常：** RemoteEmbeddingError('Embedding 服务响应必须是 JSON 对象'); RemoteEmbeddingError(f'Embedding 服务返回 HTTP {exc.code}：{detail}'); RemoteEmbeddingError(f'无法连接 Embedding 服务 {self.base_url}：{exc}'); RemoteEmbeddingError('Embedding 服务返回了无效 JSON')；**副作用：** 网络 HTTP 请求, 模型/向量计算。

### `RemoteQwen3EmbeddingModel.model_revision` (function, L248-L286)

**签名：** `def model_revision(self) -> str`

**作用：** 执行 model revision，涉及 payload.get, isinstance, RemoteEmbeddingError, self._request_json, str。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：str；直接/间接调用：payload.get, isinstance, RemoteEmbeddingError, self._request_json, str, re.search, self._service_protocol, item.get, match.group, revision.strip；返回表达式：self._resolved_revision；显式异常：RemoteEmbeddingError('远端 /v1/models 未提供模型 commit hash；请通过 --embedding-revision 显式传入远端实际 revision'); 裸 raise; RemoteEmbeddingError('远端 /embed 服务不报告模型 revision；请通过 --embedding-revision 或 EMBEDDING_MODEL_REVISION 传入实际 commit hash')；控制流：条件分支, 循环, 异常处理。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model, model, payload.get, isinstance, RemoteEmbeddingError, self._request_json, str, re.search, self._service_protocol, item.get, match.group, revision.strip, 条件分支, 循环, 异常处理

**调用：** payload.get, isinstance, RemoteEmbeddingError, self._request_json, str, re.search, self._service_protocol, item.get, match.group, revision.strip；**返回：** self._resolved_revision；**异常：** RemoteEmbeddingError('远端 /v1/models 未提供模型 commit hash；请通过 --embedding-revision 显式传入远端实际 revision'); 裸 raise; RemoteEmbeddingError('远端 /embed 服务不报告模型 revision；请通过 --embedding-revision 或 EMBEDDING_MODEL_REVISION 传入实际 commit hash')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `RemoteQwen3EmbeddingModel._normalize` (function, L289-L296)

**签名：** `def _normalize(vectors: object) -> np.ndarray`

**作用：** 规范化并适配内部资源；内部调用 np.asarray, np.linalg.norm。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：vectors: object；声明返回：np.ndarray；直接/间接调用：np.asarray, np.linalg.norm；返回表达式：array；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model, normalize, np.asarray, np.linalg.norm, 条件分支

**调用：** np.asarray, np.linalg.norm；**返回：** array；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `RemoteQwen3EmbeddingModel.embed_documents` (function, L298-L350)

**签名：** `def embed_documents(self, texts: Sequence[str]) -> np.ndarray`

**作用：** 执行 embed documents，涉及 self._service_protocol, range, np.vstack, validate_vectors, np.empty。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, texts: Sequence[str]；声明返回：np.ndarray；直接/间接调用：self._service_protocol, range, np.vstack, validate_vectors, np.empty, len, list, batches.append, self._request_json, response.get, sorted, all, RemoteEmbeddingError, self._normalize, item.get, isinstance, int；返回表达式：validate_vectors(combined, expected_count=len(texts), dimension=self.settings.dimension, normalized=self.settings.normalize); np.empty((0, self.settings.dimension), dtype=np.float32)；显式异常：RemoteEmbeddingError('Embedding 服务未返回 float 数组'); RemoteEmbeddingError('Embedding 服务返回的向量数量不匹配'); RemoteEmbeddingError('Embedding 服务返回了无效的向量 index')；控制流：条件分支, 循环。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model, embed, documents, self._service_protocol, range, np.vstack, validate_vectors, np.empty, len, list, batches.append, self._request_json, response.get, sorted, all, RemoteEmbeddingError, self._normalize, item.get, isinstance, int, 条件分支, 循环

**调用：** self._service_protocol, range, np.vstack, validate_vectors, np.empty, len, list, batches.append, self._request_json, response.get, sorted, all, RemoteEmbeddingError, self._normalize, item.get, isinstance, int；**返回：** validate_vectors(combined, expected_count=len(texts), dimension=self.settings.dimension, normalized=self.settings.normalize); np.empty((0, self.settings.dimension), dtype=np.float32)；**异常：** RemoteEmbeddingError('Embedding 服务未返回 float 数组'); RemoteEmbeddingError('Embedding 服务返回的向量数量不匹配'); RemoteEmbeddingError('Embedding 服务返回了无效的向量 index')；**副作用：** 模型/向量计算。

### `RemoteQwen3EmbeddingModel.embed_documents.lambda@339` (function, L339-L339)

**签名：** `lambda item`

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；这是匿名 lambda，输入参数：item；返回表达式：int(item['index'])；调用：int；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, lambda, int

**调用：** int；**返回：** int(item['index'])；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RemoteQwen3EmbeddingModel.embed_query` (function, L352-L356)

**签名：** `def embed_query(self, query: str, *, code: bool=False) -> np.ndarray`

**作用：** 执行 embed query，涉及 self.embed_documents, build_query_embedding_input。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, query: str, *, code: bool=False；声明返回：np.ndarray；直接/间接调用：self.embed_documents, build_query_embedding_input；返回表达式：self.embed_documents([build_query_embedding_input(query, instruction)])[0]；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model, embed, query, self.embed_documents, build_query_embedding_input, 条件分支

**调用：** self.embed_documents, build_query_embedding_input；**返回：** self.embed_documents([build_query_embedding_input(query, instruction)])[0]；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `RemoteQwen3EmbeddingModel.token_count` (function, L358-L378)

**签名：** `def token_count(self, text: str) -> int`

**作用：** Use vLLM's tokenizer endpoint when an exact count is required.

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, text: str；声明返回：int；直接/间接调用：RemoteEmbeddingError, self._request_json, response.get, isinstance, len, errors.append；返回表达式：count; len(tokens)；显式异常：RemoteEmbeddingError('远端服务未提供 /tokenize 或 /v1/tokenize，无法执行精确 Token 检查')；控制流：条件分支, 循环, 异常处理。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model, token, count, RemoteEmbeddingError, self._request_json, response.get, isinstance, len, errors.append, 条件分支, 循环, 异常处理

**调用：** RemoteEmbeddingError, self._request_json, response.get, isinstance, len, errors.append；**返回：** count; len(tokens)；**异常：** RemoteEmbeddingError('远端服务未提供 /tokenize 或 /v1/tokenize，无法执行精确 Token 检查')；**副作用：** 模型/向量计算。

### `RemoteQwen3EmbeddingModel.fits_token_limit` (function, L380-L385)

**签名：** `def fits_token_limit(self, text: str, max_tokens: int) -> bool`

**作用：** 执行 fits token limit，涉及 self.token_count, len, text.encode。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, text: str, max_tokens: int；声明返回：bool；直接/间接调用：self.token_count, len, text.encode；返回表达式：self.token_count(text) <= max_tokens; True；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, Remote, Model, fits, token, limit, self.token_count, len, text.encode, 条件分支

**调用：** self.token_count, len, text.encode；**返回：** self.token_count(text) <= max_tokens; True；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `cosine_similarity` (function, L388-L392)

**签名：** `def cosine_similarity(left: np.ndarray, right: np.ndarray) -> float`

**作用：** 执行 cosine similarity，涉及 float, np.linalg.norm, math.isfinite, np.dot。

**详细语义：** 所属模块职责：定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：left: np.ndarray, right: np.ndarray；声明返回：float；直接/间接调用：float, np.linalg.norm, math.isfinite, np.dot；返回表达式：float(np.dot(left, right) / denominator); 0.0；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, cosine, similarity, float, np.linalg.norm, math.isfinite, np.dot, 条件分支

**调用：** float, np.linalg.norm, math.isfinite, np.dot；**返回：** float(np.dot(left, right) / denominator); 0.0；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

## personal_local_knowledge_base_v0/knowledge_search/extractors.py

**文件作用：** 按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。

**语言/关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, Python, py

**函数/类/脚本记录数：** 7

### `_choose_text_encoding` (function, L38-L58)

**签名：** `def _choose_text_encoding(first_bytes: bytes, path: Path) -> str`

**作用：** 根据文件开头选择文本编码，避免读取完整文件才能判断编码。

**详细语义：** 所属模块职责：按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；输入参数：first_bytes: bytes, path: Path；声明返回：str；直接/间接调用：codecs.getincrementaldecoder, utf8_decoder.decode, gb_decoder.decode, logger.warning；返回表达式：'utf-8-sig'; 'gb18030'; 'utf-8'；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, choose, text, encoding, codecs.getincrementaldecoder, utf8_decoder.decode, gb_decoder.decode, logger.warning, 异常处理

**调用：** codecs.getincrementaldecoder, utf8_decoder.decode, gb_decoder.decode, logger.warning；**返回：** 'utf-8-sig'; 'gb18030'; 'utf-8'；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `_iter_text_file` (function, L61-L93)

**签名：** `def _iter_text_file(path: Path, read_size: int=DEFAULT_READ_SIZE) -> Iterator[str]`

**作用：** 以增量解码方式读取 TXT/Markdown，不把整个文件放进内存。

**详细语义：** 所属模块职责：按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；输入参数：path: Path, read_size: int=DEFAULT_READ_SIZE；声明返回：Iterator[str]；直接/间接调用：ValueError, path.open, stream.read, _choose_text_encoding, codecs.getincrementaldecoder, decoder.decode；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('read_size 必须大于 0')；控制流：条件分支, 循环, 上下文管理, 生成器 yield。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, iter, text, file, ValueError, path.open, stream.read, _choose_text_encoding, codecs.getincrementaldecoder, decoder.decode, 条件分支, 循环, 上下文管理, 生成器 yield

**调用：** ValueError, path.open, stream.read, _choose_text_encoding, codecs.getincrementaldecoder, decoder.decode；**返回：** 未记录；**异常：** ValueError('read_size 必须大于 0')；**副作用：** 文件系统读写。

### `_iter_pdf_text` (function, L96-L117)

**签名：** `def _iter_pdf_text(path: Path) -> Iterator[str]`

**作用：** 逐页抽取 PDF 文本，每次只把当前页交给下游。

**详细语义：** 所属模块职责：按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；输入参数：path: Path；声明返回：Iterator[str]；直接/间接调用：PdfReader, enumerate, str, RuntimeError, page.extract_text, logger.exception；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：RuntimeError('PDF 抽取需要 pypdf，请先安装 requirements.txt')；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, iter, pdf, text, PdfReader, enumerate, str, RuntimeError, page.extract_text, logger.exception, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** PdfReader, enumerate, str, RuntimeError, page.extract_text, logger.exception；**返回：** 未记录；**异常：** RuntimeError('PDF 抽取需要 pypdf，请先安装 requirements.txt')；**副作用：** 日志输出。

### `_extract_pptx_shape_text` (function, L120-L145)

**签名：** `def _extract_pptx_shape_text(shape, group_shape_type) -> list[str]`

**作用：** 递归抽取一个 PPTX 图形中的文本框、表格和组合图形文字。

**详细语义：** 所属模块职责：按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；输入参数：shape, group_shape_type；声明返回：list[str]；直接/间接调用：getattr, shape.text.strip, texts.append, texts.extend, cell.text.strip, _extract_pptx_shape_text, Constant.join；返回表达式：texts；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, extract, pptx, shape, text, getattr, shape.text.strip, texts.append, texts.extend, cell.text.strip, _extract_pptx_shape_text, Constant.join, 条件分支, 循环

**调用：** getattr, shape.text.strip, texts.append, texts.extend, cell.text.strip, _extract_pptx_shape_text, Constant.join；**返回：** texts；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_iter_pptx_text` (function, L148-L170)

**签名：** `def _iter_pptx_text(path: Path) -> Iterator[str]`

**作用：** 逐张幻灯片抽取 PPTX 文本框、标题、表格和组合图形文字。

**详细语义：** 所属模块职责：按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；输入参数：path: Path；声明返回：Iterator[str]；直接/间接调用：Presentation, enumerate, str, RuntimeError, slide_texts.extend, _extract_pptx_shape_text, Constant.join；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：RuntimeError('PPTX 抽取需要 python-pptx，请先安装 requirements.txt')；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, iter, pptx, text, Presentation, enumerate, str, RuntimeError, slide_texts.extend, _extract_pptx_shape_text, Constant.join, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** Presentation, enumerate, str, RuntimeError, slide_texts.extend, _extract_pptx_shape_text, Constant.join；**返回：** 未记录；**异常：** RuntimeError('PPTX 抽取需要 python-pptx，请先安装 requirements.txt')；**副作用：** 未发现明显外部副作用。

### `extract_document` (function, L173-L231)

**签名：** `def extract_document(path: Path, *, parser_fingerprint: str='') -> ExtractedDocument`

**作用：** 读取文件元数据并流式计算哈希，不在这里一次性抽取全文。

**详细语义：** 所属模块职责：按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；输入参数：path: Path, *, parser_fingerprint: str=''；声明返回：ExtractedDocument；直接/间接调用：path.expanduser.resolve, path.suffix.lower, hashlib.sha256, path.stat, parser_by_type.get, ExtractedDocument, path.is_file, FileNotFoundError, ValueError, path.open, path.expanduser, stream.read, hasher.update, hasher.hexdigest, tokenize.open, ast.parse, source.read, str；返回表达式：ExtractedDocument(path=path, file_type=suffix[1:], text=None, sha256=hasher.hexdigest(), size=stat.st_size, modified_ns=stat.st_mtime_ns, parser_fingerprint=parser_fingerprint, pa…；显式异常：FileNotFoundError(f'文件不存在：{path}'); ValueError(f'不支持的文件类型：{path.suffix or '<无扩展名>'}')；控制流：条件分支, 循环, 异常处理, 上下文管理。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, extract, document, path.expanduser.resolve, path.suffix.lower, hashlib.sha256, path.stat, parser_by_type.get, ExtractedDocument, path.is_file, FileNotFoundError, ValueError, path.open, path.expanduser, stream.read, hasher.update, hasher.hexdigest, tokenize.open, ast.parse, source.read, str, 条件分支, 循环, 异常处理, 上下文管理

**调用：** path.expanduser.resolve, path.suffix.lower, hashlib.sha256, path.stat, parser_by_type.get, ExtractedDocument, path.is_file, FileNotFoundError, ValueError, path.open, path.expanduser, stream.read, hasher.update, hasher.hexdigest, tokenize.open, ast.parse, source.read, str；**返回：** ExtractedDocument(path=path, file_type=suffix[1:], text=None, sha256=hasher.hexdigest(), size=stat.st_size, modified_ns=stat.st_mtime_ns, parser_fingerprint=parser_fingerprint, pa…；**异常：** FileNotFoundError(f'文件不存在：{path}'); ValueError(f'不支持的文件类型：{path.suffix or '<无扩展名>'}')；**副作用：** 文件系统读写。

### `iter_document_text` (function, L234-L274)

**签名：** `def iter_document_text(document: ExtractedDocument, *, read_size: int=DEFAULT_READ_SIZE, json_profile: JsonProfile | None=None, max_json_size: int=DEFAULT_MAX_JSON_SIZE, json_record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> Iterator[str]`

**作用：** 根据文档类型按块、按页或按幻灯片产生文本。

**详细语义：** 所属模块职责：按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；输入参数：document: ExtractedDocument, *, read_size: int=DEFAULT_READ_SIZE, json_profile: JsonProfile | None=None, max_json_size: int=DEFAULT_MAX_JSON_SIZE, json_record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：Iterator[str]；直接/间接调用：ValueError, _iter_text_file, _iter_pdf_text, _iter_pptx_text, iter_json_text；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError(f'不支持的文档类型：{document.file_type}'); ValueError('索引 JSON 文件必须提供 --json-config 配置文件')；控制流：条件分支, 生成器 yield。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, iter, document, text, ValueError, _iter_text_file, _iter_pdf_text, _iter_pptx_text, iter_json_text, 条件分支, 生成器 yield

**调用：** ValueError, _iter_text_file, _iter_pdf_text, _iter_pptx_text, iter_json_text；**返回：** 未记录；**异常：** ValueError(f'不支持的文档类型：{document.file_type}'); ValueError('索引 JSON 文件必须提供 --json-config 配置文件')；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/highlighting.py

**文件作用：** 把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。

**语言/关键词：** 关键词, FTS5, 转义, 高亮, Python, py

**函数/类/脚本记录数：** 4

### `query_terms` (function, L7-L20)

**签名：** `def query_terms(query: str) -> list[str]`

**作用：** 提取用于高亮的查询词，支持简单的双引号短语。

**详细语义：** 所属模块职责：把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。；输入参数：query: str；声明返回：list[str]；直接/间接调用：re.findall, query.strip, term.strip.strip, terms.append, term.strip；返回表达式：terms；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 关键词, FTS5, 转义, 高亮, query, terms, re.findall, query.strip, term.strip.strip, terms.append, term.strip, 条件分支, 循环

**调用：** re.findall, query.strip, term.strip.strip, terms.append, term.strip；**返回：** terms；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `to_fts_query` (function, L23-L31)

**签名：** `def to_fts_query(query: str) -> str`

**作用：** 将普通关键词转换成安全的 FTS5 AND 查询，避免用户输入破坏 MATCH 语法。

**详细语义：** 所属模块职责：把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。；输入参数：query: str；声明返回：str；直接/间接调用：query_terms, Constant.join, ValueError, term.replace, chr；返回表达式：' AND '.join((f'"{term.replace(chr(34), chr(34) * 2)}"' for term in terms))；显式异常：ValueError('搜索关键词不能为空')；控制流：条件分支。

**关键词：** 关键词, FTS5, 转义, 高亮, to, fts, query, query_terms, Constant.join, ValueError, term.replace, chr, 条件分支

**调用：** query_terms, Constant.join, ValueError, term.replace, chr；**返回：** ' AND '.join((f'"{term.replace(chr(34), chr(34) * 2)}"' for term in terms))；**异常：** ValueError('搜索关键词不能为空')；**副作用：** SQLite/数据库写入或查询。

### `highlight_text` (function, L34-L50)

**签名：** `def highlight_text(text: str, query: str, prefix: str='<mark>', suffix: str='</mark>') -> str`

**作用：** 高亮文本中命中的词；最长的词优先，避免短词切断长词。

**详细语义：** 所属模块职责：把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。；输入参数：text: str, query: str, prefix: str='<mark>', suffix: str='</mark>'；声明返回：str；直接/间接调用：sorted, re.compile, pattern.sub, query_terms, Constant.join, re.escape, match.group；返回表达式：pattern.sub(lambda match: f'{prefix}{match.group(0)}{suffix}', text); text；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 关键词, FTS5, 转义, 高亮, highlight, text, sorted, re.compile, pattern.sub, query_terms, Constant.join, re.escape, match.group, 条件分支

**调用：** sorted, re.compile, pattern.sub, query_terms, Constant.join, re.escape, match.group；**返回：** pattern.sub(lambda match: f'{prefix}{match.group(0)}{suffix}', text); text；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `highlight_text.lambda@50` (function, L50-L50)

**签名：** `lambda match`

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。；这是匿名 lambda，输入参数：match；返回表达式：f'{prefix}{match.group(0)}{suffix}'；调用：match.group；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 关键词, FTS5, 转义, 高亮, lambda, match.group

**调用：** match.group；**返回：** f'{prefix}{match.group(0)}{suffix}'；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/indexer.py

**文件作用：** 发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。

**语言/关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, Python, py

**函数/类/脚本记录数：** 9

### `_normalise_rule` (function, L49-L55)

**签名：** `def _normalise_rule(rule: str | Path) -> str`

**作用：** 把用户输入的目录规则转换为跨平台、可比较的形式。

**详细语义：** 所属模块职责：发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：rule: str | Path；声明返回：str；直接/间接调用：str.strip.replace, text.startswith, text.rstrip, str.strip, str；返回表达式：text.rstrip('/')；显式异常：未发现显式 raise；控制流：循环。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, normalise, rule, str.strip.replace, text.startswith, text.rstrip, str.strip, str, 循环

**调用：** str.strip.replace, text.startswith, text.rstrip, str.strip, str；**返回：** text.rstrip('/')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_matches_excluded_directory` (function, L58-L84)

**签名：** `def _matches_excluded_directory(directory: Path, root: Path, rules: tuple[str, ...], absolute_rules: tuple[Path, ...]) -> bool`

**作用：** 判断目录是否命中名称、相对路径或绝对路径规则。

**详细语义：** 所属模块职责：发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：directory: Path, root: Path, rules: tuple[str, ...], absolute_rules: tuple[Path, ...]；声明返回：bool；直接/间接调用：directory.resolve, any, directory.relative_to.as_posix, fnmatch.fnmatchcase, directory.relative_to, candidate.casefold, rule.casefold；返回表达式：any((fnmatch.fnmatchcase(candidate.casefold(), rule.casefold()) for rule in rules for candidate in candidates)); True；显式异常：未发现显式 raise；控制流：条件分支, 异常处理。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, matches, excluded, directory, directory.resolve, any, directory.relative_to.as_posix, fnmatch.fnmatchcase, directory.relative_to, candidate.casefold, rule.casefold, 条件分支, 异常处理

**调用：** directory.resolve, any, directory.relative_to.as_posix, fnmatch.fnmatchcase, directory.relative_to, candidate.casefold, rule.casefold；**返回：** any((fnmatch.fnmatchcase(candidate.casefold(), rule.casefold()) for rule in rules for candidate in candidates)); True；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `discover_files` (function, L87-L177)

**签名：** `def discover_files(inputs: Iterable[Path], *, include_json: bool=False, exclude_dirs: Iterable[str | Path] | None=None, exclude_files: Iterable[Path]=(), max_files: int | None=None) -> Iterator[Path]`

**作用：** 递归发现支持的文件，并应用排除、去重和数量上限规则。

**详细语义：** 所属模块职责：发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：inputs: Iterable[Path], *, include_json: bool=False, exclude_dirs: Iterable[str | Path] | None=None, exclude_files: Iterable[Path]=(), max_files: int | None=None；声明返回：Iterator[Path]；直接/间接调用：tuple, set, ValueError, Path.expanduser.resolve, path.resolve, seen.add, Path.expanduser, path.is_file, path.is_dir, logger.warning, _matches_excluded_directory, os.walk, Path.expanduser.is_absolute, Path, path.suffix.lower, logger.info, sorted, _normalise_rule, emit, child.is_file, child.suffix.lower；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('最大文件数不能小于 0')；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, discover, files, tuple, set, ValueError, Path.expanduser.resolve, path.resolve, seen.add, Path.expanduser, path.is_file, path.is_dir, logger.warning, _matches_excluded_directory, os.walk, Path.expanduser.is_absolute, Path, path.suffix.lower, logger.info, sorted, _normalise_rule, emit, child.is_file, child.suffix.lower, 条件分支, 循环, 生成器 yield

**调用：** tuple, set, ValueError, Path.expanduser.resolve, path.resolve, seen.add, Path.expanduser, path.is_file, path.is_dir, logger.warning, _matches_excluded_directory, os.walk, Path.expanduser.is_absolute, Path, path.suffix.lower, logger.info, sorted, _normalise_rule, emit, child.is_file, child.suffix.lower；**返回：** 未记录；**异常：** ValueError('最大文件数不能小于 0')；**副作用：** 文件系统读写, 日志输出。

### `discover_files.emit` (function, L129-L138)

**签名：** `def emit(path: Path) -> Iterator[Path]`

**作用：** 把当前解析或索引状态转换为一个可消费的记录/进度事件。

**详细语义：** 所属模块职责：发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：path: Path；声明返回：Iterator[Path]；直接/间接调用：path.resolve, seen.add；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 生成器 yield。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, discover, files, emit, path.resolve, seen.add, 条件分支, 生成器 yield

**调用：** path.resolve, seen.add；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_iter_index_chunks` (function, L180-L228)

**签名：** `def _iter_index_chunks(text_chunks: Iterable[str], *, chunk_size: int, overlap: int, separate_records: bool=False) -> Iterator[Chunk]`

**作用：** 清洗并分段；JSON record 模式下不让相邻记录合并到同一分段。

**详细语义：** 所属模块职责：发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：text_chunks: Iterable[str], *, chunk_size: int, overlap: int, separate_records: bool=False；声明返回：Iterator[Chunk]；直接/间接调用：iter, iter_clean_text, iter_chunk_text, next, record_blocks, getattr, Chunk；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, iter, index, chunks, iter_clean_text, iter_chunk_text, next, record_blocks, getattr, Chunk, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** iter, iter_clean_text, iter_chunk_text, next, record_blocks, getattr, Chunk；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_iter_index_chunks.record_blocks` (function, L205-L215)

**签名：** `def record_blocks() -> 未声明`

**作用：** 消费当前记录的块，不把超大记录拼回单个字符串。

**详细语义：** 所属模块职责：发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：；声明返回：未声明；直接/间接调用：getattr, next；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, iter, index, chunks, record, blocks, getattr, next, 条件分支, 循环, 生成器 yield

**调用：** getattr, next；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `index_paths` (function, L231-L396)

**签名：** `def index_paths(knowledge_base: KnowledgeBase, inputs: Iterable[Path], *, chunk_size: int=800, overlap: int=200, min_chunk_chars: int=200, max_chunk_chars: int=1600, semantic_merge_threshold: float=0.8, max_chunk_tokens: int=8192, embedding_backend: EmbeddingBackend | None=None, force: bool=False, json_profile: JsonProfile | None=None, exclude_dirs: Iterable[str | Path] | None=None, exclude_files: Iterable[Path]=(), max_files: int | None=None, max_json_size: int=DEFAULT_MAX_JSON_SIZE, json_record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE, progress_callback: Callable[[IndexProgress], None] | None=None) -> IndexStats`

**作用：** 执行 index paths，涉及 IndexStats, ChunkingConfig, list, len, logger.info。

**详细语义：** 所属模块职责：发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：knowledge_base: KnowledgeBase, inputs: Iterable[Path], *, chunk_size: int=800, overlap: int=200, min_chunk_chars: int=200, max_chunk_chars: int=1600, semantic_merge_threshold: float=0.8, max_chunk_tokens: int=8192, embedding_backend: EmbeddingBackend | None=None, force: bool=False, json_profile: JsonProfile | None=None, exclude_dirs: Iterable[str | Path] | None=None, exclude_files: Iterable[Path]=(), max_files: int | None=None, max_json_size: int=DEFAULT_MAX_JSON_SIZE, json_record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE, progress_callback: Callable[[IndexProgress], None] | None=None；声明返回：IndexStats；直接/间接调用：IndexStats, ChunkingConfig, list, len, logger.info, chunking_config.fingerprint_for, enumerate, ValueError, excluded_files.append, discover_files, report, min, progress_callback, extract_document, iter_document_blocks, iter_chunk_blocks, knowledge_base.replace_document, IndexProgress, logger.exception, ensure_json_size, knowledge_base.is_unchanged, counted_chunks, knowledge_base.remove_document, logger.warning；返回表达式：stats；显式异常：ValueError('JSON 最大文件大小不能小于 0'); ValueError('JSON 单条记录探测窗口必须大于 0'); ValueError('索引 JSON 文件必须提供 --json-config 配置文件')；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, index, paths, IndexStats, ChunkingConfig, list, len, logger.info, chunking_config.fingerprint_for, enumerate, ValueError, excluded_files.append, discover_files, report, min, progress_callback, extract_document, iter_document_blocks, iter_chunk_blocks, knowledge_base.replace_document, IndexProgress, logger.exception, ensure_json_size, knowledge_base.is_unchanged, counted_chunks, knowledge_base.remove_document, logger.warning, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** IndexStats, ChunkingConfig, list, len, logger.info, chunking_config.fingerprint_for, enumerate, ValueError, excluded_files.append, discover_files, report, min, progress_callback, extract_document, iter_document_blocks, iter_chunk_blocks, knowledge_base.replace_document, IndexProgress, logger.exception, ensure_json_size, knowledge_base.is_unchanged, counted_chunks, knowledge_base.remove_document, logger.warning；**返回：** stats；**异常：** ValueError('JSON 最大文件大小不能小于 0'); ValueError('JSON 单条记录探测窗口必须大于 0'); ValueError('索引 JSON 文件必须提供 --json-config 配置文件')；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 日志输出, 模型/向量计算。

### `index_paths.report` (function, L287-L301)

**签名：** `def report(current: int, path: Path, status: str) -> None`

**作用：** 向回调或日志报告当前文件的索引进度和状态。

**详细语义：** 所属模块职责：发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：current: int, path: Path, status: str；声明返回：None；直接/间接调用：progress_callback, IndexProgress, logger.exception, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 异常处理。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, index, paths, report, progress_callback, IndexProgress, logger.exception, len, 条件分支, 异常处理

**调用：** progress_callback, IndexProgress, logger.exception, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `index_paths.counted_chunks` (function, L358-L362)

**签名：** `def counted_chunks() -> 未声明`

**作用：** 包装分块迭代器并累计实际产生的分段数量。

**详细语义：** 所属模块职责：发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：；声明返回：未声明；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环, 生成器 yield。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, index, paths, counted, chunks, 循环, 生成器 yield

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/json_parser.py

**文件作用：** 实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。

**语言/关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Python, py

**函数/类/脚本记录数：** 65

### `parse_size` (function, L45-L77)

**签名：** `def parse_size(value: str | int) -> int`

**作用：** 将 ``1GB``、``512MB`` 等人类可读大小转换为字节数。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：value: str | int；声明返回：int；直接/间接调用：isinstance, _SIZE_PATTERN.fullmatch, BoolOp.upper, int, ValueError, Decimal, size.to_integral_value, match.group；返回表达式：int(size); value；显式异常：ValueError('文件大小不能是布尔值'); ValueError('文件大小必须是数字或带单位的字符串，例如 512MB'); ValueError(f'无法识别文件大小：{value!r}；示例：512MB、1GB、0'); ValueError(f'文件大小换算后不是完整字节数：{value!r}'); ValueError('文件大小不能小于 0'); ValueError(f'无法识别文件大小：{value!r}')；控制流：条件分支, 异常处理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, parse, size, isinstance, _SIZE_PATTERN.fullmatch, BoolOp.upper, int, ValueError, Decimal, size.to_integral_value, match.group, 条件分支, 异常处理

**调用：** isinstance, _SIZE_PATTERN.fullmatch, BoolOp.upper, int, ValueError, Decimal, size.to_integral_value, match.group；**返回：** int(size); value；**异常：** ValueError('文件大小不能是布尔值'); ValueError('文件大小必须是数字或带单位的字符串，例如 512MB'); ValueError(f'无法识别文件大小：{value!r}；示例：512MB、1GB、0'); ValueError(f'文件大小换算后不是完整字节数：{value!r}'); ValueError('文件大小不能小于 0'); ValueError(f'无法识别文件大小：{value!r}')；**副作用：** 未发现明显外部副作用。

### `JsonSizeLimitError` (class, L80-L81)

**签名：** `class JsonSizeLimitError`

**作用：** JSON 文件超过安全处理上限。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 0 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Size, Limit, Error

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_JsonEndOfStream` (class, L84-L85)

**签名：** `class _JsonEndOfStream`

**作用：** Internal marker used when a streaming reader reaches clean EOF.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 0 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, End, Of, Stream

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_LargeJsonRecord` (class, L88-L103)

**签名：** `class _LargeJsonRecord`

**作用：** A JSON record whose raw text must remain streamed instead of parsed.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 3 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Large, Json, Record

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_LargeJsonRecord.__init__` (function, L91-L92)

**签名：** `def __init__(self, scanner: '_RawValueScanner') -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self, scanner: '_RawValueScanner'；声明返回：None；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Large, Json, Record, init

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_LargeJsonRecord.iter_chunks` (function, L94-L100)

**签名：** `def iter_chunks(self) -> Iterator[str]`

**作用：** Yield the complete raw record in bounded text chunks.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：Iterator[str]；直接/间接调用：self.close, self._scanner.iter_large_chunks；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 生成器 yield。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Large, Json, Record, iter, chunks, self.close, self._scanner.iter_large_chunks, 异常处理, 生成器 yield

**调用：** self.close, self._scanner.iter_large_chunks；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_LargeJsonRecord.close` (function, L102-L103)

**签名：** `def close(self) -> None`

**作用：** 关闭并释放内部资源；内部调用 self._scanner.close。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：None；直接/间接调用：self._scanner.close；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Large, Json, Record, close, self._scanner.close

**调用：** self._scanner.close；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonTextBlock` (class, L106-L121)

**签名：** `class JsonTextBlock`

**作用：** Text block carrying record-boundary metadata through the pipeline.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 1 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Text, Block

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonTextBlock.__new__` (function, L109-L121)

**签名：** `def __new__(cls, text: str, *, record_start: bool, record_end: bool, record_path: str | None=None) -> 'JsonTextBlock'`

**作用：** 创建并初始化不可变值对象，同时附加结构化元数据。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：cls, text: str, *, record_start: bool, record_end: bool, record_path: str | None=None；声明返回：'JsonTextBlock'；直接/间接调用：super.__new__, super；返回表达式：value；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Text, Block, new, super.__new__, super

**调用：** super.__new__, super；**返回：** value；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonRecordTooLargeError` (class, L124-L125)

**签名：** `class JsonRecordTooLargeError`

**作用：** 记录超过探测窗口，当前操作需要完整 JSON 对象。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 0 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Record, Too, Large, Error

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_raise_large_record_for_materialized_consumer` (function, L128-L134)

**签名：** `def _raise_large_record_for_materialized_consumer(record: _LargeJsonRecord) -> None`

**作用：** 执行  raise large record for materialized consumer，涉及 record.close, JsonRecordTooLargeError。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：record: _LargeJsonRecord；声明返回：None；直接/间接调用：record.close, JsonRecordTooLargeError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：JsonRecordTooLargeError('JSON 单条记录超过探测窗口，无法执行需要完整对象的操作')；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, raise, large, record, for, materialized, consumer, record.close, JsonRecordTooLargeError

**调用：** record.close, JsonRecordTooLargeError；**返回：** 未记录；**异常：** JsonRecordTooLargeError('JSON 单条记录超过探测窗口，无法执行需要完整对象的操作')；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner` (class, L137-L320)

**签名：** `class _RawValueScanner`

**作用：** 扫描一个 JSON 值，并在超过探测窗口后转为原始文本流。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 12 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner.__init__` (function, L140-L157)

**签名：** `def __init__(self, reader: '_JsonChunkReader', probe_size: int) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self, reader: '_JsonChunkReader', probe_size: int；声明返回：None；直接/间接调用：tempfile.TemporaryFile, self.reader._active_scanners.add；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, init, tempfile.TemporaryFile, self.reader._active_scanners.add

**调用：** tempfile.TemporaryFile, self.reader._active_scanners.add；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_RawValueScanner.close` (function, L159-L162)

**签名：** `def close(self) -> None`

**作用：** 关闭并释放内部资源；内部调用 self.reader._active_scanners.discard, self.store.close。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：None；直接/间接调用：self.reader._active_scanners.discard, self.store.close；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, close, self.reader._active_scanners.discard, self.store.close, 条件分支

**调用：** self.reader._active_scanners.discard, self.store.close；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner._flush_prefix` (function, L164-L168)

**签名：** `def _flush_prefix(self) -> None`

**作用：** 把探测窗口内缓存的 JSON 前缀刷入临时文件。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：None；直接/间接调用：self.store.write, self.prefix_buffer.clear, Constant.join；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, flush, prefix, self.store.write, self.prefix_buffer.clear, Constant.join, 条件分支

**调用：** self.store.write, self.prefix_buffer.clear, Constant.join；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner._capture` (function, L170-L180)

**签名：** `def _capture(self, character: str) -> None`

**作用：** 记录流式 JSON 值的字符并在超过探测窗口时切换到临时文件。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self, character: str；声明返回：None；直接/间接调用：len, self.prefix_buffer.append, character.encode, self._flush_prefix, self.store.flush；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, capture, len, self.prefix_buffer.append, character.encode, self._flush_prefix, self.store.flush, 条件分支

**调用：** len, self.prefix_buffer.append, character.encode, self._flush_prefix, self.store.flush；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner._advance` (function, L182-L211)

**签名：** `def _advance(self, character: str) -> None`

**作用：** 推进 JSON 字符扫描状态机，处理字符串、转义和括号栈。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self, character: str；声明返回：None；直接/间接调用：self.stack.append, self.stack.pop, ValueError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError(f'JSON 记录括号不匹配：{self.reader.path}')；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, advance, self.stack.append, self.stack.pop, ValueError, 条件分支

**调用：** self.stack.append, self.stack.pop, ValueError；**返回：** 未记录；**异常：** ValueError(f'JSON 记录括号不匹配：{self.reader.path}')；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner._consume_first` (function, L213-L221)

**签名：** `def _consume_first(self) -> str`

**作用：** 读取 JSON 记录首字符并初始化标量/容器扫描模式。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：str；直接/间接调用：self.reader.skip_whitespace, self.reader.take_raw_character, self._capture, self._advance；返回表达式：first；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, consume, first, self.reader.skip_whitespace, self.reader.take_raw_character, self._capture, self._advance, 条件分支

**调用：** self.reader.skip_whitespace, self.reader.take_raw_character, self._capture, self._advance；**返回：** first；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner._consume_next` (function, L223-L227)

**签名：** `def _consume_next(self) -> str`

**作用：** 读取 JSON 记录后续字符并更新扫描状态。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：str；直接/间接调用：self.reader.take_raw_character, self._capture, self._advance；返回表达式：character；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, consume, next, self.reader.take_raw_character, self._capture, self._advance

**调用：** self.reader.take_raw_character, self._capture, self._advance；**返回：** character；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner._is_scalar_boundary` (function, L229-L240)

**签名：** `def _is_scalar_boundary(self) -> bool`

**作用：** 执行  is scalar boundary，涉及 self.reader.peek_raw_character, character.isspace。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：bool；直接/间接调用：self.reader.peek_raw_character, character.isspace；返回表达式：False; True；显式异常：未发现显式 raise；控制流：条件分支, 异常处理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, is, scalar, boundary, self.reader.peek_raw_character, character.isspace, 条件分支, 异常处理

**调用：** self.reader.peek_raw_character, character.isspace；**返回：** False; True；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner._scan_until_large_or_complete` (function, L242-L249)

**签名：** `def _scan_until_large_or_complete(self) -> None`

**作用：** 执行  scan until large or complete，涉及 self._consume_first, self._is_scalar_boundary, self._consume_next。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：None；直接/间接调用：self._consume_first, self._is_scalar_boundary, self._consume_next；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, scan, until, large, or, complete, self._consume_first, self._is_scalar_boundary, self._consume_next, 条件分支, 循环

**调用：** self._consume_first, self._is_scalar_boundary, self._consume_next；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner._load_small_value` (function, L251-L258)

**签名：** `def _load_small_value(self) -> Any`

**作用：** 加载并校验small value；内部调用 self._flush_prefix, self.store.flush, self.store.seek, json.load, self.close。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：Any；直接/间接调用：self._flush_prefix, self.store.flush, self.store.seek, json.load, self.close；返回表达式：json.load(self.store)；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, load, small, value, self._flush_prefix, self.store.flush, self.store.seek, json.load, self.close, 异常处理

**调用：** self._flush_prefix, self.store.flush, self.store.seek, json.load, self.close；**返回：** json.load(self.store)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner.iter_large_chunks` (function, L260-L312)

**签名：** `def iter_large_chunks(self) -> Iterator[str]`

**作用：** 先吐出探测窗口，再继续读取当前记录的后续文本。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：Iterator[str]；直接/间接调用：self._flush_prefix, self.store.flush, self.store.seek, Constant.join, self.output_buffer.clear, self.store.read, self._is_scalar_boundary, self.output_buffer.append, len, JsonTextBlock, self._consume_next, ValueError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError(f'JSON 超大记录缺少结束符：{self.reader.path}')；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, iter, large, chunks, self._flush_prefix, self.store.flush, self.store.seek, Constant.join, self.output_buffer.clear, self.store.read, self._is_scalar_boundary, self.output_buffer.append, len, JsonTextBlock, self._consume_next, ValueError, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** self._flush_prefix, self.store.flush, self.store.seek, Constant.join, self.output_buffer.clear, self.store.read, self._is_scalar_boundary, self.output_buffer.append, len, JsonTextBlock, self._consume_next, ValueError；**返回：** 未记录；**异常：** ValueError(f'JSON 超大记录缺少结束符：{self.reader.path}')；**副作用：** 未发现明显外部副作用。

### `_RawValueScanner.read_or_large` (function, L314-L320)

**签名：** `def read_or_large(self) -> Any | _LargeJsonRecord`

**作用：** 解析小记录，或返回延迟执行的超大记录流。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：Any | _LargeJsonRecord；直接/间接调用：self._scan_until_large_or_complete, self._load_small_value, _LargeJsonRecord；返回表达式：self._load_small_value(); _LargeJsonRecord(self)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Raw, Value, Scanner, read, or, large, self._scan_until_large_or_complete, self._load_small_value, _LargeJsonRecord, 条件分支

**调用：** self._scan_until_large_or_complete, self._load_small_value, _LargeJsonRecord；**返回：** self._load_small_value(); _LargeJsonRecord(self)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonField` (class, L324-L329)

**签名：** `class JsonField`

**作用：** 一条待写入索引的 JSON 字段规则。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 0 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Field

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonFilter` (class, L333-L338)

**签名：** `class JsonFilter`

**作用：** 一条记录过滤规则。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 0 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Filter

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonProfile` (class, L342-L432)

**签名：** `class JsonProfile`

**作用：** JSON 解析和索引配置。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 1 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Profile

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonProfile.from_file` (function, L355-L432)

**签名：** `def from_file(cls, path: Path) -> 'JsonProfile'`

**作用：** 读取并校验 JSON 配置文件。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：cls, path: Path；声明返回：'JsonProfile'；直接/间接调用：Path.expanduser.resolve, raw_config.get, _parse_path, enumerate, _parse_filters, json.dumps, hashlib.sha256.hexdigest, cls, config_path.is_file, FileNotFoundError, isinstance, ValueError, raw_field.get, fields.append, Path.expanduser, config_path.open, json.load, name.strip, record_path.strip, JsonField, hashlib.sha256, tuple, field_path.strip, canonical_config.encode；返回表达式：cls(name=name.strip(), record_path=record_path, index_mode=index_mode, fields=tuple(fields), separator=separator, filters=filters, fingerprint=fingerprint, config_path=config_path)；显式异常：FileNotFoundError(f'JSON 配置文件不存在：{config_path}'); ValueError('JSON 配置的根节点必须是对象'); ValueError('JSON 配置的 name 必须是非空字符串'); ValueError('JSON 配置的 record_path 必须是非空字符串'); ValueError('JSON 配置的 index_mode 只能是 record 或 file'); ValueError('JSON 配置的 fields 必须是非空数组'); ValueError('JSON 配置的 separator 必须是字符串'); ValueError(f'JSON 配置格式错误：{config_path}：{exc}')；控制流：条件分支, 循环, 异常处理, 上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Profile, from, file, Path.expanduser.resolve, raw_config.get, _parse_path, enumerate, _parse_filters, json.dumps, hashlib.sha256.hexdigest, cls, config_path.is_file, FileNotFoundError, isinstance, ValueError, raw_field.get, fields.append, Path.expanduser, config_path.open, json.load, name.strip, record_path.strip, JsonField, hashlib.sha256, tuple, field_path.strip, canonical_config.encode, 条件分支, 循环, 异常处理, 上下文管理

**调用：** Path.expanduser.resolve, raw_config.get, _parse_path, enumerate, _parse_filters, json.dumps, hashlib.sha256.hexdigest, cls, config_path.is_file, FileNotFoundError, isinstance, ValueError, raw_field.get, fields.append, Path.expanduser, config_path.open, json.load, name.strip, record_path.strip, JsonField, hashlib.sha256, tuple, field_path.strip, canonical_config.encode；**返回：** cls(name=name.strip(), record_path=record_path, index_mode=index_mode, fields=tuple(fields), separator=separator, filters=filters, fingerprint=fingerprint, config_path=config_path)；**异常：** FileNotFoundError(f'JSON 配置文件不存在：{config_path}'); ValueError('JSON 配置的根节点必须是对象'); ValueError('JSON 配置的 name 必须是非空字符串'); ValueError('JSON 配置的 record_path 必须是非空字符串'); ValueError('JSON 配置的 index_mode 只能是 record 或 file'); ValueError('JSON 配置的 fields 必须是非空数组'); ValueError('JSON 配置的 separator 必须是字符串'); ValueError(f'JSON 配置格式错误：{config_path}：{exc}')；**副作用：** 文件系统读写。

### `ensure_json_size` (function, L435-L452)

**签名：** `def ensure_json_size(path: Path, max_size: int=DEFAULT_MAX_JSON_SIZE) -> None`

**作用：** 在打开 JSON 前检查字节大小，避免意外处理超大数据文件。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：path: Path, max_size: int=DEFAULT_MAX_JSON_SIZE；声明返回：None；直接/间接调用：Path.expanduser.resolve, ValueError, json_path.stat, JsonSizeLimitError, Path.expanduser, Path；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('JSON 最大文件大小不能小于 0'); JsonSizeLimitError(f'JSON 文件超过大小上限：{json_path}（{size} 字节 > {max_size} 字节）')；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, ensure, json, size, Path.expanduser.resolve, ValueError, json_path.stat, JsonSizeLimitError, Path.expanduser, Path, 条件分支

**调用：** Path.expanduser.resolve, ValueError, json_path.stat, JsonSizeLimitError, Path.expanduser, Path；**返回：** 未记录；**异常：** ValueError('JSON 最大文件大小不能小于 0'); JsonSizeLimitError(f'JSON 文件超过大小上限：{json_path}（{size} 字节 > {max_size} 字节）')；**副作用：** 文件系统读写。

### `_parse_filters` (function, L455-L485)

**签名：** `def _parse_filters(raw_filter: Any) -> tuple[JsonFilter, ...]`

**作用：** 解析并转换filters；内部调用 enumerate, tuple, isinstance, item.get, _parse_path。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：raw_filter: Any；声明返回：tuple[JsonFilter, ...]；直接/间接调用：enumerate, tuple, isinstance, item.get, _parse_path, filters.append, ValueError, len, JsonFilter, path.strip；返回表达式：tuple(filters); ()；显式异常：ValueError(f'filter[{position}] 必须是对象'); ValueError(f'filter[{position}].path 必须是非空字符串'); ValueError(f'filter[{position}] 必须且只能设置一个条件：equals、not_equals、in 或 exists'); ValueError(f'filter[{position}].in 必须是非空数组'); ValueError(f'filter[{position}].exists 必须是布尔值')；控制流：条件分支, 循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, parse, filters, enumerate, tuple, isinstance, item.get, _parse_path, filters.append, ValueError, len, JsonFilter, path.strip, 条件分支, 循环

**调用：** enumerate, tuple, isinstance, item.get, _parse_path, filters.append, ValueError, len, JsonFilter, path.strip；**返回：** tuple(filters); ()；**异常：** ValueError(f'filter[{position}] 必须是对象'); ValueError(f'filter[{position}].path 必须是非空字符串'); ValueError(f'filter[{position}] 必须且只能设置一个条件：equals、not_equals、in 或 exists'); ValueError(f'filter[{position}].in 必须是非空数组'); ValueError(f'filter[{position}].exists 必须是布尔值')；**副作用：** 文件系统读写。

### `_parse_path` (function, L488-L521)

**签名：** `def _parse_path(path: str) -> tuple[str | int, ...]`

**作用：** 解析一个有限 JSONPath，支持点号字段和 [*]/[数字]。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：path: str；声明返回：tuple[str | int, ...]；直接/间接调用：path.strip, path.startswith, tuple, len, _PATH_TOKEN.match, match.groups, match.end, ValueError, tokens.append, int；返回表达式：tuple(tokens); ()；显式异常：ValueError(f'不支持的 JSON 路径：{path}'); ValueError('JSON 路径不能以 . 结尾')；控制流：条件分支, 循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, parse, path, path.strip, path.startswith, tuple, len, _PATH_TOKEN.match, match.groups, match.end, ValueError, tokens.append, int, 条件分支, 循环

**调用：** path.strip, path.startswith, tuple, len, _PATH_TOKEN.match, match.groups, match.end, ValueError, tokens.append, int；**返回：** tuple(tokens); ()；**异常：** ValueError(f'不支持的 JSON 路径：{path}'); ValueError('JSON 路径不能以 . 结尾')；**副作用：** 文件系统读写。

### `_resolve` (function, L524-L546)

**签名：** `def _resolve(value: Any, path: str) -> list[Any]`

**作用：** 从 value 中读取路径对应的所有值。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：value: Any, path: str；声明返回：list[Any]；直接/间接调用：_parse_path, isinstance, next_values.append, next_values.extend, len, current.values；返回表达式：values；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, resolve, _parse_path, isinstance, next_values.append, next_values.extend, len, current.values, 条件分支, 循环

**调用：** _parse_path, isinstance, next_values.append, next_values.extend, len, current.values；**返回：** values；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_scalar_text` (function, L549-L562)

**签名：** `def _scalar_text(value: Any, join: str) -> str`

**作用：** 把 JSON 标量、数组或对象规范化为可检索字符串。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：value: Any, join: str；声明返回：str；直接/间接调用：isinstance, str, json.dumps, join.join, _scalar_text；返回表达式：str(value); ''; 'true' if value else 'false'; json.dumps(value, ensure_ascii=False, sort_keys=True); join.join((text for item in value if (text := _scalar_text(item, join))))；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, scalar, text, isinstance, str, json.dumps, join.join, _scalar_text, 条件分支

**调用：** isinstance, str, json.dumps, join.join, _scalar_text；**返回：** str(value); ''; 'true' if value else 'false'; json.dumps(value, ensure_ascii=False, sort_keys=True); join.join((text for item in value if (text := _scalar_text(item, join))))；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_field_text` (function, L565-L575)

**签名：** `def _field_text(record: Any, field: JsonField, root: Any) -> str`

**作用：** 从 JSON 记录抽取配置字段并拼接成可索引文本。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：record: Any, field: JsonField, root: Any；声明返回：str；直接/间接调用：_resolve, field.join.join, field.path.strip.startswith, field.path.strip, _scalar_text；返回表达式：text; f'{field.name}: {text}'；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, field, text, _resolve, field.join.join, field.path.strip.startswith, field.path.strip, _scalar_text, 条件分支

**调用：** _resolve, field.join.join, field.path.strip.startswith, field.path.strip, _scalar_text；**返回：** text; f'{field.name}: {text}'；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_matches_filter` (function, L578-L587)

**签名：** `def _matches_filter(record: Any, rule: JsonFilter, root: Any) -> bool`

**作用：** 按 equals/not_equals/in/exists 规则判断记录是否保留。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：record: Any, rule: JsonFilter, root: Any；声明返回：bool；直接/间接调用：_resolve, any, rule.path.strip.startswith, bool, all, rule.path.strip；返回表达式：any((value in rule.expected for value in values)); bool(values) is rule.expected; any((value == rule.expected for value in values)); bool(values) and all((value != rule.expected for value in values))；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, matches, filter, _resolve, any, rule.path.strip.startswith, bool, all, rule.path.strip, 条件分支

**调用：** _resolve, any, rule.path.strip.startswith, bool, all, rule.path.strip；**返回：** any((value in rule.expected for value in values)); bool(values) is rule.expected; any((value == rule.expected for value in values)); bool(values) and all((value != rule.expected for value in values))；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_format_record` (function, L590-L596)

**签名：** `def _format_record(record: Any, profile: JsonProfile, root: Any) -> str`

**作用：** 执行  format record，涉及 profile.separator.join, _field_text。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：record: Any, profile: JsonProfile, root: Any；声明返回：str；直接/间接调用：profile.separator.join, _field_text；返回表达式：profile.separator.join(field_texts)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, format, record, profile.separator.join, _field_text

**调用：** profile.separator.join, _field_text；**返回：** profile.separator.join(field_texts)；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_JsonChunkReader` (class, L599-L784)

**签名：** `class _JsonChunkReader`

**作用：** Read JSON syntax from a bounded text buffer.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 14 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.__init__` (function, L607-L619)

**签名：** `def __init__(self, path: Path, read_size: int) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self, path: Path, read_size: int；声明返回：None；直接/间接调用：Path, self.path.open, json.JSONDecoder, set, ValueError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('JSON read_size 必须大于 0')；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, init, Path, self.path.open, json.JSONDecoder, set, ValueError, 条件分支

**调用：** Path, self.path.open, json.JSONDecoder, set, ValueError；**返回：** 未记录；**异常：** ValueError('JSON read_size 必须大于 0')；**副作用：** 文件系统读写。

### `_JsonChunkReader.close` (function, L621-L624)

**签名：** `def close(self) -> None`

**作用：** 关闭并释放内部资源；内部调用 tuple, self.stream.close, scanner.close。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：None；直接/间接调用：tuple, self.stream.close, scanner.close；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, close, tuple, self.stream.close, scanner.close, 循环

**调用：** tuple, self.stream.close, scanner.close；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader._fill` (function, L626-L634)

**签名：** `def _fill(self) -> bool`

**作用：** 执行  fill，涉及 self.stream.read。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：bool；直接/间接调用：self.stream.read；返回表达式：True; False；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, fill, self.stream.read, 条件分支

**调用：** self.stream.read；**返回：** True; False；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader._compact` (function, L636-L641)

**签名：** `def _compact(self) -> None`

**作用：** 执行  compact。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：None；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, compact, 条件分支

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.skip_whitespace` (function, L643-L650)

**签名：** `def skip_whitespace(self) -> bool`

**作用：** 跳过当前输入中的空白字符并报告是否仍有数据。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：bool；直接/间接调用：Subscript.isspace, len, self._fill；返回表达式：True; False；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, skip, whitespace, Subscript.isspace, len, self._fill, 条件分支, 循环

**调用：** Subscript.isspace, len, self._fill；**返回：** True; False；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.peek` (function, L652-L655)

**签名：** `def peek(self) -> str`

**作用：** 查看流式读取器的下一个字符但不消费它。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：str；直接/间接调用：self.skip_whitespace；返回表达式：self.buffer[self.position]；显式异常：_JsonEndOfStream；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, peek, self.skip_whitespace, 条件分支

**调用：** self.skip_whitespace；**返回：** self.buffer[self.position]；**异常：** _JsonEndOfStream；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.take` (function, L657-L663)

**签名：** `def take(self) -> str`

**作用：** 消费并返回流式读取器的下一个字符。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：str；直接/间接调用：self._compact, self.skip_whitespace；返回表达式：character；显式异常：_JsonEndOfStream；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, take, self._compact, self.skip_whitespace, 条件分支

**调用：** self._compact, self.skip_whitespace；**返回：** character；**异常：** _JsonEndOfStream；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.peek_raw_character` (function, L665-L670)

**签名：** `def peek_raw_character(self) -> str`

**作用：** 查看下一个字符，但不跳过 JSON 值内部的空白。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：str；直接/间接调用：len, self._fill；返回表达式：self.buffer[self.position]；显式异常：_JsonEndOfStream；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, peek, raw, character, len, self._fill, 条件分支

**调用：** len, self._fill；**返回：** self.buffer[self.position]；**异常：** _JsonEndOfStream；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.take_raw_character` (function, L672-L678)

**签名：** `def take_raw_character(self) -> str`

**作用：** 消费下一个字符，但不跳过 JSON 值内部的空白。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：str；直接/间接调用：self.peek_raw_character, self._compact；返回表达式：character；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, take, raw, character, self.peek_raw_character, self._compact

**调用：** self.peek_raw_character, self._compact；**返回：** character；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.expect` (function, L680-L687)

**签名：** `def expect(self, expected: str) -> None`

**作用：** Consume one syntax character and validate it.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self, expected: str；声明返回：None；直接/间接调用：self.take, ValueError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError(f'JSON 语法错误：期望 {expected!r}，实际为 {actual!r}：{self.path}')；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, expect, self.take, ValueError, 条件分支

**调用：** self.take, ValueError；**返回：** 未记录；**异常：** ValueError(f'JSON 语法错误：期望 {expected!r}，实际为 {actual!r}：{self.path}')；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.skip_string` (function, L689-L708)

**签名：** `def skip_string(self) -> None`

**作用：** 跳过字符串值，不把无关的大字符串读入内存。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：None；直接/间接调用：self.expect, self._compact, ValueError, len, self._fill, ord；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError(f'JSON 字符串缺少结束引号：{self.path}'); ValueError(f'JSON 字符串包含未转义控制字符：{self.path}')；控制流：条件分支, 循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, skip, string, self.expect, self._compact, ValueError, len, self._fill, ord, 条件分支, 循环

**调用：** self.expect, self._compact, ValueError, len, self._fill, ord；**返回：** 未记录；**异常：** ValueError(f'JSON 字符串缺少结束引号：{self.path}'); ValueError(f'JSON 字符串包含未转义控制字符：{self.path}')；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.skip_value` (function, L710-L750)

**签名：** `def skip_value(self) -> None`

**作用：** 递归跳过一个 JSON 值，保留近似读取块大小的缓存。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：None；直接/间接调用：self.peek, self.read_value, self.skip_string, self.take, self.expect, self.skip_value, ValueError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError(f'JSON 对象键必须是字符串：{self.path}'); ValueError(f'JSON 对象缺少逗号或结束符：{self.path}'); ValueError(f'JSON 对象不允许尾逗号：{self.path}'); ValueError(f'JSON 数组缺少逗号或结束符：{self.path}'); ValueError(f'JSON 数组不允许尾逗号：{self.path}')；控制流：条件分支, 循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, skip, value, self.peek, self.read_value, self.skip_string, self.take, self.expect, self.skip_value, ValueError, 条件分支, 循环

**调用：** self.peek, self.read_value, self.skip_string, self.take, self.expect, self.skip_value, ValueError；**返回：** 未记录；**异常：** ValueError(f'JSON 对象键必须是字符串：{self.path}'); ValueError(f'JSON 对象缺少逗号或结束符：{self.path}'); ValueError(f'JSON 对象不允许尾逗号：{self.path}'); ValueError(f'JSON 数组缺少逗号或结束符：{self.path}'); ValueError(f'JSON 数组不允许尾逗号：{self.path}')；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.read_value` (function, L752-L764)

**签名：** `def read_value(self) -> Any`

**作用：** 执行 read value，涉及 self._compact, self.skip_whitespace, self.decoder.raw_decode, self._fill。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：Any；直接/间接调用：self._compact, self.skip_whitespace, self.decoder.raw_decode, self._fill；返回表达式：value；显式异常：_JsonEndOfStream; 裸 raise；控制流：条件分支, 循环, 异常处理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, read, value, self._compact, self.skip_whitespace, self.decoder.raw_decode, self._fill, 条件分支, 循环, 异常处理

**调用：** self._compact, self.skip_whitespace, self.decoder.raw_decode, self._fill；**返回：** value；**异常：** _JsonEndOfStream; 裸 raise；**副作用：** 未发现明显外部副作用。

### `_JsonChunkReader.read_value_streaming` (function, L766-L784)

**签名：** `def read_value_streaming(self, probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> Any | _LargeJsonRecord`

**作用：** 读取一个值；过大时切换为原始记录分块流。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self, probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：Any | _LargeJsonRecord；直接/间接调用：_RawValueScanner, ValueError, scanner.read_or_large, scanner.close；返回表达式：scanner.read_or_large()；显式异常：ValueError('JSON record_probe_size 必须大于 0'); 裸 raise；控制流：条件分支, 异常处理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Chunk, Reader, read, value, streaming, _RawValueScanner, ValueError, scanner.read_or_large, scanner.close, 条件分支, 异常处理

**调用：** _RawValueScanner, ValueError, scanner.read_or_large, scanner.close；**返回：** scanner.read_or_large()；**异常：** ValueError('JSON record_probe_size 必须大于 0'); 裸 raise；**副作用：** 未发现明显外部副作用。

### `_iter_json_values` (function, L787-L806)

**签名：** `def _iter_json_values(path: Path, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> Iterator[Any | _LargeJsonRecord]`

**作用：** Yield top-level JSON values without loading the complete file.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：path: Path, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：Iterator[Any | _LargeJsonRecord]；直接/间接调用：_iter_streamed_records；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：生成器 yield。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, iter, json, values, _iter_streamed_records, 生成器 yield

**调用：** _iter_streamed_records；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_iter_values_at_path` (function, L809-L881)

**签名：** `def _iter_values_at_path(reader: _JsonChunkReader, tokens: tuple[str | int, ...], *, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> Iterator[Any | _LargeJsonRecord]`

**作用：** 从当前位置导航到 JSONPath，并只 materialize 命中的值。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：reader: _JsonChunkReader, tokens: tuple[str | int, ...], *, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：Iterator[Any | _LargeJsonRecord]；直接/间接调用：reader.peek, reader.skip_value, ValueError, isinstance, reader.take, reader.read_value_streaming, reader.read_value, reader.expect, _iter_values_at_path；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError(f'JSON 路径无法匹配容器：{reader.path}'); ValueError(f'JSON 对象键必须是字符串：{reader.path}'); ValueError(f'JSON 对象缺少逗号或结束符：{reader.path}'); ValueError(f'JSON 对象不允许尾逗号：{reader.path}'); ValueError(f'JSON 数组缺少逗号或结束符：{reader.path}'); ValueError(f'JSON 数组不允许尾逗号：{reader.path}')；控制流：条件分支, 循环, 生成器 yield。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, iter, values, at, path, reader.peek, reader.skip_value, ValueError, isinstance, reader.take, reader.read_value_streaming, reader.read_value, reader.expect, _iter_values_at_path, 条件分支, 循环, 生成器 yield

**调用：** reader.peek, reader.skip_value, ValueError, isinstance, reader.take, reader.read_value_streaming, reader.read_value, reader.expect, _iter_values_at_path；**返回：** 未记录；**异常：** ValueError(f'JSON 路径无法匹配容器：{reader.path}'); ValueError(f'JSON 对象键必须是字符串：{reader.path}'); ValueError(f'JSON 对象缺少逗号或结束符：{reader.path}'); ValueError(f'JSON 对象不允许尾逗号：{reader.path}'); ValueError(f'JSON 数组缺少逗号或结束符：{reader.path}'); ValueError(f'JSON 数组不允许尾逗号：{reader.path}')；**副作用：** 未发现明显外部副作用。

### `_iter_streamed_records` (function, L884-L949)

**签名：** `def _iter_streamed_records(path: Path, record_path: str, *, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> Iterator[Any | _LargeJsonRecord]`

**作用：** 按配置路径逐条读取记录，不先解析完整顶层对象。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：path: Path, record_path: str, *, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：Iterator[Any | _LargeJsonRecord]；直接/间接调用：Path.expanduser.resolve, ensure_json_size, _JsonChunkReader, _parse_path, reader.close, Path.expanduser, reader.peek, reader.take, reader.skip_whitespace, ValueError, Path, _iter_values_at_path, reader.read_value_streaming；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError(f'JSON 记录缺少结束符：{path}'); ValueError(f'JSON 文件格式错误：{path}：{exc}'); ValueError(f'JSON 文件不是有效的 UTF-8：{path}：{exc}'); ValueError(f'JSON 文件存在多余内容：{path}'); ValueError(f'JSON 数组缺少逗号或结束符：{path}'); ValueError(f'JSON 数组不允许尾逗号：{path}')；控制流：条件分支, 循环, 异常处理, 生成器 yield。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, iter, streamed, records, Path.expanduser.resolve, ensure_json_size, _JsonChunkReader, _parse_path, reader.close, Path.expanduser, reader.peek, reader.take, reader.skip_whitespace, ValueError, Path, _iter_values_at_path, reader.read_value_streaming, 条件分支, 循环, 异常处理, 生成器 yield

**调用：** Path.expanduser.resolve, ensure_json_size, _JsonChunkReader, _parse_path, reader.close, Path.expanduser, reader.peek, reader.take, reader.skip_whitespace, ValueError, Path, _iter_values_at_path, reader.read_value_streaming；**返回：** 未记录；**异常：** ValueError(f'JSON 记录缺少结束符：{path}'); ValueError(f'JSON 文件格式错误：{path}：{exc}'); ValueError(f'JSON 文件不是有效的 UTF-8：{path}：{exc}'); ValueError(f'JSON 文件存在多余内容：{path}'); ValueError(f'JSON 数组缺少逗号或结束符：{path}'); ValueError(f'JSON 数组不允许尾逗号：{path}')；**副作用：** 文件系统读写。

### `_iter_formatted_records` (function, L952-L1007)

**签名：** `def _iter_formatted_records(path: Path, profile: JsonProfile, *, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE, allow_large_records: bool=True) -> Iterator[str | JsonTextBlock]`

**作用：** Yield configured records one by one without materializing the root object.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：path: Path, profile: JsonProfile, *, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE, allow_large_records: bool=True；声明返回：Iterator[str | JsonTextBlock]；直接/间接调用：_iter_streamed_records, enumerate, any, _record_locator, isinstance, _format_record, profile.record_path.strip, ValueError, logger.warning, record.iter_chunks, all, field.path.strip.startswith, rule.path.strip.startswith, _raise_large_record_for_materialized_consumer, JsonTextBlock, _matches_filter, field.path.strip, rule.path.strip, str, getattr；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('record_path 不是 $ 时，fields/filter 不能使用以 $ 开头的根节点路径')；控制流：条件分支, 循环, 生成器 yield。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, iter, formatted, records, _iter_streamed_records, enumerate, any, _record_locator, isinstance, _format_record, profile.record_path.strip, ValueError, logger.warning, record.iter_chunks, all, field.path.strip.startswith, rule.path.strip.startswith, _raise_large_record_for_materialized_consumer, JsonTextBlock, _matches_filter, field.path.strip, rule.path.strip, str, getattr, 条件分支, 循环, 生成器 yield

**调用：** _iter_streamed_records, enumerate, any, _record_locator, isinstance, _format_record, profile.record_path.strip, ValueError, logger.warning, record.iter_chunks, all, field.path.strip.startswith, rule.path.strip.startswith, _raise_large_record_for_materialized_consumer, JsonTextBlock, _matches_filter, field.path.strip, rule.path.strip, str, getattr；**返回：** 未记录；**异常：** ValueError('record_path 不是 $ 时，fields/filter 不能使用以 $ 开头的根节点路径')；**副作用：** 文件系统读写, 日志输出。

### `_record_locator` (function, L1010-L1019)

**签名：** `def _record_locator(configured_path: str, record_number: int) -> str`

**作用：** Convert a configured wildcard path to a concrete citation locator.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：configured_path: str, record_number: int；声明返回：str；直接/间接调用：configured_path.strip, locator.removeprefix.removeprefix, locator.replace, locator.removeprefix；返回表达式：locator or '$'; f'$[{record_number}]'; locator.replace('[*]', f'[{record_number}]', 1)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, record, locator, configured_path.strip, locator.removeprefix.removeprefix, locator.replace, locator.removeprefix, 条件分支

**调用：** configured_path.strip, locator.removeprefix.removeprefix, locator.replace, locator.removeprefix；**返回：** locator or '$'; f'$[{record_number}]'; locator.replace('[*]', f'[{record_number}]', 1)；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `iter_json_record_text` (function, L1022-L1038)

**签名：** `def iter_json_record_text(path: Path, profile: JsonProfile, *, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> Iterator[JsonTextBlock]`

**作用：** Stream formatted records with explicit boundaries and source paths.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：path: Path, profile: JsonProfile, *, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：Iterator[JsonTextBlock]；直接/间接调用：_iter_formatted_records；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：生成器 yield。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, iter, json, record, text, _iter_formatted_records, 生成器 yield

**调用：** _iter_formatted_records；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `iter_json_text` (function, L1041-L1071)

**签名：** `def iter_json_text(path: Path, profile: JsonProfile, *, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> Iterator[str]`

**作用：** 按配置产生 JSON 文本；整个文件不会一次性载入内存。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：path: Path, profile: JsonProfile, *, read_size: int=DEFAULT_JSON_READ_SIZE, max_size: int=DEFAULT_MAX_JSON_SIZE, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：Iterator[str]；直接/间接调用：_iter_formatted_records, getattr；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, iter, json, text, _iter_formatted_records, getattr, 条件分支, 循环, 生成器 yield

**调用：** _iter_formatted_records, getattr；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonStructureEntry` (class, L1075-L1080)

**签名：** `class JsonStructureEntry`

**作用：** One path in a JSON structure summary.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 0 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Structure, Entry

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonStructureReport` (class, L1084-L1090)

**签名：** `class JsonStructureReport`

**作用：** Bounded-memory report returned by :func:`inspect_json_structure`.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 0 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, Json, Structure, Report

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_json_type` (function, L1093-L1108)

**签名：** `def _json_type(value: Any) -> str`

**作用：** 执行  json type，涉及 isinstance, type。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：value: Any；声明返回：str；直接/间接调用：isinstance, type；返回表达式：type(value).__name__; 'null'; 'boolean'; 'integer'; 'number'; 'string'; 'array'; 'object'；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, json, type, isinstance, 条件分支

**调用：** isinstance, type；**返回：** type(value).__name__; 'null'; 'boolean'; 'integer'; 'number'; 'string'; 'array'; 'object'；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_child_path` (function, L1111-L1118)

**签名：** `def _child_path(parent: str, key: str | int) -> str`

**作用：** 执行  child path，涉及 isinstance, _IDENTIFIER.fullmatch, json.dumps。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：parent: str, key: str | int；声明返回：str；直接/间接调用：isinstance, _IDENTIFIER.fullmatch, json.dumps；返回表达式：f'{parent}[{json.dumps(key, ensure_ascii=False)}]'; f'{parent}[*]'; f'{parent}[{key}]'; f'{parent}.{key}'；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, child, path, isinstance, _IDENTIFIER.fullmatch, json.dumps, 条件分支

**调用：** isinstance, _IDENTIFIER.fullmatch, json.dumps；**返回：** f'{parent}[{json.dumps(key, ensure_ascii=False)}]'; f'{parent}[*]'; f'{parent}[{key}]'; f'{parent}.{key}'；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `inspect_json_structure` (function, L1121-L1206)

**签名：** `def inspect_json_structure(path: Path, *, max_records: int=100, read_size: int=DEFAULT_JSON_READ_SIZE, max_depth: int=20, max_paths: int=10000, max_size: int=0, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> JsonStructureReport`

**作用：** Scan JSON Lines/array records and return paths, types and counts.

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：path: Path, *, max_records: int=100, read_size: int=DEFAULT_JSON_READ_SIZE, max_depth: int=20, max_paths: int=10000, max_size: int=0, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：JsonStructureReport；直接/间接调用：Path.expanduser.resolve, iter, tuple, JsonStructureReport, ValueError, entries.setdefault, isinstance, _iter_json_values, visit, Path.expanduser, _json_type, value.items, next, value.close, JsonRecordTooLargeError, JsonStructureEntry, len, Counter, sorted, Path, _child_path, entries.items, type_counts.items；返回表达式：JsonStructureReport(path=path, records_scanned=records_scanned, complete=not truncated, entries=structure_entries)；显式异常：ValueError('max_records 不能小于 0'); ValueError('max_depth 不能小于 0'); ValueError('max_paths 必须大于 0'); JsonRecordTooLargeError(f'JSON 单条记录超过结构扫描可解析大小：{path}（{record_probe_size} 字节）')；控制流：条件分支, 循环, 异常处理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, inspect, json, structure, Path.expanduser.resolve, iter, tuple, JsonStructureReport, ValueError, entries.setdefault, isinstance, _iter_json_values, visit, Path.expanduser, _json_type, value.items, next, value.close, JsonRecordTooLargeError, JsonStructureEntry, len, Counter, sorted, Path, _child_path, entries.items, type_counts.items, 条件分支, 循环, 异常处理

**调用：** Path.expanduser.resolve, iter, tuple, JsonStructureReport, ValueError, entries.setdefault, isinstance, _iter_json_values, visit, Path.expanduser, _json_type, value.items, next, value.close, JsonRecordTooLargeError, JsonStructureEntry, len, Counter, sorted, Path, _child_path, entries.items, type_counts.items；**返回：** JsonStructureReport(path=path, records_scanned=records_scanned, complete=not truncated, entries=structure_entries)；**异常：** ValueError('max_records 不能小于 0'); ValueError('max_depth 不能小于 0'); ValueError('max_paths 必须大于 0'); JsonRecordTooLargeError(f'JSON 单条记录超过结构扫描可解析大小：{path}（{record_probe_size} 字节）')；**副作用：** 文件系统读写。

### `inspect_json_structure.visit` (function, L1151-L1164)

**签名：** `def visit(value: Any, current_path: str, depth: int) -> None`

**作用：** 执行 visit，涉及 entries.setdefault, isinstance, _json_type, value.items, len。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：value: Any, current_path: str, depth: int；声明返回：None；直接/间接调用：entries.setdefault, isinstance, _json_type, value.items, len, Counter, visit, _child_path；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, inspect, json, structure, visit, entries.setdefault, isinstance, _json_type, value.items, len, Counter, _child_path, 条件分支, 循环

**调用：** entries.setdefault, isinstance, _json_type, value.items, len, Counter, visit, _child_path；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `parse_json_preview` (function, L1209-L1234)

**签名：** `def parse_json_preview(path: Path, profile: JsonProfile, limit: int, *, max_size: int=0, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE) -> list[str]`

**作用：** 返回供 CLI 预览的已格式化记录。

**详细语义：** 所属模块职责：实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：path: Path, profile: JsonProfile, limit: int, *, max_size: int=0, record_probe_size: int=DEFAULT_JSON_RECORD_PROBE_SIZE；声明返回：list[str]；直接/间接调用：_iter_formatted_records, ValueError, records.append, len, profile.separator.join；返回表达式：records; [profile.separator.join(records)] if records else []；显式异常：ValueError('preview limit 必须大于 0')；控制流：条件分支, 循环。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, parse, json, preview, _iter_formatted_records, ValueError, records.append, len, profile.separator.join, 条件分支, 循环

**调用：** _iter_formatted_records, ValueError, records.append, len, profile.separator.join；**返回：** records; [profile.separator.join(records)] if records else []；**异常：** ValueError('preview limit 必须大于 0')；**副作用：** 文件系统读写。

## personal_local_knowledge_base_v0/knowledge_search/logging_config.py

**文件作用：** 配置控制台与文件日志格式、级别和 UTF-8 输出。

**语言/关键词：** 日志, 脱敏边界, 文件日志, Python, py

**函数/类/脚本记录数：** 1

### `configure_logging` (function, L10-L27)

**签名：** `def configure_logging(level: str='INFO', log_file: Path | None=None) -> None`

**作用：** 执行 configure logging，涉及 logging.basicConfig, logging.StreamHandler, log_file.parent.mkdir, handlers.append, logging.FileHandler。

**详细语义：** 所属模块职责：配置控制台与文件日志格式、级别和 UTF-8 输出。；输入参数：level: str='INFO', log_file: Path | None=None；声明返回：None；直接/间接调用：logging.basicConfig, logging.StreamHandler, log_file.parent.mkdir, handlers.append, logging.FileHandler, getattr, level.upper；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 日志, 脱敏边界, 文件日志, configure, logging, logging.basicConfig, logging.StreamHandler, log_file.parent.mkdir, handlers.append, logging.FileHandler, getattr, level.upper, 条件分支

**调用：** logging.basicConfig, logging.StreamHandler, log_file.parent.mkdir, handlers.append, logging.FileHandler, getattr, level.upper；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 日志输出。

## personal_local_knowledge_base_v0/knowledge_search/models.py

**文件作用：** 定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。

**语言/关键词：** 数据模型, dataclass, 数据契约, Python, py

**函数/类/脚本记录数：** 10

### `ExtractedDocument` (class, L8-L26)

**签名：** `class ExtractedDocument`

**作用：** 已从文件中读取出的原始文档及其文件元数据。

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；类体包含 0 个直接方法。

**关键词：** 数据模型, dataclass, 数据契约, Extracted, Document

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DocumentBlock` (class, L30-L52)

**签名：** `class DocumentBlock`

**作用：** 文件抽取与正式长度分块之间的统一结构块。

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；类体包含 0 个直接方法。

**关键词：** 数据模型, dataclass, 数据契约, Document, Block

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `Chunk` (class, L56-L88)

**签名：** `class Chunk`

**作用：** 文档被切分后的一个可检索片段。

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；类体包含 1 个直接方法。

**关键词：** 数据模型, dataclass, 数据契约, Chunk

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `Chunk.canonical_content` (function, L87-L88)

**签名：** `def canonical_content(self) -> str`

**作用：** 执行 canonical content。

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；输入参数：self；声明返回：str；直接/间接调用：无明显函数调用；返回表达式：self.content；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据模型, dataclass, 数据契约, Chunk, canonical, content

**调用：** 无明显调用；**返回：** self.content；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `SearchResult` (class, L92-L128)

**签名：** `class SearchResult`

**作用：** A search hit; BM25 is lower-better, vector similarity is higher-better.

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；类体包含 0 个直接方法。

**关键词：** 数据模型, dataclass, 数据契约, Search, Result

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DocumentInfo` (class, L132-L143)

**签名：** `class DocumentInfo`

**作用：** 已索引文档及其可管理的统计信息。

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；类体包含 0 个直接方法。

**关键词：** 数据模型, dataclass, 数据契约, Document, Info

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatabaseHealth` (class, L147-L160)

**签名：** `class DatabaseHealth`

**作用：** 数据库一致性检查结果。

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；类体包含 1 个直接方法。

**关键词：** 数据模型, dataclass, 数据契约, Database, Health

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatabaseHealth.healthy` (function, L159-L160)

**签名：** `def healthy(self) -> bool`

**作用：** 执行 healthy。

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；输入参数：self；声明返回：bool；直接/间接调用：无明显函数调用；返回表达式：not self.issues；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据模型, dataclass, 数据契约, Database, Health, healthy

**调用：** 无明显调用；**返回：** not self.issues；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `IndexProgress` (class, L164-L174)

**签名：** `class IndexProgress`

**作用：** 索引器发出的单文件进度事件。

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；类体包含 0 个直接方法。

**关键词：** 数据模型, dataclass, 数据契约, Index, Progress

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `IndexStats` (class, L178-L192)

**签名：** `class IndexStats`

**作用：** 定义 IndexStats 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。；类体包含 0 个直接方法。

**关键词：** 数据模型, dataclass, 数据契约, Index, Stats

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/rag/__init__.py

**文件作用：** RAG 子包的公开符号聚合入口，统一导出检索、回答和 LLM 客户端类型。

**语言/关键词：** RAG, 包入口, 公开 API, Python, py

**函数/类/脚本记录数：** 0

## personal_local_knowledge_base_v0/knowledge_search/rag/answer.py

**文件作用：** 编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。

**语言/关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Python, py

**函数/类/脚本记录数：** 13

### `CitationValidationError` (class, L23-L24)

**签名：** `class CitationValidationError`

**作用：** The model response did not use only citations from this retrieval.

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；类体包含 0 个直接方法。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Citation, Validation, Error

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagConfig` (class, L28-L63)

**签名：** `class RagConfig`

**作用：** 定义 RagConfig 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；类体包含 2 个直接方法。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Config

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagConfig.__post_init__` (function, L33-L39)

**签名：** `def __post_init__(self) -> None`

**作用：** 执行 dataclass 配置校验，拒绝不满足范围、格式或不变量的参数。

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；输入参数：self；声明返回：None；直接/间接调用：ValueError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('top_k 必须大于 0'); ValueError('max_context_chars 必须大于 0'); ValueError('temperature 必须在 0 到 2 之间')；控制流：条件分支。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Config, post, init, ValueError, 条件分支

**调用：** ValueError；**返回：** 未记录；**异常：** ValueError('top_k 必须大于 0'); ValueError('max_context_chars 必须大于 0'); ValueError('temperature 必须在 0 到 2 之间')；**副作用：** 未发现明显外部副作用。

### `RagConfig.from_file` (function, L42-L63)

**签名：** `def from_file(cls, path: Path) -> 'RagConfig'`

**作用：** 执行 from file，涉及 sorted, json.loads, isinstance, ValueError, cls。

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；输入参数：cls, path: Path；声明返回：'RagConfig'；直接/间接调用：sorted, json.loads, isinstance, ValueError, cls, path.read_text, set, int, float, Constant.join, data.get；返回表达式：cls(top_k=int(data.get('top_k', 5)), max_context_chars=int(data.get('max_context_chars', 12000)), temperature=float(data.get('temperature', 0)))；显式异常：ValueError('RAG 配置顶层必须是 JSON 对象'); ValueError(f'RAG 配置包含未知字段：{', '.join(unknown)}'); ValueError(f'RAG 配置文件不存在：{path}'); ValueError(f'RAG 配置不是有效 JSON：{path}'); ValueError('RAG 配置字段类型无效')；控制流：条件分支, 异常处理。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Config, from, file, sorted, json.loads, isinstance, ValueError, cls, path.read_text, set, int, float, Constant.join, data.get, 条件分支, 异常处理

**调用：** sorted, json.loads, isinstance, ValueError, cls, path.read_text, set, int, float, Constant.join, data.get；**返回：** cls(top_k=int(data.get('top_k', 5)), max_context_chars=int(data.get('max_context_chars', 12000)), temperature=float(data.get('temperature', 0)))；**异常：** ValueError('RAG 配置顶层必须是 JSON 对象'); ValueError(f'RAG 配置包含未知字段：{', '.join(unknown)}'); ValueError(f'RAG 配置文件不存在：{path}'); ValueError(f'RAG 配置不是有效 JSON：{path}'); ValueError('RAG 配置字段类型无效')；**副作用：** 文件系统读写。

### `AnswerResult` (class, L67-L75)

**签名：** `class AnswerResult`

**作用：** 定义 AnswerResult 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；类体包含 0 个直接方法。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Answer, Result

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagAnswerer` (class, L78-L244)

**签名：** `class RagAnswerer`

**作用：** Run retrieval first and create the LLM client only when it is needed.

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；类体包含 7 个直接方法。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Answerer

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagAnswerer.__init__` (function, L81-L90)

**签名：** `def __init__(self, retriever: ChunkRetriever, *, temperature: float=0.0, client_factory: Callable[[], LLMClient]=LLMClient.from_env) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；输入参数：self, retriever: ChunkRetriever, *, temperature: float=0.0, client_factory: Callable[[], LLMClient]=LLMClient.from_env；声明返回：None；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Answerer, init

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagAnswerer.answer` (function, L92-L144)

**签名：** `def answer(self, question: str) -> AnswerResult`

**作用：** 执行 answer，涉及 time.perf_counter, self.retriever.retrieve, AnswerResult, self._log_result, self.client_factory.complete。

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；输入参数：self, question: str；声明返回：AnswerResult；直接/间接调用：time.perf_counter, self.retriever.retrieve, AnswerResult, self._log_result, self.client_factory.complete, response.content.startswith, self._validate_citations, build_messages, self._log_failure, self.client_factory；返回表达式：result；显式异常：裸 raise；控制流：条件分支, 异常处理。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Answerer, answer, time.perf_counter, self.retriever.retrieve, AnswerResult, self._log_result, self.client_factory.complete, response.content.startswith, self._validate_citations, build_messages, self._log_failure, self.client_factory, 条件分支, 异常处理

**调用：** time.perf_counter, self.retriever.retrieve, AnswerResult, self._log_result, self.client_factory.complete, response.content.startswith, self._validate_citations, build_messages, self._log_failure, self.client_factory；**返回：** result；**异常：** 裸 raise；**副作用：** 未发现明显外部副作用。

### `RagAnswerer._validate_citations` (function, L147-L170)

**签名：** `def _validate_citations(answer: str, sources: tuple[RetrievedChunk, ...], *, refused: bool) -> None`

**作用：** Reject missing or invented citations before a response becomes successful.

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；输入参数：answer: str, sources: tuple[RetrievedChunk, ...], *, refused: bool；声明返回：None；直接/间接调用：sorted, int, Constant.join, CitationValidationError, CITATION_PATTERN.findall, set；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：CitationValidationError(f'大模型回答引用校验失败：引用 {invalid_text} 不属于本次检索结果；可用引用为 {available_text}。请重试。'); CitationValidationError('大模型回答引用校验失败：非拒答答案没有提供 [n] 格式的引用。本次回答未被接受，请重试。')；控制流：条件分支。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Answerer, validate, citations, sorted, int, Constant.join, CitationValidationError, CITATION_PATTERN.findall, set, 条件分支

**调用：** sorted, int, Constant.join, CitationValidationError, CITATION_PATTERN.findall, set；**返回：** 未记录；**异常：** CitationValidationError(f'大模型回答引用校验失败：引用 {invalid_text} 不属于本次检索结果；可用引用为 {available_text}。请重试。'); CitationValidationError('大模型回答引用校验失败：非拒答答案没有提供 [n] 格式的引用。本次回答未被接受，请重试。')；**副作用：** 未发现明显外部副作用。

### `RagAnswerer._source_records` (function, L172-L185)

**签名：** `def _source_records(self, sources: tuple[RetrievedChunk, ...]) -> list[dict[str, object]]`

**作用：** 执行  source records，涉及 self._redact。

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；输入参数：self, sources: tuple[RetrievedChunk, ...]；声明返回：list[dict[str, object]]；直接/间接调用：self._redact；返回表达式：[{'citation_id': source.citation_id, 'chunk_id': source.chunk_id, 'path': self._redact(source.document_path), 'filename': self._redact(source.filename), 'chunk_index': source.chun…；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Answerer, source, records, self._redact

**调用：** self._redact；**返回：** [{'citation_id': source.citation_id, 'chunk_id': source.chunk_id, 'path': self._redact(source.document_path), 'filename': self._redact(source.filename), 'chunk_index': source.chun…；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagAnswerer._redact` (function, L188-L197)

**签名：** `def _redact(value: str) -> str`

**作用：** Keep configured credentials out of audit records if a model echoes one.

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；输入参数：value: str；声明返回：str；直接/间接调用：LLMClient.load_dotenv, os.environ.get, value.replace；返回表达式：value; value.replace(api_key, '[REDACTED]')；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Answerer, redact, LLMClient.load_dotenv, os.environ.get, value.replace, 条件分支

**调用：** LLMClient.load_dotenv, os.environ.get, value.replace；**返回：** value; value.replace(api_key, '[REDACTED]')；**异常：** 未发现显式 raise；**副作用：** 环境变量读取。

### `RagAnswerer._log_result` (function, L199-L215)

**签名：** `def _log_result(self, result: AnswerResult) -> None`

**作用：** 执行  log result，涉及 logger.info, self._redact, self._source_records, round, json.dumps。

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；输入参数：self, result: AnswerResult；声明返回：None；直接/间接调用：logger.info, self._redact, self._source_records, round, json.dumps；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Answerer, log, result, logger.info, self._redact, self._source_records, round, json.dumps

**调用：** logger.info, self._redact, self._source_records, round, json.dumps；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `RagAnswerer._log_failure` (function, L217-L244)

**签名：** `def _log_failure(self, question: str, sources: tuple[RetrievedChunk, ...], elapsed_ms: float, error: LLMClientError, *, usage: TokenUsage | None=None) -> None`

**作用：** 执行  log failure，涉及 logger.error, self._redact, self._source_records, round, json.dumps。

**详细语义：** 所属模块职责：编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。；输入参数：self, question: str, sources: tuple[RetrievedChunk, ...], elapsed_ms: float, error: LLMClientError, *, usage: TokenUsage | None=None；声明返回：None；直接/间接调用：logger.error, self._redact, self._source_records, round, json.dumps, type, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** RAG, 引用校验, 拒答, Prompt, 审计日志, Rag, Answerer, log, failure, logger.error, self._redact, self._source_records, round, json.dumps, type, str, 条件分支

**调用：** logger.error, self._redact, self._source_records, round, json.dumps, type, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

## personal_local_knowledge_base_v0/knowledge_search/rag/llm_client.py

**文件作用：** 通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。

**语言/关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, Python, py

**函数/类/脚本记录数：** 12

### `LLMClientError` (class, L19-L20)

**签名：** `class LLMClientError`

**作用：** A user-facing, sanitized LLM configuration or request error.

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；类体包含 0 个直接方法。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient, Error

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `TokenUsage` (class, L24-L27)

**签名：** `class TokenUsage`

**作用：** 定义 TokenUsage 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；类体包含 0 个直接方法。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, Token, Usage

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `LLMResponse` (class, L31-L33)

**签名：** `class LLMResponse`

**作用：** 定义 LLMResponse 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；类体包含 0 个直接方法。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMResponse

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `LLMClient` (class, L36-L171)

**签名：** `class LLMClient`

**作用：** Call an OpenAI-compatible ``/chat/completions`` endpoint.

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；类体包含 8 个直接方法。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `LLMClient.__init__` (function, L39-L63)

**签名：** `def __init__(self, *, api_key: str, base_url: str, model: str, timeout_seconds: float=60.0) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；输入参数：self, *, api_key: str, base_url: str, model: str, timeout_seconds: float=60.0；声明返回：None；直接/间接调用：urllib.parse.urlsplit, base_url.rstrip, LLMClientError, ValueError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：LLMClientError('未配置 LLM_API_KEY。'); LLMClientError('未配置 LLM_BASE_URL。'); LLMClientError('未配置 LLM_MODEL。'); ValueError('timeout_seconds 必须大于 0'); LLMClientError('LLM_BASE_URL 必须是有效的 HTTP(S) 地址。')；控制流：条件分支。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient, init, urllib.parse.urlsplit, base_url.rstrip, LLMClientError, ValueError, 条件分支

**调用：** urllib.parse.urlsplit, base_url.rstrip, LLMClientError, ValueError；**返回：** 未记录；**异常：** LLMClientError('未配置 LLM_API_KEY。'); LLMClientError('未配置 LLM_BASE_URL。'); LLMClientError('未配置 LLM_MODEL。'); ValueError('timeout_seconds 必须大于 0'); LLMClientError('LLM_BASE_URL 必须是有效的 HTTP(S) 地址。')；**副作用：** 网络 HTTP 请求。

### `LLMClient.from_env` (function, L66-L77)

**签名：** `def from_env(cls, environ: Mapping[str, str] | None=None) -> 'LLMClient'`

**作用：** 执行 from env，涉及 cls, cls.load_dotenv, values.get.strip, values.get。

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；输入参数：cls, environ: Mapping[str, str] | None=None；声明返回：'LLMClient'；直接/间接调用：cls, cls.load_dotenv, values.get.strip, values.get；返回表达式：cls(api_key=values.get('LLM_API_KEY', '').strip(), base_url=values.get('LLM_BASE_URL', '').strip(), model=values.get('LLM_MODEL', '').strip())；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient, from, env, cls, cls.load_dotenv, values.get.strip, values.get, 条件分支

**调用：** cls, cls.load_dotenv, values.get.strip, values.get；**返回：** cls(api_key=values.get('LLM_API_KEY', '').strip(), base_url=values.get('LLM_BASE_URL', '').strip(), model=values.get('LLM_MODEL', '').strip())；**异常：** 未发现显式 raise；**副作用：** 环境变量读取。

### `LLMClient.load_dotenv` (function, L80-L89)

**签名：** `def load_dotenv() -> None`

**作用：** Load the nearest project .env without overriding real environment vars.

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；输入参数：；声明返回：None；直接/间接调用：find_dotenv, project_dotenv.is_file, load_dotenv, str, Path.resolve, Path；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient, load, dotenv, find_dotenv, project_dotenv.is_file, load_dotenv, str, Path.resolve, Path, 条件分支

**调用：** find_dotenv, project_dotenv.is_file, load_dotenv, str, Path.resolve, Path；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 环境变量读取。

### `LLMClient.endpoint` (function, L92-L95)

**签名：** `def endpoint(self) -> str`

**作用：** 执行 endpoint，涉及 self._base_url.endswith。

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；输入参数：self；声明返回：str；直接/间接调用：self._base_url.endswith；返回表达式：f'{self._base_url}/chat/completions'; self._base_url；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient, endpoint, self._base_url.endswith, 条件分支

**调用：** self._base_url.endswith；**返回：** f'{self._base_url}/chat/completions'; self._base_url；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `LLMClient._sanitize` (function, L97-L99)

**签名：** `def _sanitize(self, message: str) -> str`

**作用：** 执行  sanitize，涉及 message.replace, sanitized.replace。

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；输入参数：self, message: str；声明返回：str；直接/间接调用：message.replace, sanitized.replace；返回表达式：sanitized.replace(self._base_url, '[REDACTED_URL]')；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient, sanitize, message.replace, sanitized.replace

**调用：** message.replace, sanitized.replace；**返回：** sanitized.replace(self._base_url, '[REDACTED_URL]')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `LLMClient.complete` (function, L101-L145)

**签名：** `def complete(self, messages: Sequence[Mapping[str, str]], *, temperature: float=0.0) -> LLMResponse`

**作用：** 执行 complete，涉及 json.dumps.encode, self._parse_response, urllib.request.Request, json.dumps, urllib.request.urlopen。

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；输入参数：self, messages: Sequence[Mapping[str, str]], *, temperature: float=0.0；声明返回：LLMResponse；直接/间接调用：json.dumps.encode, self._parse_response, urllib.request.Request, json.dumps, urllib.request.urlopen, json.loads, self._http_error_detail, LLMClientError, response.read.decode, self._sanitize, list, response.read；返回表达式：self._parse_response(response_data)；显式异常：LLMClientError(self._sanitize(f'大模型请求失败（HTTP {exc.code}）：{detail}')); LLMClientError('无法连接到大模型服务，请检查 LLM_BASE_URL、网络连接和服务状态。'); LLMClientError('大模型服务返回了无法解析的响应。'); LLMClientError('LLM_BASE_URL 无效，无法创建大模型请求。')；控制流：异常处理, 上下文管理。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient, complete, json.dumps.encode, self._parse_response, urllib.request.Request, json.dumps, urllib.request.urlopen, json.loads, self._http_error_detail, LLMClientError, response.read.decode, self._sanitize, list, response.read, 异常处理, 上下文管理

**调用：** json.dumps.encode, self._parse_response, urllib.request.Request, json.dumps, urllib.request.urlopen, json.loads, self._http_error_detail, LLMClientError, response.read.decode, self._sanitize, list, response.read；**返回：** self._parse_response(response_data)；**异常：** LLMClientError(self._sanitize(f'大模型请求失败（HTTP {exc.code}）：{detail}')); LLMClientError('无法连接到大模型服务，请检查 LLM_BASE_URL、网络连接和服务状态。'); LLMClientError('大模型服务返回了无法解析的响应。'); LLMClientError('LLM_BASE_URL 无效，无法创建大模型请求。')；**副作用：** 网络 HTTP 请求。

### `LLMClient._http_error_detail` (function, L147-L156)

**签名：** `def _http_error_detail(self, exc: urllib.error.HTTPError) -> str`

**作用：** 执行  http error detail，涉及 exc.read.decode, json.loads, data.get.get, isinstance, message.strip。

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；输入参数：self, exc: urllib.error.HTTPError；声明返回：str；直接/间接调用：exc.read.decode, json.loads, data.get.get, isinstance, message.strip, exc.read, data.get；返回表达式：'请检查模型配置、额度和服务状态。'; message.strip()；显式异常：未发现显式 raise；控制流：条件分支, 异常处理。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient, http, error, detail, exc.read.decode, json.loads, data.get.get, isinstance, message.strip, exc.read, data.get, 条件分支, 异常处理

**调用：** exc.read.decode, json.loads, data.get.get, isinstance, message.strip, exc.read, data.get；**返回：** '请检查模型配置、额度和服务状态。'; message.strip()；**异常：** 未发现显式 raise；**副作用：** 网络 HTTP 请求。

### `LLMClient._parse_response` (function, L158-L171)

**签名：** `def _parse_response(self, data: Any) -> LLMResponse`

**作用：** 解析并转换response；内部调用 LLMResponse, TokenUsage, LLMClientError, data.get, isinstance。

**详细语义：** 所属模块职责：通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。；输入参数：self, data: Any；声明返回：LLMResponse；直接/间接调用：LLMResponse, TokenUsage, LLMClientError, data.get, isinstance, content.strip, int, usage_data.get；返回表达式：LLMResponse(content=content.strip(), usage=usage)；显式异常：LLMClientError('大模型服务返回了空答案。'); LLMClientError('大模型服务响应缺少答案或 token 使用量格式无效。')；控制流：条件分支, 异常处理。

**关键词：** LLM, OpenAI 兼容, HTTP, token 用量, API Key 脱敏, LLMClient, parse, response, LLMResponse, TokenUsage, LLMClientError, data.get, isinstance, content.strip, int, usage_data.get, 条件分支, 异常处理

**调用：** LLMResponse, TokenUsage, LLMClientError, data.get, isinstance, content.strip, int, usage_data.get；**返回：** LLMResponse(content=content.strip(), usage=usage)；**异常：** LLMClientError('大模型服务返回了空答案。'); LLMClientError('大模型服务响应缺少答案或 token 使用量格式无效。')；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/rag/prompt.py

**文件作用：** 生成要求只依据检索上下文、把上下文视为不可信资料并逐句引用的聊天消息。

**语言/关键词：** Prompt, grounding, 引用, 拒答, Python, py

**函数/类/脚本记录数：** 1

### `build_messages` (function, L19-L39)

**签名：** `def build_messages(question: str, context: str) -> Sequence[Mapping[str, str]]`

**作用：** Build chat-completions messages without adding outside knowledge.

**详细语义：** 所属模块职责：生成要求只依据检索上下文、把上下文视为不可信资料并逐句引用的聊天消息。；输入参数：question: str, context: str；声明返回：Sequence[Mapping[str, str]]；直接/间接调用：ValueError, question.strip, context.strip；返回表达式：({'role': 'system', 'content': SYSTEM_PROMPT}, {'role': 'user', 'content': user_prompt})；显式异常：ValueError('问题不能为空'); ValueError('检索上下文不能为空')；控制流：条件分支。

**关键词：** Prompt, grounding, 引用, 拒答, build, messages, ValueError, question.strip, context.strip, 条件分支

**调用：** ValueError, question.strip, context.strip；**返回：** ({'role': 'system', 'content': SYSTEM_PROMPT}, {'role': 'user', 'content': user_prompt})；**异常：** ValueError('问题不能为空'); ValueError('检索上下文不能为空')；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/rag/retriever.py

**文件作用：** 把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。

**语言/关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Python, py

**函数/类/脚本记录数：** 13

### `RetrievedChunk` (class, L15-L67)

**签名：** `class RetrievedChunk`

**作用：** A source chunk and the exact excerpt included in the prompt.

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；类体包含 2 个直接方法。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Retrieved, Chunk

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RetrievedChunk.location_parts` (function, L37-L57)

**签名：** `def location_parts(self) -> tuple[str, ...]`

**作用：** 执行 location parts，涉及 tuple, parts.append, str, Constant.join, separator.join。

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；输入参数：self；声明返回：tuple[str, ...]；直接/间接调用：tuple, parts.append, str, Constant.join, separator.join；返回表达式：tuple(parts)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Retrieved, Chunk, location, parts, tuple, parts.append, str, Constant.join, separator.join, 条件分支

**调用：** tuple, parts.append, str, Constant.join, separator.join；**返回：** tuple(parts)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RetrievedChunk.citation` (function, L60-L67)

**签名：** `def citation(self) -> str`

**作用：** 执行 citation，涉及 Constant.join, len, str。

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；输入参数：self；声明返回：str；直接/间接调用：Constant.join, len, str；返回表达式：f'[{self.citation_id}] {self.filename}，分段 {chunk_label}{suffix}'；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Retrieved, Chunk, citation, Constant.join, len, str, 条件分支

**调用：** Constant.join, len, str；**返回：** f'[{self.citation_id}] {self.filename}，分段 {chunk_label}{suffix}'；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RetrievalResult` (class, L71-L80)

**签名：** `class RetrievalResult`

**作用：** Retrieved chunks plus the bounded context sent to the model.

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；类体包含 1 个直接方法。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Retrieval, Result

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RetrievalResult.context_chars` (function, L79-L80)

**签名：** `def context_chars(self) -> int`

**作用：** 执行 context chars，涉及 len。

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；输入参数：self；声明返回：int；直接/间接调用：len；返回表达式：len(self.context)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Retrieval, Result, context, chars, len

**调用：** len；**返回：** len(self.context)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkRetriever` (class, L83-L220)

**签名：** `class ChunkRetriever`

**作用：** Match question chunks to structured document chunks without jieba.

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；类体包含 3 个直接方法。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Chunk, Retriever

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkRetriever.__init__` (function, L86-L99)

**签名：** `def __init__(self, knowledge_base: KnowledgeBase, *, top_k: int=5, max_context_chars: int=12000) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；输入参数：self, knowledge_base: KnowledgeBase, *, top_k: int=5, max_context_chars: int=12000；声明返回：None；直接/间接调用：ValueError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('top_k 必须大于 0'); ValueError('max_context_chars 必须大于 0')；控制流：条件分支。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Chunk, Retriever, init, ValueError, 条件分支

**调用：** ValueError；**返回：** 未记录；**异常：** ValueError('top_k 必须大于 0'); ValueError('max_context_chars 必须大于 0')；**副作用：** SQLite/数据库写入或查询。

### `ChunkRetriever._search` (function, L101-L126)

**签名：** `def _search(self, question: str) -> list[SearchResult]`

**作用：** 执行受约束的检索内部资源；内部调用 ChunkingConfig, chunk_text, max, self.knowledge_base.search_chunk_matches, sorted。

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；输入参数：self, question: str；声明返回：list[SearchResult]；直接/间接调用：ChunkingConfig, chunk_text, max, self.knowledge_base.search_chunk_matches, sorted, candidates.get, candidates.values；返回表达式：sorted(candidates.values(), key=lambda result: (result.score, result.document_path, result.chunk_index))[:self.top_k]；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Chunk, Retriever, search, ChunkingConfig, chunk_text, max, self.knowledge_base.search_chunk_matches, sorted, candidates.get, candidates.values, 条件分支, 循环

**调用：** ChunkingConfig, chunk_text, max, self.knowledge_base.search_chunk_matches, sorted, candidates.get, candidates.values；**返回：** sorted(candidates.values(), key=lambda result: (result.score, result.document_path, result.chunk_index))[:self.top_k]；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkRetriever._search.lambda@121` (function, L121-L125)

**签名：** `lambda result`

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；这是匿名 lambda，输入参数：result；返回表达式：(result.score, result.document_path, result.chunk_index)；调用：无明显函数调用；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, lambda

**调用：** 无明显调用；**返回：** (result.score, result.document_path, result.chunk_index)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkRetriever.retrieve` (function, L128-L220)

**签名：** `def retrieve(self, question: str) -> RetrievalResult`

**作用：** 执行 retrieve，涉及 self._search, RetrievalResult, ValueError, self.knowledge_base.chunk_window, Constant.join。

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；输入参数：self, question: str；声明返回：RetrievalResult；直接/间接调用：self._search, RetrievalResult, ValueError, self.knowledge_base.chunk_window, Constant.join, Subscript.rstrip, blocks.append, chunks.append, len, question.strip, tuple, location_parts.append, str, RetrievedChunk, separator_symbol.join；返回表达式：RetrievalResult(chunks=tuple(chunks), context=''.join(blocks), truncated=truncated)；显式异常：ValueError('问题不能为空')；控制流：条件分支, 循环。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Chunk, Retriever, retrieve, self._search, RetrievalResult, ValueError, self.knowledge_base.chunk_window, Constant.join, Subscript.rstrip, blocks.append, chunks.append, len, question.strip, tuple, location_parts.append, str, RetrievedChunk, separator_symbol.join, 条件分支, 循环

**调用：** self._search, RetrievalResult, ValueError, self.knowledge_base.chunk_window, Constant.join, Subscript.rstrip, blocks.append, chunks.append, len, question.strip, tuple, location_parts.append, str, RetrievedChunk, separator_symbol.join；**返回：** RetrievalResult(chunks=tuple(chunks), context=''.join(blocks), truncated=truncated)；**异常：** ValueError('问题不能为空')；**副作用：** 未发现明显外部副作用。

### `VectorRetriever` (class, L223-L246)

**签名：** `class VectorRetriever`

**作用：** Use query embeddings plus sqlite-vec, with a NumPy fallback.

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；类体包含 2 个直接方法。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Vector, Retriever

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `VectorRetriever.__init__` (function, L226-L241)

**签名：** `def __init__(self, knowledge_base: KnowledgeBase, embedding_backend: EmbeddingBackend, *, top_k: int=5, max_context_chars: int=12000, code: bool=False) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；输入参数：self, knowledge_base: KnowledgeBase, embedding_backend: EmbeddingBackend, *, top_k: int=5, max_context_chars: int=12000, code: bool=False；声明返回：None；直接/间接调用：super.__init__, VectorIndex, super；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Vector, Retriever, init, super.__init__, VectorIndex, super

**调用：** super.__init__, VectorIndex, super；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `VectorRetriever._search` (function, L243-L246)

**签名：** `def _search(self, question: str) -> list[SearchResult]`

**作用：** 执行受约束的检索内部资源；内部调用 self.vector_index.search。

**详细语义：** 所属模块职责：把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。；输入参数：self, question: str；声明返回：list[SearchResult]；直接/间接调用：self.vector_index.search；返回表达式：self.vector_index.search(question, top_k=self.top_k, code=self.code)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** RAG 检索, 来源, 引用 ID, 上下文预算, 相邻分段, Vector, Retriever, search, self.vector_index.search

**调用：** self.vector_index.search；**返回：** self.vector_index.search(question, top_k=self.top_k, code=self.code)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/tokenization.py

**文件作用：** 使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。

**语言/关键词：** 中文分词, jieba, 字符回退, FTS5, Python, py

**函数/类/脚本记录数：** 3

### `_fallback_tokens` (function, L14-L30)

**签名：** `def _fallback_tokens(text: str) -> Iterator[str]`

**作用：** jieba 不可用时，按英文单词和单个中文字符提供最低限度兜底。

**详细语义：** 所属模块职责：使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。；输入参数：text: str；声明返回：Iterator[str]；直接/间接调用：char.isascii, current.append, Constant.join, char.isalnum；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 生成器 yield。

**关键词：** 中文分词, jieba, 字符回退, FTS5, fallback, tokens, char.isascii, current.append, Constant.join, char.isalnum, 条件分支, 循环, 生成器 yield

**调用：** char.isascii, current.append, Constant.join, char.isalnum；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `tokenize_for_search` (function, L33-L58)

**签名：** `def tokenize_for_search(text: str) -> list[str]`

**作用：** 优先使用 jieba 搜索模式切词，并去除空白和纯标点词。

**详细语义：** 所属模块职责：使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。；输入参数：text: str；声明返回：list[str]；直接/间接调用：jieba.cut_for_search, candidate.strip, text.strip, logger.warning, _fallback_tokens, any, tokens.append, char.isalnum；返回表达式：tokens; []；显式异常：未发现显式 raise；控制流：条件分支, 循环, 异常处理。

**关键词：** 中文分词, jieba, 字符回退, FTS5, tokenize, for, search, jieba.cut_for_search, candidate.strip, text.strip, logger.warning, _fallback_tokens, any, tokens.append, char.isalnum, 条件分支, 循环, 异常处理

**调用：** jieba.cut_for_search, candidate.strip, text.strip, logger.warning, _fallback_tokens, any, tokens.append, char.isalnum；**返回：** tokens; []；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 日志输出。

### `to_token_fts_query` (function, L61-L70)

**签名：** `def to_token_fts_query(query: str) -> str`

**作用：** 把 jieba 词项转换为安全的 FTS5 AND 查询。

**详细语义：** 所属模块职责：使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。；输入参数：query: str；声明返回：str；直接/间接调用：Constant.join, tokenize_for_search, query_terms, token.replace, chr；返回表达式：' AND '.join((f'"{token.replace(chr(34), chr(34) * 2)}"' for token in tokens)); ''；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 中文分词, jieba, 字符回退, FTS5, to, token, fts, query, Constant.join, tokenize_for_search, query_terms, token.replace, chr, 条件分支

**调用：** Constant.join, tokenize_for_search, query_terms, token.replace, chr；**返回：** ' AND '.join((f'"{token.replace(chr(34), chr(34) * 2)}"' for token in tokens)); ''；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

## personal_local_knowledge_base_v0/knowledge_search/vector_search.py

**文件作用：** 提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。

**语言/关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Python, py

**函数/类/脚本记录数：** 16

### `SqliteVecUnavailable` (class, L19-L20)

**签名：** `class SqliteVecUnavailable`

**作用：** The optional sqlite-vec extension cannot be used on this connection.

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；类体包含 0 个直接方法。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Sqlite, Vec, Unavailable

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_load_sqlite_vec` (function, L23-L48)

**签名：** `def _load_sqlite_vec(connection: sqlite3.Connection) -> 未声明`

**作用：** Load sqlite-vec once and return its Python helper module.

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：connection: sqlite3.Connection；声明返回：未声明；直接/间接调用：connection.enable_load_extension, sqlite_vec.load, SqliteVecUnavailable；返回表达式：sqlite_vec；显式异常：SqliteVecUnavailable('未安装 sqlite-vec；将回退到 NumPy 向量检索'); SqliteVecUnavailable(f'sqlite-vec 扩展加载失败；将回退到 NumPy 向量检索：{exc}')；控制流：异常处理。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, load, sqlite, vec, connection.enable_load_extension, sqlite_vec.load, SqliteVecUnavailable, 异常处理

**调用：** connection.enable_load_extension, sqlite_vec.load, SqliteVecUnavailable；**返回：** sqlite_vec；**异常：** SqliteVecUnavailable('未安装 sqlite-vec；将回退到 NumPy 向量检索'); SqliteVecUnavailable(f'sqlite-vec 扩展加载失败；将回退到 NumPy 向量检索：{exc}')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `SqliteVecVectorIndex` (class, L51-L216)

**签名：** `class SqliteVecVectorIndex`

**作用：** Persistent sqlite-vec KNN retrieval for one embedding configuration.

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；类体包含 6 个直接方法。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Sqlite, Vec, Vector, Index

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `SqliteVecVectorIndex.__init__` (function, L56-L69)

**签名：** `def __init__(self, knowledge_base: KnowledgeBase, backend: EmbeddingBackend) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self, knowledge_base: KnowledgeBase, backend: EmbeddingBackend；声明返回：None；直接/间接调用：RLock, _load_sqlite_vec, knowledge_base.embedding_model_id, self._ensure_schema, SqliteVecUnavailable；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：SqliteVecUnavailable(f'sqlite-vec 虚拟表不可用；将回退到 NumPy 向量检索：{exc}')；控制流：异常处理。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Sqlite, Vec, Vector, Index, init, RLock, _load_sqlite_vec, knowledge_base.embedding_model_id, self._ensure_schema, SqliteVecUnavailable, 异常处理

**调用：** RLock, _load_sqlite_vec, knowledge_base.embedding_model_id, self._ensure_schema, SqliteVecUnavailable；**返回：** 未记录；**异常：** SqliteVecUnavailable(f'sqlite-vec 虚拟表不可用；将回退到 NumPy 向量检索：{exc}')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `SqliteVecVectorIndex._ensure_schema` (function, L71-L86)

**签名：** `def _ensure_schema(self) -> None`

**作用：** 执行  ensure schema，涉及 connection.execute。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self；声明返回：None；直接/间接调用：connection.execute；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Sqlite, Vec, Vector, Index, ensure, schema, connection.execute

**调用：** connection.execute；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `SqliteVecVectorIndex._sync_if_needed` (function, L88-L147)

**签名：** `def _sync_if_needed(self) -> int`

**作用：** Rebuild the derived vec table only after the source cache changes.

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self；声明返回：int；直接/间接调用：knowledge_base.embedding_cache_signature, connection.execute.fetchone, int, connection.execute.fetchall, connection.execute, connection.executemany, str, ValueError, knowledge_base._valid_vector_blob, sqlite3.Binary；返回表达式：signature[1]；显式异常：ValueError(f'Chunk {row['chunk_id']} 的 Embedding 数据无效')；控制流：条件分支, 循环, 上下文管理。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Sqlite, Vec, Vector, Index, sync, if, needed, knowledge_base.embedding_cache_signature, connection.execute.fetchone, int, connection.execute.fetchall, connection.execute, connection.executemany, str, ValueError, knowledge_base._valid_vector_blob, sqlite3.Binary, 条件分支, 循环, 上下文管理

**调用：** knowledge_base.embedding_cache_signature, connection.execute.fetchone, int, connection.execute.fetchall, connection.execute, connection.executemany, str, ValueError, knowledge_base._valid_vector_blob, sqlite3.Binary；**返回：** signature[1]；**异常：** ValueError(f'Chunk {row['chunk_id']} 的 Embedding 数据无效')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `SqliteVecVectorIndex._knn` (function, L149-L158)

**签名：** `def _knn(self, query_blob: bytes, limit: int) -> list[sqlite3.Row]`

**作用：** 执行  knn，涉及 self.knowledge_base.connection.execute.fetchall, self.knowledge_base.connection.execute。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self, query_blob: bytes, limit: int；声明返回：list[sqlite3.Row]；直接/间接调用：self.knowledge_base.connection.execute.fetchall, self.knowledge_base.connection.execute；返回表达式：self.knowledge_base.connection.execute(f'\n            SELECT rowid, distance\n            FROM {self._table}\n            WHERE embedding MATCH ? AND k = ?\n            ORDER BY …；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Sqlite, Vec, Vector, Index, knn, self.knowledge_base.connection.execute.fetchall, self.knowledge_base.connection.execute

**调用：** self.knowledge_base.connection.execute.fetchall, self.knowledge_base.connection.execute；**返回：** self.knowledge_base.connection.execute(f'\n            SELECT rowid, distance\n            FROM {self._table}\n            WHERE embedding MATCH ? AND k = ?\n            ORDER BY …；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `SqliteVecVectorIndex._score` (function, L161-L164)

**签名：** `def _score(distance: float) -> float`

**作用：** 执行  score，涉及 float。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：distance: float；声明返回：float；直接/间接调用：float；返回表达式：1.0 - float(distance) ** 2 / 2.0；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Sqlite, Vec, Vector, Index, score, float

**调用：** float；**返回：** 1.0 - float(distance) ** 2 / 2.0；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `SqliteVecVectorIndex.search` (function, L166-L216)

**签名：** `def search(self, query: str, *, top_k: int=5, code: bool=False, file_type: str | None=None, path: Path | None=None) -> list[SearchResult]`

**作用：** 执行检索内部资源；内部调用 self.knowledge_base.results_for_vector_scores, ValueError, query.strip, self._sync_if_needed, self._sqlite_vec.serialize_float32。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self, query: str, *, top_k: int=5, code: bool=False, file_type: str | None=None, path: Path | None=None；声明返回：list[SearchResult]；直接/间接调用：self.knowledge_base.results_for_vector_scores, ValueError, query.strip, self._sync_if_needed, self._sqlite_vec.serialize_float32, self.knowledge_base.vector_candidate_chunk_ids, min, validate_vectors, query_vector.tolist, max, self._knn, len, self.backend.embed_query, int, self._score；返回表达式：self.knowledge_base.results_for_vector_scores(chunk_ids, scores, query); []；显式异常：ValueError('top_k 必须大于 0'); ValueError('查询不能为空')；控制流：条件分支, 循环, 上下文管理。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Sqlite, Vec, Vector, Index, search, self.knowledge_base.results_for_vector_scores, ValueError, query.strip, self._sync_if_needed, self._sqlite_vec.serialize_float32, self.knowledge_base.vector_candidate_chunk_ids, min, validate_vectors, query_vector.tolist, max, self._knn, len, self.backend.embed_query, int, self._score, 条件分支, 循环, 上下文管理

**调用：** self.knowledge_base.results_for_vector_scores, ValueError, query.strip, self._sync_if_needed, self._sqlite_vec.serialize_float32, self.knowledge_base.vector_candidate_chunk_ids, min, validate_vectors, query_vector.tolist, max, self._knn, len, self.backend.embed_query, int, self._score；**返回：** self.knowledge_base.results_for_vector_scores(chunk_ids, scores, query); []；**异常：** ValueError('top_k 必须大于 0'); ValueError('查询不能为空')；**副作用：** SQLite/数据库写入或查询。

### `VectorIndex` (class, L219-L240)

**签名：** `class VectorIndex`

**作用：** Prefer sqlite-vec and keep NumPy as a transparent compatibility fallback.

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；类体包含 2 个直接方法。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Vector, Index

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `VectorIndex.__init__` (function, L222-L237)

**签名：** `def __init__(self, knowledge_base: KnowledgeBase, backend: EmbeddingBackend, *, prefer_sqlite_vec: bool=True) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self, knowledge_base: KnowledgeBase, backend: EmbeddingBackend, *, prefer_sqlite_vec: bool=True；声明返回：None；直接/间接调用：NumpyVectorIndex, SqliteVecVectorIndex, logger.info；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 异常处理。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Vector, Index, init, NumpyVectorIndex, SqliteVecVectorIndex, logger.info, 条件分支, 异常处理

**调用：** NumpyVectorIndex, SqliteVecVectorIndex, logger.info；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 日志输出, 模型/向量计算。

### `VectorIndex.search` (function, L239-L240)

**签名：** `def search(self, *args, **kwargs) -> list[SearchResult]`

**作用：** 执行检索内部资源；内部调用 self._index.search。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self, *args, **kwargs；声明返回：list[SearchResult]；直接/间接调用：self._index.search；返回表达式：self._index.search(*args, **kwargs)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Vector, Index, search, self._index.search

**调用：** self._index.search；**返回：** self._index.search(*args, **kwargs)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `NumpyVectorIndex` (class, L243-L312)

**签名：** `class NumpyVectorIndex`

**作用：** Cache one exact embedding configuration and invalidate on DB changes.

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；类体包含 3 个直接方法。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Numpy, Vector, Index

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `NumpyVectorIndex.__init__` (function, L246-L254)

**签名：** `def __init__(self, knowledge_base: KnowledgeBase, backend: EmbeddingBackend) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self, knowledge_base: KnowledgeBase, backend: EmbeddingBackend；声明返回：None；直接/间接调用：np.empty, RLock；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Numpy, Vector, Index, init, np.empty, RLock

**调用：** np.empty, RLock；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `NumpyVectorIndex._refresh_if_needed` (function, L256-L263)

**签名：** `def _refresh_if_needed(self) -> None`

**作用：** 执行  refresh if needed，涉及 self.knowledge_base.embedding_cache_signature, self.knowledge_base.load_embedding_matrix。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self；声明返回：None；直接/间接调用：self.knowledge_base.embedding_cache_signature, self.knowledge_base.load_embedding_matrix；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Numpy, Vector, Index, refresh, if, needed, self.knowledge_base.embedding_cache_signature, self.knowledge_base.load_embedding_matrix, 条件分支

**调用：** self.knowledge_base.embedding_cache_signature, self.knowledge_base.load_embedding_matrix；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `NumpyVectorIndex.search` (function, L265-L312)

**签名：** `def search(self, query: str, *, top_k: int=5, code: bool=False, file_type: str | None=None, path: Path | None=None) -> list[SearchResult]`

**作用：** 执行检索内部资源；内部调用 self.knowledge_base.results_for_vector_scores, ValueError, query.strip, self._refresh_if_needed, self.knowledge_base.vector_candidate_chunk_ids。

**详细语义：** 所属模块职责：提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。；输入参数：self, query: str, *, top_k: int=5, code: bool=False, file_type: str | None=None, path: Path | None=None；声明返回：list[SearchResult]；直接/间接调用：self.knowledge_base.results_for_vector_scores, ValueError, query.strip, self._refresh_if_needed, self.knowledge_base.vector_candidate_chunk_ids, min, Subscript.astype.tolist, validate_vectors, np.arange, np.flatnonzero, np.isin, np.argsort, np.argpartition, Subscript.astype, self.backend.embed_query, np.fromiter；返回表达式：self.knowledge_base.results_for_vector_scores(chunk_ids, top_scores, query); []；显式异常：ValueError('top_k 必须大于 0'); ValueError('查询不能为空')；控制流：条件分支, 上下文管理。

**关键词：** 向量检索, sqlite-vec, NumPy, KNN, 余弦相似度, Numpy, Vector, Index, search, self.knowledge_base.results_for_vector_scores, ValueError, query.strip, self._refresh_if_needed, self.knowledge_base.vector_candidate_chunk_ids, min, Subscript.astype.tolist, validate_vectors, np.arange, np.flatnonzero, np.isin, np.argsort, np.argpartition, Subscript.astype, self.backend.embed_query, np.fromiter, 条件分支, 上下文管理

**调用：** self.knowledge_base.results_for_vector_scores, ValueError, query.strip, self._refresh_if_needed, self.knowledge_base.vector_candidate_chunk_ids, min, Subscript.astype.tolist, validate_vectors, np.arange, np.flatnonzero, np.isin, np.argsort, np.argpartition, Subscript.astype, self.backend.embed_query, np.fromiter；**返回：** self.knowledge_base.results_for_vector_scores(chunk_ids, top_scores, query); []；**异常：** ValueError('top_k 必须大于 0'); ValueError('查询不能为空')；**副作用：** 模型/向量计算。

## personal_local_knowledge_base_v0/knowledge_search/web/__init__.py

**文件作用：** 网页子包公开入口，导出 KnowledgeWebApp、create_server 和 run_web。

**语言/关键词：** Web, 包入口, 公开 API, Python, py

**函数/类/脚本记录数：** 0

## personal_local_knowledge_base_v0/knowledge_search/web/app.py

**文件作用：** 提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。

**语言/关键词：** Web API, HTTP, 上传, 安全边界, 并发, Python, py

**函数/类/脚本记录数：** 32

### `_ExclusiveThreadingHTTPServer` (class, L61-L64)

**签名：** `class _ExclusiveThreadingHTTPServer`

**作用：** Bind exclusively so a second server cannot reuse the port on Windows.

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；类体包含 0 个直接方法。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Exclusive, Threading, HTTPServer

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_search_result_location` (function, L67-L87)

**签名：** `def _search_result_location(result: Any) -> str`

**作用：** 执行受约束的检索 result location；内部调用 Constant.join, parts.append, str, separator.join。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：result: Any；声明返回：str；直接/间接调用：Constant.join, parts.append, str, separator.join；返回表达式：' · '.join(parts)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, search, result, location, Constant.join, parts.append, str, separator.join, 条件分支

**调用：** Constant.join, parts.append, str, separator.join；**返回：** ' · '.join(parts)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeWebApp` (class, L90-L359)

**签名：** `class KnowledgeWebApp`

**作用：** Bind a database path to the operations exposed over HTTP.

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；类体包含 10 个直接方法。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeWebApp.__init__` (function, L93-L105)

**签名：** `def __init__(self, *, db_path: Path, upload_dir: Path=DEFAULT_UPLOAD_DIR, client_factory: Callable[[], LLMClient]=LLMClient.from_env, embedding_backend: EmbeddingBackend | None=None) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, *, db_path: Path, upload_dir: Path=DEFAULT_UPLOAD_DIR, client_factory: Callable[[], LLMClient]=LLMClient.from_env, embedding_backend: EmbeddingBackend | None=None；声明返回：None；直接/间接调用：Path.expanduser.resolve, threading.RLock, Path.expanduser, Path；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, init, Path.expanduser.resolve, threading.RLock, Path.expanduser, Path

**调用：** Path.expanduser.resolve, threading.RLock, Path.expanduser, Path；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 模型/向量计算。

### `KnowledgeWebApp.open` (function, L107-L110)

**签名：** `def open(self) -> KnowledgeBase`

**作用：** 执行 open，涉及 KnowledgeBase。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：KnowledgeBase；直接/间接调用：KnowledgeBase；返回表达式：KnowledgeBase(self.db_path)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, open, KnowledgeBase

**调用：** KnowledgeBase；**返回：** KnowledgeBase(self.db_path)；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeWebApp.stats` (function, L114-L124)

**签名：** `def stats(self) -> dict[str, Any]`

**作用：** 执行 stats，涉及 self.open, str, knowledge_base.document_count, knowledge_base.chunk_count。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：dict[str, Any]；直接/间接调用：self.open, str, knowledge_base.document_count, knowledge_base.chunk_count；返回表达式：{'database': str(knowledge_base.db_path), 'documents': knowledge_base.document_count(), 'chunks': knowledge_base.chunk_count(), 'search_mode': 'semantic' if self.embedding_backend…；显式异常：未发现显式 raise；控制流：条件分支, 上下文管理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, stats, self.open, str, knowledge_base.document_count, knowledge_base.chunk_count, 条件分支, 上下文管理

**调用：** self.open, str, knowledge_base.document_count, knowledge_base.chunk_count；**返回：** {'database': str(knowledge_base.db_path), 'documents': knowledge_base.document_count(), 'chunks': knowledge_base.chunk_count(), 'search_mode': 'semantic' if self.embedding_backend…；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 模型/向量计算。

### `KnowledgeWebApp.documents` (function, L126-L141)

**签名：** `def documents(self) -> list[dict[str, Any]]`

**作用：** 执行 documents，涉及 self.open, knowledge_base.list_documents。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：list[dict[str, Any]]；直接/间接调用：self.open, knowledge_base.list_documents；返回表达式：[{'id': document.document_id, 'path': document.path, 'filename': document.filename, 'file_type': document.file_type, 'size': document.size, 'chunks': document.chunk_count, 'indexe…；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, documents, self.open, knowledge_base.list_documents, 上下文管理

**调用：** self.open, knowledge_base.list_documents；**返回：** [{'id': document.document_id, 'path': document.path, 'filename': document.filename, 'file_type': document.file_type, 'size': document.size, 'chunks': document.chunk_count, 'indexe…；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `KnowledgeWebApp.search` (function, L143-L192)

**签名：** `def search(self, query: str, limit: int=10, *, semantic: bool | None=None) -> list[dict[str, Any]]`

**作用：** 执行检索内部资源；内部调用 str.strip, ValueError, str, self.open, list。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, query: str, limit: int=10, *, semantic: bool | None=None；声明返回：list[dict[str, Any]]；直接/间接调用：str.strip, ValueError, str, self.open, list, _search_result_location, VectorIndex.search, knowledge_base.search, VectorIndex；返回表达式：[{'filename': result.filename, 'file_type': result.file_type, 'path': result.document_path, 'chunk_index': result.chunk_index, 'score': result.score, 'content': result.content, 'h…; []；显式异常：ValueError(f'搜索条数必须在 1 到 {_MAX_SEARCH_LIMIT} 之间。'); ValueError('语义检索未配置 Embedding 服务。')；控制流：条件分支, 上下文管理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, search, str.strip, ValueError, str, self.open, list, _search_result_location, VectorIndex.search, knowledge_base.search, VectorIndex, 条件分支, 上下文管理

**调用：** str.strip, ValueError, str, self.open, list, _search_result_location, VectorIndex.search, knowledge_base.search, VectorIndex；**返回：** [{'filename': result.filename, 'file_type': result.file_type, 'path': result.document_path, 'chunk_index': result.chunk_index, 'score': result.score, 'content': result.content, 'h…; []；**异常：** ValueError(f'搜索条数必须在 1 到 {_MAX_SEARCH_LIMIT} 之间。'); ValueError('语义检索未配置 Embedding 服务。')；**副作用：** 文件系统读写, 模型/向量计算。

### `KnowledgeWebApp.ask` (function, L194-L269)

**签名：** `def ask(self, question: str, config: RagConfig, *, semantic: bool | None=None) -> dict[str, Any]`

**作用：** 执行 ask，涉及 str.strip, ValueError, len, round, str。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, question: str, config: RagConfig, *, semantic: bool | None=None；声明返回：dict[str, Any]；直接/间接调用：str.strip, ValueError, len, round, str, self.open, RagAnswerer, VectorRetriever, ChunkRetriever, answerer.answer, list, Constant.join, _redact_error；返回表达式：{'question': result.question, 'answer': result.answer, 'refused': result.refused, 'elapsed_ms': round(result.elapsed_ms, 2), 'context_chars': result.context_chars, 'usage': {'prom…; {'error': _redact_error(str(exc))}；显式异常：ValueError('问题不能为空。'); ValueError(f'问题不能超过 {_MAX_QUESTION_CHARS} 个字符。'); ValueError('语义检索未配置 Embedding 服务。')；控制流：条件分支, 异常处理, 上下文管理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, ask, str.strip, ValueError, len, round, str, self.open, RagAnswerer, VectorRetriever, ChunkRetriever, answerer.answer, list, Constant.join, _redact_error, 条件分支, 异常处理, 上下文管理

**调用：** str.strip, ValueError, len, round, str, self.open, RagAnswerer, VectorRetriever, ChunkRetriever, answerer.answer, list, Constant.join, _redact_error；**返回：** {'question': result.question, 'answer': result.answer, 'refused': result.refused, 'elapsed_ms': round(result.elapsed_ms, 2), 'context_chars': result.context_chars, 'usage': {'prom…; {'error': _redact_error(str(exc))}；**异常：** ValueError('问题不能为空。'); ValueError(f'问题不能超过 {_MAX_QUESTION_CHARS} 个字符。'); ValueError('语义检索未配置 Embedding 服务。')；**副作用：** 文件系统读写, 模型/向量计算。

### `KnowledgeWebApp.index_paths` (function, L271-L302)

**签名：** `def index_paths(self, paths: list[Path], *, chunk_size: int=800, overlap: int=200) -> dict[str, Any]`

**作用：** 执行 index paths，涉及 ValueError, len, self.open, index_paths。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, paths: list[Path], *, chunk_size: int=800, overlap: int=200；声明返回：dict[str, Any]；直接/间接调用：ValueError, len, self.open, index_paths；返回表达式：{'files_found': stats.files_found, 'indexed': stats.indexed, 'skipped': stats.skipped, 'empty': stats.empty, 'failed': stats.failed, 'oversized': stats.oversized}；显式异常：ValueError('没有可索引的路径。'); ValueError(f'一次最多索引 {_MAX_INDEX_PATHS} 个路径。'); ValueError(f'chunk_size 必须在 1 到 {_MAX_CHUNK_SIZE} 之间。'); ValueError('overlap 必须大于等于 0 且小于 chunk_size。')；控制流：条件分支, 上下文管理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, index, paths, ValueError, len, self.open, index_paths, 条件分支, 上下文管理

**调用：** ValueError, len, self.open, index_paths；**返回：** {'files_found': stats.files_found, 'indexed': stats.indexed, 'skipped': stats.skipped, 'empty': stats.empty, 'failed': stats.failed, 'oversized': stats.oversized}；**异常：** ValueError('没有可索引的路径。'); ValueError(f'一次最多索引 {_MAX_INDEX_PATHS} 个路径。'); ValueError(f'chunk_size 必须在 1 到 {_MAX_CHUNK_SIZE} 之间。'); ValueError('overlap 必须大于等于 0 且小于 chunk_size。')；**副作用：** 文件系统读写, 模型/向量计算。

### `KnowledgeWebApp.remove` (function, L304-L313)

**签名：** `def remove(self, document_id: int) -> dict[str, Any]`

**作用：** 删除并清理内部资源；内部调用 ValueError, bool, self.open, self._path_for_id, knowledge_base.remove_document。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, document_id: int；声明返回：dict[str, Any]；直接/间接调用：ValueError, bool, self.open, self._path_for_id, knowledge_base.remove_document, Path；返回表达式：{'removed': bool(removed), 'path': path}; {'removed': False, 'reason': 'not_found'}；显式异常：ValueError('文档 ID 必须是正整数。')；控制流：条件分支, 上下文管理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, remove, ValueError, bool, self.open, self._path_for_id, knowledge_base.remove_document, Path, 条件分支, 上下文管理

**调用：** ValueError, bool, self.open, self._path_for_id, knowledge_base.remove_document, Path；**返回：** {'removed': bool(removed), 'path': path}; {'removed': False, 'reason': 'not_found'}；**异常：** ValueError('文档 ID 必须是正整数。')；**副作用：** 文件系统读写。

### `KnowledgeWebApp._path_for_id` (function, L316-L320)

**签名：** `def _path_for_id(knowledge_base: KnowledgeBase, document_id: int) -> str | None`

**作用：** 执行  path for id，涉及 knowledge_base.list_documents。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：knowledge_base: KnowledgeBase, document_id: int；声明返回：str | None；直接/间接调用：knowledge_base.list_documents；返回表达式：None; document.path；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, path, for, id, knowledge_base.list_documents, 条件分支, 循环

**调用：** knowledge_base.list_documents；**返回：** None; document.path；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeWebApp.save_upload` (function, L324-L359)

**签名：** `def save_upload(self, filename: str, data: bytes) -> tuple[str, str]`

**作用：** Persist an uploaded file and return its real path plus basename.

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, filename: str, data: bytes；声明返回：tuple[str, str]；直接/间接调用：str.replace, Path.suffix.lower, self.upload_dir.mkdir, self.upload_dir.resolve, target.exists, target.write_bytes, isinstance, ValueError, len, Path, str, target.resolve；返回表达式：(str(target.resolve()), target.name)；显式异常：ValueError('上传内容无效。'); ValueError('上传文件为空。'); ValueError('上传文件超过 512MB 上限。'); ValueError('上传文件缺少文件名。'); ValueError('上传文件名无效。'); ValueError('不支持的文件类型；仅支持 TXT、Markdown、PDF、PPTX、JSON、Python 和 C/C++。'); ValueError('上传路径无效。')；控制流：条件分支, 循环。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Web, App, save, upload, str.replace, Path.suffix.lower, self.upload_dir.mkdir, self.upload_dir.resolve, target.exists, target.write_bytes, isinstance, ValueError, len, Path, str, target.resolve, 条件分支, 循环

**调用：** str.replace, Path.suffix.lower, self.upload_dir.mkdir, self.upload_dir.resolve, target.exists, target.write_bytes, isinstance, ValueError, len, Path, str, target.resolve；**返回：** (str(target.resolve()), target.name)；**异常：** ValueError('上传内容无效。'); ValueError('上传文件为空。'); ValueError('上传文件超过 512MB 上限。'); ValueError('上传文件缺少文件名。'); ValueError('上传文件名无效。'); ValueError('不支持的文件类型；仅支持 TXT、Markdown、PDF、PPTX、JSON、Python 和 C/C++。'); ValueError('上传路径无效。')；**副作用：** 文件系统读写。

### `_redact_error` (function, L362-L375)

**签名：** `def _redact_error(message: str) -> str`

**作用：** Remove credentials from errors returned through the browser API.

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：message: str；声明返回：str；直接/间接调用：LLMClient.load_dotenv, os.environ.get, message.replace；返回表达式：message；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, redact, error, LLMClient.load_dotenv, os.environ.get, message.replace, 条件分支

**调用：** LLMClient.load_dotenv, os.environ.get, message.replace；**返回：** message；**异常：** 未发现显式 raise；**副作用：** 环境变量读取。

### `KnowledgeRequestHandler` (class, L378-L598)

**签名：** `class KnowledgeRequestHandler`

**作用：** Route HTTP requests to :class:`KnowledgeWebApp`.

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；类体包含 11 个直接方法。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeRequestHandler.app` (function, L388-L389)

**签名：** `def app(self) -> KnowledgeWebApp`

**作用：** 执行 app。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：KnowledgeWebApp；直接/间接调用：无明显函数调用；返回表达式：self.server.app；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, app

**调用：** 无明显调用；**返回：** self.server.app；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeRequestHandler.rag_config` (function, L392-L393)

**签名：** `def rag_config(self) -> RagConfig`

**作用：** 执行 rag config，涉及 self.server.rag_config。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：RagConfig；直接/间接调用：self.server.rag_config；返回表达式：self.server.rag_config()；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, rag, config, self.server.rag_config

**调用：** self.server.rag_config；**返回：** self.server.rag_config()；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeRequestHandler.log_message` (function, L395-L396)

**签名：** `def log_message(self, format: str, *args: Any) -> None`

**作用：** 执行 log message，涉及 logger.info, self.address_string。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, format: str, *args: Any；声明返回：None；直接/间接调用：logger.info, self.address_string；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, log, message, logger.info, self.address_string

**调用：** logger.info, self.address_string；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `KnowledgeRequestHandler._send_json` (function, L400-L407)

**签名：** `def _send_json(self, payload: Any, status: int=HTTPStatus.OK) -> None`

**作用：** 执行  send json，涉及 json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, payload: Any, status: int=HTTPStatus.OK；声明返回：None；直接/间接调用：json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write, str, json.dumps, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, send, json, json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write, str, json.dumps, len

**调用：** json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write, str, json.dumps, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `KnowledgeRequestHandler._read_json` (function, L409-L420)

**签名：** `def _read_json(self) -> Any`

**作用：** 执行  read json，涉及 self.rfile.read, int, ValueError, json.loads, raw.decode。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：Any；直接/间接调用：self.rfile.read, int, ValueError, json.loads, raw.decode, self.headers.get；返回表达式：json.loads(raw.decode('utf-8'))；显式异常：ValueError('请求体无效或过大。'); ValueError('请求体长度无效。'); ValueError('请求体不是有效 JSON。')；控制流：条件分支, 异常处理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, read, json, self.rfile.read, int, ValueError, json.loads, raw.decode, self.headers.get, 条件分支, 异常处理

**调用：** self.rfile.read, int, ValueError, json.loads, raw.decode, self.headers.get；**返回：** json.loads(raw.decode('utf-8'))；**异常：** ValueError('请求体无效或过大。'); ValueError('请求体长度无效。'); ValueError('请求体不是有效 JSON。')；**副作用：** 文件系统读写。

### `KnowledgeRequestHandler._read_json_object` (function, L422-L426)

**签名：** `def _read_json_object(self) -> dict[str, Any]`

**作用：** 执行  read json object，涉及 self._read_json, isinstance, ValueError。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：dict[str, Any]；直接/间接调用：self._read_json, isinstance, ValueError；返回表达式：payload；显式异常：ValueError('JSON 请求体必须是对象。')；控制流：条件分支。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, read, json, object, self._read_json, isinstance, ValueError, 条件分支

**调用：** self._read_json, isinstance, ValueError；**返回：** payload；**异常：** ValueError('JSON 请求体必须是对象。')；**副作用：** 未发现明显外部副作用。

### `KnowledgeRequestHandler._static` (function, L428-L446)

**签名：** `def _static(self, path: str) -> None`

**作用：** 执行  static，涉及 urllib.parse.unquote, BinOp.resolve, candidate.read_bytes, self.send_response, self.send_header。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, path: str；声明返回：None；直接/间接调用：urllib.parse.unquote, BinOp.resolve, candidate.read_bytes, self.send_response, self.send_header, self.end_headers, self.wfile.write, path.lstrip, self.send_error, candidate.is_file, str, mimetypes.guess_type, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, static, urllib.parse.unquote, BinOp.resolve, candidate.read_bytes, self.send_response, self.send_header, self.end_headers, self.wfile.write, path.lstrip, self.send_error, candidate.is_file, str, mimetypes.guess_type, len, 条件分支

**调用：** urllib.parse.unquote, BinOp.resolve, candidate.read_bytes, self.send_response, self.send_header, self.end_headers, self.wfile.write, path.lstrip, self.send_error, candidate.is_file, str, mimetypes.guess_type, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 网络 HTTP 请求。

### `KnowledgeRequestHandler.do_GET` (function, L450-L487)

**签名：** `def do_GET(self) -> None`

**作用：** 执行 do GET，涉及 urllib.parse.urlsplit, urllib.parse.parse_qs, self.send_error, self._static, self._send_json。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：None；直接/间接调用：urllib.parse.urlsplit, urllib.parse.parse_qs, self.send_error, self._static, self._send_json, Subscript.strip, logger.warning, self.app.stats, int, self.app.documents, ValueError, query.get, self.app.search, str, _semantic_option；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('limit 必须是整数。')；控制流：条件分支, 异常处理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, do, GET, urllib.parse.urlsplit, urllib.parse.parse_qs, self.send_error, self._static, self._send_json, Subscript.strip, logger.warning, self.app.stats, int, self.app.documents, ValueError, query.get, self.app.search, str, _semantic_option, 条件分支, 异常处理

**调用：** urllib.parse.urlsplit, urllib.parse.parse_qs, self.send_error, self._static, self._send_json, Subscript.strip, logger.warning, self.app.stats, int, self.app.documents, ValueError, query.get, self.app.search, str, _semantic_option；**返回：** 未记录；**异常：** ValueError('limit 必须是整数。')；**副作用：** 网络 HTTP 请求, 日志输出。

### `KnowledgeRequestHandler.do_POST` (function, L489-L563)

**签名：** `def do_POST(self) -> None`

**作用：** 执行 do POST，涉及 urllib.parse.urlsplit, self.send_error, self._read_json_object, str.strip, int。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：None；直接/间接调用：urllib.parse.urlsplit, self.send_error, self._read_json_object, str.strip, int, self._send_json, self._config_from, payload.get, self._read_upload, self.app.save_upload, self.app.index_paths, logger.exception, ValueError, self.app.ask, Path.expanduser, self.app.remove, str, self.app.search, isinstance, all, Path, _semantic_option, item.strip；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：ValueError('问题不能为空。'); ValueError('paths 必须是非空字符串数组。'); ValueError('没有可索引的路径。')；控制流：条件分支, 异常处理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, do, POST, urllib.parse.urlsplit, self.send_error, self._read_json_object, str.strip, int, self._send_json, self._config_from, payload.get, self._read_upload, self.app.save_upload, self.app.index_paths, logger.exception, ValueError, self.app.ask, Path.expanduser, self.app.remove, str, self.app.search, isinstance, all, Path, _semantic_option, item.strip, 条件分支, 异常处理

**调用：** urllib.parse.urlsplit, self.send_error, self._read_json_object, str.strip, int, self._send_json, self._config_from, payload.get, self._read_upload, self.app.save_upload, self.app.index_paths, logger.exception, ValueError, self.app.ask, Path.expanduser, self.app.remove, str, self.app.search, isinstance, all, Path, _semantic_option, item.strip；**返回：** 未记录；**异常：** ValueError('问题不能为空。'); ValueError('paths 必须是非空字符串数组。'); ValueError('没有可索引的路径。')；**副作用：** 文件系统读写, 网络 HTTP 请求, 日志输出。

### `KnowledgeRequestHandler._config_from` (function, L565-L582)

**签名：** `def _config_from(self, payload: dict[str, Any], base: RagConfig) -> RagConfig`

**作用：** 执行  config from，涉及 RagConfig, int, float, ValueError, payload.get。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self, payload: dict[str, Any], base: RagConfig；声明返回：RagConfig；直接/间接调用：RagConfig, int, float, ValueError, payload.get；返回表达式：RagConfig(top_k=top_k, max_context_chars=max_context_chars, temperature=temperature)；显式异常：ValueError(f'top_k 不能超过 {_MAX_SEARCH_LIMIT}。'); ValueError(f'max_context_chars 不能超过 {_MAX_CONTEXT_CHARS}。'); ValueError('问答参数类型无效。')；控制流：条件分支, 异常处理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, config, from, RagConfig, int, float, ValueError, payload.get, 条件分支, 异常处理

**调用：** RagConfig, int, float, ValueError, payload.get；**返回：** RagConfig(top_k=top_k, max_context_chars=max_context_chars, temperature=temperature)；**异常：** ValueError(f'top_k 不能超过 {_MAX_SEARCH_LIMIT}。'); ValueError(f'max_context_chars 不能超过 {_MAX_CONTEXT_CHARS}。'); ValueError('问答参数类型无效。')；**副作用：** 未发现明显外部副作用。

### `KnowledgeRequestHandler._read_upload` (function, L584-L598)

**签名：** `def _read_upload(self) -> tuple[str, bytes]`

**作用：** 执行  read upload，涉及 self.headers.get, self.rfile.read, _parse_multipart, content_type.startswith, ValueError。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：self；声明返回：tuple[str, bytes]；直接/间接调用：self.headers.get, self.rfile.read, _parse_multipart, content_type.startswith, ValueError, int, len；返回表达式：(filename, data)；显式异常：ValueError('上传请求必须是 multipart/form-data。'); ValueError('上传文件无效或超过大小上限。'); ValueError('上传文件超过 512MB 上限。'); ValueError('上传请求长度无效。')；控制流：条件分支, 异常处理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, Knowledge, Request, Handler, read, upload, self.headers.get, self.rfile.read, _parse_multipart, content_type.startswith, ValueError, int, len, 条件分支, 异常处理

**调用：** self.headers.get, self.rfile.read, _parse_multipart, content_type.startswith, ValueError, int, len；**返回：** (filename, data)；**异常：** ValueError('上传请求必须是 multipart/form-data。'); ValueError('上传文件无效或超过大小上限。'); ValueError('上传文件超过 512MB 上限。'); ValueError('上传请求长度无效。')；**副作用：** 文件系统读写。

### `_parse_multipart` (function, L601-L638)

**签名：** `def _parse_multipart(body: bytes, content_type: str) -> tuple[str, bytes]`

**作用：** Minimal multipart parser for a single file part.

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：body: bytes, content_type: str；声明返回：tuple[str, bytes]；直接/间接调用：re.search, boundary_text.encode, body.split, ValueError, match.group, segment.find, Subscript.decode, header_block.split, headers.get, _extract_quoted, Subscript.rstrip, len, segment.strip, disposition.lower, line.split, value.strip, key.strip.lower, key.strip；返回表达式：(filename, data)；显式异常：ValueError('multipart 请求中没有文件。'); ValueError('multipart 请求缺少 boundary。'); ValueError('multipart boundary 无效。'); ValueError('multipart 请求体无效。')；控制流：条件分支, 循环。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, parse, multipart, re.search, boundary_text.encode, body.split, ValueError, match.group, segment.find, Subscript.decode, header_block.split, headers.get, _extract_quoted, Subscript.rstrip, len, segment.strip, disposition.lower, line.split, value.strip, key.strip.lower, key.strip, 条件分支, 循环

**调用：** re.search, boundary_text.encode, body.split, ValueError, match.group, segment.find, Subscript.decode, header_block.split, headers.get, _extract_quoted, Subscript.rstrip, len, segment.strip, disposition.lower, line.split, value.strip, key.strip.lower, key.strip；**返回：** (filename, data)；**异常：** ValueError('multipart 请求中没有文件。'); ValueError('multipart 请求缺少 boundary。'); ValueError('multipart boundary 无效。'); ValueError('multipart 请求体无效。')；**副作用：** 未发现明显外部副作用。

### `_extract_quoted` (function, L641-L652)

**签名：** `def _extract_quoted(header: str, key: str) -> str`

**作用：** 执行  extract quoted，涉及 re.search, match.groups, BoolOp.strip, quoted.replace.replace, re.escape。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：header: str, key: str；声明返回：str；直接/间接调用：re.search, match.groups, BoolOp.strip, quoted.replace.replace, re.escape, quoted.replace；返回表达式：(bare or '').strip(); ''; quoted.replace('\\"', '"').replace('\\\\', '\\')；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, extract, quoted, re.search, match.groups, BoolOp.strip, quoted.replace.replace, re.escape, quoted.replace, 条件分支

**调用：** re.search, match.groups, BoolOp.strip, quoted.replace.replace, re.escape, quoted.replace；**返回：** (bare or '').strip(); ''; quoted.replace('\\"', '"').replace('\\\\', '\\')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_semantic_option` (function, L655-L665)

**签名：** `def _semantic_option(payload: dict[str, Any]) -> bool | None`

**作用：** Parse the optional retrieval mode without breaking old API clients.

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：payload: dict[str, Any]；声明返回：bool | None；直接/间接调用：payload.get, ValueError；返回表达式：None; True; False；显式异常：ValueError('mode 必须是 semantic、vector 或 keyword。')；控制流：条件分支。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, semantic, option, payload.get, ValueError, 条件分支

**调用：** payload.get, ValueError；**返回：** None; True; False；**异常：** ValueError('mode 必须是 semantic、vector 或 keyword。')；**副作用：** SQLite/数据库写入或查询。

### `create_server` (function, L668-L678)

**签名：** `def create_server(app: KnowledgeWebApp, rag_config: Callable[[], RagConfig], host: str='127.0.0.1', port: int=8000) -> ThreadingHTTPServer`

**作用：** 执行 create server，涉及 _ExclusiveThreadingHTTPServer。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：app: KnowledgeWebApp, rag_config: Callable[[], RagConfig], host: str='127.0.0.1', port: int=8000；声明返回：ThreadingHTTPServer；直接/间接调用：_ExclusiveThreadingHTTPServer；返回表达式：server；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, create, server, _ExclusiveThreadingHTTPServer

**调用：** _ExclusiveThreadingHTTPServer；**返回：** server；**异常：** 未发现显式 raise；**副作用：** 网络 HTTP 请求。

### `run_web` (function, L681-L716)

**签名：** `def run_web(*, db_path: Path, host: str='127.0.0.1', port: int=8000, upload_dir: Path=DEFAULT_UPLOAD_DIR, embedding_backend: EmbeddingBackend | None=None) -> None`

**作用：** Start the blocking web server for CLI use.

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：*, db_path: Path, host: str='127.0.0.1', port: int=8000, upload_dir: Path=DEFAULT_UPLOAD_DIR, embedding_backend: EmbeddingBackend | None=None；声明返回：None；直接/间接调用：KnowledgeWebApp, Path, logger.info, rag_config_path.exists, RagConfig, create_server, server.serve_forever, server.server_close, RagConfig.from_file, RuntimeError, getattr, Path.resolve；返回表达式：RagConfig(); RagConfig.from_file(rag_config_path)；显式异常：裸 raise; RuntimeError(f'端口 {port} 已被占用，Web 服务未启动。')；控制流：条件分支, 异常处理。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, run, web, KnowledgeWebApp, Path, logger.info, rag_config_path.exists, RagConfig, create_server, server.serve_forever, server.server_close, RagConfig.from_file, RuntimeError, getattr, Path.resolve, 条件分支, 异常处理

**调用：** KnowledgeWebApp, Path, logger.info, rag_config_path.exists, RagConfig, create_server, server.serve_forever, server.server_close, RagConfig.from_file, RuntimeError, getattr, Path.resolve；**返回：** RagConfig(); RagConfig.from_file(rag_config_path)；**异常：** 裸 raise; RuntimeError(f'端口 {port} 已被占用，Web 服务未启动。')；**副作用：** 文件系统读写, 日志输出, 模型/向量计算。

### `run_web.load_config` (function, L699-L702)

**签名：** `def load_config() -> RagConfig`

**作用：** 加载并校验config；内部调用 rag_config_path.exists, RagConfig, RagConfig.from_file。

**详细语义：** 所属模块职责：提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。；输入参数：；声明返回：RagConfig；直接/间接调用：rag_config_path.exists, RagConfig, RagConfig.from_file；返回表达式：RagConfig(); RagConfig.from_file(rag_config_path)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Web API, HTTP, 上传, 安全边界, 并发, run, web, load, config, rag_config_path.exists, RagConfig, RagConfig.from_file, 条件分支

**调用：** rag_config_path.exists, RagConfig, RagConfig.from_file；**返回：** RagConfig(); RagConfig.from_file(rag_config_path)；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

## personal_local_knowledge_base_v0/knowledge_search/web/static/app.css

**文件作用：** 网页单页应用的视觉样式、布局、状态色、响应式断点和组件外观。

**语言/关键词：** CSS, 布局, 响应式, 视觉状态, css

**函数/类/脚本记录数：** 1

### `<module>.__main__` (script, L1-L276)

**签名：** `module-level script`

**作用：** 网页单页应用的视觉样式、布局、状态色、响应式断点和组件外观。

**详细语义：** 脚本语言：CSS；无可声明的命名函数，主体按顺序执行。核心命令/操作：参数校验、文件处理和流程控制。

**关键词：** CSS, 布局, 响应式, 视觉状态

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/web/static/app.js

**文件作用：** 网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。

**语言/关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, JavaScript, js

**函数/类/脚本记录数：** 33

### `$` (function, L3-L15)

**签名：** `$ = (selector) =>`

**作用：** 执行 $，涉及 querySelector, from, querySelectorAll, toast, toggle。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：$ = (selector) =>；调用：querySelector, from, querySelectorAll, toast, toggle, clearTimeout, setTimeout；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, querySelector, from, querySelectorAll, toast, toggle, clearTimeout, setTimeout, 条件分支, JavaScript

**调用：** querySelector, from, querySelectorAll, toast, toggle, clearTimeout, setTimeout；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `$$` (function, L4-L15)

**签名：** `$$ = (selector) =>`

**作用：** 执行 $$，涉及 from, querySelectorAll, toast, toggle, clearTimeout。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：$$ = (selector) =>；调用：from, querySelectorAll, toast, toggle, clearTimeout, setTimeout；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, from, querySelectorAll, toast, toggle, clearTimeout, setTimeout, 条件分支, JavaScript

**调用：** from, querySelectorAll, toast, toggle, clearTimeout, setTimeout；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `toast` (function, L8-L15)

**签名：** `function toast(message, isError = false)`

**作用：** 执行 toast，涉及 toast, toggle, clearTimeout, setTimeout。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：function toast(message, isError = false)；调用：toast, toggle, clearTimeout, setTimeout；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, toast, toggle, clearTimeout, setTimeout, 条件分支, JavaScript

**调用：** toast, toggle, clearTimeout, setTimeout；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@14` (function, L14-L14)

**签名：** `anonymous_arrow@14 = () =>`

**作用：** 匿名回调：执行 anonymous arrow@14。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@14 = () =>；调用：无明显调用；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 14, JavaScript

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `escapeHtml` (function, L16-L289)

**签名：** `function escapeHtml(value)`

**作用：** 执行 escapeHtml，涉及 escapeHtml, String, replace, formatBytes, Number。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：function escapeHtml(value)；调用：escapeHtml, String, replace, formatBytes, Number, toFixed, api, fetch, json, Error, forEach, addEventListener, toggle, setAttribute, loadStats, async, preventDefault, trim, encodeURIComponent, renderSearch, map；控制流：条件分支, 循环/集合遍历, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, escape, Html, escapeHtml, String, replace, formatBytes, Number, toFixed, api, fetch, json, Error, forEach, addEventListener, toggle, setAttribute, loadStats, async, preventDefault, trim, encodeURIComponent, renderSearch, map, 条件分支, 循环/集合遍历, 异常处理, 异步等待, JavaScript

**调用：** escapeHtml, String, replace, formatBytes, Number, toFixed, api, fetch, json, Error, forEach, addEventListener, toggle, setAttribute, loadStats, async, preventDefault, trim, encodeURIComponent, renderSearch, map；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 网络 HTTP 请求。

### `formatBytes` (function, L25-L33)

**签名：** `function formatBytes(bytes)`

**作用：** 执行 formatBytes，涉及 formatBytes, Number, toFixed。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：function formatBytes(bytes)；调用：formatBytes, Number, toFixed；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, format, Bytes, formatBytes, Number, toFixed, 条件分支, JavaScript

**调用：** formatBytes, Number, toFixed；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `api` (function, L34-L47)

**签名：** `async function api(path, options = {})`

**作用：** 执行 api，涉及 api, fetch, json, Error。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：async function api(path, options = {})；调用：api, fetch, json, Error；控制流：条件分支, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, api, fetch, json, Error, 条件分支, 异常处理, 异步等待, JavaScript

**调用：** api, fetch, json, Error；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 网络 HTTP 请求。

### `anonymous_arrow@50` (function, L50-L61)

**签名：** `anonymous_arrow@50 = (tab) =>`

**作用：** 匿名回调：执行 anonymous arrow@50，涉及 addEventListener, forEach, toggle, setAttribute, String。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@50 = (tab) =>；调用：addEventListener, forEach, toggle, setAttribute, String；控制流：循环/集合遍历；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 50, addEventListener, forEach, toggle, setAttribute, String, 循环/集合遍历, JavaScript

**调用：** addEventListener, forEach, toggle, setAttribute, String；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@51` (function, L51-L60)

**签名：** `anonymous_arrow@51 = () =>`

**作用：** 匿名回调：执行 anonymous arrow@51，涉及 forEach, toggle, setAttribute, String。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@51 = () =>；调用：forEach, toggle, setAttribute, String；控制流：循环/集合遍历；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 51, forEach, toggle, setAttribute, String, 循环/集合遍历, JavaScript

**调用：** forEach, toggle, setAttribute, String；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@52` (function, L52-L56)

**签名：** `anonymous_arrow@52 = (t) =>`

**作用：** 匿名回调：执行 anonymous arrow@52，涉及 toggle, setAttribute, String。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@52 = (t) =>；调用：toggle, setAttribute, String；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 52, toggle, setAttribute, String, JavaScript

**调用：** toggle, setAttribute, String；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@57` (function, L57-L59)

**签名：** `anonymous_arrow@57 = (panel) =>`

**作用：** 匿名回调：执行 anonymous arrow@57。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@57 = (panel) =>；调用：无明显调用；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 57, JavaScript

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `loadStats` (function, L64-L76)

**签名：** `async function loadStats()`

**作用：** 执行 loadStats，涉及 loadStats, api。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：async function loadStats()；调用：loadStats, api；控制流：条件分支, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, load, Stats, loadStats, api, 条件分支, 异常处理, 异步等待, JavaScript

**调用：** loadStats, api；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@79` (function, L79-L91)

**签名：** `async anonymous_arrow@79 = (event) =>`

**作用：** 匿名回调：执行 anonymous arrow@79，涉及 async, preventDefault, trim, api, encodeURIComponent。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：async anonymous_arrow@79 = (event) =>；调用：async, preventDefault, trim, api, encodeURIComponent, renderSearch, escapeHtml；控制流：条件分支, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 79, async, preventDefault, trim, api, encodeURIComponent, renderSearch, escapeHtml, 条件分支, 异常处理, 异步等待, JavaScript

**调用：** async, preventDefault, trim, api, encodeURIComponent, renderSearch, escapeHtml；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `renderSearch` (function, L92-L110)

**签名：** `function renderSearch(results)`

**作用：** 执行 renderSearch，涉及 renderSearch, map, escapeHtml, Number, toFixed。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：function renderSearch(results)；调用：renderSearch, map, escapeHtml, Number, toFixed, highlightedContent, join；控制流：条件分支, 循环/集合遍历；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, render, Search, renderSearch, map, escapeHtml, Number, toFixed, highlightedContent, join, 条件分支, 循环/集合遍历, JavaScript

**调用：** renderSearch, map, escapeHtml, Number, toFixed, highlightedContent, join；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@99` (function, L99-L102)

**签名：** `anonymous_arrow@99 = (result) =>`

**作用：** 匿名回调：执行 anonymous arrow@99，涉及 escapeHtml。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@99 = (result) =>；调用：escapeHtml；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 99, escapeHtml, JavaScript

**调用：** escapeHtml；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `highlightedContent` (function, L111-L120)

**签名：** `function highlightedContent(html)`

**作用：** 执行 highlightedContent，涉及 highlightedContent, String, replace。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：function highlightedContent(html)；调用：highlightedContent, String, replace；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, highlighted, Content, highlightedContent, String, replace, JavaScript

**调用：** highlightedContent, String, replace；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@123` (function, L123-L146)

**签名：** `async anonymous_arrow@123 = (event) =>`

**作用：** 匿名回调：执行 anonymous arrow@123，涉及 async, preventDefault, trim, toast, parseInt。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：async anonymous_arrow@123 = (event) =>；调用：async, preventDefault, trim, toast, parseInt, parseFloat, api, stringify, renderAnswer, escapeHtml；控制流：条件分支, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 123, async, preventDefault, trim, toast, parseInt, parseFloat, api, stringify, renderAnswer, escapeHtml, 条件分支, 异常处理, 异步等待, JavaScript

**调用：** async, preventDefault, trim, toast, parseInt, parseFloat, api, stringify, renderAnswer, escapeHtml；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `renderAnswer` (function, L147-L176)

**签名：** `function renderAnswer(data)`

**作用：** 执行 renderAnswer，涉及 renderAnswer, escapeHtml, map, join。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：function renderAnswer(data)；调用：renderAnswer, escapeHtml, map, join；控制流：条件分支, 循环/集合遍历；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, render, Answer, renderAnswer, escapeHtml, map, join, 条件分支, 循环/集合遍历, JavaScript

**调用：** renderAnswer, escapeHtml, map, join；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@156` (function, L156-L158)

**签名：** `anonymous_arrow@156 = (source) =>`

**作用：** 匿名回调：执行 anonymous arrow@156。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@156 = (source) =>；调用：无明显调用；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 156, JavaScript

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@181` (function, L181-L182)

**签名：** `anonymous_arrow@181 = () =>`

**作用：** 匿名回调：执行 anonymous arrow@181，涉及 click, addEventListener, preventDefault, var。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@181 = () =>；调用：click, addEventListener, preventDefault, var；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 181, click, addEventListener, preventDefault, var, JavaScript

**调用：** click, addEventListener, preventDefault, var；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@182` (function, L182-L182)

**签名：** `anonymous_arrow@182 = (event) =>`

**作用：** 匿名回调：执行 anonymous arrow@182，涉及 preventDefault, var。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@182 = (event) =>；调用：preventDefault, var；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 182, preventDefault, var, JavaScript

**调用：** preventDefault, var；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@183` (function, L183-L183)

**签名：** `anonymous_arrow@183 = () =>`

**作用：** 匿名回调：执行 anonymous arrow@183。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@183 = () =>；调用：无明显调用；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 183, JavaScript

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@184` (function, L184-L188)

**签名：** `anonymous_arrow@184 = (event) =>`

**作用：** 匿名回调：执行 anonymous arrow@184，涉及 preventDefault, uploadFiles。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@184 = (event) =>；调用：preventDefault, uploadFiles；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 184, preventDefault, uploadFiles, 条件分支, JavaScript

**调用：** preventDefault, uploadFiles；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@189` (function, L189-L191)

**签名：** `anonymous_arrow@189 = () =>`

**作用：** 匿名回调：执行 anonymous arrow@189，涉及 uploadFiles。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@189 = () =>；调用：uploadFiles；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 189, uploadFiles, 条件分支, JavaScript

**调用：** uploadFiles；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `uploadFiles` (function, L192-L211)

**签名：** `async function uploadFiles(files)`

**作用：** 执行 uploadFiles，涉及 uploadFiles, escapeHtml, FormData, append, fetch。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：async function uploadFiles(files)；调用：uploadFiles, escapeHtml, FormData, append, fetch, json, Error, loadStats；控制流：条件分支, 循环/集合遍历, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, upload, Files, uploadFiles, escapeHtml, FormData, append, fetch, json, Error, loadStats, 条件分支, 循环/集合遍历, 异常处理, 异步等待, JavaScript

**调用：** uploadFiles, escapeHtml, FormData, append, fetch, json, Error, loadStats；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 网络 HTTP 请求。

### `anonymous_arrow@214` (function, L214-L230)

**签名：** `async anonymous_arrow@214 = (event) =>`

**作用：** 匿名回调：执行 anonymous arrow@214，涉及 async, preventDefault, trim, escapeHtml, api。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：async anonymous_arrow@214 = (event) =>；调用：async, preventDefault, trim, escapeHtml, api, stringify, loadStats；控制流：条件分支, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 214, async, preventDefault, trim, escapeHtml, api, stringify, loadStats, 条件分支, 异常处理, 异步等待, JavaScript

**调用：** async, preventDefault, trim, escapeHtml, api, stringify, loadStats；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `loadDocuments` (function, L233-L242)

**签名：** `async function loadDocuments()`

**作用：** 执行 loadDocuments，涉及 loadDocuments, api, renderDocuments, escapeHtml。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：async function loadDocuments()；调用：loadDocuments, api, renderDocuments, escapeHtml；控制流：异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, load, Documents, loadDocuments, api, renderDocuments, escapeHtml, 异常处理, 异步等待, JavaScript

**调用：** loadDocuments, api, renderDocuments, escapeHtml；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `renderDocuments` (function, L243-L280)

**签名：** `function renderDocuments(documents)`

**作用：** 执行 renderDocuments，涉及 renderDocuments, map, escapeHtml, formatBytes, join。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：function renderDocuments(documents)；调用：renderDocuments, map, escapeHtml, formatBytes, join, forEach, addEventListener, async, confirm, api, stringify, parseInt, toast, loadDocuments, loadStats；控制流：条件分支, 循环/集合遍历, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, render, Documents, renderDocuments, map, escapeHtml, formatBytes, join, forEach, addEventListener, async, confirm, api, stringify, parseInt, toast, loadDocuments, loadStats, 条件分支, 循环/集合遍历, 异常处理, 异步等待, JavaScript

**调用：** renderDocuments, map, escapeHtml, formatBytes, join, forEach, addEventListener, async, confirm, api, stringify, parseInt, toast, loadDocuments, loadStats；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@250` (function, L250-L251)

**签名：** `anonymous_arrow@250 = (doc) =>`

**作用：** 匿名回调：执行 anonymous arrow@250。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@250 = (doc) =>；调用：无明显调用；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 250, JavaScript

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@264` (function, L264-L279)

**签名：** `anonymous_arrow@264 = (button) =>`

**作用：** 匿名回调：执行 anonymous arrow@264，涉及 addEventListener, async, confirm, api, stringify。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@264 = (button) =>；调用：addEventListener, async, confirm, api, stringify, parseInt, toast, loadDocuments, loadStats；控制流：条件分支, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 264, addEventListener, async, confirm, api, stringify, parseInt, toast, loadDocuments, loadStats, 条件分支, 异常处理, 异步等待, JavaScript

**调用：** addEventListener, async, confirm, api, stringify, parseInt, toast, loadDocuments, loadStats；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@265` (function, L265-L278)

**签名：** `async anonymous_arrow@265 = () =>`

**作用：** 匿名回调：执行 anonymous arrow@265，涉及 async, confirm, api, stringify, parseInt。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：async anonymous_arrow@265 = () =>；调用：async, confirm, api, stringify, parseInt, toast, loadDocuments, loadStats；控制流：条件分支, 异常处理, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 265, async, confirm, api, stringify, parseInt, toast, loadDocuments, loadStats, 条件分支, 异常处理, 异步等待, JavaScript

**调用：** async, confirm, api, stringify, parseInt, toast, loadDocuments, loadStats；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@283` (function, L283-L287)

**签名：** `anonymous_arrow@283 = (tab) =>`

**作用：** 匿名回调：执行 anonymous arrow@283，涉及 addEventListener, loadDocuments。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@283 = (tab) =>；调用：addEventListener, loadDocuments；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 283, addEventListener, loadDocuments, 条件分支, JavaScript

**调用：** addEventListener, loadDocuments；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@284` (function, L284-L286)

**签名：** `anonymous_arrow@284 = () =>`

**作用：** 匿名回调：执行 anonymous arrow@284，涉及 loadDocuments。

**详细语义：** 所属模块职责：网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。；JavaScript 输入签名：anonymous_arrow@284 = () =>；调用：loadDocuments；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** 前端, Fetch API, DOM, 搜索, 问答, 上传, anonymous, arrow, 284, loadDocuments, 条件分支, JavaScript

**调用：** loadDocuments；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/knowledge_search/web/static/index.html

**文件作用：** 网页单页应用的语义结构和表单骨架，定义搜索、问答、导入、文档管理视图及可访问性标记。

**语言/关键词：** HTML, 网页结构, 表单, 可访问性, html

**函数/类/脚本记录数：** 1

### `<module>.__main__` (script, L1-L131)

**签名：** `module-level script`

**作用：** 网页单页应用的语义结构和表单骨架，定义搜索、问答、导入、文档管理视图及可访问性标记。

**详细语义：** 脚本语言：HTML；无可声明的命名函数，主体按顺序执行。核心命令/操作：Python。

**关键词：** HTML, 网页结构, 表单, 可访问性

**调用：** Python；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

## personal_local_knowledge_base_v0/scripts/clean_rag_log.py

**文件作用：** 清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。

**语言/关键词：** 评估, 日志清洗, 事实核对, 引用验证, Python, py

**函数/类/脚本记录数：** 8

### `normalize` (function, L18-L20)

**签名：** `def normalize(text: str) -> str`

**作用：** 规范化并适配内部资源；内部调用 re.sub.casefold, text.replace.replace.replace, re.sub, text.replace.replace, text.replace。

**详细语义：** 所属模块职责：清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。；输入参数：text: str；声明返回：str；直接/间接调用：re.sub.casefold, text.replace.replace.replace, re.sub, text.replace.replace, text.replace；返回表达式：text.replace('：', '比').replace('∶', '比').replace(':', '比')；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 评估, 日志清洗, 事实核对, 引用验证, normalize, re.sub.casefold, text.replace.replace.replace, re.sub, text.replace.replace, text.replace

**调用：** re.sub.casefold, text.replace.replace.replace, re.sub, text.replace.replace, text.replace；**返回：** text.replace('：', '比').replace('∶', '比').replace(':', '比')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `contains_any` (function, L23-L25)

**签名：** `def contains_any(text: str, alternatives: list[str]) -> bool`

**作用：** 执行 contains any，涉及 normalize, any。

**详细语义：** 所属模块职责：清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。；输入参数：text: str, alternatives: list[str]；声明返回：bool；直接/间接调用：normalize, any；返回表达式：any((normalize(value) in normalized for value in alternatives))；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 评估, 日志清洗, 事实核对, 引用验证, contains, any, normalize

**调用：** normalize, any；**返回：** any((normalize(value) in normalized for value in alternatives))；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `read_records` (function, L28-L35)

**签名：** `def read_records(path: Path) -> list[dict[str, Any]]`

**作用：** 执行 read records，涉及 path.read_text.splitlines, records.append, path.read_text, line.split, json.loads。

**详细语义：** 所属模块职责：清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。；输入参数：path: Path；声明返回：list[dict[str, Any]]；直接/间接调用：path.read_text.splitlines, records.append, path.read_text, line.split, json.loads；返回表达式：records；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 评估, 日志清洗, 事实核对, 引用验证, read, records, path.read_text.splitlines, records.append, path.read_text, line.split, json.loads, 条件分支, 循环

**调用：** path.read_text.splitlines, records.append, path.read_text, line.split, json.loads；**返回：** records；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `relevant_excerpt` (function, L38-L56)

**签名：** `def relevant_excerpt(evidence: str, facts: list[dict[str, Any]]) -> str`

**作用：** 执行 relevant excerpt，涉及 re.sub.strip, compact.casefold, sorted, Constant.join, re.sub。

**详细语义：** 所属模块职责：清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。；输入参数：evidence: str, facts: list[dict[str, Any]]；声明返回：str；直接/间接调用：re.sub.strip, compact.casefold, sorted, Constant.join, re.sub, lowered.find, merged.append, re.sub.casefold, spans.append, max, Subscript.strip, min, len；返回表达式：' ... '.join((compact[start:end].strip() for start, end in merged))[:1200]; compact[:400]；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 评估, 日志清洗, 事实核对, 引用验证, relevant, excerpt, re.sub.strip, compact.casefold, sorted, Constant.join, re.sub, lowered.find, merged.append, re.sub.casefold, spans.append, max, Subscript.strip, min, len, 条件分支, 循环

**调用：** re.sub.strip, compact.casefold, sorted, Constant.join, re.sub, lowered.find, merged.append, re.sub.casefold, spans.append, max, Subscript.strip, min, len；**返回：** ' ... '.join((compact[start:end].strip() for start, end in merged))[:1200]; compact[:400]；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `clean_record` (function, L59-L132)

**签名：** `def clean_record(record: dict[str, Any], case: dict[str, Any]) -> dict[str, Any]`

**作用：** 执行 clean record，涉及 sorted, Constant.join, sum, len, record.get。

**详细语义：** 所属模块职责：清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。；输入参数：record: dict[str, Any], case: dict[str, Any]；声明返回：dict[str, Any]；直接/间接调用：sorted, Constant.join, sum, len, record.get, int, contains_any, fact_checks.append, case.get, item.get, bool, CITATION_PATTERN.findall, relevant_excerpt；返回表达式：{'case_id': case['id'], 'kind': case['kind'], 'question': case['question'], 'answer': answer, 'expected_sources': expected_sources, 'retrieved_source': retrieved_source, 'cited_so…；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 评估, 日志清洗, 事实核对, 引用验证, clean, record, sorted, Constant.join, sum, len, record.get, int, contains_any, fact_checks.append, case.get, item.get, bool, CITATION_PATTERN.findall, relevant_excerpt, 条件分支, 循环

**调用：** sorted, Constant.join, sum, len, record.get, int, contains_any, fact_checks.append, case.get, item.get, bool, CITATION_PATTERN.findall, relevant_excerpt；**返回：** {'case_id': case['id'], 'kind': case['kind'], 'question': case['question'], 'answer': answer, 'expected_sources': expected_sources, 'retrieved_source': retrieved_source, 'cited_so…；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `database_counts` (function, L135-L139)

**签名：** `def database_counts(path: Path) -> tuple[int, int]`

**作用：** 执行 database counts，涉及 sqlite3.connect, int, connection.execute.fetchone, connection.execute。

**详细语义：** 所属模块职责：清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。；输入参数：path: Path；声明返回：tuple[int, int]；直接/间接调用：sqlite3.connect, int, connection.execute.fetchone, connection.execute；返回表达式：(document_count, chunk_count)；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 评估, 日志清洗, 事实核对, 引用验证, database, counts, sqlite3.connect, int, connection.execute.fetchone, connection.execute, 上下文管理

**调用：** sqlite3.connect, int, connection.execute.fetchone, connection.execute；**返回：** (document_count, chunk_count)；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `render_report` (function, L142-L251)

**签名：** `def render_report(cleaned: list[dict[str, Any]], *, raw_log: Path, ablation: dict[str, Any], document_count: int, chunk_count: int) -> str`

**作用：** 执行 render report，涉及 sum, hashlib.sha256.hexdigest, lines.extend, enumerate, Constant.join。

**详细语义：** 所属模块职责：清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。；输入参数：cleaned: list[dict[str, Any]], *, raw_log: Path, ablation: dict[str, Any], document_count: int, chunk_count: int；声明返回：str；直接/间接调用：sum, hashlib.sha256.hexdigest, lines.extend, enumerate, Constant.join, len, lines.append, hashlib.sha256, raw_log.read_bytes, str；返回表达式：'\n'.join(lines)；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 评估, 日志清洗, 事实核对, 引用验证, render, report, sum, hashlib.sha256.hexdigest, lines.extend, enumerate, Constant.join, len, lines.append, hashlib.sha256, raw_log.read_bytes, str, 条件分支, 循环

**调用：** sum, hashlib.sha256.hexdigest, lines.extend, enumerate, Constant.join, len, lines.append, hashlib.sha256, raw_log.read_bytes, str；**返回：** '\n'.join(lines)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `main` (function, L254-L294)

**签名：** `def main() -> int`

**作用：** 执行模块主流程，编排参数、业务调用、输出和进程退出码。

**详细语义：** 所属模块职责：清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。；输入参数：；声明返回：int；直接/间接调用：argparse.ArgumentParser, parser.add_argument, parser.parse_args, read_records, json.loads, args.jsonl_output.parent.mkdir, args.jsonl_output.write_text, database_counts, args.report_output.write_text, args.cases.read_text, args.ablation_result.read_text, len, ValueError, records_by_question.get, cleaned.append, Constant.join, render_report, all, clean_record, json.dumps；返回表达式：0 if all((item['passed'] for item in cleaned)) else 1；显式异常：ValueError(f'日志记录数 {len(records)} 与用例数 {len(cases)} 不一致'); ValueError(f'日志中缺少问题：{case['question']}')；控制流：条件分支, 循环。

**关键词：** 评估, 日志清洗, 事实核对, 引用验证, main, argparse.ArgumentParser, parser.add_argument, parser.parse_args, read_records, json.loads, args.jsonl_output.parent.mkdir, args.jsonl_output.write_text, database_counts, args.report_output.write_text, args.cases.read_text, args.ablation_result.read_text, len, ValueError, records_by_question.get, cleaned.append, Constant.join, render_report, all, clean_record, json.dumps, 条件分支, 循环

**调用：** argparse.ArgumentParser, parser.add_argument, parser.parse_args, read_records, json.loads, args.jsonl_output.parent.mkdir, args.jsonl_output.write_text, database_counts, args.report_output.write_text, args.cases.read_text, args.ablation_result.read_text, len, ValueError, records_by_question.get, cleaned.append, Constant.join, render_report, all, clean_record, json.dumps；**返回：** 0 if all((item['passed'] for item in cleaned)) else 1；**异常：** ValueError(f'日志记录数 {len(records)} 与用例数 {len(cases)} 不一致'); ValueError(f'日志中缺少问题：{case['question']}')；**副作用：** 文件系统读写。

## personal_local_knowledge_base_v0/scripts/generate_code_index.py

**文件作用：** 测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。

**语言/关键词：** 代码, 回归, 辅助脚本, Python, py

**函数/类/脚本记录数：** 26

### `Entity` (class, L71-L106)

**签名：** `class Entity`

**作用：** 定义 Entity 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；类体包含 1 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, Entity

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `Entity.as_dict` (function, L88-L106)

**签名：** `def as_dict(self) -> dict[str, Any]`

**作用：** 执行 as dict。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：self；声明返回：dict[str, Any]；直接/间接调用：无明显函数调用；返回表达式：{'entity_id': f'{self.path}::{self.qualified_name}', 'kind': self.kind, 'file': self.path, 'symbol': self.qualified_name, 'line_start': self.line_start, 'line_end': self.line_end,…；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, Entity, as, dict

**调用：** 无明显调用；**返回：** {'entity_id': f'{self.path}::{self.qualified_name}', 'kind': self.kind, 'file': self.path, 'symbol': self.qualified_name, 'line_start': self.line_start, 'line_end': self.line_end,…；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `relative` (function, L109-L110)

**签名：** `def relative(path: Path) -> str`

**作用：** 执行 relative，涉及 path.relative_to.as_posix, path.relative_to。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：path: Path；声明返回：str；直接/间接调用：path.relative_to.as_posix, path.relative_to；返回表达式：path.relative_to(PROJECT_DIR.parent).as_posix()；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, relative, path.relative_to.as_posix, path.relative_to

**调用：** path.relative_to.as_posix, path.relative_to；**返回：** path.relative_to(PROJECT_DIR.parent).as_posix()；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `short_node_name` (function, L113-L120)

**签名：** `def short_node_name(node: ast.AST) -> str`

**作用：** 执行 short node name，涉及 isinstance, short_node_name, type。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：node: ast.AST；声明返回：str；直接/间接调用：isinstance, short_node_name, type；返回表达式：type(node).__name__; node.id; f'{short_node_name(node.value)}.{node.attr}'; short_node_name(node.func)；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 代码, 回归, 辅助脚本, short, node, name, isinstance, short_node_name, type, 条件分支

**调用：** isinstance, short_node_name, type；**返回：** type(node).__name__; node.id; f'{short_node_name(node.value)}.{node.attr}'; short_node_name(node.func)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `expression_text` (function, L123-L127)

**签名：** `def expression_text(node: ast.AST | None, limit: int=180) -> str`

**作用：** 执行 expression text，涉及 ast.unparse.replace, ast.unparse, len。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：node: ast.AST | None, limit: int=180；声明返回：str；直接/间接调用：ast.unparse.replace, ast.unparse, len；返回表达式：value if len(value) <= limit else value[:limit - 1] + '…'; ''；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 代码, 回归, 辅助脚本, expression, text, ast.unparse.replace, ast.unparse, len, 条件分支

**调用：** ast.unparse.replace, ast.unparse, len；**返回：** value if len(value) <= limit else value[:limit - 1] + '…'; ''；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `name_words` (function, L130-L132)

**签名：** `def name_words(name: str) -> list[str]`

**作用：** 执行 name words，涉及 re.sub, re.split。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：name: str；声明返回：list[str]；直接/间接调用：re.sub, re.split；返回表达式：[part for part in re.split('[^A-Za-z0-9一-龥]+', name) if part]；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, name, words, re.sub, re.split

**调用：** re.sub, re.split；**返回：** [part for part in re.split('[^A-Za-z0-9一-龥]+', name) if part]；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `purpose_for` (function, L135-L211)

**签名：** `def purpose_for(name: str, docstring: str, calls: list[str], kind: str) -> str`

**作用：** 执行 purpose for，涉及 name.startswith, name.replace, Subscript.replace, Constant.join, docstring.strip.split。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：name: str, docstring: str, calls: list[str], kind: str；声明返回：str；直接/间接调用：name.startswith, name.replace, Subscript.replace, Constant.join, docstring.strip.split, docstring.strip, len；返回表达式：f'执行 {subject}{suffix}。'; docstring.strip().split('\n\n', 1)[0].replace('\n', ' '); f'定义 {name} 相关的状态、数据契约或协作接口。'; f'回归测试：验证 {name[5:].replace('_', ' ')} 的预期行为、边界条件或错误处理。'; '初始化对象字段、运行配置和可复用的外部资源句柄。'; '进入上下文管理器并返回可用的资源对象。'; '退出上下文管理器，提交或关闭资源并按约定处理异常。'; '执行模块主流程，编排参数、业务调用、输出和进程退出码。'；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, purpose, for, name.startswith, name.replace, Subscript.replace, Constant.join, docstring.strip.split, docstring.strip, len, 条件分支, 循环

**调用：** name.startswith, name.replace, Subscript.replace, Constant.join, docstring.strip.split, docstring.strip, len；**返回：** f'执行 {subject}{suffix}。'; docstring.strip().split('\n\n', 1)[0].replace('\n', ' '); f'定义 {name} 相关的状态、数据契约或协作接口。'; f'回归测试：验证 {name[5:].replace('_', ' ')} 的预期行为、边界条件或错误处理。'; '初始化对象字段、运行配置和可复用的外部资源句柄。'; '进入上下文管理器并返回可用的资源对象。'; '退出上下文管理器，提交或关闭资源并按约定处理异常。'; '执行模块主流程，编排参数、业务调用、输出和进程退出码。'；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `collect_calls` (function, L214-L221)

**签名：** `def collect_calls(node: ast.AST) -> list[str]`

**作用：** 执行 collect calls，涉及 ast.walk, isinstance, short_node_name, calls.append。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：node: ast.AST；声明返回：list[str]；直接/间接调用：ast.walk, isinstance, short_node_name, calls.append；返回表达式：calls[:24]；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, collect, calls, ast.walk, isinstance, short_node_name, calls.append, 条件分支, 循环

**调用：** ast.walk, isinstance, short_node_name, calls.append；**返回：** calls[:24]；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_returns` (function, L224-L233)

**签名：** `def collect_returns(node: ast.AST) -> list[str]`

**作用：** 执行 collect returns，涉及 ast.walk, isinstance, expression_text, values.append。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：node: ast.AST；声明返回：list[str]；直接/间接调用：ast.walk, isinstance, expression_text, values.append；返回表达式：values[:8]；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, collect, returns, ast.walk, isinstance, expression_text, values.append, 条件分支, 循环

**调用：** ast.walk, isinstance, expression_text, values.append；**返回：** values[:8]；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_raises` (function, L236-L243)

**签名：** `def collect_raises(node: ast.AST) -> list[str]`

**作用：** 执行 collect raises，涉及 ast.walk, isinstance, expression_text, result.append。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：node: ast.AST；声明返回：list[str]；直接/间接调用：ast.walk, isinstance, expression_text, result.append；返回表达式：result[:8]；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, collect, raises, ast.walk, isinstance, expression_text, result.append, 条件分支, 循环

**调用：** ast.walk, isinstance, expression_text, result.append；**返回：** result[:8]；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `infer_side_effects` (function, L246-L261)

**签名：** `def infer_side_effects(calls: Iterable[str], source: str) -> list[str]`

**作用：** 执行 infer side effects，涉及 re.search, Constant.join, effects.append。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：calls: Iterable[str], source: str；声明返回：list[str]；直接/间接调用：re.search, Constant.join, effects.append；返回表达式：effects；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, infer, side, effects, re.search, Constant.join, effects.append, 条件分支, 循环

**调用：** re.search, Constant.join, effects.append；**返回：** effects；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 网络 HTTP 请求, 日志输出, 子进程或外部命令, 环境变量读取, 模型/向量计算。

### `collect_python` (function, L264-L345)

**签名：** `def collect_python(path: Path, source: str, module_purpose: str, module_tags: tuple[str, ...]) -> list[Entity]`

**作用：** 执行 collect python，涉及 ast.parse, source.splitlines, Visitor.visit, Constant.join, entities.append。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：path: Path, source: str, module_purpose: str, module_tags: tuple[str, ...]；声明返回：list[Entity]；直接/间接调用：ast.parse, source.splitlines, Visitor.visit, Constant.join, entities.append, stack.append, self.generic_visit, stack.pop, self._function, collect_calls, isinstance, ast.unparse, collect_returns, collect_raises, list, Visitor, ast.get_docstring, Entity, ast.get_source_segment, any, flow.append, dict.fromkeys, expression_text, relative；返回表达式：entities；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, collect, python, ast.parse, source.splitlines, Visitor.visit, Constant.join, entities.append, stack.append, self.generic_visit, stack.pop, self._function, collect_calls, isinstance, ast.unparse, collect_returns, collect_raises, list, Visitor, ast.get_docstring, Entity, ast.get_source_segment, any, flow.append, dict.fromkeys, expression_text, relative, 条件分支, 循环

**调用：** ast.parse, source.splitlines, Visitor.visit, Constant.join, entities.append, stack.append, self.generic_visit, stack.pop, self._function, collect_calls, isinstance, ast.unparse, collect_returns, collect_raises, list, Visitor, ast.get_docstring, Entity, ast.get_source_segment, any, flow.append, dict.fromkeys, expression_text, relative；**返回：** entities；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_python.Visitor` (class, L270-L342)

**签名：** `class Visitor`

**作用：** 定义 Visitor 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；类体包含 5 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, Visitor

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_python.Visitor.visit_ClassDef` (function, L271-L282)

**签名：** `def visit_ClassDef(self, node: ast.ClassDef) -> None`

**作用：** 执行 visit ClassDef，涉及 Constant.join, entities.append, stack.append, self.generic_visit, stack.pop。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：self, node: ast.ClassDef；声明返回：None；直接/间接调用：Constant.join, entities.append, stack.append, self.generic_visit, stack.pop, ast.get_docstring, Entity, relative, getattr, purpose_for, list, dict.fromkeys, sum, isinstance, name_words；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, collect, python, Visitor, visit, Class, Def, Constant.join, entities.append, stack.append, self.generic_visit, stack.pop, ast.get_docstring, Entity, relative, getattr, purpose_for, list, dict.fromkeys, sum, isinstance, name_words

**调用：** Constant.join, entities.append, stack.append, self.generic_visit, stack.pop, ast.get_docstring, Entity, relative, getattr, purpose_for, list, dict.fromkeys, sum, isinstance, name_words；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_python.Visitor.visit_FunctionDef` (function, L284-L285)

**签名：** `def visit_FunctionDef(self, node: ast.FunctionDef) -> None`

**作用：** 执行 visit FunctionDef，涉及 self._function。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：self, node: ast.FunctionDef；声明返回：None；直接/间接调用：self._function；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, collect, python, Visitor, visit, Function, Def, self._function

**调用：** self._function；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_python.Visitor.visit_AsyncFunctionDef` (function, L287-L288)

**签名：** `def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None`

**作用：** 执行 visit AsyncFunctionDef，涉及 self._function。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：self, node: ast.AsyncFunctionDef；声明返回：None；直接/间接调用：self._function；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, collect, python, Visitor, visit, Async, Function, Def, self._function

**调用：** self._function；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_python.Visitor._function` (function, L290-L321)

**签名：** `def _function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None`

**作用：** 执行  function，涉及 Constant.join, collect_calls, isinstance, ast.unparse, collect_returns。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：self, node: ast.FunctionDef | ast.AsyncFunctionDef；声明返回：None；直接/间接调用：Constant.join, collect_calls, isinstance, ast.unparse, collect_returns, collect_raises, list, entities.append, stack.append, self.generic_visit, stack.pop, ast.get_docstring, ast.get_source_segment, any, flow.append, dict.fromkeys, Entity, relative, getattr, purpose_for, infer_side_effects, ast.walk, name_words；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, collect, python, Visitor, function, Constant.join, collect_calls, isinstance, ast.unparse, collect_returns, collect_raises, list, entities.append, stack.append, self.generic_visit, stack.pop, ast.get_docstring, ast.get_source_segment, any, flow.append, dict.fromkeys, Entity, relative, getattr, purpose_for, infer_side_effects, ast.walk, name_words, 条件分支, 循环

**调用：** Constant.join, collect_calls, isinstance, ast.unparse, collect_returns, collect_raises, list, entities.append, stack.append, self.generic_visit, stack.pop, ast.get_docstring, ast.get_source_segment, any, flow.append, dict.fromkeys, Entity, relative, getattr, purpose_for, infer_side_effects, ast.walk, name_words；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_python.Visitor.visit_Lambda` (function, L323-L342)

**签名：** `def visit_Lambda(self, node: ast.Lambda) -> None`

**作用：** Index anonymous Python callbacks as first-class function records.

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：self, node: ast.Lambda；声明返回：None；直接/间接调用：Constant.join, collect_calls, ast.unparse, entities.append, self.generic_visit, ast.get_source_segment, expression_text, Entity, relative, getattr, list, infer_side_effects, dict.fromkeys；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 代码, 回归, 辅助脚本, collect, python, Visitor, visit, Lambda, Constant.join, collect_calls, ast.unparse, entities.append, self.generic_visit, ast.get_source_segment, expression_text, Entity, relative, getattr, list, infer_side_effects, dict.fromkeys, 条件分支

**调用：** Constant.join, collect_calls, ast.unparse, entities.append, self.generic_visit, ast.get_source_segment, expression_text, Entity, relative, getattr, list, infer_side_effects, dict.fromkeys；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `matching_brace` (function, L348-L370)

**签名：** `def matching_brace(source: str, start: int) -> int`

**作用：** 执行 matching brace，涉及 range, len。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：source: str, start: int；声明返回：int；直接/间接调用：range, len；返回表达式：len(source) - 1; index；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, matching, brace, range, len, 条件分支, 循环

**调用：** range, len；**返回：** len(source) - 1; index；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_javascript` (function, L373-L424)

**签名：** `def collect_javascript(path: Path, source: str, module_purpose: str, module_tags: tuple[str, ...]) -> list[Entity]`

**作用：** 执行 collect javascript，涉及 re.compile, set, re.finditer, declaration.finditer, arrow.finditer。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：path: Path, source: str, module_purpose: str, module_tags: tuple[str, ...]；声明返回：list[Entity]；直接/间接调用：re.compile, set, re.finditer, declaration.finditer, arrow.finditer, sorted, line_starts.append, bisect.bisect_right, seen.add, re.search, purpose_for, list, entities.append, source.find, add, match.end, flow.append, dict.fromkeys, Entity, matching_brace, match.group, match.start, relative, line_number；返回表达式：sorted(entities, key=lambda item: (item.line_start, item.qualified_name)); bisect.bisect_right(line_starts, position)；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, collect, javascript, re.compile, set, re.finditer, declaration.finditer, arrow.finditer, sorted, line_starts.append, bisect.bisect_right, seen.add, re.search, purpose_for, list, entities.append, source.find, add, match.end, flow.append, dict.fromkeys, Entity, matching_brace, match.group, match.start, relative, line_number, 条件分支, 循环

**调用：** re.compile, set, re.finditer, declaration.finditer, arrow.finditer, sorted, line_starts.append, bisect.bisect_right, seen.add, re.search, purpose_for, list, entities.append, source.find, add, match.end, flow.append, dict.fromkeys, Entity, matching_brace, match.group, match.start, relative, line_number；**返回：** sorted(entities, key=lambda item: (item.line_start, item.qualified_name)); bisect.bisect_right(line_starts, position)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_javascript.line_number` (function, L382-L384)

**签名：** `def line_number(position: int) -> int`

**作用：** 执行 line number，涉及 bisect.bisect_right。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：position: int；声明返回：int；直接/间接调用：bisect.bisect_right；返回表达式：bisect.bisect_right(line_starts, position)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, collect, javascript, line, number, bisect.bisect_right

**调用：** bisect.bisect_right；**返回：** bisect.bisect_right(line_starts, position)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_javascript.add` (function, L386-L412)

**签名：** `def add(name: str, start: int, end: int, signature: str, anonymous: bool=False) -> None`

**作用：** 执行 add，涉及 seen.add, re.search, purpose_for, list, entities.append。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：name: str, start: int, end: int, signature: str, anonymous: bool=False；声明返回：None；直接/间接调用：seen.add, re.search, purpose_for, list, entities.append, flow.append, dict.fromkeys, Entity, relative, line_number, infer_side_effects, re.findall, Constant.join, name_words；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 代码, 回归, 辅助脚本, collect, javascript, add, seen.add, re.search, purpose_for, list, entities.append, flow.append, dict.fromkeys, Entity, relative, line_number, infer_side_effects, re.findall, Constant.join, name_words, 条件分支

**调用：** seen.add, re.search, purpose_for, list, entities.append, flow.append, dict.fromkeys, Entity, relative, line_number, infer_side_effects, re.findall, Constant.join, name_words；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `collect_javascript.lambda@424` (function, L424-L424)

**签名：** `lambda item`

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；这是匿名 lambda，输入参数：item；返回表达式：(item.line_start, item.qualified_name)；调用：无明显函数调用；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, lambda

**调用：** 无明显调用；**返回：** (item.line_start, item.qualified_name)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `script_entity` (function, L427-L430)

**签名：** `def script_entity(path: Path, source: str, purpose: str, tags: tuple[str, ...], language: str) -> Entity`

**作用：** 执行 script entity，涉及 sorted, Entity, set, relative, len。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：path: Path, source: str, purpose: str, tags: tuple[str, ...], language: str；声明返回：Entity；直接/间接调用：sorted, Entity, set, relative, len, list, infer_side_effects, re.findall, source.splitlines, dict.fromkeys, re.search, Constant.join；返回表达式：Entity('script', relative(path), '<module>.__main__', 1, len(source.splitlines()), 'module-level script', purpose, '', details, list(dict.fromkeys([*tags, language])), commands, […；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 代码, 回归, 辅助脚本, script, entity, sorted, Entity, set, relative, len, list, infer_side_effects, re.findall, source.splitlines, dict.fromkeys, re.search, Constant.join, 条件分支

**调用：** sorted, Entity, set, relative, len, list, infer_side_effects, re.findall, source.splitlines, dict.fromkeys, re.search, Constant.join；**返回：** Entity('script', relative(path), '<module>.__main__', 1, len(source.splitlines()), 'module-level script', purpose, '', details, list(dict.fromkeys([*tags, language])), commands, […；**异常：** 未发现显式 raise；**副作用：** 子进程或外部命令。

### `render_markdown` (function, L433-L466)

**签名：** `def render_markdown(records: list[dict[str, Any]]) -> str`

**作用：** 执行 render markdown，涉及 lines.extend, by_file.get, Constant.join, by_file.setdefault.append, len。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：records: list[dict[str, Any]]；声明返回：str；直接/间接调用：lines.extend, by_file.get, Constant.join, by_file.setdefault.append, len, by_file.setdefault；返回表达式：'\n'.join(lines) + '\n'；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** 代码, 回归, 辅助脚本, render, markdown, lines.extend, by_file.get, Constant.join, by_file.setdefault.append, len, by_file.setdefault, 条件分支, 循环

**调用：** lines.extend, by_file.get, Constant.join, by_file.setdefault.append, len, by_file.setdefault；**返回：** '\n'.join(lines) + '\n'；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `main` (function, L469-L531)

**签名：** `def main() -> int`

**作用：** 执行模块主流程，编排参数、业务调用、输出和进程退出码。

**详细语义：** 所属模块职责：测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。；输入参数：；声明返回：int；直接/间接调用：sorted, OUTPUT_DIR.mkdir, jsonl_path.write_text, BinOp.write_text, print, path.read_text, relative, PATH_GUIDES.get, records.append, records.extend, render_markdown, MODULE_GUIDES.get, path.stem.removeprefix, path.suffix.lower, len, list, Constant.join, PROJECT_DIR.parent.rglob, collect_python, source.splitlines, dict.fromkeys, entity.as_dict, path.is_file, collect_javascript；返回表达式：0；显式异常：未发现显式 raise；控制流：条件分支, 循环, 异常处理。

**关键词：** 代码, 回归, 辅助脚本, main, sorted, OUTPUT_DIR.mkdir, jsonl_path.write_text, BinOp.write_text, print, path.read_text, relative, PATH_GUIDES.get, records.append, records.extend, render_markdown, MODULE_GUIDES.get, path.stem.removeprefix, path.suffix.lower, len, list, Constant.join, PROJECT_DIR.parent.rglob, collect_python, source.splitlines, dict.fromkeys, entity.as_dict, path.is_file, collect_javascript, 条件分支, 循环, 异常处理

**调用：** sorted, OUTPUT_DIR.mkdir, jsonl_path.write_text, BinOp.write_text, print, path.read_text, relative, PATH_GUIDES.get, records.append, records.extend, render_markdown, MODULE_GUIDES.get, path.stem.removeprefix, path.suffix.lower, len, list, Constant.join, PROJECT_DIR.parent.rglob, collect_python, source.splitlines, dict.fromkeys, entity.as_dict, path.is_file, collect_javascript；**返回：** 0；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 日志输出。

## personal_local_knowledge_base_v0/scripts/probe_citation_failure.py

**文件作用：** 启动返回无引用答案的假 LLM 服务，验证引用校验会让 ask 失败且日志脱敏。

**语言/关键词：** 探针, 引用失败, 假服务, 回归验证, Python, py

**函数/类/脚本记录数：** 4

### `_NoCitationHandler` (class, L19-L42)

**签名：** `class _NoCitationHandler`

**作用：** 定义 _NoCitationHandler 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：启动返回无引用答案的假 LLM 服务，验证引用校验会让 ask 失败且日志脱敏。；类体包含 2 个直接方法。

**关键词：** 探针, 引用失败, 假服务, 回归验证, No, Citation, Handler

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_NoCitationHandler.do_POST` (function, L20-L39)

**签名：** `def do_POST(self) -> None`

**作用：** 执行 do POST，涉及 int, self.rfile.read, json.dumps.encode, self.send_response, self.send_header。

**详细语义：** 所属模块职责：启动返回无引用答案的假 LLM 服务，验证引用校验会让 ask 失败且日志脱敏。；输入参数：self；声明返回：None；直接/间接调用：int, self.rfile.read, json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write, self.headers.get, str, json.dumps, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 探针, 引用失败, 假服务, 回归验证, No, Citation, Handler, do, POST, int, self.rfile.read, json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write, self.headers.get, str, json.dumps, len

**调用：** int, self.rfile.read, json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write, self.headers.get, str, json.dumps, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_NoCitationHandler.log_message` (function, L41-L42)

**签名：** `def log_message(self, format: str, *args: object) -> None`

**作用：** 执行 log message。

**详细语义：** 所属模块职责：启动返回无引用答案的假 LLM 服务，验证引用校验会让 ask 失败且日志脱敏。；输入参数：self, format: str, *args: object；声明返回：None；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 探针, 引用失败, 假服务, 回归验证, No, Citation, Handler, log, message

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `main` (function, L45-L122)

**签名：** `def main() -> int`

**作用：** 执行模块主流程，编排参数、业务调用、输出和进程退出码。

**详细语义：** 所属模块职责：启动返回无引用答案的假 LLM 服务，验证引用校验会让 ask 失败且日志脱敏。；输入参数：；声明返回：int；直接/间接调用：argparse.ArgumentParser, parser.add_argument, parser.parse_args, tempfile.TemporaryDirectory, Path, source.write_text, ThreadingHTTPServer, threading.Thread, thread.start, os.environ.copy, env.update, log_file.read_text, json.dumps, print, KnowledgeBase, index_paths, subprocess.run, server.shutdown, server.server_close, thread.join, all, args.log_output.parent.mkdir, args.log_output.write_text, args.result_output.parent.mkdir；返回表达式：0 if passed else 1；显式异常：未发现显式 raise；控制流：条件分支, 异常处理, 上下文管理。

**关键词：** 探针, 引用失败, 假服务, 回归验证, main, argparse.ArgumentParser, parser.add_argument, parser.parse_args, tempfile.TemporaryDirectory, Path, source.write_text, ThreadingHTTPServer, threading.Thread, thread.start, os.environ.copy, env.update, log_file.read_text, json.dumps, print, KnowledgeBase, index_paths, subprocess.run, server.shutdown, server.server_close, thread.join, all, args.log_output.parent.mkdir, args.log_output.write_text, args.result_output.parent.mkdir, 条件分支, 异常处理, 上下文管理

**调用：** argparse.ArgumentParser, parser.add_argument, parser.parse_args, tempfile.TemporaryDirectory, Path, source.write_text, ThreadingHTTPServer, threading.Thread, thread.start, os.environ.copy, env.update, log_file.read_text, json.dumps, print, KnowledgeBase, index_paths, subprocess.run, server.shutdown, server.server_close, thread.join, all, args.log_output.parent.mkdir, args.log_output.write_text, args.result_output.parent.mkdir；**返回：** 0 if passed else 1；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 网络 HTTP 请求, 日志输出, 子进程或外部命令, 环境变量读取。

## personal_local_knowledge_base_v0/scripts/qwen_embedding_server.py

**文件作用：** 在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。

**语言/关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Python, py

**函数/类/脚本记录数：** 20

### `EmbeddingRequest` (class, L29-L33)

**签名：** `class EmbeddingRequest`

**作用：** 定义 EmbeddingRequest 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；类体包含 0 个直接方法。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Embedding, Request

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `SimpleEmbeddingRequest` (class, L36-L37)

**签名：** `class SimpleEmbeddingRequest`

**作用：** 定义 SimpleEmbeddingRequest 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；类体包含 0 个直接方法。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Simple, Embedding, Request

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `WorkItem` (class, L41-L43)

**签名：** `class WorkItem`

**作用：** 定义 WorkItem 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；类体包含 0 个直接方法。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Work, Item

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingEngine` (class, L46-L186)

**签名：** `class EmbeddingEngine`

**作用：** 定义 EmbeddingEngine 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；类体包含 7 个直接方法。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Embedding, Engine

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingEngine.__init__` (function, L47-L79)

**签名：** `def __init__(self, model_name: str, *, revision: str | None=None, max_batch_size: int=16, max_batch_tokens: int=8192, max_length: int=2048, batch_wait_ms: float=3.0) -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：self, model_name: str, *, revision: str | None=None, max_batch_size: int=16, max_batch_tokens: int=8192, max_length: int=2048, batch_wait_ms: float=3.0；声明返回：None；直接/间接调用：asyncio.Queue, threading.Lock, torch.device, AutoTokenizer.from_pretrained, AutoModel.from_pretrained.eval.to, int, torch.cuda.is_available, RuntimeError, getattr, str, AutoModel.from_pretrained.eval, AutoModel.from_pretrained；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：RuntimeError('未检测到 CUDA；此服务要求在装有 NVIDIA 驱动的服务器上运行')；控制流：条件分支。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Embedding, Engine, init, asyncio.Queue, threading.Lock, torch.device, AutoTokenizer.from_pretrained, AutoModel.from_pretrained.eval.to, int, torch.cuda.is_available, RuntimeError, getattr, str, AutoModel.from_pretrained.eval, AutoModel.from_pretrained, 条件分支

**调用：** asyncio.Queue, threading.Lock, torch.device, AutoTokenizer.from_pretrained, AutoModel.from_pretrained.eval.to, int, torch.cuda.is_available, RuntimeError, getattr, str, AutoModel.from_pretrained.eval, AutoModel.from_pretrained；**返回：** 未记录；**异常：** RuntimeError('未检测到 CUDA；此服务要求在装有 NVIDIA 驱动的服务器上运行')；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `EmbeddingEngine.start` (function, L81-L82)

**签名：** `async def start(self) -> None`

**作用：** 执行 start，涉及 asyncio.create_task, self._worker。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：self；声明返回：None；直接/间接调用：asyncio.create_task, self._worker；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Embedding, Engine, start, asyncio.create_task, self._worker, 异步协程

**调用：** asyncio.create_task, self._worker；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingEngine.stop` (function, L84-L87)

**签名：** `async def stop(self) -> None`

**作用：** 执行 stop，涉及 self._worker_task.cancel, asyncio.gather。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：self；声明返回：None；直接/间接调用：self._worker_task.cancel, asyncio.gather；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Embedding, Engine, stop, self._worker_task.cancel, asyncio.gather, 条件分支, 异步协程

**调用：** self._worker_task.cancel, asyncio.gather；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingEngine.submit` (function, L89-L121)

**签名：** `async def submit(self, texts: list[str]) -> list[list[float]]`

**作用：** 执行 submit，涉及 asyncio.get_running_loop, any, ValueError, len, self._estimate_tokens。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：self, texts: list[str]；声明返回：list[list[float]]；直接/间接调用：asyncio.get_running_loop, any, ValueError, len, self._estimate_tokens, current.append, groups.append, loop.create_future, futures.append, asyncio.gather, self.queue.put, WorkItem, isinstance, text.strip；返回表达式：[vector for group in results for vector in group]；显式异常：ValueError('input 必须是非空字符串数组'); ValueError(f'单次最多 {self.max_batch_size} 条文本')；控制流：条件分支, 循环, 异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Embedding, Engine, submit, asyncio.get_running_loop, any, ValueError, len, self._estimate_tokens, current.append, groups.append, loop.create_future, futures.append, asyncio.gather, self.queue.put, WorkItem, isinstance, text.strip, 条件分支, 循环, 异步协程

**调用：** asyncio.get_running_loop, any, ValueError, len, self._estimate_tokens, current.append, groups.append, loop.create_future, futures.append, asyncio.gather, self.queue.put, WorkItem, isinstance, text.strip；**返回：** [vector for group in results for vector in group]；**异常：** ValueError('input 必须是非空字符串数组'); ValueError(f'单次最多 {self.max_batch_size} 条文本')；**副作用：** 未发现明显外部副作用。

### `EmbeddingEngine._worker` (function, L123-L162)

**签名：** `async def _worker(self) -> None`

**作用：** 执行  worker，涉及 len, sum, self.queue.get, time.monotonic, max。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：self；声明返回：None；直接/间接调用：len, sum, self.queue.get, time.monotonic, max, items.append, self._estimate_tokens, asyncio.to_thread, item.future.set_result, asyncio.wait_for, self.queue.put, item.future.done, item.future.set_exception；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 异常处理, 异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Embedding, Engine, worker, len, sum, self.queue.get, time.monotonic, max, items.append, self._estimate_tokens, asyncio.to_thread, item.future.set_result, asyncio.wait_for, self.queue.put, item.future.done, item.future.set_exception, 条件分支, 循环, 异常处理, 异步协程

**调用：** len, sum, self.queue.get, time.monotonic, max, items.append, self._estimate_tokens, asyncio.to_thread, item.future.set_result, asyncio.wait_for, self.queue.put, item.future.done, item.future.set_exception；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingEngine._estimate_tokens` (function, L165-L168)

**签名：** `def _estimate_tokens(text: str) -> int`

**作用：** 执行  estimate tokens，涉及 max, len, text.encode。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：text: str；声明返回：int；直接/间接调用：max, len, text.encode；返回表达式：max(1, len(text.encode('utf-8')) // 2 + 8)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Embedding, Engine, estimate, tokens, max, len, text.encode

**调用：** max, len, text.encode；**返回：** max(1, len(text.encode('utf-8')) // 2 + 8)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingEngine._encode` (function, L170-L186)

**签名：** `def _encode(self, texts: list[str]) -> list[list[float]]`

**作用：** 执行  encode，涉及 torch.inference_mode, self.tokenizer, self.model, F.normalize, pooled.cpu.tolist。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：self, texts: list[str]；声明返回：list[list[float]]；直接/间接调用：torch.inference_mode, self.tokenizer, self.model, F.normalize, pooled.cpu.tolist, value.to, Subscript.sum, pooled.float, encoded.items, torch.arange, pooled.cpu, hidden.size；返回表达式：pooled.cpu().tolist()；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, Embedding, Engine, encode, torch.inference_mode, self.tokenizer, self.model, F.normalize, pooled.cpu.tolist, value.to, Subscript.sum, pooled.float, encoded.items, torch.arange, pooled.cpu, hidden.size, 上下文管理

**调用：** torch.inference_mode, self.tokenizer, self.model, F.normalize, pooled.cpu.tolist, value.to, Subscript.sum, pooled.float, encoded.items, torch.arange, pooled.cpu, hidden.size；**返回：** pooled.cpu().tolist()；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `create_app` (function, L189-L244)

**签名：** `def create_app(engine: EmbeddingEngine) -> FastAPI`

**作用：** 执行 create app，涉及 FastAPI, app.on_event, app.get, app.post, payload.get。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：engine: EmbeddingEngine；声明返回：FastAPI；直接/间接调用：FastAPI, app.on_event, app.get, app.post, payload.get, engine.start, engine.stop, isinstance, HTTPException, engine.tokenizer, len, engine.submit, enumerate, str；返回表达式：app; {'status': 'ok', 'model': engine.model_name, 'dimension': engine.dimension}; {'data': [{'id': engine.model_name, 'model_revision': engine.revision, 'owned_by': 'local'}]}; {'object': 'list', 'model': engine.model_name, 'data': [{'object': 'embedding', 'index': i, 'embedding': vector} for i, vector in enumerate(vectors)], 'usage': {'prompt_tokens': 0…; {'count': len(tokens)}; {'embeddings': await engine.submit(request.texts)}；显式异常：HTTPException(status_code=400, detail=f'只加载了模型 {engine.model_name}'); HTTPException(status_code=400, detail='仅支持 encoding_format=float'); HTTPException(status_code=400, detail=f'仅支持 dimensions={engine.dimension}'); HTTPException(status_code=400, detail='prompt 必须是字符串'); HTTPException(status_code=400, detail=str(exc))；控制流：条件分支, 异常处理。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, create, app, app.on_event, app.get, app.post, payload.get, engine.start, engine.stop, isinstance, HTTPException, engine.tokenizer, len, engine.submit, enumerate, str, 条件分支, 异常处理

**调用：** FastAPI, app.on_event, app.get, app.post, payload.get, engine.start, engine.stop, isinstance, HTTPException, engine.tokenizer, len, engine.submit, enumerate, str；**返回：** app; {'status': 'ok', 'model': engine.model_name, 'dimension': engine.dimension}; {'data': [{'id': engine.model_name, 'model_revision': engine.revision, 'owned_by': 'local'}]}; {'object': 'list', 'model': engine.model_name, 'data': [{'object': 'embedding', 'index': i, 'embedding': vector} for i, vector in enumerate(vectors)], 'usage': {'prompt_tokens': 0…; {'count': len(tokens)}; {'embeddings': await engine.submit(request.texts)}；**异常：** HTTPException(status_code=400, detail=f'只加载了模型 {engine.model_name}'); HTTPException(status_code=400, detail='仅支持 encoding_format=float'); HTTPException(status_code=400, detail=f'仅支持 dimensions={engine.dimension}'); HTTPException(status_code=400, detail='prompt 必须是字符串'); HTTPException(status_code=400, detail=str(exc))；**副作用：** 模型/向量计算。

### `create_app._startup` (function, L193-L194)

**签名：** `async def _startup() -> None`

**作用：** 执行  startup，涉及 app.on_event, engine.start。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：；声明返回：None；直接/间接调用：app.on_event, engine.start；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, create, app, startup, app.on_event, engine.start, 异步协程

**调用：** app.on_event, engine.start；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `create_app._shutdown` (function, L197-L198)

**签名：** `async def _shutdown() -> None`

**作用：** 执行  shutdown，涉及 app.on_event, engine.stop。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：；声明返回：None；直接/间接调用：app.on_event, engine.stop；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, create, app, shutdown, app.on_event, engine.stop, 异步协程

**调用：** app.on_event, engine.stop；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `create_app.health` (function, L201-L202)

**签名：** `async def health() -> dict[str, Any]`

**作用：** 执行 health，涉及 app.get。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：；声明返回：dict[str, Any]；直接/间接调用：app.get；返回表达式：{'status': 'ok', 'model': engine.model_name, 'dimension': engine.dimension}；显式异常：未发现显式 raise；控制流：异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, create, app, health, app.get, 异步协程

**调用：** app.get；**返回：** {'status': 'ok', 'model': engine.model_name, 'dimension': engine.dimension}；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `create_app.models` (function, L205-L206)

**签名：** `async def models() -> dict[str, Any]`

**作用：** 执行 models，涉及 app.get。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：；声明返回：dict[str, Any]；直接/间接调用：app.get；返回表达式：{'data': [{'id': engine.model_name, 'model_revision': engine.revision, 'owned_by': 'local'}]}；显式异常：未发现显式 raise；控制流：异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, create, app, models, app.get, 异步协程

**调用：** app.get；**返回：** {'data': [{'id': engine.model_name, 'model_revision': engine.revision, 'owned_by': 'local'}]}；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `create_app.simple_embed` (function, L209-L213)

**签名：** `async def simple_embed(request: SimpleEmbeddingRequest) -> dict[str, Any]`

**作用：** 执行 simple embed，涉及 app.post, HTTPException, engine.submit, str。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：request: SimpleEmbeddingRequest；声明返回：dict[str, Any]；直接/间接调用：app.post, HTTPException, engine.submit, str；返回表达式：{'embeddings': await engine.submit(request.texts)}；显式异常：HTTPException(status_code=400, detail=str(exc))；控制流：异常处理, 异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, create, app, simple, embed, app.post, HTTPException, engine.submit, str, 异常处理, 异步协程

**调用：** app.post, HTTPException, engine.submit, str；**返回：** {'embeddings': await engine.submit(request.texts)}；**异常：** HTTPException(status_code=400, detail=str(exc))；**副作用：** 模型/向量计算。

### `create_app.openai_embed` (function, L216-L233)

**签名：** `async def openai_embed(request: EmbeddingRequest) -> dict[str, Any]`

**作用：** 执行 openai embed，涉及 app.post, isinstance, HTTPException, engine.submit, enumerate。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：request: EmbeddingRequest；声明返回：dict[str, Any]；直接/间接调用：app.post, isinstance, HTTPException, engine.submit, enumerate, str；返回表达式：{'object': 'list', 'model': engine.model_name, 'data': [{'object': 'embedding', 'index': i, 'embedding': vector} for i, vector in enumerate(vectors)], 'usage': {'prompt_tokens': 0…；显式异常：HTTPException(status_code=400, detail=f'只加载了模型 {engine.model_name}'); HTTPException(status_code=400, detail='仅支持 encoding_format=float'); HTTPException(status_code=400, detail=f'仅支持 dimensions={engine.dimension}'); HTTPException(status_code=400, detail=str(exc))；控制流：条件分支, 异常处理, 异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, create, app, openai, embed, app.post, isinstance, HTTPException, engine.submit, enumerate, str, 条件分支, 异常处理, 异步协程

**调用：** app.post, isinstance, HTTPException, engine.submit, enumerate, str；**返回：** {'object': 'list', 'model': engine.model_name, 'data': [{'object': 'embedding', 'index': i, 'embedding': vector} for i, vector in enumerate(vectors)], 'usage': {'prompt_tokens': 0…；**异常：** HTTPException(status_code=400, detail=f'只加载了模型 {engine.model_name}'); HTTPException(status_code=400, detail='仅支持 encoding_format=float'); HTTPException(status_code=400, detail=f'仅支持 dimensions={engine.dimension}'); HTTPException(status_code=400, detail=str(exc))；**副作用：** 模型/向量计算。

### `create_app.tokenize` (function, L237-L242)

**签名：** `async def tokenize(payload: dict[str, Any]) -> dict[str, Any]`

**作用：** 执行 tokenize，涉及 app.post, payload.get, isinstance, HTTPException, engine.tokenizer。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：payload: dict[str, Any]；声明返回：dict[str, Any]；直接/间接调用：app.post, payload.get, isinstance, HTTPException, engine.tokenizer, len；返回表达式：{'count': len(tokens)}；显式异常：HTTPException(status_code=400, detail='prompt 必须是字符串')；控制流：条件分支, 异步协程。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, create, app, tokenize, app.post, payload.get, isinstance, HTTPException, engine.tokenizer, len, 条件分支, 异步协程

**调用：** app.post, payload.get, isinstance, HTTPException, engine.tokenizer, len；**返回：** {'count': len(tokens)}；**异常：** HTTPException(status_code=400, detail='prompt 必须是字符串')；**副作用：** 未发现明显外部副作用。

### `main` (function, L247-L269)

**签名：** `def main() -> None`

**作用：** 执行模块主流程，编排参数、业务调用、输出和进程退出码。

**详细语义：** 所属模块职责：在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。；输入参数：；声明返回：None；直接/间接调用：argparse.ArgumentParser, parser.add_argument, parser.parse_args, torch.set_float32_matmul_precision, EmbeddingEngine, uvicorn.run, create_app, os.getenv, int, float；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding 服务, Qwen, Transformers, 微批, FastAPI, main, argparse.ArgumentParser, parser.add_argument, parser.parse_args, torch.set_float32_matmul_precision, EmbeddingEngine, uvicorn.run, create_app, os.getenv, int, float

**调用：** argparse.ArgumentParser, parser.add_argument, parser.parse_args, torch.set_float32_matmul_precision, EmbeddingEngine, uvicorn.run, create_app, os.getenv, int, float；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 环境变量读取, 模型/向量计算。

## personal_local_knowledge_base_v0/scripts/run_rag_eval.py

**文件作用：** 按固定评估用例调用 ask 子进程并收集可复现的 RAG 评测日志。

**语言/关键词：** RAG 评估, 子进程, 可复现, Python, py

**函数/类/脚本记录数：** 1

### `main` (function, L15-L53)

**签名：** `def main() -> int`

**作用：** 执行模块主流程，编排参数、业务调用、输出和进程退出码。

**详细语义：** 所属模块职责：按固定评估用例调用 ask 子进程并收集可复现的 RAG 评测日志。；输入参数：；声明返回：int；直接/间接调用：argparse.ArgumentParser, parser.add_argument, parser.parse_args, json.loads, any, RagConfig.from_file, args.log_file.parent.mkdir, args.log_file.write_text, configure_logging, args.cases.read_text, ValueError, case.get, len, KnowledgeBase, KeywordRetriever, RagAnswerer, enumerate, Path, isinstance, set, print, answerer.answer, question.strip；返回表达式：0；显式异常：ValueError('评估用例必须是非空 JSON 数组'); ValueError('每个评估用例都必须包含非空 question'); ValueError('评估问题不能重复')；控制流：条件分支, 循环, 上下文管理。

**关键词：** RAG 评估, 子进程, 可复现, main, argparse.ArgumentParser, parser.add_argument, parser.parse_args, json.loads, any, RagConfig.from_file, args.log_file.parent.mkdir, args.log_file.write_text, configure_logging, args.cases.read_text, ValueError, case.get, len, KnowledgeBase, KeywordRetriever, RagAnswerer, enumerate, Path, isinstance, set, print, answerer.answer, question.strip, 条件分支, 循环, 上下文管理

**调用：** argparse.ArgumentParser, parser.add_argument, parser.parse_args, json.loads, any, RagConfig.from_file, args.log_file.parent.mkdir, args.log_file.write_text, configure_logging, args.cases.read_text, ValueError, case.get, len, KnowledgeBase, KeywordRetriever, RagAnswerer, enumerate, Path, isinstance, set, print, answerer.answer, question.strip；**返回：** 0；**异常：** ValueError('评估用例必须是非空 JSON 数组'); ValueError('每个评估用例都必须包含非空 question'); ValueError('评估问题不能重复')；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 日志输出。

## personal_local_knowledge_base_v0/server.py

**文件作用：** 项目根目录的兼容启动包装器；把上一级入口转发到本地 Embedding 服务实现。

**语言/关键词：** 启动入口, 模块加载, 路径兼容, Python, py

**函数/类/脚本记录数：** 1

### `_load_embedding_module` (function, L20-L41)

**签名：** `def _load_embedding_module() -> 未声明`

**作用：** Load the implementation even when this wrapper is one directory above the project.

**详细语义：** 所属模块职责：项目根目录的兼容启动包装器；把上一级入口转发到本地 Embedding 服务实现。；输入参数：；声明返回：未声明；直接/间接调用：Constant.join, RuntimeError, Path.resolve, importlib.util.spec_from_file_location, importlib.util.module_from_spec, spec.loader.exec_module, path.is_file, str, Path；返回表达式：module；显式异常：RuntimeError('找不到 scripts/qwen_embedding_server.py，请同步该文件。已搜索：\n' + searched)；控制流：条件分支, 循环。

**关键词：** 启动入口, 模块加载, 路径兼容, load, embedding, module, Constant.join, RuntimeError, Path.resolve, importlib.util.spec_from_file_location, importlib.util.module_from_spec, spec.loader.exec_module, path.is_file, str, Path, 条件分支, 循环

**调用：** Constant.join, RuntimeError, Path.resolve, importlib.util.spec_from_file_location, importlib.util.module_from_spec, spec.loader.exec_module, path.is_file, str, Path；**返回：** module；**异常：** RuntimeError('找不到 scripts/qwen_embedding_server.py，请同步该文件。已搜索：\n' + searched)；**副作用：** 文件系统读写, 模型/向量计算。

## personal_local_knowledge_base_v0/tests/__init__.py

**文件作用：** 测试包标记文件；不实现业务函数，只让 unittest 按包组织测试。

**语言/关键词：** 测试包, unittest, Python, py

**函数/类/脚本记录数：** 0

## personal_local_knowledge_base_v0/tests/test_chunking.py

**文件作用：** 测试文件：验证 chunking 模块的行为、边界和错误处理；在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。

**语言/关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 6

### `ChunkingTests` (class, L8-L46)

**签名：** `class ChunkingTests`

**作用：** 定义 ChunkingTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 chunking 模块的行为、边界和错误处理；在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；类体包含 5 个直接方法。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, unittest, 回归测试, Chunking, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkingTests.test_keeps_short_paragraphs_together` (function, L9-L14)

**签名：** `def test_keeps_short_paragraphs_together(self) -> 未声明`

**作用：** 回归测试：验证 keeps short paragraphs together 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 chunking 模块的行为、边界和错误处理；在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self；声明返回：未声明；直接/间接调用：chunk_text, self.assertEqual, self.assertIn, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, unittest, 回归测试, Chunking, Tests, test, keeps, short, paragraphs, together, chunk_text, self.assertEqual, self.assertIn, len

**调用：** chunk_text, self.assertEqual, self.assertIn, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkingTests.test_splits_long_text` (function, L16-L21)

**签名：** `def test_splits_long_text(self) -> 未声明`

**作用：** 回归测试：验证 splits long text 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 chunking 模块的行为、边界和错误处理；在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self；声明返回：未声明；直接/间接调用：chunk_text, self.assertGreater, self.assertTrue, self.assertEqual, len, all, list, range；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, unittest, 回归测试, Chunking, Tests, test, splits, long, text, chunk_text, self.assertGreater, self.assertTrue, self.assertEqual, len, all, list, range

**调用：** chunk_text, self.assertGreater, self.assertTrue, self.assertEqual, len, all, list, range；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkingTests.test_rejects_invalid_options` (function, L23-L29)

**签名：** `def test_rejects_invalid_options(self) -> 未声明`

**作用：** 回归测试：验证 rejects invalid options 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 chunking 模块的行为、边界和错误处理；在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertRaises, chunk_text；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, unittest, 回归测试, Chunking, Tests, test, rejects, invalid, options, self.assertRaises, chunk_text, 上下文管理

**调用：** self.assertRaises, chunk_text；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkingTests.test_streaming_chunker_consumes_text_blocks` (function, L31-L36)

**签名：** `def test_streaming_chunker_consumes_text_blocks(self) -> 未声明`

**作用：** 回归测试：验证 streaming chunker consumes text blocks 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 chunking 模块的行为、边界和错误处理；在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self；声明返回：未声明；直接/间接调用：list, self.assertGreater, self.assertEqual, iter_chunk_text, len, range；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, unittest, 回归测试, Chunking, Tests, test, streaming, chunker, consumes, text, blocks, list, self.assertGreater, self.assertEqual, iter_chunk_text, len, range

**调用：** list, self.assertGreater, self.assertEqual, iter_chunk_text, len, range；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ChunkingTests.test_streaming_chunks_keep_tail_head_overlap` (function, L38-L46)

**签名：** `def test_streaming_chunks_keep_tail_head_overlap(self) -> 未声明`

**作用：** 回归测试：验证 streaming chunks keep tail head overlap 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 chunking 模块的行为、边界和错误处理；在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。；输入参数：self；声明返回：未声明；直接/间接调用：iter, list, self.assertGreater, zip, iter_chunk_text, len, self.assertEqual；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环。

**关键词：** 语义分块, 核心块, 重叠, Token 限制, 硬边界, unittest, 回归测试, Chunking, Tests, test, streaming, chunks, keep, tail, head, overlap, iter, list, self.assertGreater, zip, iter_chunk_text, len, self.assertEqual, 循环

**调用：** iter, list, self.assertGreater, zip, iter_chunk_text, len, self.assertEqual；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/tests/test_cleaning.py

**文件作用：** 测试文件：验证 cleaning 模块的行为、边界和错误处理；对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。

**语言/关键词：** 文本清洗, 流式, Unicode, 换行, 空白, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 4

### `CleaningTests` (class, L8-L23)

**签名：** `class CleaningTests`

**作用：** 定义 CleaningTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 cleaning 模块的行为、边界和错误处理；对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。；类体包含 3 个直接方法。

**关键词：** 文本清洗, 流式, Unicode, 换行, 空白, unittest, 回归测试, Cleaning, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `CleaningTests.test_normalizes_whitespace_and_newlines` (function, L9-L13)

**签名：** `def test_normalizes_whitespace_and_newlines(self) -> 未声明`

**作用：** 回归测试：验证 normalizes whitespace and newlines 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 cleaning 模块的行为、边界和错误处理；对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, clean_text；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 文本清洗, 流式, Unicode, 换行, 空白, unittest, 回归测试, Cleaning, Tests, test, normalizes, whitespace, and, newlines, self.assertEqual, clean_text

**调用：** self.assertEqual, clean_text；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `CleaningTests.test_empty_text` (function, L15-L17)

**签名：** `def test_empty_text(self) -> 未声明`

**作用：** 回归测试：验证 empty text 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 cleaning 模块的行为、边界和错误处理；对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, clean_text；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 文本清洗, 流式, Unicode, 换行, 空白, unittest, 回归测试, Cleaning, Tests, test, empty, text, self.assertEqual, clean_text

**调用：** self.assertEqual, clean_text；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `CleaningTests.test_streaming_cleaner_accepts_multiple_chunks` (function, L19-L23)

**签名：** `def test_streaming_cleaner_accepts_multiple_chunks(self) -> 未声明`

**作用：** 回归测试：验证 streaming cleaner accepts multiple chunks 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 cleaning 模块的行为、边界和错误处理；对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。；输入参数：self；声明返回：未声明；直接/间接调用：iter, Constant.join.strip, self.assertEqual, Constant.join, iter_clean_text；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 文本清洗, 流式, Unicode, 换行, 空白, unittest, 回归测试, Cleaning, Tests, test, streaming, cleaner, accepts, multiple, chunks, iter, Constant.join.strip, self.assertEqual, Constant.join, iter_clean_text

**调用：** iter, Constant.join.strip, self.assertEqual, Constant.join, iter_clean_text；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## personal_local_knowledge_base_v0/tests/test_cli_integration.py

**文件作用：** 测试文件：验证 cli_integration 相关功能的行为、边界和错误处理。

**语言/关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 7

### `_reset_logging_handlers` (function, L13-L17)

**签名：** `def _reset_logging_handlers() -> None`

**作用：** 执行  reset logging handlers，涉及 logging.getLogger, root_logger.removeHandler, handler.close。

**详细语义：** 所属模块职责：测试文件：验证 cli_integration 相关功能的行为、边界和错误处理。；输入参数：；声明返回：None；直接/间接调用：logging.getLogger, root_logger.removeHandler, handler.close；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, reset, logging, handlers, logging.getLogger, root_logger.removeHandler, handler.close, 循环

**调用：** logging.getLogger, root_logger.removeHandler, handler.close；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `CLIIntegrationTests` (class, L20-L156)

**签名：** `class CLIIntegrationTests`

**作用：** 定义 CLIIntegrationTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 cli_integration 相关功能的行为、边界和错误处理。；类体包含 5 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, CLIIntegration, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `CLIIntegrationTests.test_web_port_defaults_to_8000_and_accepts_override` (function, L21-L25)

**签名：** `def test_web_port_defaults_to_8000_and_accepts_override(self) -> 未声明`

**作用：** 回归测试：验证 web port defaults to 8000 and accepts override 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 cli_integration 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：build_parser, self.assertEqual, parser.parse_args；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, CLIIntegration, Tests, test, web, port, defaults, to, 8000, and, accepts, override, build_parser, self.assertEqual, parser.parse_args

**调用：** build_parser, self.assertEqual, parser.parse_args；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `CLIIntegrationTests.test_web_command_reports_occupied_port_and_exits` (function, L27-L54)

**签名：** `def test_web_command_reports_occupied_port_and_exits(self) -> 未声明`

**作用：** 回归测试：验证 web command reports occupied port and exits 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 cli_integration 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertEqual, self.assertIn, socket.socket, occupied.bind, occupied.listen, io.StringIO, errors.getvalue, occupied.getsockname, _reset_logging_handlers, contextlib.redirect_stderr, main, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, CLIIntegration, Tests, test, web, command, reports, occupied, port, and, exits, tempfile.TemporaryDirectory, Path, self.assertEqual, self.assertIn, socket.socket, occupied.bind, occupied.listen, io.StringIO, errors.getvalue, occupied.getsockname, _reset_logging_handlers, contextlib.redirect_stderr, main, str, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertEqual, self.assertIn, socket.socket, occupied.bind, occupied.listen, io.StringIO, errors.getvalue, occupied.getsockname, _reset_logging_handlers, contextlib.redirect_stderr, main, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 日志输出。

### `CLIIntegrationTests.test_size_options_accept_human_readable_units` (function, L56-L69)

**签名：** `def test_size_options_accept_human_readable_units(self) -> 未声明`

**作用：** 回归测试：验证 size options accept human readable units 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 cli_integration 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：build_parser.parse_args, self.assertEqual, build_parser；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, CLIIntegration, Tests, test, size, options, accept, human, readable, units, build_parser.parse_args, self.assertEqual, build_parser

**调用：** build_parser.parse_args, self.assertEqual, build_parser；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `CLIIntegrationTests.test_json_structure_command_reports_streamed_schema` (function, L71-L107)

**签名：** `def test_json_structure_command_reports_streamed_schema(self) -> 未声明`

**作用：** 回归测试：验证 json structure command reports streamed schema 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 cli_integration 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, path.write_text, io.StringIO, self.assertEqual, self.assertIn, Constant.join, _reset_logging_handlers, output.getvalue, contextlib.redirect_stdout, main, json.dumps, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, CLIIntegration, Tests, test, json, structure, command, reports, streamed, schema, tempfile.TemporaryDirectory, Path, path.write_text, io.StringIO, self.assertEqual, self.assertIn, Constant.join, _reset_logging_handlers, output.getvalue, contextlib.redirect_stdout, main, json.dumps, str, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, path.write_text, io.StringIO, self.assertEqual, self.assertIn, Constant.join, _reset_logging_handlers, output.getvalue, contextlib.redirect_stdout, main, json.dumps, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 日志输出。

### `CLIIntegrationTests.test_json_index_command_uses_configured_stream` (function, L109-L156)

**签名：** `def test_json_index_command_uses_configured_stream(self) -> 未声明`

**作用：** 回归测试：验证 json index command uses configured stream 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 cli_integration 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, data_path.write_text, config_path.write_text, io.StringIO, self.assertEqual, self.assertIn, Constant.join, json.dumps, _reset_logging_handlers, output.getvalue, contextlib.redirect_stdout, main, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, CLIIntegration, Tests, test, json, index, command, uses, configured, stream, tempfile.TemporaryDirectory, Path, data_path.write_text, config_path.write_text, io.StringIO, self.assertEqual, self.assertIn, Constant.join, json.dumps, _reset_logging_handlers, output.getvalue, contextlib.redirect_stdout, main, str, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, data_path.write_text, config_path.write_text, io.StringIO, self.assertEqual, self.assertIn, Constant.join, json.dumps, _reset_logging_handlers, output.getvalue, contextlib.redirect_stdout, main, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 日志输出, 模型/向量计算。

## personal_local_knowledge_base_v0/tests/test_database.py

**文件作用：** 测试文件：验证 database 模块的行为、边界和错误处理；封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。

**语言/关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 4

### `DatabaseTests` (class, L11-L89)

**签名：** `class DatabaseTests`

**作用：** 定义 DatabaseTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 database 模块的行为、边界和错误处理；封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；类体包含 3 个直接方法。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, unittest, 回归测试, Database, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatabaseTests.test_chunk_window_returns_neighbors_from_same_document` (function, L12-L32)

**签名：** `def test_chunk_window_returns_neighbors_from_same_document(self) -> 未声明`

**作用：** 回归测试：验证 chunk window returns neighbors from same document 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 database 模块的行为、边界和错误处理；封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, ExtractedDocument, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, knowledge_base.chunk_window, BinOp.resolve, knowledge_base.search, Chunk；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, unittest, 回归测试, Database, Tests, test, chunk, window, returns, neighbors, from, same, document, tempfile.TemporaryDirectory, Path, ExtractedDocument, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, knowledge_base.chunk_window, BinOp.resolve, knowledge_base.search, Chunk, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, ExtractedDocument, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, knowledge_base.chunk_window, BinOp.resolve, knowledge_base.search, Chunk；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `DatabaseTests.test_fts5_search_and_replace_document` (function, L33-L70)

**签名：** `def test_fts5_search_and_replace_document(self) -> 未声明`

**作用：** 回归测试：验证 fts5 search and replace document 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 database 模块的行为、边界和错误处理；封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, source_path.write_text, ExtractedDocument, Path, KnowledgeBase, knowledge_base.replace_document, knowledge_base.search, self.assertEqual, self.assertIn, source_path.resolve, len, knowledge_base.document_count, knowledge_base.chunk_count, Chunk；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, unittest, 回归测试, Database, Tests, test, fts5, search, and, replace, document, tempfile.TemporaryDirectory, source_path.write_text, ExtractedDocument, Path, KnowledgeBase, knowledge_base.replace_document, knowledge_base.search, self.assertEqual, self.assertIn, source_path.resolve, len, knowledge_base.document_count, knowledge_base.chunk_count, Chunk, 上下文管理

**调用：** tempfile.TemporaryDirectory, source_path.write_text, ExtractedDocument, Path, KnowledgeBase, knowledge_base.replace_document, knowledge_base.search, self.assertEqual, self.assertIn, source_path.resolve, len, knowledge_base.document_count, knowledge_base.chunk_count, Chunk；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `DatabaseTests.test_health_check_reports_orphan_chunks_and_missing_token_rows` (function, L72-L89)

**签名：** `def test_health_check_reports_orphan_chunks_and_missing_token_rows(self) -> 未声明`

**作用：** 回归测试：验证 health check reports orphan chunks and missing token rows 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 database 模块的行为、边界和错误处理；封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, self.assertFalse, self.assertTrue, Path, KnowledgeBase, knowledge_base.connection.execute, knowledge_base.connection.commit, knowledge_base.check_health, any；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** SQLite, FTS5, jieba, Embedding 缓存, 事务, 增量索引, unittest, 回归测试, Database, Tests, test, health, check, reports, orphan, chunks, and, missing, token, rows, tempfile.TemporaryDirectory, self.assertFalse, self.assertTrue, Path, KnowledgeBase, knowledge_base.connection.execute, knowledge_base.connection.commit, knowledge_base.check_health, any, 上下文管理

**调用：** tempfile.TemporaryDirectory, self.assertFalse, self.assertTrue, Path, KnowledgeBase, knowledge_base.connection.execute, knowledge_base.connection.commit, knowledge_base.check_health, any；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

## personal_local_knowledge_base_v0/tests/test_dataset_reader.py

**文件作用：** 测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。

**语言/关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 16

### `DatasetNormalizationTests` (class, L30-L152)

**签名：** `class DatasetNormalizationTests`

**作用：** 定义 DatasetNormalizationTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；类体包含 6 个直接方法。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Normalization, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetNormalizationTests.assert_record_shape` (function, L31-L35)

**签名：** `def assert_record_shape(self, record) -> 未声明`

**作用：** 执行 assert record shape，涉及 self.assertEqual, self.assertIsInstance, tuple。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self, record；声明返回：未声明；直接/间接调用：self.assertEqual, self.assertIsInstance, tuple；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Normalization, Tests, assert, record, shape, self.assertEqual, self.assertIsInstance, tuple

**调用：** self.assertEqual, self.assertIsInstance, tuple；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetNormalizationTests.test_normalizes_dureader_and_collects_negatives` (function, L37-L54)

**签名：** `def test_normalizes_dureader_and_collects_negatives(self) -> 未声明`

**作用：** 回归测试：验证 normalizes dureader and collects negatives 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：normalize, self.assert_record_shape, self.assertEqual；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Normalization, Tests, test, normalizes, dureader, and, collects, negatives, normalize, self.assert_record_shape, self.assertEqual

**调用：** normalize, self.assert_record_shape, self.assertEqual；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetNormalizationTests.test_normalizes_code_datasets` (function, L56-L86)

**签名：** `def test_normalizes_code_datasets(self) -> 未声明`

**作用：** 回归测试：验证 normalizes code datasets 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：normalize, self.assert_record_shape, self.assertEqual；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Normalization, Tests, test, normalizes, code, datasets, normalize, self.assert_record_shape, self.assertEqual

**调用：** normalize, self.assert_record_shape, self.assertEqual；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetNormalizationTests.test_normalizes_qa_datasets_and_removes_nq_html_tokens` (function, L88-L122)

**签名：** `def test_normalizes_qa_datasets_and_removes_nq_html_tokens(self) -> 未声明`

**作用：** 回归测试：验证 normalizes qa datasets and removes nq html tokens 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：normalize, self.assertEqual, self.assertNotIn；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Normalization, Tests, test, normalizes, qa, datasets, and, removes, nq, html, tokens, normalize, self.assertEqual, self.assertNotIn

**调用：** normalize, self.assertEqual, self.assertNotIn；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetNormalizationTests.test_normalizes_msmarco_and_rejects_unknown_adapter` (function, L124-L133)

**签名：** `def test_normalizes_msmarco_and_rejects_unknown_adapter(self) -> 未声明`

**作用：** 回归测试：验证 normalizes msmarco and rejects unknown adapter 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：normalize, self.assert_record_shape, self.assertEqual, self.assertRaisesRegex；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Normalization, Tests, test, normalizes, msmarco, and, rejects, unknown, adapter, normalize, self.assert_record_shape, self.assertEqual, self.assertRaisesRegex, 上下文管理

**调用：** normalize, self.assert_record_shape, self.assertEqual, self.assertRaisesRegex；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetNormalizationTests.test_registers_custom_adapter_without_new_physical_parser` (function, L135-L152)

**签名：** `def test_registers_custom_adapter_without_new_physical_parser(self) -> 未声明`

**作用：** 回归测试：验证 registers custom adapter without new physical parser 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：register_adapter, normalize, self.assertIn, self.assertEqual, available_adapters；返回表达式：{'id': row['key'], 'title': None, 'text': row['body'], 'query': None, 'answers': [], 'meta': {'index': index}}；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Normalization, Tests, test, registers, custom, adapter, without, new, physical, parser, register_adapter, normalize, self.assertIn, self.assertEqual, available_adapters

**调用：** register_adapter, normalize, self.assertIn, self.assertEqual, available_adapters；**返回：** {'id': row['key'], 'title': None, 'text': row['body'], 'query': None, 'answers': [], 'meta': {'index': index}}；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetNormalizationTests.test_registers_custom_adapter_without_new_physical_parser.custom_adapter` (function, L136-L144)

**签名：** `def custom_adapter(row, index) -> 未声明`

**作用：** 执行 custom adapter。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：row, index；声明返回：未声明；直接/间接调用：无明显函数调用；返回表达式：{'id': row['key'], 'title': None, 'text': row['body'], 'query': None, 'answers': [], 'meta': {'index': index}}；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Normalization, Tests, test, registers, custom, adapter, without, new, physical, parser

**调用：** 无明显调用；**返回：** {'id': row['key'], 'title': None, 'text': row['body'], 'query': None, 'answers': [], 'meta': {'index': index}}；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetStreamingTests` (class, L155-L299)

**签名：** `class DatasetStreamingTests`

**作用：** 定义 DatasetStreamingTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；类体包含 7 个直接方法。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Streaming, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetStreamingTests.test_infers_parquet_jsonl_and_gzip_formats` (function, L156-L161)

**签名：** `def test_infers_parquet_jsonl_and_gzip_formats(self) -> 未声明`

**作用：** 回归测试：验证 infers parquet jsonl and gzip formats 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, infer_local_format, self.assertRaisesRegex, Path；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Streaming, Tests, test, infers, parquet, jsonl, and, gzip, formats, self.assertEqual, infer_local_format, self.assertRaisesRegex, Path, 上下文管理

**调用：** self.assertEqual, infer_local_format, self.assertRaisesRegex, Path；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetStreamingTests.test_unified_entry_treats_dataset_file_names_as_local` (function, L163-L165)

**签名：** `def test_unified_entry_treats_dataset_file_names_as_local(self) -> 未声明`

**作用：** 回归测试：验证 unified entry treats dataset file names as local 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertRaisesRegex, next, iter_dataset；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Streaming, Tests, test, unified, entry, treats, dataset, file, names, as, local, self.assertRaisesRegex, next, iter_dataset, 上下文管理

**调用：** self.assertRaisesRegex, next, iter_dataset；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetStreamingTests.test_local_reader_streams_rows_through_one_adapter` (function, L167-L187)

**签名：** `def test_local_reader_streams_rows_through_one_adapter(self) -> 未声明`

**作用：** 回归测试：验证 local reader streams rows through one adapter 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, mocked.assert_called_once_with, tempfile.TemporaryDirectory, path.touch, Path, patch, list, iter_local_dataset, str, iter, path.resolve；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Streaming, Tests, test, local, reader, streams, rows, through, one, adapter, self.assertEqual, mocked.assert_called_once_with, tempfile.TemporaryDirectory, path.touch, Path, patch, list, iter_local_dataset, str, iter, path.resolve, 上下文管理

**调用：** self.assertEqual, mocked.assert_called_once_with, tempfile.TemporaryDirectory, path.touch, Path, patch, list, iter_local_dataset, str, iter, path.resolve；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `DatasetStreamingTests.test_dureader_convenience_reader_and_huggingface_config` (function, L189-L226)

**签名：** `def test_dureader_convenience_reader_and_huggingface_config(self) -> 未声明`

**作用：** 回归测试：验证 dureader convenience reader and huggingface config 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, mocked.assert_called_once_with, tempfile.TemporaryDirectory, path.touch, patch, next, Path, iter_huggingface, iter, iter_local_dureader；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Streaming, Tests, test, dureader, convenience, reader, and, huggingface, config, self.assertEqual, mocked.assert_called_once_with, tempfile.TemporaryDirectory, path.touch, patch, next, Path, iter_huggingface, iter, iter_local_dureader, 上下文管理

**调用：** self.assertEqual, mocked.assert_called_once_with, tempfile.TemporaryDirectory, path.touch, patch, next, Path, iter_huggingface, iter, iter_local_dureader；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `DatasetStreamingTests.test_dataset_blocks_keep_text_canonical_and_records_independent` (function, L228-L255)

**签名：** `def test_dataset_blocks_keep_text_canonical_and_records_independent(self) -> 未声明`

**作用：** 回归测试：验证 dataset blocks keep text canonical and records independent 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：list, self.assertEqual, self.assertTrue, iter_dataset_blocks, all；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Streaming, Tests, test, dataset, blocks, keep, text, canonical, and, records, independent, list, self.assertEqual, self.assertTrue, iter_dataset_blocks, all

**调用：** list, self.assertEqual, self.assertTrue, iter_dataset_blocks, all；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetStreamingTests.test_reader_wraps_backend_failures` (function, L257-L263)

**签名：** `def test_reader_wraps_backend_failures(self) -> 未声明`

**作用：** 回归测试：验证 reader wraps backend failures 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：patch, self.assertRaisesRegex, next, OSError, iter_huggingface；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Streaming, Tests, test, reader, wraps, backend, failures, patch, self.assertRaisesRegex, next, OSError, iter_huggingface, 上下文管理

**调用：** patch, self.assertRaisesRegex, next, OSError, iter_huggingface；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `DatasetStreamingTests.test_real_parquet_and_gzipped_jsonl_are_streamed` (function, L266-L299)

**签名：** `def test_real_parquet_and_gzipped_jsonl_are_streamed(self) -> 未声明`

**作用：** 回归测试：验证 real parquet and gzipped jsonl are streamed 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 dataset_reader 模块的行为、边界和错误处理；将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。；输入参数：self；声明返回：未声明；直接/间接调用：unittest.skipUnless, self.assertEqual, tempfile.TemporaryDirectory, Path, parquet.write_table, list, pa.table, iter_local_dureader, gzip.open, stream.write, iter_local_dataset, json.dumps；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 数据集, Hugging Face, Parquet, JSONL, 适配器, 流式读取, unittest, 回归测试, Dataset, Streaming, Tests, test, real, parquet, and, gzipped, jsonl, are, streamed, unittest.skipUnless, self.assertEqual, tempfile.TemporaryDirectory, Path, parquet.write_table, list, pa.table, iter_local_dureader, gzip.open, stream.write, iter_local_dataset, json.dumps, 上下文管理

**调用：** unittest.skipUnless, self.assertEqual, tempfile.TemporaryDirectory, Path, parquet.write_table, list, pa.table, iter_local_dureader, gzip.open, stream.write, iter_local_dataset, json.dumps；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

## personal_local_knowledge_base_v0/tests/test_embedding.py

**文件作用：** 测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。

**语言/关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 27

### `FakeEmbeddingBackend` (class, L32-L58)

**签名：** `class FakeEmbeddingBackend`

**作用：** 定义 FakeEmbeddingBackend 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 5 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Fake, Backend

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `FakeEmbeddingBackend.__init__` (function, L33-L41)

**签名：** `def __init__(self, revision='fake-commit') -> 未声明`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, revision='fake-commit'；声明返回：未声明；直接/间接调用：EmbeddingSettings；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Fake, Backend, init, EmbeddingSettings

**调用：** EmbeddingSettings；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `FakeEmbeddingBackend.model_revision` (function, L44-L45)

**签名：** `def model_revision(self) -> 未声明`

**作用：** 执行 model revision。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：无明显函数调用；返回表达式：self.revision；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Fake, Backend, model

**调用：** 无明显调用；**返回：** self.revision；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `FakeEmbeddingBackend.embed_documents` (function, L47-L52)

**签名：** `def embed_documents(self, texts) -> 未声明`

**作用：** 执行 embed documents，涉及 self.document_calls.append, np.asarray, list, vectors.append。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, texts；声明返回：未声明；直接/间接调用：self.document_calls.append, np.asarray, list, vectors.append；返回表达式：np.asarray(vectors, dtype=np.float32)；显式异常：未发现显式 raise；控制流：条件分支, 循环。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Fake, Backend, embed, documents, self.document_calls.append, np.asarray, list, vectors.append, 条件分支, 循环

**调用：** self.document_calls.append, np.asarray, list, vectors.append；**返回：** np.asarray(vectors, dtype=np.float32)；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `FakeEmbeddingBackend.embed_query` (function, L54-L55)

**签名：** `def embed_query(self, query, *, code=False) -> 未声明`

**作用：** 执行 embed query，涉及 np.asarray。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, query, *, code=False；声明返回：未声明；直接/间接调用：np.asarray；返回表达式：np.asarray([1.0, 0.0], dtype=np.float32)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Fake, Backend, embed, query, np.asarray

**调用：** np.asarray；**返回：** np.asarray([1.0, 0.0], dtype=np.float32)；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `FakeEmbeddingBackend.token_count` (function, L57-L58)

**签名：** `def token_count(self, text) -> 未声明`

**作用：** 执行 token count，涉及 len。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, text；声明返回：未声明；直接/间接调用：len；返回表达式：len(text)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Fake, Backend, token, count, len

**调用：** len；**返回：** len(text)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `block` (function, L61-L75)

**签名：** `def block(content, *, block_id='b0', hard_before=False, hard_after=False) -> 未声明`

**作用：** 执行 block，涉及 DocumentBlock。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：content, *, block_id='b0', hard_before=False, hard_after=False；声明返回：未声明；直接/间接调用：DocumentBlock；返回表达式：DocumentBlock(block_id=block_id, path='sample.md', block_type='paragraph', language=None, heading_path=('Topic',), symbol_path=(), content=content, start_line=1, end_line=1, page_…；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, block, DocumentBlock

**调用：** DocumentBlock；**返回：** DocumentBlock(block_id=block_id, path='sample.md', block_type='paragraph', language=None, heading_path=('Topic',), symbol_path=(), content=content, start_line=1, end_line=1, page_…；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `SemanticChunkingTests` (class, L78-L137)

**签名：** `class SemanticChunkingTests`

**作用：** 定义 SemanticChunkingTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 3 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Semantic, Chunking, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `SemanticChunkingTests.test_similarity_uses_non_overlapping_cores_then_embeds_final_text` (function, L79-L100)

**签名：** `def test_similarity_uses_non_overlapping_cores_then_embeds_final_text(self) -> 未声明`

**作用：** 回归测试：验证 similarity uses non overlapping cores then embeds final text 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：FakeEmbeddingBackend, list, self.assertEqual, self.assertTrue, iter_chunk_blocks, len, all, block；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Semantic, Chunking, Tests, test, similarity, uses, non, overlapping, cores, then, embeds, final, text, FakeEmbeddingBackend, list, self.assertEqual, self.assertTrue, iter_chunk_blocks, len, all, block

**调用：** FakeEmbeddingBackend, list, self.assertEqual, self.assertTrue, iter_chunk_blocks, len, all, block；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `SemanticChunkingTests.test_hard_boundary_prevents_merge_and_overlap` (function, L102-L118)

**签名：** `def test_hard_boundary_prevents_merge_and_overlap(self) -> 未声明`

**作用：** 回归测试：验证 hard boundary prevents merge and overlap 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：FakeEmbeddingBackend, block, list, self.assertEqual, iter_chunk_blocks；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Semantic, Chunking, Tests, test, hard, boundary, prevents, merge, and, overlap, FakeEmbeddingBackend, block, list, self.assertEqual, iter_chunk_blocks

**调用：** FakeEmbeddingBackend, block, list, self.assertEqual, iter_chunk_blocks；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `SemanticChunkingTests.test_different_structure_prevents_merge` (function, L120-L137)

**签名：** `def test_different_structure_prevents_merge(self) -> 未声明`

**作用：** 回归测试：验证 different structure prevents merge 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：FakeEmbeddingBackend, block, replace, list, self.assertEqual, iter_chunk_blocks, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Semantic, Chunking, Tests, test, different, structure, prevents, merge, FakeEmbeddingBackend, block, replace, list, self.assertEqual, iter_chunk_blocks, len

**调用：** FakeEmbeddingBackend, block, replace, list, self.assertEqual, iter_chunk_blocks, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `EmbeddingStorageTests` (class, L140-L242)

**签名：** `class EmbeddingStorageTests`

**作用：** 定义 EmbeddingStorageTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 2 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Storage, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingStorageTests.test_vectors_are_cached_validated_and_retrieved_with_numpy` (function, L141-L207)

**签名：** `def test_vectors_are_cached_validated_and_retrieved_with_numpy(self) -> 未声明`

**作用：** 回归测试：验证 vectors are cached validated and retrieved with numpy 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, path.write_text, FakeEmbeddingBackend, ChunkingConfig, self.assertEqual, self.assertAlmostEqual, self.assertTrue, KnowledgeBase, index_paths, knowledge_base.connection.execute.fetchone, knowledge_base.connection.execute, knowledge_base.ensure_document_embeddings, NumpyVectorIndex.search, knowledge_base.connection.execute.fetchall, all, config.fingerprint_for, NumpyVectorIndex, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Storage, Tests, test, vectors, are, cached, validated, and, retrieved, with, numpy, tempfile.TemporaryDirectory, Path, path.write_text, FakeEmbeddingBackend, ChunkingConfig, self.assertEqual, self.assertAlmostEqual, self.assertTrue, KnowledgeBase, index_paths, knowledge_base.connection.execute.fetchone, knowledge_base.connection.execute, knowledge_base.ensure_document_embeddings, NumpyVectorIndex.search, knowledge_base.connection.execute.fetchall, all, config.fingerprint_for, NumpyVectorIndex, len, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, path.write_text, FakeEmbeddingBackend, ChunkingConfig, self.assertEqual, self.assertAlmostEqual, self.assertTrue, KnowledgeBase, index_paths, knowledge_base.connection.execute.fetchone, knowledge_base.connection.execute, knowledge_base.ensure_document_embeddings, NumpyVectorIndex.search, knowledge_base.connection.execute.fetchall, all, config.fingerprint_for, NumpyVectorIndex, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 模型/向量计算。

### `EmbeddingStorageTests.test_sqlite_vec_retrieval_embeds_query_and_syncs_cached_vectors` (function, L210-L242)

**签名：** `def test_sqlite_vec_retrieval_embeds_query_and_syncs_cached_vectors(self) -> 未声明`

**作用：** 回归测试：验证 sqlite vec retrieval embeds query and syncs cached vectors 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：unittest.skipUnless, tempfile.TemporaryDirectory, Path, BinOp.write_text, FakeEmbeddingBackend, self.assertEqual, self.assertAlmostEqual, KnowledgeBase, index_paths, VectorIndex, index.search, knowledge_base.connection.execute.fetchone, knowledge_base.connection.execute；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Storage, Tests, test, sqlite, vec, retrieval, embeds, query, and, syncs, cached, vectors, unittest.skipUnless, tempfile.TemporaryDirectory, Path, BinOp.write_text, FakeEmbeddingBackend, self.assertEqual, self.assertAlmostEqual, KnowledgeBase, index_paths, VectorIndex, index.search, knowledge_base.connection.execute.fetchone, knowledge_base.connection.execute, 上下文管理

**调用：** unittest.skipUnless, tempfile.TemporaryDirectory, Path, BinOp.write_text, FakeEmbeddingBackend, self.assertEqual, self.assertAlmostEqual, KnowledgeBase, index_paths, VectorIndex, index.search, knowledge_base.connection.execute.fetchone, knowledge_base.connection.execute；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 模型/向量计算。

### `EmbeddingInputTests` (class, L245-L263)

**签名：** `class EmbeddingInputTests`

**作用：** 定义 EmbeddingInputTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 1 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Input, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `EmbeddingInputTests.test_document_and_query_templates_are_stable_natural_text` (function, L246-L263)

**签名：** `def test_document_and_query_templates_are_stable_natural_text(self) -> 未声明`

**作用：** 回归测试：验证 document and query templates are stable natural text 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：build_document_embedding_input, self.assertIn, self.assertNotIn, self.assertEqual, build_query_embedding_input；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Input, Tests, test, document, and, query, templates, are, stable, natural, text, build_document_embedding_input, self.assertIn, self.assertNotIn, self.assertEqual, build_query_embedding_input

**调用：** build_document_embedding_input, self.assertIn, self.assertNotIn, self.assertEqual, build_query_embedding_input；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `_EmbeddingHandler` (class, L266-L313)

**签名：** `class _EmbeddingHandler`

**作用：** 定义 _EmbeddingHandler 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 4 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Handler

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_EmbeddingHandler.log_message` (function, L269-L270)

**签名：** `def log_message(self, format, *args) -> 未声明`

**作用：** 执行 log message。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, format, *args；声明返回：未声明；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Handler, log, message

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `_EmbeddingHandler._send` (function, L272-L278)

**签名：** `def _send(self, payload) -> 未声明`

**作用：** 执行  send，涉及 json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self, payload；声明返回：未声明；直接/间接调用：json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write, str, json.dumps, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Handler, send, json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write, str, json.dumps, len

**调用：** json.dumps.encode, self.send_response, self.send_header, self.end_headers, self.wfile.write, str, json.dumps, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_EmbeddingHandler.do_GET` (function, L280-L293)

**签名：** `def do_GET(self) -> 未声明`

**作用：** 执行 do GET，涉及 self.send_error, self._send。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：self.send_error, self._send；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Handler, do, GET, self.send_error, self._send, 条件分支

**调用：** self.send_error, self._send；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `_EmbeddingHandler.do_POST` (function, L295-L313)

**签名：** `def do_POST(self) -> 未声明`

**作用：** 执行 do POST，涉及 int, json.loads, self.send_error, self.headers.get, self.rfile.read。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：int, json.loads, self.send_error, self.headers.get, self.rfile.read, self.embedding_inputs.extend, self._send, len, enumerate；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Handler, do, POST, int, json.loads, self.send_error, self.headers.get, self.rfile.read, self.embedding_inputs.extend, self._send, len, enumerate, 条件分支

**调用：** int, json.loads, self.send_error, self.headers.get, self.rfile.read, self.embedding_inputs.extend, self._send, len, enumerate；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 模型/向量计算。

### `RemoteEmbeddingTests` (class, L316-L382)

**签名：** `class RemoteEmbeddingTests`

**作用：** 定义 RemoteEmbeddingTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 2 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Remote, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RemoteEmbeddingTests.test_openai_compatible_remote_service_is_batched_and_normalized` (function, L317-L342)

**签名：** `def test_openai_compatible_remote_service_is_batched_and_normalized(self) -> 未声明`

**作用：** 回归测试：验证 openai compatible remote service is batched and normalized 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：ThreadingHTTPServer, threading.Thread, thread.start, RemoteQwen3EmbeddingModel, self.assertEqual, backend.embed_documents, backend.embed_query, self.assertTrue, self.assertFalse, server.shutdown, server.server_close, thread.join, EmbeddingSettings, np.allclose, Subscript.startswith, backend.fits_token_limit；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Remote, Tests, test, openai, compatible, remote, service, is, batched, and, normalized, ThreadingHTTPServer, threading.Thread, thread.start, RemoteQwen3EmbeddingModel, self.assertEqual, backend.embed_documents, backend.embed_query, self.assertTrue, self.assertFalse, server.shutdown, server.server_close, thread.join, EmbeddingSettings, np.allclose, Subscript.startswith, backend.fits_token_limit, 异常处理

**调用：** ThreadingHTTPServer, threading.Thread, thread.start, RemoteQwen3EmbeddingModel, self.assertEqual, backend.embed_documents, backend.embed_query, self.assertTrue, self.assertFalse, server.shutdown, server.server_close, thread.join, EmbeddingSettings, np.allclose, Subscript.startswith, backend.fits_token_limit；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 网络 HTTP 请求, 模型/向量计算。

### `RemoteEmbeddingTests.test_auto_detects_simple_embed_protocol` (function, L344-L382)

**签名：** `def test_auto_detects_simple_embed_protocol(self) -> 未声明`

**作用：** 回归测试：验证 auto detects simple embed protocol 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：ThreadingHTTPServer, threading.Thread, thread.start, RemoteQwen3EmbeddingModel, backend.embed_documents, self.assertTrue, server.shutdown, server.server_close, thread.join, self.send_error, int, json.loads, EmbeddingSettings, np.allclose, self._send, self.headers.get, self.rfile.read；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 异常处理。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Remote, Tests, test, auto, detects, simple, embed, protocol, ThreadingHTTPServer, threading.Thread, thread.start, RemoteQwen3EmbeddingModel, backend.embed_documents, self.assertTrue, server.shutdown, server.server_close, thread.join, self.send_error, int, json.loads, EmbeddingSettings, np.allclose, self._send, self.headers.get, self.rfile.read, 条件分支, 异常处理

**调用：** ThreadingHTTPServer, threading.Thread, thread.start, RemoteQwen3EmbeddingModel, backend.embed_documents, self.assertTrue, server.shutdown, server.server_close, thread.join, self.send_error, int, json.loads, EmbeddingSettings, np.allclose, self._send, self.headers.get, self.rfile.read；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 网络 HTTP 请求, 模型/向量计算。

### `RemoteEmbeddingTests.test_auto_detects_simple_embed_protocol.SimpleHandler` (class, L345-L364)

**签名：** `class SimpleHandler`

**作用：** 定义 SimpleHandler 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；类体包含 2 个直接方法。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Simple, Handler

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RemoteEmbeddingTests.test_auto_detects_simple_embed_protocol.SimpleHandler.do_GET` (function, L346-L350)

**签名：** `def do_GET(self) -> 未声明`

**作用：** 执行 do GET，涉及 self.send_error, self._send。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：self.send_error, self._send；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Remote, Tests, test, auto, detects, simple, embed, protocol, Simple, Handler, do, GET, self.send_error, self._send, 条件分支

**调用：** self.send_error, self._send；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RemoteEmbeddingTests.test_auto_detects_simple_embed_protocol.SimpleHandler.do_POST` (function, L352-L364)

**签名：** `def do_POST(self) -> 未声明`

**作用：** 执行 do POST，涉及 int, json.loads, self.send_error, self.headers.get, self.rfile.read。

**详细语义：** 所属模块职责：测试文件：验证 embedding 模块的行为、边界和错误处理；定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。；输入参数：self；声明返回：未声明；直接/间接调用：int, json.loads, self.send_error, self.headers.get, self.rfile.read, self._send；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** Embedding, Qwen3, 向量校验, 远程 HTTP, revision, 归一化, unittest, 回归测试, Remote, Tests, test, auto, detects, simple, embed, protocol, Simple, Handler, do, POST, int, json.loads, self.send_error, self.headers.get, self.rfile.read, self._send, 条件分支

**调用：** int, json.loads, self.send_error, self.headers.get, self.rfile.read, self._send；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 模型/向量计算。

## personal_local_knowledge_base_v0/tests/test_extractors.py

**文件作用：** 测试文件：验证 extractors 模块的行为、边界和错误处理；按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。

**语言/关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 3

### `ExtractorTests` (class, L13-L76)

**签名：** `class ExtractorTests`

**作用：** 定义 ExtractorTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 extractors 模块的行为、边界和错误处理；按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；类体包含 2 个直接方法。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, unittest, 回归测试, Extractor, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `ExtractorTests.test_extracts_text_from_pdf_text_layer` (function, L15-L46)

**签名：** `def test_extracts_text_from_pdf_text_layer(self) -> 未声明`

**作用：** 回归测试：验证 extracts text from pdf text layer 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 extractors 模块的行为、边界和错误处理；按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；输入参数：self；声明返回：未声明；直接/间接调用：unittest.skipUnless, tempfile.TemporaryDirectory, PdfWriter, writer.add_blank_page, DictionaryObject, DecodedStreamObject, stream.set_data, extract_document, self.assertEqual, self.assertIsNone, self.assertIn, Path, NameObject, path.open, writer.write, Constant.join, iter_document_text；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, unittest, 回归测试, Extractor, Tests, test, extracts, text, from, pdf, layer, unittest.skipUnless, tempfile.TemporaryDirectory, PdfWriter, writer.add_blank_page, DictionaryObject, DecodedStreamObject, stream.set_data, extract_document, self.assertEqual, self.assertIsNone, self.assertIn, Path, NameObject, path.open, writer.write, Constant.join, iter_document_text, 上下文管理

**调用：** unittest.skipUnless, tempfile.TemporaryDirectory, PdfWriter, writer.add_blank_page, DictionaryObject, DecodedStreamObject, stream.set_data, extract_document, self.assertEqual, self.assertIsNone, self.assertIn, Path, NameObject, path.open, writer.write, Constant.join, iter_document_text；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `ExtractorTests.test_extracts_text_and_table_from_pptx` (function, L49-L76)

**签名：** `def test_extracts_text_and_table_from_pptx(self) -> 未声明`

**作用：** 回归测试：验证 extracts text and table from pptx 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 extractors 模块的行为、边界和错误处理；按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。；输入参数：self；声明返回：未声明；直接/间接调用：unittest.skipUnless, tempfile.TemporaryDirectory, Presentation, presentation.slides.add_slide, slide.shapes.add_textbox, presentation.save, extract_document, self.assertEqual, self.assertIsNone, Constant.join, self.assertIn, Path, Inches, slide.shapes.add_table, table.cell, iter_document_text；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 文件抽取, TXT, Markdown, PDF, PPTX, SHA-256, unittest, 回归测试, Extractor, Tests, test, extracts, text, and, table, from, pptx, unittest.skipUnless, tempfile.TemporaryDirectory, Presentation, presentation.slides.add_slide, slide.shapes.add_textbox, presentation.save, extract_document, self.assertEqual, self.assertIsNone, Constant.join, self.assertIn, Path, Inches, slide.shapes.add_table, table.cell, iter_document_text, 上下文管理

**调用：** unittest.skipUnless, tempfile.TemporaryDirectory, Presentation, presentation.slides.add_slide, slide.shapes.add_textbox, presentation.save, extract_document, self.assertEqual, self.assertIsNone, Constant.join, self.assertIn, Path, Inches, slide.shapes.add_table, table.cell, iter_document_text；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

## personal_local_knowledge_base_v0/tests/test_highlighting.py

**文件作用：** 测试文件：验证 highlighting 模块的行为、边界和错误处理；把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。

**语言/关键词：** 关键词, FTS5, 转义, 高亮, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 4

### `HighlightingTests` (class, L8-L23)

**签名：** `class HighlightingTests`

**作用：** 定义 HighlightingTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 highlighting 模块的行为、边界和错误处理；把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。；类体包含 3 个直接方法。

**关键词：** 关键词, FTS5, 转义, 高亮, unittest, 回归测试, Highlighting, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `HighlightingTests.test_highlights_case_insensitively` (function, L9-L14)

**签名：** `def test_highlights_case_insensitively(self) -> 未声明`

**作用：** 回归测试：验证 highlights case insensitively 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 highlighting 模块的行为、边界和错误处理；把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, highlight_text；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 关键词, FTS5, 转义, 高亮, unittest, 回归测试, Highlighting, Tests, test, highlights, case, insensitively, self.assertEqual, highlight_text

**调用：** self.assertEqual, highlight_text；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `HighlightingTests.test_escapes_fts_syntax` (function, L16-L18)

**签名：** `def test_escapes_fts_syntax(self) -> 未声明`

**作用：** 回归测试：验证 escapes fts syntax 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 highlighting 模块的行为、边界和错误处理；把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, to_fts_query；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 关键词, FTS5, 转义, 高亮, unittest, 回归测试, Highlighting, Tests, test, escapes, fts, syntax, self.assertEqual, to_fts_query

**调用：** self.assertEqual, to_fts_query；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `HighlightingTests.test_rejects_blank_query` (function, L20-L23)

**签名：** `def test_rejects_blank_query(self) -> 未声明`

**作用：** 回归测试：验证 rejects blank query 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 highlighting 模块的行为、边界和错误处理；把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertRaises, to_fts_query；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 关键词, FTS5, 转义, 高亮, unittest, 回归测试, Highlighting, Tests, test, rejects, blank, query, self.assertRaises, to_fts_query, 上下文管理

**调用：** self.assertRaises, to_fts_query；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

## personal_local_knowledge_base_v0/tests/test_indexer.py

**文件作用：** 测试文件：验证 indexer 模块的行为、边界和错误处理；发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。

**语言/关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 7

### `IndexerTests` (class, L12-L186)

**签名：** `class IndexerTests`

**作用：** 定义 IndexerTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 indexer 模块的行为、边界和错误处理；发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；类体包含 6 个直接方法。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, unittest, 回归测试, Indexer, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `IndexerTests.test_excludes_directories_deduplicates_inputs_and_limits_files` (function, L13-L35)

**签名：** `def test_excludes_directories_deduplicates_inputs_and_limits_files(self) -> 未声明`

**作用：** 回归测试：验证 excludes directories deduplicates inputs and limits files 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 indexer 模块的行为、边界和错误处理；发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, BinOp.write_text, BinOp.mkdir, list, self.assertEqual, discover_files, sorted；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, unittest, 回归测试, Indexer, Tests, test, excludes, directories, deduplicates, inputs, and, limits, files, tempfile.TemporaryDirectory, Path, BinOp.write_text, BinOp.mkdir, list, self.assertEqual, discover_files, sorted, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, BinOp.write_text, BinOp.mkdir, list, self.assertEqual, discover_files, sorted；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `IndexerTests.test_json_config_is_not_indexed_when_inside_input_directory` (function, L37-L62)

**签名：** `def test_json_config_is_not_indexed_when_inside_input_directory(self) -> 未声明`

**作用：** 回归测试：验证 json config is not indexed when inside input directory 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 indexer 模块的行为、边界和错误处理；发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, data_path.write_text, config_path.write_text, JsonProfile.from_file, KnowledgeBase, index_paths, self.assertEqual, knowledge_base.document_count, knowledge_base.list_documents；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, unittest, 回归测试, Indexer, Tests, test, json, config, is, not, indexed, when, inside, input, directory, tempfile.TemporaryDirectory, Path, data_path.write_text, config_path.write_text, JsonProfile.from_file, KnowledgeBase, index_paths, self.assertEqual, knowledge_base.document_count, knowledge_base.list_documents, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, data_path.write_text, config_path.write_text, JsonProfile.from_file, KnowledgeBase, index_paths, self.assertEqual, knowledge_base.document_count, knowledge_base.list_documents；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `IndexerTests.test_oversized_json_is_rejected_before_parsing` (function, L64-L86)

**签名：** `def test_oversized_json_is_rejected_before_parsing(self) -> 未声明`

**作用：** 回归测试：验证 oversized json is rejected before parsing 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 indexer 模块的行为、边界和错误处理；发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, data_path.write_text, config_path.write_text, JsonProfile.from_file, KnowledgeBase, index_paths, self.assertEqual, knowledge_base.document_count；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, unittest, 回归测试, Indexer, Tests, test, oversized, json, is, rejected, before, parsing, tempfile.TemporaryDirectory, Path, data_path.write_text, config_path.write_text, JsonProfile.from_file, KnowledgeBase, index_paths, self.assertEqual, knowledge_base.document_count, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, data_path.write_text, config_path.write_text, JsonProfile.from_file, KnowledgeBase, index_paths, self.assertEqual, knowledge_base.document_count；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `IndexerTests.test_reports_single_file_progress_events` (function, L88-L108)

**签名：** `def test_reports_single_file_progress_events(self) -> 未声明`

**作用：** 回归测试：验证 reports single file progress events 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 indexer 模块的行为、边界和错误处理；发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, BinOp.write_text, self.assertEqual, KnowledgeBase, index_paths；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, unittest, 回归测试, Indexer, Tests, test, reports, single, file, progress, events, tempfile.TemporaryDirectory, Path, BinOp.write_text, self.assertEqual, KnowledgeBase, index_paths, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, BinOp.write_text, self.assertEqual, KnowledgeBase, index_paths；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `IndexerTests.test_large_json_record_is_chunked_without_merging_next_record` (function, L110-L149)

**签名：** `def test_large_json_record_is_chunked_without_merging_next_record(self) -> 未声明`

**作用：** 回归测试：验证 large json record is chunked without merging next record 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 indexer 模块的行为、边界和错误处理；发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, data_path.write_text, JsonProfile, self.assertEqual, self.assertGreater, self.assertTrue, KnowledgeBase, index_paths, knowledge_base.connection.execute.fetchall, len, JsonField, knowledge_base.connection.execute；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, unittest, 回归测试, Indexer, Tests, test, large, json, record, is, chunked, without, merging, next, tempfile.TemporaryDirectory, Path, data_path.write_text, JsonProfile, self.assertEqual, self.assertGreater, self.assertTrue, KnowledgeBase, index_paths, knowledge_base.connection.execute.fetchall, len, JsonField, knowledge_base.connection.execute, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, data_path.write_text, JsonProfile, self.assertEqual, self.assertGreater, self.assertTrue, KnowledgeBase, index_paths, knowledge_base.connection.execute.fetchall, len, JsonField, knowledge_base.connection.execute；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `IndexerTests.test_indexes_txt_and_markdown_incrementally` (function, L151-L186)

**签名：** `def test_indexes_txt_and_markdown_incrementally(self) -> 未声明`

**作用：** 回归测试：验证 indexes txt and markdown incrementally 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 indexer 模块的行为、边界和错误处理；发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, BinOp.write_text, KnowledgeBase, index_paths, self.assertEqual, self.assertTrue, knowledge_base.search, knowledge_base.document_count；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 增量索引, 文件发现, 排除规则, 进度, 单文件隔离, unittest, 回归测试, Indexer, Tests, test, indexes, txt, and, markdown, incrementally, tempfile.TemporaryDirectory, Path, BinOp.write_text, KnowledgeBase, index_paths, self.assertEqual, self.assertTrue, knowledge_base.search, knowledge_base.document_count, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, BinOp.write_text, KnowledgeBase, index_paths, self.assertEqual, self.assertTrue, knowledge_base.search, knowledge_base.document_count；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

## personal_local_knowledge_base_v0/tests/test_json_parser.py

**文件作用：** 测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。

**语言/关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 18

### `JsonParserTests` (class, L22-L360)

**签名：** `class JsonParserTests`

**作用：** 定义 JsonParserTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；类体包含 17 个直接方法。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonParserTests.test_parse_human_readable_sizes` (function, L23-L28)

**签名：** `def test_parse_human_readable_sizes(self) -> 未声明`

**作用：** 回归测试：验证 parse human readable sizes 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, parse_size；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, parse, human, readable, sizes, self.assertEqual, parse_size

**调用：** self.assertEqual, parse_size；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonParserTests.test_parse_size_rejects_invalid_values` (function, L30-L33)

**签名：** `def test_parse_size_rejects_invalid_values(self) -> 未声明`

**作用：** 回归测试：验证 parse size rejects invalid values 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：self.subTest, self.assertRaises, parse_size；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环, 上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, parse, size, rejects, invalid, values, self.subTest, self.assertRaises, parse_size, 循环, 上下文管理

**调用：** self.subTest, self.assertRaises, parse_size；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonParserTests._profile` (function, L35-L59)

**签名：** `def _profile(self, *, index_mode: str='record', record_path: str='$', filters: tuple[JsonFilter, ...] | None=None) -> JsonProfile`

**作用：** 执行  profile，涉及 JsonProfile, JsonField, JsonFilter。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self, *, index_mode: str='record', record_path: str='$', filters: tuple[JsonFilter, ...] | None=None；声明返回：JsonProfile；直接/间接调用：JsonProfile, JsonField, JsonFilter；返回表达式：JsonProfile(name='items', record_path=record_path, index_mode=index_mode, fields=(JsonField(path='id', name='ID'), JsonField(path='title', name='标题'), JsonField(path='tags[*]', na…；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, profile, JsonProfile, JsonField, JsonFilter, 条件分支

**调用：** JsonProfile, JsonField, JsonFilter；**返回：** JsonProfile(name='items', record_path=record_path, index_mode=index_mode, fields=(JsonField(path='id', name='ID'), JsonField(path='title', name='标题'), JsonField(path='tags[*]', na…；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `JsonParserTests._write_json_lines` (function, L61-L83)

**签名：** `def _write_json_lines(self, root: Path) -> Path`

**作用：** 执行  write json lines，涉及 path.write_text, Constant.join, json.dumps。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self, root: Path；声明返回：Path；直接/间接调用：path.write_text, Constant.join, json.dumps；返回表达式：path；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, write, json, lines, path.write_text, Constant.join, json.dumps

**调用：** path.write_text, Constant.join, json.dumps；**返回：** path；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `JsonParserTests.test_json_lines_are_parsed_across_small_read_chunks` (function, L85-L94)

**签名：** `def test_json_lines_are_parsed_across_small_read_chunks(self) -> 未声明`

**作用：** 回归测试：验证 json lines are parsed across small read chunks 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, self._write_json_lines, list, self.assertEqual, self.assertIn, self.assertNotIn, Path, iter_json_text, len, self._profile；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, json, lines, are, parsed, across, small, read, chunks, tempfile.TemporaryDirectory, self._write_json_lines, list, self.assertEqual, self.assertIn, self.assertNotIn, Path, iter_json_text, len, self._profile, 上下文管理

**调用：** tempfile.TemporaryDirectory, self._write_json_lines, list, self.assertEqual, self.assertIn, self.assertNotIn, Path, iter_json_text, len, self._profile；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `JsonParserTests.test_top_level_array_is_streamed_one_record_at_a_time` (function, L96-L115)

**签名：** `def test_top_level_array_is_streamed_one_record_at_a_time(self) -> 未声明`

**作用：** 回归测试：验证 top level array is streamed one record at a time 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, path.write_text, self._profile, list, self.assertEqual, self.assertIn, Path, json.dumps, iter_json_text, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, top, level, array, is, streamed, one, record, at, a, time, tempfile.TemporaryDirectory, path.write_text, self._profile, list, self.assertEqual, self.assertIn, Path, json.dumps, iter_json_text, len, 上下文管理

**调用：** tempfile.TemporaryDirectory, path.write_text, self._profile, list, self.assertEqual, self.assertIn, Path, json.dumps, iter_json_text, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonParserTests.test_nested_record_path_yields_before_later_record_is_parsed` (function, L117-L142)

**签名：** `def test_nested_record_path_yields_before_later_record_is_parsed(self) -> 未声明`

**作用：** 回归测试：验证 nested record path yields before later record is parsed 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, path.write_text, self._profile, iter_json_text, Path, next, self.assertIn, records.close, self.assertRaises；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, nested, record, path, yields, before, later, is, parsed, tempfile.TemporaryDirectory, path.write_text, self._profile, iter_json_text, Path, next, self.assertIn, records.close, self.assertRaises, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, path.write_text, self._profile, iter_json_text, Path, next, self.assertIn, records.close, self.assertRaises；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonParserTests.test_nested_record_path_indexes_each_array_item` (function, L144-L174)

**签名：** `def test_nested_record_path_indexes_each_array_item(self) -> 未声明`

**作用：** 回归测试：验证 nested record path indexes each array item 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, path.write_text, JsonProfile, list, self.assertEqual, json.dumps, iter_json_text, JsonField, JsonFilter；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, nested, record, path, indexes, each, array, item, tempfile.TemporaryDirectory, Path, path.write_text, JsonProfile, list, self.assertEqual, json.dumps, iter_json_text, JsonField, JsonFilter, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, path.write_text, JsonProfile, list, self.assertEqual, json.dumps, iter_json_text, JsonField, JsonFilter；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonParserTests.test_record_larger_than_probe_is_streamed_without_merging_records` (function, L176-L215)

**签名：** `def test_record_larger_than_probe_is_streamed_without_merging_records(self) -> 未声明`

**作用：** 回归测试：验证 record larger than probe is streamed without merging records 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, json.dumps, path.write_text, JsonProfile, list, self.assertGreater, self.assertTrue, self.assertEqual, Path, iter_json_text, len, all, current.append, Constant.join, getattr, str, JsonField；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, record, larger, than, probe, is, streamed, without, merging, records, tempfile.TemporaryDirectory, json.dumps, path.write_text, JsonProfile, list, self.assertGreater, self.assertTrue, self.assertEqual, Path, iter_json_text, len, all, current.append, Constant.join, getattr, str, JsonField, 条件分支, 循环, 上下文管理

**调用：** tempfile.TemporaryDirectory, json.dumps, path.write_text, JsonProfile, list, self.assertGreater, self.assertTrue, self.assertEqual, Path, iter_json_text, len, all, current.append, Constant.join, getattr, str, JsonField；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonParserTests.test_nested_large_record_keeps_record_boundary` (function, L217-L256)

**签名：** `def test_nested_large_record_keeps_record_boundary(self) -> 未声明`

**作用：** 回归测试：验证 nested large record keeps record boundary 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, path.write_text, JsonProfile, list, self.assertEqual, Path, json.dumps, iter_json_text, current.append, Constant.join, getattr, str, JsonField；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支, 循环, 上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, nested, large, record, keeps, boundary, tempfile.TemporaryDirectory, path.write_text, JsonProfile, list, self.assertEqual, Path, json.dumps, iter_json_text, current.append, Constant.join, getattr, str, JsonField, 条件分支, 循环, 上下文管理

**调用：** tempfile.TemporaryDirectory, path.write_text, JsonProfile, list, self.assertEqual, Path, json.dumps, iter_json_text, current.append, Constant.join, getattr, str, JsonField；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonParserTests.test_preview_rejects_a_record_that_cannot_be_materialized` (function, L258-L281)

**签名：** `def test_preview_rejects_a_record_that_cannot_be_materialized(self) -> 未声明`

**作用：** 回归测试：验证 preview rejects a record that cannot be materialized 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, path.write_text, JsonProfile, Path, json.dumps, self.assertRaises, parse_json_preview, JsonField；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, preview, rejects, a, record, that, cannot, be, materialized, tempfile.TemporaryDirectory, path.write_text, JsonProfile, Path, json.dumps, self.assertRaises, parse_json_preview, JsonField, 上下文管理

**调用：** tempfile.TemporaryDirectory, path.write_text, JsonProfile, Path, json.dumps, self.assertRaises, parse_json_preview, JsonField；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonParserTests.test_file_mode_keeps_streaming_blocks_but_combines_downstream` (function, L283-L291)

**签名：** `def test_file_mode_keeps_streaming_blocks_but_combines_downstream(self) -> 未声明`

**作用：** 回归测试：验证 file mode keeps streaming blocks but combines downstream 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, self._write_json_lines, self._profile, list, self.assertEqual, self.assertIn, Path, iter_json_text, Constant.join.count, Constant.join；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, file, mode, keeps, streaming, blocks, but, combines, downstream, tempfile.TemporaryDirectory, self._write_json_lines, self._profile, list, self.assertEqual, self.assertIn, Path, iter_json_text, Constant.join.count, Constant.join, 上下文管理

**调用：** tempfile.TemporaryDirectory, self._write_json_lines, self._profile, list, self.assertEqual, self.assertIn, Path, iter_json_text, Constant.join.count, Constant.join；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `JsonParserTests.test_preview_only_consumes_requested_records` (function, L293-L300)

**签名：** `def test_preview_only_consumes_requested_records(self) -> 未声明`

**作用：** 回归测试：验证 preview only consumes requested records 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, self._write_json_lines, parse_json_preview, self.assertEqual, self.assertIn, Path, self._profile, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, preview, only, consumes, requested, records, tempfile.TemporaryDirectory, self._write_json_lines, parse_json_preview, self.assertEqual, self.assertIn, Path, self._profile, len, 上下文管理

**调用：** tempfile.TemporaryDirectory, self._write_json_lines, parse_json_preview, self.assertEqual, self.assertIn, Path, self._profile, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `JsonParserTests.test_json_size_limit_is_checked_before_streaming` (function, L302-L307)

**签名：** `def test_json_size_limit_is_checked_before_streaming(self) -> 未声明`

**作用：** 回归测试：验证 json size limit is checked before streaming 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, self._write_json_lines, Path, self.assertRaises, list, iter_json_text, self._profile；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, json, size, limit, is, checked, before, streaming, tempfile.TemporaryDirectory, self._write_json_lines, Path, self.assertRaises, list, iter_json_text, self._profile, 上下文管理

**调用：** tempfile.TemporaryDirectory, self._write_json_lines, Path, self.assertRaises, list, iter_json_text, self._profile；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonParserTests.test_structure_scan_does_not_use_index_size_limit_by_default` (function, L309-L316)

**签名：** `def test_structure_scan_does_not_use_index_size_limit_by_default(self) -> 未声明`

**作用：** 回归测试：验证 structure scan does not use index size limit by default 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, self._write_json_lines, check_size.assert_called_once_with, Path, patch, inspect_json_structure, path.resolve；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, structure, scan, does, not, use, index, size, limit, by, default, tempfile.TemporaryDirectory, self._write_json_lines, check_size.assert_called_once_with, Path, patch, inspect_json_structure, path.resolve, 上下文管理

**调用：** tempfile.TemporaryDirectory, self._write_json_lines, check_size.assert_called_once_with, Path, patch, inspect_json_structure, path.resolve；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonParserTests.test_structure_report_summarizes_nested_paths` (function, L318-L344)

**签名：** `def test_structure_report_summarizes_nested_paths(self) -> 未声明`

**作用：** 回归测试：验证 structure report summarizes nested paths 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, path.write_text, inspect_json_structure, self.assertFalse, self.assertEqual, Path, json.dumps；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, structure, report, summarizes, nested, paths, tempfile.TemporaryDirectory, path.write_text, inspect_json_structure, self.assertFalse, self.assertEqual, Path, json.dumps, 上下文管理

**调用：** tempfile.TemporaryDirectory, path.write_text, inspect_json_structure, self.assertFalse, self.assertEqual, Path, json.dumps；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `JsonParserTests.test_json_lines_can_go_through_the_indexer` (function, L346-L360)

**签名：** `def test_json_lines_can_go_through_the_indexer(self) -> 未声明`

**作用：** 回归测试：验证 json lines can go through the indexer 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 json_parser 模块的行为、边界和错误处理；实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self._write_json_lines, KnowledgeBase, index_paths, self.assertEqual, self.assertTrue, self.assertFalse, knowledge_base.chunk_count, knowledge_base.search, self._profile；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** JSON, JSONPath, 流式解析, 记录边界, 超大记录, 字段过滤, unittest, 回归测试, Json, Parser, Tests, test, json, lines, can, go, through, the, indexer, tempfile.TemporaryDirectory, Path, self._write_json_lines, KnowledgeBase, index_paths, self.assertEqual, self.assertTrue, self.assertFalse, knowledge_base.chunk_count, knowledge_base.search, self._profile, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self._write_json_lines, KnowledgeBase, index_paths, self.assertEqual, self.assertTrue, self.assertFalse, knowledge_base.chunk_count, knowledge_base.search, self._profile；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

## personal_local_knowledge_base_v0/tests/test_rag.py

**文件作用：** 测试文件：验证 rag 相关功能的行为、边界和错误处理。

**语言/关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 42

### `_document` (function, L27-L36)

**签名：** `def _document(path: Path, content: str, sha256: str) -> ExtractedDocument`

**作用：** 执行  document，涉及 path.write_text, ExtractedDocument, path.resolve, len, content.encode。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：path: Path, content: str, sha256: str；声明返回：ExtractedDocument；直接/间接调用：path.write_text, ExtractedDocument, path.resolve, len, content.encode；返回表达式：ExtractedDocument(path=path.resolve(), file_type='md', text=content, sha256=sha256, size=len(content.encode('utf-8')), modified_ns=1)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, document, path.write_text, ExtractedDocument, path.resolve, len, content.encode

**调用：** path.write_text, ExtractedDocument, path.resolve, len, content.encode；**返回：** ExtractedDocument(path=path.resolve(), file_type='md', text=content, sha256=sha256, size=len(content.encode('utf-8')), modified_ns=1)；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `_reset_logging_handlers` (function, L39-L43)

**签名：** `def _reset_logging_handlers() -> None`

**作用：** 执行  reset logging handlers，涉及 logging.getLogger, root_logger.removeHandler, handler.close。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：；声明返回：None；直接/间接调用：logging.getLogger, root_logger.removeHandler, handler.close；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, reset, logging, handlers, logging.getLogger, root_logger.removeHandler, handler.close, 循环

**调用：** logging.getLogger, root_logger.removeHandler, handler.close；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 日志输出。

### `FakeClient` (class, L46-L62)

**签名：** `class FakeClient`

**作用：** 定义 FakeClient 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；类体包含 2 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Client

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `FakeClient.__init__` (function, L47-L50)

**签名：** `def __init__(self, content: str='FTS5 是 SQLite 的全文搜索扩展。[1]') -> None`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self, content: str='FTS5 是 SQLite 的全文搜索扩展。[1]'；声明返回：None；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Client, init

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `FakeClient.complete` (function, L52-L62)

**签名：** `def complete(self, messages, *, temperature=0.0) -> 未声明`

**作用：** 执行 complete，涉及 LLMResponse, TokenUsage。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self, messages, *, temperature=0.0；声明返回：未声明；直接/间接调用：LLMResponse, TokenUsage；返回表达式：LLMResponse(content=self.content, usage=TokenUsage(prompt_tokens=120, completion_tokens=18, total_tokens=138))；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Client, complete, LLMResponse, TokenUsage

**调用：** LLMResponse, TokenUsage；**返回：** LLMResponse(content=self.content, usage=TokenUsage(prompt_tokens=120, completion_tokens=18, total_tokens=138))；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests` (class, L65-L644)

**签名：** `class RagTests`

**作用：** 定义 RagTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；类体包含 26 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_client_automatically_loads_dotenv` (function, L66-L97)

**签名：** `def test_client_automatically_loads_dotenv(self) -> 未声明`

**作用：** 回归测试：验证 client automatically loads dotenv 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, BinOp.write_text, Path.cwd, self.assertEqual, os.chdir, patch.dict, LLMClient.from_env, os.environ.pop；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环, 异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, client, automatically, loads, dotenv, tempfile.TemporaryDirectory, Path, BinOp.write_text, Path.cwd, self.assertEqual, os.chdir, patch.dict, LLMClient.from_env, os.environ.pop, 循环, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, BinOp.write_text, Path.cwd, self.assertEqual, os.chdir, patch.dict, LLMClient.from_env, os.environ.pop；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 环境变量读取。

### `RagTests.test_environment_variables_override_dotenv` (function, L99-L128)

**签名：** `def test_environment_variables_override_dotenv(self) -> 未声明`

**作用：** 回归测试：验证 environment variables override dotenv 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, BinOp.write_text, Path.cwd, self.assertEqual, os.chdir, patch.dict, LLMClient.from_env；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, environment, variables, override, dotenv, tempfile.TemporaryDirectory, Path, BinOp.write_text, Path.cwd, self.assertEqual, os.chdir, patch.dict, LLMClient.from_env, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, BinOp.write_text, Path.cwd, self.assertEqual, os.chdir, patch.dict, LLMClient.from_env；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 环境变量读取。

### `RagTests.test_natural_question_retrieves_relevant_chunk` (function, L130-L148)

**签名：** `def test_natural_question_retrieves_relevant_chunk(self) -> 未声明`

**作用：** 回归测试：验证 natural question retrieves relevant chunk 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertEqual, self.assertIn, KnowledgeBase, knowledge_base.replace_document, KeywordRetriever, retriever.retrieve, _document, Chunk；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, natural, question, retrieves, relevant, chunk, tempfile.TemporaryDirectory, Path, self.assertEqual, self.assertIn, KnowledgeBase, knowledge_base.replace_document, KeywordRetriever, retriever.retrieve, _document, Chunk, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertEqual, self.assertIn, KnowledgeBase, knowledge_base.replace_document, KeywordRetriever, retriever.retrieve, _document, Chunk；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_question_chunk_matching_does_not_use_jieba` (function, L150-L169)

**签名：** `def test_question_chunk_matching_does_not_use_jieba(self) -> 未声明`

**作用：** 回归测试：验证 question chunk matching does not use jieba 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, _document, patch, ChunkRetriever.retrieve, Chunk, AssertionError, ChunkRetriever；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, question, chunk, matching, does, not, use, jieba, tempfile.TemporaryDirectory, Path, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, _document, patch, ChunkRetriever.retrieve, Chunk, AssertionError, ChunkRetriever, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, _document, patch, ChunkRetriever.retrieve, Chunk, AssertionError, ChunkRetriever；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_long_natural_question_ranks_shared_phrases_in_large_noisy_corpus` (function, L171-L195)

**签名：** `def test_long_natural_question_ranks_shared_phrases_in_large_noisy_corpus(self) -> 未声明`

**作用：** 回归测试：验证 long natural question ranks shared phrases in large noisy corpus 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertEqual, KnowledgeBase, range, knowledge_base.replace_document, KeywordRetriever.retrieve, _document, Chunk, KeywordRetriever；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, long, natural, question, ranks, shared, phrases, in, large, noisy, corpus, tempfile.TemporaryDirectory, Path, self.assertEqual, KnowledgeBase, range, knowledge_base.replace_document, KeywordRetriever.retrieve, _document, Chunk, KeywordRetriever, 循环, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertEqual, KnowledgeBase, range, knowledge_base.replace_document, KeywordRetriever.retrieve, _document, Chunk, KeywordRetriever；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_model_refusal_is_recorded_as_refused` (function, L197-L210)

**签名：** `def test_model_refusal_is_recorded_as_refused(self) -> 未声明`

**作用：** 回归测试：验证 model refusal is recorded as refused 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertTrue, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, model, refusal, is, recorded, as, refused, tempfile.TemporaryDirectory, Path, self.assertTrue, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertTrue, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_model_refusal_is_recorded_as_refused.lambda@207` (function, L207-L207)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：FakeClient(REFUSAL_ANSWER)；调用：FakeClient；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, FakeClient

**调用：** FakeClient；**返回：** FakeClient(REFUSAL_ANSWER)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_model_specific_refusal_is_recorded_as_refused` (function, L212-L227)

**签名：** `def test_model_specific_refusal_is_recorded_as_refused(self) -> 未声明`

**作用：** 回归测试：验证 model specific refusal is recorded as refused 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertTrue, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, model, specific, refusal, is, recorded, as, refused, tempfile.TemporaryDirectory, Path, self.assertTrue, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertTrue, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_model_specific_refusal_is_recorded_as_refused.lambda@222` (function, L222-L224)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：FakeClient('根据当前知识库资料，无法回答项目预算；资料未提供。')；调用：FakeClient；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, FakeClient

**调用：** FakeClient；**返回：** FakeClient('根据当前知识库资料，无法回答项目预算；资料未提供。')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_context_never_exceeds_limit_with_multiple_documents` (function, L229-L248)

**签名：** `def test_context_never_exceeds_limit_with_multiple_documents(self) -> 未声明`

**作用：** 回归测试：验证 context never exceeds limit with multiple documents 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertLessEqual, self.assertTrue, self.assertGreaterEqual, KnowledgeBase, range, KeywordRetriever.retrieve, len, knowledge_base.replace_document, _document, KeywordRetriever, Chunk；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, context, never, exceeds, limit, with, multiple, documents, tempfile.TemporaryDirectory, Path, self.assertLessEqual, self.assertTrue, self.assertGreaterEqual, KnowledgeBase, range, KeywordRetriever.retrieve, len, knowledge_base.replace_document, _document, KeywordRetriever, Chunk, 循环, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertLessEqual, self.assertTrue, self.assertGreaterEqual, KnowledgeBase, range, KeywordRetriever.retrieve, len, knowledge_base.replace_document, _document, KeywordRetriever, Chunk；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_retrieval_includes_adjacent_chunk_under_same_citation` (function, L250-L272)

**签名：** `def test_retrieval_includes_adjacent_chunk_under_same_citation(self) -> 未声明`

**作用：** 回归测试：验证 retrieval includes adjacent chunk under same citation 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertEqual, self.assertIn, KnowledgeBase, _document, knowledge_base.replace_document, KeywordRetriever.retrieve, Chunk, KeywordRetriever；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, retrieval, includes, adjacent, chunk, under, same, citation, tempfile.TemporaryDirectory, Path, self.assertEqual, self.assertIn, KnowledgeBase, _document, knowledge_base.replace_document, KeywordRetriever.retrieve, Chunk, KeywordRetriever, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertEqual, self.assertIn, KnowledgeBase, _document, knowledge_base.replace_document, KeywordRetriever.retrieve, Chunk, KeywordRetriever；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_answer_uses_context_and_reports_sources_usage_and_time` (function, L274-L294)

**签名：** `def test_answer_uses_context_and_reports_sources_usage_and_time(self) -> 未声明`

**作用：** 回归测试：验证 answer uses context and reports sources usage and time 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertIn, self.assertEqual, self.assertGreaterEqual, KnowledgeBase, knowledge_base.replace_document, FakeClient, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, answer, uses, context, and, reports, sources, usage, time, tempfile.TemporaryDirectory, Path, self.assertIn, self.assertEqual, self.assertGreaterEqual, KnowledgeBase, knowledge_base.replace_document, FakeClient, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertIn, self.assertEqual, self.assertGreaterEqual, KnowledgeBase, knowledge_base.replace_document, FakeClient, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_answer_uses_context_and_reports_sources_usage_and_time.lambda@285` (function, L285-L285)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：client；调用：无明显函数调用；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda

**调用：** 无明显调用；**返回：** client；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_valid_model_citation_is_accepted` (function, L296-L310)

**签名：** `def test_valid_model_citation_is_accepted(self) -> 未声明`

**作用：** 回归测试：验证 valid model citation is accepted 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertFalse, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, valid, model, citation, is, accepted, tempfile.TemporaryDirectory, Path, self.assertFalse, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertFalse, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_valid_model_citation_is_accepted.lambda@306` (function, L306-L306)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：FakeClient('项目代号是晨星。[1]')；调用：FakeClient；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, FakeClient

**调用：** FakeClient；**返回：** FakeClient('项目代号是晨星。[1]')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_model_answer_without_citation_is_rejected` (function, L312-L324)

**签名：** `def test_model_answer_without_citation_is_rejected(self) -> 未声明`

**作用：** 回归测试：验证 model answer without citation is rejected 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, model, answer, without, citation, is, rejected, tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_model_answer_without_citation_is_rejected.lambda@323` (function, L323-L323)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：FakeClient('This answer has no citation.')；调用：FakeClient；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, FakeClient

**调用：** FakeClient；**返回：** FakeClient('This answer has no citation.')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_model_answer_with_only_invalid_citation_is_rejected` (function, L326-L338)

**签名：** `def test_model_answer_with_only_invalid_citation_is_rejected(self) -> 未声明`

**作用：** 回归测试：验证 model answer with only invalid citation is rejected 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, model, answer, with, only, invalid, citation, is, rejected, tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_model_answer_with_only_invalid_citation_is_rejected.lambda@337` (function, L337-L337)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：FakeClient('项目代号是晨星。[99]')；调用：FakeClient；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, FakeClient

**调用：** FakeClient；**返回：** FakeClient('项目代号是晨星。[99]')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_model_answer_with_valid_and_invalid_citations_is_rejected` (function, L340-L354)

**签名：** `def test_model_answer_with_valid_and_invalid_citations_is_rejected(self) -> 未声明`

**作用：** 回归测试：验证 model answer with valid and invalid citations is rejected 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, model, answer, with, valid, and, invalid, citations, is, rejected, tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_model_answer_with_valid_and_invalid_citations_is_rejected.lambda@351` (function, L351-L353)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：FakeClient('项目代号是晨星。[1] 负责人是未知。[99]')；调用：FakeClient；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, FakeClient

**调用：** FakeClient；**返回：** FakeClient('项目代号是晨星。[1] 负责人是未知。[99]')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_model_refusal_without_citation_is_accepted` (function, L356-L370)

**签名：** `def test_model_refusal_without_citation_is_accepted(self) -> 未声明`

**作用：** 回归测试：验证 model refusal without citation is accepted 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertTrue, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, model, refusal, without, citation, is, accepted, tempfile.TemporaryDirectory, Path, self.assertTrue, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertTrue, self.assertEqual, KnowledgeBase, knowledge_base.replace_document, RagAnswerer.answer, _document, Chunk, RagAnswerer, KeywordRetriever, FakeClient；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_model_refusal_without_citation_is_accepted.lambda@366` (function, L366-L366)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：FakeClient(REFUSAL_ANSWER)；调用：FakeClient；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, FakeClient

**调用：** FakeClient；**返回：** FakeClient(REFUSAL_ANSWER)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_model_refusal_with_invalid_citation_is_rejected` (function, L372-L384)

**签名：** `def test_model_refusal_with_invalid_citation_is_rejected(self) -> 未声明`

**作用：** 回归测试：验证 model refusal with invalid citation is rejected 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, model, refusal, with, invalid, citation, is, rejected, tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, KnowledgeBase, knowledge_base.replace_document, _document, self.assertRaisesRegex, RagAnswerer.answer, Chunk, RagAnswerer, KeywordRetriever, FakeClient；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_model_refusal_with_invalid_citation_is_rejected.lambda@383` (function, L383-L383)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：FakeClient(f'{REFUSAL_ANSWER}[99]')；调用：FakeClient；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, FakeClient

**调用：** FakeClient；**返回：** FakeClient(f'{REFUSAL_ANSWER}[99]')；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_no_results_refuses_without_creating_client` (function, L386-L404)

**签名：** `def test_no_results_refuses_without_creating_client(self) -> 未声明`

**作用：** 回归测试：验证 no results refuses without creating client 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, self.assertTrue, self.assertEqual, self.assertFalse, FakeClient, KnowledgeBase, RagAnswerer.answer, RagAnswerer, KeywordRetriever；返回表达式：FakeClient()；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, no, results, refuses, without, creating, client, tempfile.TemporaryDirectory, Path, self.assertTrue, self.assertEqual, self.assertFalse, FakeClient, KnowledgeBase, RagAnswerer.answer, RagAnswerer, KeywordRetriever, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, self.assertTrue, self.assertEqual, self.assertFalse, FakeClient, KnowledgeBase, RagAnswerer.answer, RagAnswerer, KeywordRetriever；**返回：** FakeClient()；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `RagTests.test_no_results_refuses_without_creating_client.create_client` (function, L391-L394)

**签名：** `def create_client() -> 未声明`

**作用：** 执行 create client，涉及 FakeClient。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：；声明返回：未声明；直接/间接调用：FakeClient；返回表达式：FakeClient()；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, no, results, refuses, without, creating, client, create, FakeClient

**调用：** FakeClient；**返回：** FakeClient()；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_prompt_treats_context_as_untrusted_and_requires_refusal` (function, L406-L412)

**签名：** `def test_prompt_treats_context_as_untrusted_and_requires_refusal(self) -> 未声明`

**作用：** 回归测试：验证 prompt treats context as untrusted and requires refusal 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：build_messages, self.assertIn, self.assertEqual；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, prompt, treats, context, as, untrusted, and, requires, refusal, build_messages, self.assertIn, self.assertEqual

**调用：** build_messages, self.assertIn, self.assertEqual；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_config_rejects_secret_and_unknown_fields` (function, L414-L423)

**签名：** `def test_config_rejects_secret_and_unknown_fields(self) -> 未声明`

**作用：** 回归测试：验证 config rejects secret and unknown fields 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, path.write_text, Path, json.dumps, self.assertRaisesRegex, RagConfig.from_file；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, config, rejects, secret, and, unknown, fields, tempfile.TemporaryDirectory, path.write_text, Path, json.dumps, self.assertRaisesRegex, RagConfig.from_file, 上下文管理

**调用：** tempfile.TemporaryDirectory, path.write_text, Path, json.dumps, self.assertRaisesRegex, RagConfig.from_file；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `RagTests.test_http_error_never_exposes_api_key` (function, L425-L448)

**签名：** `def test_http_error_never_exposes_api_key(self) -> 未声明`

**作用：** 回归测试：验证 http error never exposes api key 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：LLMClient, json.dumps.encode, urllib.error.HTTPError, self.assertNotIn, self.assertIn, io.BytesIO, patch, str, json.dumps, self.assertRaises, client.complete；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, http, error, never, exposes, api, key, LLMClient, json.dumps.encode, urllib.error.HTTPError, self.assertNotIn, self.assertIn, io.BytesIO, patch, str, json.dumps, self.assertRaises, client.complete, 上下文管理

**调用：** LLMClient, json.dumps.encode, urllib.error.HTTPError, self.assertNotIn, self.assertIn, io.BytesIO, patch, str, json.dumps, self.assertRaises, client.complete；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 网络 HTTP 请求。

### `RagTests.test_cli_failure_log_never_contains_api_key` (function, L450-L496)

**签名：** `def test_cli_failure_log_never_contains_api_key(self) -> 未声明`

**作用：** 回归测试：验证 cli failure log never contains api key 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, source.write_text, json.dumps.encode, urllib.error.HTTPError, BinOp.read_text, self.assertEqual, self.assertNotIn, self.assertIn, KnowledgeBase, index_paths, io.BytesIO, _reset_logging_handlers, json.dumps, patch.dict, patch, main, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, cli, failure, log, never, contains, api, key, tempfile.TemporaryDirectory, Path, source.write_text, json.dumps.encode, urllib.error.HTTPError, BinOp.read_text, self.assertEqual, self.assertNotIn, self.assertIn, KnowledgeBase, index_paths, io.BytesIO, _reset_logging_handlers, json.dumps, patch.dict, patch, main, str, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, source.write_text, json.dumps.encode, urllib.error.HTTPError, BinOp.read_text, self.assertEqual, self.assertNotIn, self.assertIn, KnowledgeBase, index_paths, io.BytesIO, _reset_logging_handlers, json.dumps, patch.dict, patch, main, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 网络 HTTP 请求, 日志输出, 环境变量读取。

### `RagTests.test_cli_invalid_model_citation_returns_nonzero_and_logs_only_error` (function, L498-L538)

**签名：** `def test_cli_invalid_model_citation_returns_nonzero_and_logs_only_error(self) -> 未声明`

**作用：** 回归测试：验证 cli invalid model citation returns nonzero and logs only error 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, source.write_text, BinOp.read_text, self.assertEqual, self.assertIn, self.assertNotIn, KnowledgeBase, index_paths, _reset_logging_handlers, patch.dict, patch, main, FakeClient, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, cli, invalid, model, citation, returns, nonzero, and, logs, only, error, tempfile.TemporaryDirectory, Path, source.write_text, BinOp.read_text, self.assertEqual, self.assertIn, self.assertNotIn, KnowledgeBase, index_paths, _reset_logging_handlers, patch.dict, patch, main, FakeClient, str, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, source.write_text, BinOp.read_text, self.assertEqual, self.assertIn, self.assertNotIn, KnowledgeBase, index_paths, _reset_logging_handlers, patch.dict, patch, main, FakeClient, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 日志输出, 环境变量读取。

### `RagTests.test_no_result_log_redacts_api_key_loaded_from_dotenv` (function, L540-L573)

**签名：** `def test_no_result_log_redacts_api_key_loaded_from_dotenv(self) -> 未声明`

**作用：** 回归测试：验证 no result log redacts api key loaded from dotenv 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, BinOp.write_text, Path.cwd, BinOp.read_text, self.assertEqual, self.assertNotIn, self.assertIn, os.chdir, _reset_logging_handlers, patch.dict, main, os.environ.pop, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环, 异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, no, result, log, redacts, api, key, loaded, from, dotenv, tempfile.TemporaryDirectory, Path, BinOp.write_text, Path.cwd, BinOp.read_text, self.assertEqual, self.assertNotIn, self.assertIn, os.chdir, _reset_logging_handlers, patch.dict, main, os.environ.pop, str, 循环, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, BinOp.write_text, Path.cwd, BinOp.read_text, self.assertEqual, self.assertNotIn, self.assertIn, os.chdir, _reset_logging_handlers, patch.dict, main, os.environ.pop, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 日志输出, 环境变量读取。

### `RagTests.test_invalid_base_url_has_friendly_error` (function, L575-L581)

**签名：** `def test_invalid_base_url_has_friendly_error(self) -> 未声明`

**作用：** 回归测试：验证 invalid base url has friendly error 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertRaisesRegex, LLMClient；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, invalid, base, url, has, friendly, error, self.assertRaisesRegex, LLMClient, 上下文管理

**调用：** self.assertRaisesRegex, LLMClient；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `RagTests.test_cli_ask_outputs_refusal_without_llm_configuration` (function, L583-L604)

**签名：** `def test_cli_ask_outputs_refusal_without_llm_configuration(self) -> 未声明`

**作用：** 回归测试：验证 cli ask outputs refusal without llm configuration 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, io.StringIO, self.assertEqual, self.assertIn, _reset_logging_handlers, output.getvalue, contextlib.redirect_stdout, main, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, cli, ask, outputs, refusal, without, llm, configuration, tempfile.TemporaryDirectory, Path, io.StringIO, self.assertEqual, self.assertIn, _reset_logging_handlers, output.getvalue, contextlib.redirect_stdout, main, str, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, io.StringIO, self.assertEqual, self.assertIn, _reset_logging_handlers, output.getvalue, contextlib.redirect_stdout, main, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 日志输出。

### `RagTests.test_cli_ask_outputs_answer_sources_and_token_usage` (function, L606-L644)

**签名：** `def test_cli_ask_outputs_answer_sources_and_token_usage(self) -> 未声明`

**作用：** 回归测试：验证 cli ask outputs answer sources and token usage 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 rag 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, source.write_text, io.StringIO, FakeClient, output.getvalue, self.assertEqual, self.assertIn, BinOp.read_text, KnowledgeBase, index_paths, _reset_logging_handlers, patch, contextlib.redirect_stdout, main, str；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Rag, Tests, test, cli, ask, outputs, answer, sources, and, token, usage, tempfile.TemporaryDirectory, Path, source.write_text, io.StringIO, FakeClient, output.getvalue, self.assertEqual, self.assertIn, BinOp.read_text, KnowledgeBase, index_paths, _reset_logging_handlers, patch, contextlib.redirect_stdout, main, str, 异常处理, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, source.write_text, io.StringIO, FakeClient, output.getvalue, self.assertEqual, self.assertIn, BinOp.read_text, KnowledgeBase, index_paths, _reset_logging_handlers, patch, contextlib.redirect_stdout, main, str；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 日志输出。

## personal_local_knowledge_base_v0/tests/test_search_validation.py

**文件作用：** 测试文件：验证 search_validation 相关功能的行为、边界和错误处理。

**语言/关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 2

### `SearchValidationTests` (class, L9-L27)

**签名：** `class SearchValidationTests`

**作用：** 定义 SearchValidationTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 search_validation 相关功能的行为、边界和错误处理。；类体包含 1 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Search, Validation, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `SearchValidationTests.test_expected_document_is_returned_for_each_keyword` (function, L10-L27)

**签名：** `def test_expected_document_is_returned_for_each_keyword(self) -> 未声明`

**作用：** 回归测试：验证 expected document is returned for each keyword 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 search_validation 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, BinOp.write_text, KnowledgeBase, index_paths, self.assertEqual, knowledge_base.search；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Search, Validation, Tests, test, expected, document, is, returned, for, each, keyword, tempfile.TemporaryDirectory, Path, BinOp.write_text, KnowledgeBase, index_paths, self.assertEqual, knowledge_base.search, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, BinOp.write_text, KnowledgeBase, index_paths, self.assertEqual, knowledge_base.search；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

## personal_local_knowledge_base_v0/tests/test_structured_blocks.py

**文件作用：** 测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。

**语言/关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 12

### `_profile` (function, L21-L34)

**签名：** `def _profile() -> JsonProfile`

**作用：** 执行  profile，涉及 JsonProfile, JsonField。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：；声明返回：JsonProfile；直接/间接调用：JsonProfile, JsonField；返回表达式：JsonProfile(name='users', record_path='$.users[*]', index_mode='record', fields=(JsonField(path='id', name='id'), JsonField(path='name', name='name'), JsonField(path='profile.city…；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, profile, JsonProfile, JsonField

**调用：** JsonProfile, JsonField；**返回：** JsonProfile(name='users', record_path='$.users[*]', index_mode='record', fields=(JsonField(path='id', name='id'), JsonField(path='name', name='name'), JsonField(path='profile.city…；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `StructuredBlockTests` (class, L37-L272)

**签名：** `class StructuredBlockTests`

**作用：** 定义 StructuredBlockTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；类体包含 8 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Block, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `StructuredBlockTests.test_markdown_heading_example_and_node_types` (function, L38-L63)

**签名：** `def test_markdown_heading_example_and_node_types(self) -> 未声明`

**作用：** 回归测试：验证 markdown heading example and node types 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, self.assertTrue, tempfile.TemporaryDirectory, path.write_text, list, Set.issubset, Path, iter_document_blocks, extract_document；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Block, Tests, test, markdown, heading, example, and, node, types, self.assertEqual, self.assertTrue, tempfile.TemporaryDirectory, path.write_text, list, Set.issubset, Path, iter_document_blocks, extract_document, 上下文管理

**调用：** self.assertEqual, self.assertTrue, tempfile.TemporaryDirectory, path.write_text, list, Set.issubset, Path, iter_document_blocks, extract_document；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `StructuredBlockTests.test_canonical_and_embedding_content_are_stored_separately` (function, L65-L88)

**签名：** `def test_canonical_and_embedding_content_are_stored_separately(self) -> 未声明`

**作用：** 回归测试：验证 canonical and embedding content are stored separately 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, path.write_text, self.assertEqual, self.assertNotIn, self.assertIn, KnowledgeBase, index_paths, knowledge_base.connection.execute.fetchone, KeywordRetriever.retrieve, knowledge_base.search, knowledge_base.connection.execute, KeywordRetriever；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Block, Tests, test, canonical, and, embedding, content, are, stored, separately, tempfile.TemporaryDirectory, Path, path.write_text, self.assertEqual, self.assertNotIn, self.assertIn, KnowledgeBase, index_paths, knowledge_base.connection.execute.fetchone, KeywordRetriever.retrieve, knowledge_base.search, knowledge_base.connection.execute, KeywordRetriever, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, path.write_text, self.assertEqual, self.assertNotIn, self.assertIn, KnowledgeBase, index_paths, knowledge_base.connection.execute.fetchone, KeywordRetriever.retrieve, knowledge_base.search, knowledge_base.connection.execute, KeywordRetriever；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 模型/向量计算。

### `StructuredBlockTests.test_json_records_keep_paths_and_hard_windows` (function, L90-L121)

**签名：** `def test_json_records_keep_paths_and_hard_windows(self) -> 未声明`

**作用：** 回归测试：验证 json records keep paths and hard windows 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, self.assertIn, self.assertTrue, tempfile.TemporaryDirectory, Path, path.write_text, _profile, extract_document, list, all, json.dumps, iter_document_blocks, KnowledgeBase, index_paths, knowledge_base.chunk_window, knowledge_base.search；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Block, Tests, test, json, records, keep, paths, and, hard, windows, self.assertEqual, self.assertIn, self.assertTrue, tempfile.TemporaryDirectory, Path, path.write_text, _profile, extract_document, list, all, json.dumps, iter_document_blocks, KnowledgeBase, index_paths, knowledge_base.chunk_window, knowledge_base.search, 上下文管理

**调用：** self.assertEqual, self.assertIn, self.assertTrue, tempfile.TemporaryDirectory, Path, path.write_text, _profile, extract_document, list, all, json.dumps, iter_document_blocks, KnowledgeBase, index_paths, knowledge_base.chunk_window, knowledge_base.search；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `StructuredBlockTests.test_python_ast_symbols_source_metadata_and_fallback` (function, L123-L171)

**签名：** `def test_python_ast_symbols_source_metadata_and_fallback(self) -> 未声明`

**作用：** 回归测试：验证 python ast symbols source metadata and fallback 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, self.assertIn, self.assertIsNotNone, self.assertTrue, tempfile.TemporaryDirectory, Path, valid.write_text, invalid.write_text, extract_document, list, next, all, iter_document_blocks, KnowledgeBase, index_paths, knowledge_base.list_documents；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Block, Tests, test, python, ast, symbols, source, metadata, and, fallback, self.assertEqual, self.assertIn, self.assertIsNotNone, self.assertTrue, tempfile.TemporaryDirectory, Path, valid.write_text, invalid.write_text, extract_document, list, next, all, iter_document_blocks, KnowledgeBase, index_paths, knowledge_base.list_documents, 上下文管理

**调用：** self.assertEqual, self.assertIn, self.assertIsNotNone, self.assertTrue, tempfile.TemporaryDirectory, Path, valid.write_text, invalid.write_text, extract_document, list, next, all, iter_document_blocks, KnowledgeBase, index_paths, knowledge_base.list_documents；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写。

### `StructuredBlockTests.test_cpp_namespace_class_and_method_symbols` (function, L173-L197)

**签名：** `def test_cpp_namespace_class_and_method_symbols(self) -> 未声明`

**作用：** 回归测试：验证 cpp namespace class and method symbols 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：next, self.assertEqual, self.assertIn, tempfile.TemporaryDirectory, path.write_text, list, Path, iter_document_blocks, extract_document；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Block, Tests, test, cpp, namespace, class, and, method, symbols, next, self.assertEqual, self.assertIn, tempfile.TemporaryDirectory, path.write_text, list, Path, iter_document_blocks, extract_document, 上下文管理

**调用：** next, self.assertEqual, self.assertIn, tempfile.TemporaryDirectory, path.write_text, list, Path, iter_document_blocks, extract_document；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `StructuredBlockTests.test_large_structural_block_splits_without_losing_metadata` (function, L199-L209)

**签名：** `def test_large_structural_block_splits_without_losing_metadata(self) -> 未声明`

**作用：** 回归测试：验证 large structural block splits without losing metadata 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertGreater, self.assertTrue, tempfile.TemporaryDirectory, path.write_text, iter_document_blocks, list, len, all, Path, extract_document, iter_chunk_blocks；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Block, Tests, test, large, structural, block, splits, without, losing, metadata, self.assertGreater, self.assertTrue, tempfile.TemporaryDirectory, path.write_text, iter_document_blocks, list, len, all, Path, extract_document, iter_chunk_blocks, 上下文管理

**调用：** self.assertGreater, self.assertTrue, tempfile.TemporaryDirectory, path.write_text, iter_document_blocks, list, len, all, Path, extract_document, iter_chunk_blocks；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写, 模型/向量计算。

### `StructuredBlockTests.test_pdf_blocks_keep_page_numbers_and_boundaries` (function, L212-L241)

**签名：** `def test_pdf_blocks_keep_page_numbers_and_boundaries(self) -> 未声明`

**作用：** 回归测试：验证 pdf blocks keep page numbers and boundaries 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：unittest.skipUnless, self.assertEqual, self.assertTrue, tempfile.TemporaryDirectory, PdfWriter, list, all, Path, writer.add_blank_page, DictionaryObject, DecodedStreamObject, stream.set_data, path.open, writer.write, iter_document_blocks, NameObject, extract_document；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：循环, 上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Block, Tests, test, pdf, blocks, keep, page, numbers, and, boundaries, unittest.skipUnless, self.assertEqual, self.assertTrue, tempfile.TemporaryDirectory, PdfWriter, list, all, Path, writer.add_blank_page, DictionaryObject, DecodedStreamObject, stream.set_data, path.open, writer.write, iter_document_blocks, NameObject, extract_document, 循环, 上下文管理

**调用：** unittest.skipUnless, self.assertEqual, self.assertTrue, tempfile.TemporaryDirectory, PdfWriter, list, all, Path, writer.add_blank_page, DictionaryObject, DecodedStreamObject, stream.set_data, path.open, writer.write, iter_document_blocks, NameObject, extract_document；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `StructuredBlockTests.test_pptx_blocks_keep_slide_shape_title_text_and_table` (function, L244-L272)

**签名：** `def test_pptx_blocks_keep_slide_shape_title_text_and_table(self) -> 未声明`

**作用：** 回归测试：验证 pptx blocks keep slide shape title text and table 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：unittest.skipUnless, self.assertTrue, self.assertIn, tempfile.TemporaryDirectory, Presentation, presentation.slides.add_slide, slide.shapes.add_textbox, presentation.save, list, all, Path, Inches, slide.shapes.add_table, table.cell, iter_document_blocks, extract_document；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Block, Tests, test, pptx, blocks, keep, slide, shape, title, text, and, table, unittest.skipUnless, self.assertTrue, self.assertIn, tempfile.TemporaryDirectory, Presentation, presentation.slides.add_slide, slide.shapes.add_textbox, presentation.save, list, all, Path, Inches, slide.shapes.add_table, table.cell, iter_document_blocks, extract_document, 上下文管理

**调用：** unittest.skipUnless, self.assertTrue, self.assertIn, tempfile.TemporaryDirectory, Presentation, presentation.slides.add_slide, slide.shapes.add_textbox, presentation.save, list, all, Path, Inches, slide.shapes.add_table, table.cell, iter_document_blocks, extract_document；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `StructuredDatabaseMigrationTests` (class, L275-L333)

**签名：** `class StructuredDatabaseMigrationTests`

**作用：** 定义 StructuredDatabaseMigrationTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；类体包含 1 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Database, Migration, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `StructuredDatabaseMigrationTests.test_legacy_v0_database_is_migrated_without_replacing_original_fts` (function, L276-L333)

**签名：** `def test_legacy_v0_database_is_migrated_without_replacing_original_fts(self) -> 未声明`

**作用：** 回归测试：验证 legacy v0 database is migrated without replacing original fts 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 structured_blocks 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, self.assertIn, tempfile.TemporaryDirectory, sqlite3.connect, connection.executescript, connection.commit, connection.close, Path, KnowledgeBase, knowledge_base.connection.execute.fetchone, knowledge_base.search, knowledge_base.connection.execute；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Structured, Database, Migration, Tests, test, legacy, v0, database, is, migrated, without, replacing, original, fts, self.assertEqual, self.assertIn, tempfile.TemporaryDirectory, sqlite3.connect, connection.executescript, connection.commit, connection.close, Path, KnowledgeBase, knowledge_base.connection.execute.fetchone, knowledge_base.search, knowledge_base.connection.execute, 上下文管理

**调用：** self.assertEqual, self.assertIn, tempfile.TemporaryDirectory, sqlite3.connect, connection.executescript, connection.commit, connection.close, Path, KnowledgeBase, knowledge_base.connection.execute.fetchone, knowledge_base.search, knowledge_base.connection.execute；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 模型/向量计算。

## personal_local_knowledge_base_v0/tests/test_tokenization.py

**文件作用：** 测试文件：验证 tokenization 模块的行为、边界和错误处理；使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。

**语言/关键词：** 中文分词, jieba, 字符回退, FTS5, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 4

### `TokenizationTests` (class, L9-L35)

**签名：** `class TokenizationTests`

**作用：** 定义 TokenizationTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 tokenization 模块的行为、边界和错误处理；使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。；类体包含 3 个直接方法。

**关键词：** 中文分词, jieba, 字符回退, FTS5, unittest, 回归测试, Tokenization, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `TokenizationTests.test_tokenizes_chinese_query_for_search` (function, L10-L19)

**签名：** `def test_tokenizes_chinese_query_for_search(self) -> 未声明`

**作用：** 回归测试：验证 tokenizes chinese query for search 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 tokenization 模块的行为、边界和错误处理；使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。；输入参数：self；声明返回：未声明；直接/间接调用：tokenize_for_search, importlib.util.find_spec, self.assertEqual, self.assertIn；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 中文分词, jieba, 字符回退, FTS5, unittest, 回归测试, Tokenization, Tests, test, tokenizes, chinese, query, for, search, tokenize_for_search, importlib.util.find_spec, self.assertEqual, self.assertIn, 条件分支

**调用：** tokenize_for_search, importlib.util.find_spec, self.assertEqual, self.assertIn；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `TokenizationTests.test_builds_and_fts_query` (function, L21-L31)

**签名：** `def test_builds_and_fts_query(self) -> 未声明`

**作用：** 回归测试：验证 builds and fts query 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 tokenization 模块的行为、边界和错误处理；使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。；输入参数：self；声明返回：未声明；直接/间接调用：to_token_fts_query, importlib.util.find_spec, self.assertEqual；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：条件分支。

**关键词：** 中文分词, jieba, 字符回退, FTS5, unittest, 回归测试, Tokenization, Tests, test, builds, and, fts, query, to_token_fts_query, importlib.util.find_spec, self.assertEqual, 条件分支

**调用：** to_token_fts_query, importlib.util.find_spec, self.assertEqual；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `TokenizationTests.test_blank_query_returns_empty_token_query` (function, L33-L35)

**签名：** `def test_blank_query_returns_empty_token_query(self) -> 未声明`

**作用：** 回归测试：验证 blank query returns empty token query 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 tokenization 模块的行为、边界和错误处理；使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, to_token_fts_query；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 中文分词, jieba, 字符回退, FTS5, unittest, 回归测试, Tokenization, Tests, test, blank, query, returns, empty, token, self.assertEqual, to_token_fts_query

**调用：** self.assertEqual, to_token_fts_query；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

## personal_local_knowledge_base_v0/tests/test_web.py

**文件作用：** 测试文件：验证 web 相关功能的行为、边界和错误处理。

**语言/关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Python, py

**函数/类/脚本记录数：** 38

### `_indexed_temp_db` (function, L25-L36)

**签名：** `def _indexed_temp_db(text: str='SQLite FTS5 提供本地全文搜索。', embedding_backend=None) -> 未声明`

**作用：** 执行  indexed temp db，涉及 tempfile.TemporaryDirectory, Path, source.write_text, KnowledgeBase, index_paths。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：text: str='SQLite FTS5 提供本地全文搜索。', embedding_backend=None；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, source.write_text, KnowledgeBase, index_paths；返回表达式：(temp_dir, root, db_path)；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, indexed, temp, db, tempfile.TemporaryDirectory, Path, source.write_text, KnowledgeBase, index_paths, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, source.write_text, KnowledgeBase, index_paths；**返回：** (temp_dir, root, db_path)；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 模型/向量计算。

### `FakeClient` (class, L39-L44)

**签名：** `class FakeClient`

**作用：** 定义 FakeClient 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；类体包含 1 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Client

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `FakeClient.complete` (function, L40-L44)

**签名：** `def complete(self, messages, *, temperature=0.0) -> 未声明`

**作用：** 执行 complete，涉及 LLMResponse, TokenUsage。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self, messages, *, temperature=0.0；声明返回：未声明；直接/间接调用：LLMResponse, TokenUsage；返回表达式：LLMResponse(content='FTS5 是 SQLite 的全文搜索扩展。[1]', usage=TokenUsage(prompt_tokens=10, completion_tokens=8, total_tokens=18))；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Client, complete, LLMResponse, TokenUsage

**调用：** LLMResponse, TokenUsage；**返回：** LLMResponse(content='FTS5 是 SQLite 的全文搜索扩展。[1]', usage=TokenUsage(prompt_tokens=10, completion_tokens=8, total_tokens=18))；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `FakeEmbeddingBackend` (class, L47-L73)

**签名：** `class FakeEmbeddingBackend`

**作用：** 定义 FakeEmbeddingBackend 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；类体包含 5 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Embedding, Backend

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `FakeEmbeddingBackend.__init__` (function, L55-L56)

**签名：** `def __init__(self) -> 未声明`

**作用：** 初始化对象字段、运行配置和可复用的外部资源句柄。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：无明显函数调用；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Embedding, Backend, init

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `FakeEmbeddingBackend.model_revision` (function, L59-L60)

**签名：** `def model_revision(self) -> 未声明`

**作用：** 执行 model revision。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：无明显函数调用；返回表达式：'web-test'；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Embedding, Backend, model, revision

**调用：** 无明显调用；**返回：** 'web-test'；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `FakeEmbeddingBackend.embed_documents` (function, L62-L66)

**签名：** `def embed_documents(self, texts) -> 未声明`

**作用：** 执行 embed documents，涉及 np.asarray。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self, texts；声明返回：未声明；直接/间接调用：np.asarray；返回表达式：np.asarray([[1.0, 0.0] for _ in texts], dtype=np.float32)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Embedding, Backend, embed, documents, np.asarray

**调用：** np.asarray；**返回：** np.asarray([[1.0, 0.0] for _ in texts], dtype=np.float32)；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `FakeEmbeddingBackend.embed_query` (function, L68-L70)

**签名：** `def embed_query(self, query, *, code=False) -> 未声明`

**作用：** 执行 embed query，涉及 self.query_calls.append, np.asarray。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self, query, *, code=False；声明返回：未声明；直接/间接调用：self.query_calls.append, np.asarray；返回表达式：np.asarray([1.0, 0.0], dtype=np.float32)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Embedding, Backend, embed, query, self.query_calls.append, np.asarray

**调用：** self.query_calls.append, np.asarray；**返回：** np.asarray([1.0, 0.0], dtype=np.float32)；**异常：** 未发现显式 raise；**副作用：** 模型/向量计算。

### `FakeEmbeddingBackend.token_count` (function, L72-L73)

**签名：** `def token_count(self, text) -> 未声明`

**作用：** 执行 token count，涉及 len。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self, text；声明返回：未声明；直接/间接调用：len；返回表达式：len(text)；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Fake, Embedding, Backend, token, count, len

**调用：** len；**返回：** len(text)；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeWebAppTests` (class, L76-L220)

**签名：** `class KnowledgeWebAppTests`

**作用：** 定义 KnowledgeWebAppTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；类体包含 10 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `KnowledgeWebAppTests.test_stats_and_documents_report_indexed_state` (function, L77-L94)

**签名：** `def test_stats_and_documents_report_indexed_state(self) -> 未声明`

**作用：** 回归测试：验证 stats and documents report indexed state 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：_indexed_temp_db, KnowledgeWebApp, app.stats, self.assertEqual, self.assertGreaterEqual, app.documents, temp_dir.cleanup, len；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, stats, and, documents, report, indexed, state, _indexed_temp_db, KnowledgeWebApp, app.stats, self.assertEqual, self.assertGreaterEqual, app.documents, temp_dir.cleanup, len, 异常处理

**调用：** _indexed_temp_db, KnowledgeWebApp, app.stats, self.assertEqual, self.assertGreaterEqual, app.documents, temp_dir.cleanup, len；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeWebAppTests.test_search_returns_highlighted_content` (function, L96-L105)

**签名：** `def test_search_returns_highlighted_content(self) -> 未声明`

**作用：** 回归测试：验证 search returns highlighted content 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：_indexed_temp_db, KnowledgeWebApp, app.search, self.assertTrue, self.assertEqual, self.assertIn, temp_dir.cleanup；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, search, returns, highlighted, content, _indexed_temp_db, KnowledgeWebApp, app.search, self.assertTrue, self.assertEqual, self.assertIn, temp_dir.cleanup, 异常处理

**调用：** _indexed_temp_db, KnowledgeWebApp, app.search, self.assertTrue, self.assertEqual, self.assertIn, temp_dir.cleanup；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeWebAppTests.test_ask_uses_fake_client_and_returns_citation_sources` (function, L107-L121)

**签名：** `def test_ask_uses_fake_client_and_returns_citation_sources(self) -> 未声明`

**作用：** 回归测试：验证 ask uses fake client and returns citation sources 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：_indexed_temp_db, KnowledgeWebApp, app.ask, self.assertNotIn, self.assertIn, self.assertEqual, temp_dir.cleanup, RagConfig；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, ask, uses, fake, client, and, returns, citation, sources, _indexed_temp_db, KnowledgeWebApp, app.ask, self.assertNotIn, self.assertIn, self.assertEqual, temp_dir.cleanup, RagConfig, 异常处理

**调用：** _indexed_temp_db, KnowledgeWebApp, app.ask, self.assertNotIn, self.assertIn, self.assertEqual, temp_dir.cleanup, RagConfig；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeWebAppTests.test_semantic_search_uses_query_embedding_and_sqlite_vec` (function, L123-L142)

**签名：** `def test_semantic_search_uses_query_embedding_and_sqlite_vec(self) -> 未声明`

**作用：** 回归测试：验证 semantic search uses query embedding and sqlite vec 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：FakeEmbeddingBackend, _indexed_temp_db, KnowledgeWebApp, app.stats, app.search, self.assertEqual, temp_dir.cleanup, self.skipTest；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, semantic, search, uses, query, embedding, and, sqlite, vec, FakeEmbeddingBackend, _indexed_temp_db, KnowledgeWebApp, app.stats, app.search, self.assertEqual, temp_dir.cleanup, self.skipTest, 异常处理

**调用：** FakeEmbeddingBackend, _indexed_temp_db, KnowledgeWebApp, app.stats, app.search, self.assertEqual, temp_dir.cleanup, self.skipTest；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeWebAppTests.test_semantic_ask_uses_query_embedding` (function, L144-L163)

**签名：** `def test_semantic_ask_uses_query_embedding(self) -> 未声明`

**作用：** 回归测试：验证 semantic ask uses query embedding 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：FakeEmbeddingBackend, _indexed_temp_db, KnowledgeWebApp, app.ask, self.assertNotIn, self.assertEqual, temp_dir.cleanup, self.skipTest, RagConfig；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, semantic, ask, uses, query, embedding, FakeEmbeddingBackend, _indexed_temp_db, KnowledgeWebApp, app.ask, self.assertNotIn, self.assertEqual, temp_dir.cleanup, self.skipTest, RagConfig, 异常处理

**调用：** FakeEmbeddingBackend, _indexed_temp_db, KnowledgeWebApp, app.ask, self.assertNotIn, self.assertEqual, temp_dir.cleanup, self.skipTest, RagConfig；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 模型/向量计算。

### `KnowledgeWebAppTests.test_ask_returns_structured_error_when_client_fails` (function, L165-L183)

**签名：** `def test_ask_returns_structured_error_when_client_fails(self) -> 未声明`

**作用：** 回归测试：验证 ask returns structured error when client fails 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：_indexed_temp_db, LLMClientError, KnowledgeWebApp, app.ask, self.assertIn, temp_dir.cleanup, RagConfig；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：LLMClientError('未配置 LLM_API_KEY。')；控制流：异常处理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, ask, returns, structured, error, when, client, fails, _indexed_temp_db, LLMClientError, KnowledgeWebApp, app.ask, self.assertIn, temp_dir.cleanup, RagConfig, 异常处理

**调用：** _indexed_temp_db, LLMClientError, KnowledgeWebApp, app.ask, self.assertIn, temp_dir.cleanup, RagConfig；**返回：** 未记录；**异常：** LLMClientError('未配置 LLM_API_KEY。')；**副作用：** SQLite/数据库写入或查询。

### `KnowledgeWebAppTests.test_ask_returns_structured_error_when_client_fails.failing_client` (function, L168-L171)

**签名：** `def failing_client() -> 未声明`

**作用：** 执行 failing client，涉及 LLMClientError。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：；声明返回：未声明；直接/间接调用：LLMClientError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：LLMClientError('未配置 LLM_API_KEY。')；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, ask, returns, structured, error, when, client, fails, failing, LLMClientError

**调用：** LLMClientError；**返回：** 未记录；**异常：** LLMClientError('未配置 LLM_API_KEY。')；**副作用：** 未发现明显外部副作用。

### `KnowledgeWebAppTests.test_save_upload_persists_and_deduplicates_names` (function, L185-L195)

**签名：** `def test_save_upload_persists_and_deduplicates_names(self) -> 未声明`

**作用：** 回归测试：验证 save upload persists and deduplicates names 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, KnowledgeWebApp, app.save_upload, self.assertEqual, self.assertNotEqual, self.assertTrue, Constant.encode, Path.is_file；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, save, upload, persists, and, deduplicates, names, tempfile.TemporaryDirectory, Path, KnowledgeWebApp, app.save_upload, self.assertEqual, self.assertNotEqual, self.assertTrue, Constant.encode, Path.is_file, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, KnowledgeWebApp, app.save_upload, self.assertEqual, self.assertNotEqual, self.assertTrue, Constant.encode, Path.is_file；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `KnowledgeWebAppTests.test_save_upload_rejects_unsupported_suffix` (function, L197-L202)

**签名：** `def test_save_upload_rejects_unsupported_suffix(self) -> 未声明`

**作用：** 回归测试：验证 save upload rejects unsupported suffix 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, KnowledgeWebApp, self.assertRaisesRegex, app.save_upload；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, save, upload, rejects, unsupported, suffix, tempfile.TemporaryDirectory, Path, KnowledgeWebApp, self.assertRaisesRegex, app.save_upload, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, KnowledgeWebApp, self.assertRaisesRegex, app.save_upload；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `KnowledgeWebAppTests.test_save_upload_sanitizes_traversal_name` (function, L204-L209)

**签名：** `def test_save_upload_sanitizes_traversal_name(self) -> 未声明`

**作用：** 回归测试：验证 save upload sanitizes traversal name 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：tempfile.TemporaryDirectory, Path, KnowledgeWebApp, app.save_upload, self.assertEqual, Constant.encode；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, save, upload, sanitizes, traversal, name, tempfile.TemporaryDirectory, Path, KnowledgeWebApp, app.save_upload, self.assertEqual, Constant.encode, 上下文管理

**调用：** tempfile.TemporaryDirectory, Path, KnowledgeWebApp, app.save_upload, self.assertEqual, Constant.encode；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `KnowledgeWebAppTests.test_remove_document` (function, L211-L220)

**签名：** `def test_remove_document(self) -> 未声明`

**作用：** 回归测试：验证 remove document 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：_indexed_temp_db, KnowledgeWebApp, app.remove, self.assertTrue, self.assertEqual, temp_dir.cleanup, app.documents；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Knowledge, Web, App, Tests, test, remove, document, _indexed_temp_db, KnowledgeWebApp, app.remove, self.assertTrue, self.assertEqual, temp_dir.cleanup, app.documents, 异常处理

**调用：** _indexed_temp_db, KnowledgeWebApp, app.remove, self.assertTrue, self.assertEqual, temp_dir.cleanup, app.documents；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `MultipartParsingTests` (class, L223-L253)

**签名：** `class MultipartParsingTests`

**作用：** 定义 MultipartParsingTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；类体包含 3 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Multipart, Parsing, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `MultipartParsingTests.test_parse_multipart_extracts_filename_and_data` (function, L224-L237)

**签名：** `def test_parse_multipart_extracts_filename_and_data(self) -> 未声明`

**作用：** 回归测试：验证 parse multipart extracts filename and data 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：JoinedStr.encode, _parse_multipart, self.assertEqual；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Multipart, Parsing, Tests, test, parse, multipart, extracts, filename, and, data, JoinedStr.encode, _parse_multipart, self.assertEqual

**调用：** JoinedStr.encode, _parse_multipart, self.assertEqual；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `MultipartParsingTests.test_parse_multipart_requires_file` (function, L239-L248)

**签名：** `def test_parse_multipart_requires_file(self) -> 未声明`

**作用：** 回归测试：验证 parse multipart requires file 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：JoinedStr.encode, self.assertRaisesRegex, _parse_multipart；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Multipart, Parsing, Tests, test, parse, multipart, requires, file, JoinedStr.encode, self.assertRaisesRegex, _parse_multipart, 上下文管理

**调用：** JoinedStr.encode, self.assertRaisesRegex, _parse_multipart；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `MultipartParsingTests.test_extract_quoted_handles_quoted_and_bare_values` (function, L250-L253)

**签名：** `def test_extract_quoted_handles_quoted_and_bare_values(self) -> 未声明`

**作用：** 回归测试：验证 extract quoted handles quoted and bare values 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, _extract_quoted；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Multipart, Parsing, Tests, test, extract, quoted, handles, and, bare, values, self.assertEqual, _extract_quoted

**调用：** self.assertEqual, _extract_quoted；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `HttpApiTests` (class, L256-L399)

**签名：** `class HttpApiTests`

**作用：** 定义 HttpApiTests 相关的状态、数据契约或协作接口。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；类体包含 8 个直接方法。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests

**调用：** 无明显调用；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `HttpApiTests.setUp` (function, L257-L267)

**签名：** `def setUp(self) -> 未声明`

**作用：** 执行 setUp，涉及 _indexed_temp_db, KnowledgeWebApp, create_server, threading.Thread, self.thread.start。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：_indexed_temp_db, KnowledgeWebApp, create_server, threading.Thread, self.thread.start, RagConfig；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, set, Up, _indexed_temp_db, KnowledgeWebApp, create_server, threading.Thread, self.thread.start, RagConfig

**调用：** _indexed_temp_db, KnowledgeWebApp, create_server, threading.Thread, self.thread.start, RagConfig；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `HttpApiTests.setUp.lambda@264` (function, L264-L264)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：RagConfig()；调用：RagConfig；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, RagConfig

**调用：** RagConfig；**返回：** RagConfig()；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `HttpApiTests.tearDown` (function, L269-L273)

**签名：** `def tearDown(self) -> 未声明`

**作用：** 执行 tearDown，涉及 self.server.shutdown, self.server.server_close, self.thread.join, self.temp_dir.cleanup。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.server.shutdown, self.server.server_close, self.thread.join, self.temp_dir.cleanup；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, tear, Down, self.server.shutdown, self.server.server_close, self.thread.join, self.temp_dir.cleanup

**调用：** self.server.shutdown, self.server.server_close, self.thread.join, self.temp_dir.cleanup；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `HttpApiTests.request` (function, L275-L287)

**签名：** `def request(self, method, path, body=None, headers=None) -> 未声明`

**作用：** 执行 request，涉及 http.client.HTTPConnection, connection.request, connection.getresponse, response.read, connection.close。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self, method, path, body=None, headers=None；声明返回：未声明；直接/间接调用：http.client.HTTPConnection, connection.request, connection.getresponse, response.read, connection.close, json.loads, raw.decode；返回表达式：(response.status, payload)；显式异常：未发现显式 raise；控制流：条件分支, 异常处理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, request, http.client.HTTPConnection, connection.request, connection.getresponse, response.read, connection.close, json.loads, raw.decode, 条件分支, 异常处理

**调用：** http.client.HTTPConnection, connection.request, connection.getresponse, response.read, connection.close, json.loads, raw.decode；**返回：** (response.status, payload)；**异常：** 未发现显式 raise；**副作用：** 网络 HTTP 请求。

### `HttpApiTests.test_static_stats_search_and_ask_routes` (function, L289-L309)

**签名：** `def test_static_stats_search_and_ask_routes(self) -> 未声明`

**作用：** 回归测试：验证 static stats search and ask routes 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.request, self.assertEqual, self.assertIn, json.dumps.encode, json.dumps；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, test, static, stats, search, and, ask, routes, self.request, self.assertEqual, self.assertIn, json.dumps.encode, json.dumps

**调用：** self.request, self.assertEqual, self.assertIn, json.dumps.encode, json.dumps；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 网络 HTTP 请求。

### `HttpApiTests.test_http_semantic_mode_uses_embedding_backend` (function, L311-L341)

**签名：** `def test_http_semantic_mode_uses_embedding_backend(self) -> 未声明`

**作用：** 回归测试：验证 http semantic mode uses embedding backend 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：FakeEmbeddingBackend, _indexed_temp_db, KnowledgeWebApp, create_server, threading.Thread, thread.start, http.client.HTTPConnection, self.assertEqual, server.shutdown, server.server_close, thread.join, temp_dir.cleanup, RagConfig, connection.request, connection.getresponse, json.loads, connection.close, response.read.decode, response.read；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：异常处理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, test, http, semantic, mode, uses, embedding, backend, FakeEmbeddingBackend, _indexed_temp_db, KnowledgeWebApp, create_server, threading.Thread, thread.start, http.client.HTTPConnection, self.assertEqual, server.shutdown, server.server_close, thread.join, temp_dir.cleanup, RagConfig, connection.request, connection.getresponse, json.loads, connection.close, response.read.decode, response.read, 异常处理

**调用：** FakeEmbeddingBackend, _indexed_temp_db, KnowledgeWebApp, create_server, threading.Thread, thread.start, http.client.HTTPConnection, self.assertEqual, server.shutdown, server.server_close, thread.join, temp_dir.cleanup, RagConfig, connection.request, connection.getresponse, json.loads, connection.close, response.read.decode, response.read；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 网络 HTTP 请求, 模型/向量计算。

### `HttpApiTests.test_http_semantic_mode_uses_embedding_backend.lambda@319` (function, L319-L319)

**签名：** `lambda `

**作用：** 匿名 lambda：接收参数并计算一个短表达式结果。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；这是匿名 lambda，输入参数：；返回表达式：RagConfig()；调用：RagConfig；通常作为排序键、映射函数或事件回调传递给外部 API。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, lambda, RagConfig

**调用：** RagConfig；**返回：** RagConfig()；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `HttpApiTests.test_multipart_upload_and_bad_json_are_rejected_cleanly` (function, L343-L370)

**签名：** `def test_multipart_upload_and_bad_json_are_rejected_cleanly(self) -> 未声明`

**作用：** 回归测试：验证 multipart upload and bad json are rejected cleanly 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：JoinedStr.encode, self.request, self.assertEqual, self.assertTrue, self.assertIn, Path.is_relative_to, Path；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, test, multipart, upload, and, bad, json, are, rejected, cleanly, JoinedStr.encode, self.request, self.assertEqual, self.assertTrue, self.assertIn, Path.is_relative_to, Path

**调用：** JoinedStr.encode, self.request, self.assertEqual, self.assertTrue, self.assertIn, Path.is_relative_to, Path；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 文件系统读写, 网络 HTTP 请求。

### `HttpApiTests.test_concurrent_search_requests_are_independent` (function, L372-L379)

**签名：** `def test_concurrent_search_requests_are_independent(self) -> 未声明`

**作用：** 回归测试：验证 concurrent search requests are independent 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, self.request, ThreadPoolExecutor, list, len, executor.map, range；返回表达式：(status, len(payload['results']))；显式异常：未发现显式 raise；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, test, concurrent, search, requests, are, independent, self.assertEqual, self.request, ThreadPoolExecutor, list, len, executor.map, range, 上下文管理

**调用：** self.assertEqual, self.request, ThreadPoolExecutor, list, len, executor.map, range；**返回：** (status, len(payload['results']))；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 网络 HTTP 请求。

### `HttpApiTests.test_concurrent_search_requests_are_independent.search_once` (function, L373-L375)

**签名：** `def search_once(_) -> 未声明`

**作用：** 执行检索 once；内部调用 self.request, len。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：_；声明返回：未声明；直接/间接调用：self.request, len；返回表达式：(status, len(payload['results']))；显式异常：未发现显式 raise；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, test, concurrent, search, requests, are, independent, once, self.request, len

**调用：** self.request, len；**返回：** (status, len(payload['results']))；**异常：** 未发现显式 raise；**副作用：** SQLite/数据库写入或查询, 网络 HTTP 请求。

### `HttpApiTests.test_error_response_redacts_api_key` (function, L381-L399)

**签名：** `def test_error_response_redacts_api_key(self) -> 未声明`

**作用：** 回归测试：验证 error response redacts api key 的预期行为、边界条件或错误处理。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：self；声明返回：未声明；直接/间接调用：self.assertEqual, self.assertNotIn, self.assertIn, LLMClientError, patch.dict, self.request, json.dumps.encode, json.dumps；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：LLMClientError(f'remote rejected {secret}')；控制流：上下文管理。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, test, error, response, redacts, api, key, self.assertEqual, self.assertNotIn, self.assertIn, LLMClientError, patch.dict, self.request, json.dumps.encode, json.dumps, 上下文管理

**调用：** self.assertEqual, self.assertNotIn, self.assertIn, LLMClientError, patch.dict, self.request, json.dumps.encode, json.dumps；**返回：** 未记录；**异常：** LLMClientError(f'remote rejected {secret}')；**副作用：** SQLite/数据库写入或查询, 网络 HTTP 请求, 环境变量读取。

### `HttpApiTests.test_error_response_redacts_api_key.failing_client` (function, L384-L387)

**签名：** `def failing_client() -> 未声明`

**作用：** 执行 failing client，涉及 LLMClientError。

**详细语义：** 所属模块职责：测试文件：验证 web 相关功能的行为、边界和错误处理。；输入参数：；声明返回：未声明；直接/间接调用：LLMClientError；返回表达式：无显式 return（可能只产生副作用或通过 yield 输出）；显式异常：LLMClientError(f'remote rejected {secret}')；控制流：顺序执行。

**关键词：** 代码, 回归, 辅助脚本, unittest, 回归测试, Http, Api, Tests, test, error, response, redacts, api, key, failing, client, LLMClientError

**调用：** LLMClientError；**返回：** 未记录；**异常：** LLMClientError(f'remote rejected {secret}')；**副作用：** 未发现明显外部副作用。

## redox_ppt.js

**文件作用：** 使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。

**语言/关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, js

**函数/类/脚本记录数：** 28

### `addText` (function, L42-L64)

**签名：** `function addText(slide, text, x, y, w, h, opts = {})`

**作用：** 执行 addText，涉及 addText。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function addText(slide, text, x, y, w, h, opts = {})；调用：addText；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, add, Text, addText, 条件分支

**调用：** addText；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `rect` (function, L65-L73)

**签名：** `function rect(slide, x, y, w, h, fill, radius = true, line = null, transparency = 0)`

**作用：** 执行 rect，涉及 rect, addShape。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function rect(slide, x, y, w, h, fill, radius = true, line = null, transparency = 0)；调用：rect, addShape；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, rect, addShape, 条件分支

**调用：** rect, addShape；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `line` (function, L74-L86)

**签名：** `function line(slide, x1, y1, x2, y2, color = C.line, width = 1.2, arrow = false, dash = 'solid')`

**作用：** 执行 line，涉及 line, addShape。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function line(slide, x1, y1, x2, y2, color = C.line, width = 1.2, arrow = false, dash = 'solid')；调用：line, addShape；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, line, addShape, 条件分支

**调用：** line, addShape；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `circle` (function, L87-L94)

**签名：** `function circle(slide, x, y, d, fill, lineColor = fill, transparency = 0)`

**作用：** 执行 circle，涉及 circle, addShape。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function circle(slide, x, y, d, fill, lineColor = fill, transparency = 0)；调用：circle, addShape；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, circle, addShape, 条件分支

**调用：** circle, addShape；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `pill` (function, L95-L99)

**签名：** `function pill(slide, text, x, y, w, color, textColor = C.bg)`

**作用：** 执行 pill，涉及 pill, rect, addText。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function pill(slide, text, x, y, w, color, textColor = C.bg)；调用：pill, rect, addText；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, pill, rect, addText

**调用：** pill, rect, addText；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `title` (function, L100-L106)

**签名：** `function title(slide, kicker, heading, num)`

**作用：** 执行 title，涉及 title, addText, toUpperCase, String, padStart。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function title(slide, kicker, heading, num)；调用：title, addText, toUpperCase, String, padStart, line；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, title, addText, toUpperCase, String, padStart, line

**调用：** title, addText, toUpperCase, String, padStart, line；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `footer` (function, L107-L112)

**签名：** `function footer(slide, label, num)`

**作用：** 执行 footer，涉及 footer, line, addText, String, padStart。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function footer(slide, label, num)；调用：footer, line, addText, String, padStart；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, footer, line, addText, String, padStart

**调用：** footer, line, addText, String, padStart；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `note` (function, L113-L116)

**签名：** `function note(slide, text)`

**作用：** 执行 note，涉及 note, addNotes。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function note(slide, text)；调用：note, addNotes；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, note, addNotes

**调用：** note, addNotes；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `addBg` (function, L117-L127)

**签名：** `function addBg(slide, variant = 0)`

**作用：** 执行 addBg，涉及 addBg, circle, line。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function addBg(slide, variant = 0)；调用：addBg, circle, line；控制流：条件分支, 循环/集合遍历；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, add, Bg, addBg, circle, line, 条件分支, 循环/集合遍历

**调用：** addBg, circle, line；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `card` (function, L128-L134)

**签名：** `function card(slide, x, y, w, h, opts = {})`

**作用：** 执行 card，涉及 card, rect, addShape。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function card(slide, x, y, w, h, opts = {})；调用：card, rect, addShape；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, card, rect, addShape, 条件分支

**调用：** card, rect, addShape；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `formula` (function, L135-L139)

**签名：** `function formula(slide, text, x, y, w, h, color = C.ink, fs = 18, fill = C.panel2)`

**作用：** 执行 formula，涉及 formula, rect, addText。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function formula(slide, text, x, y, w, h, color = C.ink, fs = 18, fill = C.panel2)；调用：formula, rect, addText；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, formula, rect, addText

**调用：** formula, rect, addText；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `dotLabel` (function, L140-L145)

**签名：** `function dotLabel(slide, x, y, color, label, sub)`

**作用：** 执行 dotLabel，涉及 dotLabel, circle, addText。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：function dotLabel(slide, x, y, color, label, sub)；调用：dotLabel, circle, addText；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, dot, Label, dotLabel, circle, addText, 条件分支

**调用：** dotLabel, circle, addText；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@183` (function, L183-L191)

**签名：** `anonymous_arrow@183 = (s, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@183，涉及 card, circle, addText, line。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@183 = (s, i) =>；调用：card, circle, addText, line；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 183, card, circle, addText, line, 条件分支

**调用：** card, circle, addText, line；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@242` (function, L242-L249)

**签名：** `anonymous_arrow@242 = (r, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@242，涉及 floor, card, addText。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@242 = (r, i) =>；调用：floor, card, addText；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 242, floor, card, addText

**调用：** floor, card, addText；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@257` (function, L257-L262)

**签名：** `anonymous_arrow@257 = (r, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@257，涉及 card, addText。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@257 = (r, i) =>；调用：card, addText；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 257, card, addText

**调用：** card, addText；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@301` (function, L301-L308)

**签名：** `anonymous_arrow@301 = (s, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@301，涉及 card, addText, line。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@301 = (s, i) =>；调用：card, addText, line；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 301, card, addText, line, 条件分支

**调用：** card, addText, line；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@342` (function, L342-L351)

**签名：** `anonymous_arrow@342 = (x, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@342，涉及 card, circle, addText, String, line。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@342 = (x, i) =>；调用：card, circle, addText, String, line；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 342, card, circle, addText, String, line, 条件分支

**调用：** card, circle, addText, String, line；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@369` (function, L369-L379)

**签名：** `anonymous_arrow@369 = (c) =>`

**作用：** 匿名回调：执行 anonymous arrow@369，涉及 card, addText, circle, formula。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@369 = (c) =>；调用：card, addText, circle, formula；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 369, card, addText, circle, formula

**调用：** card, addText, circle, formula；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@411` (function, L411-L418)

**签名：** `anonymous_arrow@411 = (f, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@411，涉及 circle, addText, String, line。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@411 = (f, i) =>；调用：circle, addText, String, line；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 411, circle, addText, String, line, 条件分支

**调用：** circle, addText, String, line；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@465` (function, L465-L473)

**签名：** `anonymous_arrow@465 = (it, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@465，涉及 floor, card, addText, line。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@465 = (it, i) =>；调用：floor, card, addText, line；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 465, floor, card, addText, line, 条件分支

**调用：** floor, card, addText, line；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@490` (function, L490-L497)

**签名：** `anonymous_arrow@490 = (q, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@490，涉及 card, circle, addText。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@490 = (q, i) =>；调用：card, circle, addText；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 490, card, circle, addText

**调用：** card, circle, addText；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@513` (function, L513-L522)

**签名：** `anonymous_arrow@513 = (a, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@513，涉及 card, circle, addText, line。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@513 = (a, i) =>；调用：card, circle, addText, line；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 513, card, circle, addText, line

**调用：** card, circle, addText, line；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@539` (function, L539-L544)

**签名：** `anonymous_arrow@539 = (n, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@539，涉及 circle, addText, line。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@539 = (n, i) =>；调用：circle, addText, line；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 539, circle, addText, line, 条件分支

**调用：** circle, addText, line；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@563` (function, L563-L571)

**签名：** `anonymous_arrow@563 = (t, i) =>`

**作用：** 匿名回调：执行 anonymous arrow@563，涉及 floor, card, circle, addText。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@563 = (t, i) =>；调用：floor, card, circle, addText；控制流：条件分支；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 563, floor, card, circle, addText, 条件分支

**调用：** floor, card, circle, addText；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `writeAndAddTransitions` (function, L577-L603)

**签名：** `async function writeAndAddTransitions()`

**作用：** 执行 writeAndAddTransitions，涉及 writeAndAddTransitions, join, writeFile, require, loadAsync。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：async function writeAndAddTransitions()；调用：writeAndAddTransitions, join, writeFile, require, loadAsync, readFileSync, keys, filter, test, sort, Number, match, file, async, includes, replace, generateAsync, writeFileSync, log；控制流：条件分支, 循环/集合遍历, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, write, And, Add, Transitions, writeAndAddTransitions, join, writeFile, require, loadAsync, readFileSync, keys, filter, test, sort, Number, match, file, async, includes, replace, generateAsync, writeFileSync, log, 条件分支, 循环/集合遍历, 异步等待

**调用：** writeAndAddTransitions, join, writeFile, require, loadAsync, readFileSync, keys, filter, test, sort, Number, match, file, async, includes, replace, generateAsync, writeFileSync, log；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 文件系统读写。

### `anonymous_arrow@586` (function, L586-L599)

**签名：** `anonymous_arrow@586 = (n) =>`

**作用：** 匿名回调：执行 anonymous arrow@586，涉及 test, sort, Number, match, file。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@586 = (n) =>；调用：test, sort, Number, match, file, async, includes, replace；控制流：条件分支, 循环/集合遍历, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 586, test, sort, Number, match, file, async, includes, replace, 条件分支, 循环/集合遍历, 异步等待

**调用：** test, sort, Number, match, file, async, includes, replace；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@587` (function, L587-L599)

**签名：** `anonymous_arrow@587 = (a, b) =>`

**作用：** 匿名回调：执行 anonymous arrow@587，涉及 Number, match, file, async, includes。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@587 = (a, b) =>；调用：Number, match, file, async, includes, replace；控制流：条件分支, 循环/集合遍历, 异步等待；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 587, Number, match, file, async, includes, replace, 条件分支, 循环/集合遍历, 异步等待

**调用：** Number, match, file, async, includes, replace；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

### `anonymous_arrow@605` (function, L605-L608)

**签名：** `anonymous_arrow@605 = (err) =>`

**作用：** 匿名回调：执行 anonymous arrow@605，涉及 error, exit。

**详细语义：** 所属模块职责：使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。；JavaScript 输入签名：anonymous_arrow@605 = (err) =>；调用：error, exit；控制流：顺序执行；返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。

**关键词：** JavaScript, PptxGenJS, PPTX, 教学演示, 幻灯片, anonymous, arrow, 605, error, exit

**调用：** error, exit；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 未发现明显外部副作用。

## scripts/download_segmented.ps1

**文件作用：** PowerShell 分段下载器：按 HTTP Range 下载大文件，校验每段大小后追加合并并支持断点续传。

**语言/关键词：** PowerShell, Range 下载, 断点续传, 文件校验, ps1

**函数/类/脚本记录数：** 1

### `<module>.__main__` (script, L1-L101)

**签名：** `module-level script`

**作用：** PowerShell 分段下载器：按 HTTP Range 下载大文件，校验每段大小后追加合并并支持断点续传。

**详细语义：** 脚本语言：PowerShell；无可声明的命名函数，主体按顺序执行。核心命令/操作：CopyTo, Get-Item, Move, New-Item, Start-Process, curl.exe。

**关键词：** PowerShell, Range 下载, 断点续传, 文件校验

**调用：** CopyTo, Get-Item, Move, New-Item, Start-Process, curl.exe；**返回：** 未记录；**异常：** 未发现显式 raise；**副作用：** 子进程或外部命令。


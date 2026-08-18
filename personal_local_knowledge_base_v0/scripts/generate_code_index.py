"""Generate searchable file/class/function annotations for the knowledge base.

The output is deliberately data-oriented: one JSON object per indexed entity in
``docs/code-function-index.jsonl`` and a readable mirror in Markdown.  Python
entities come from ``ast``; JavaScript entities use a small balanced-brace
scanner because the project has no JavaScript parser dependency.  The scanner
records anonymous arrow callbacks as well, so event handlers are not silently
omitted from the inventory.
"""

from __future__ import annotations

import ast
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR / "docs"
CODE_SUFFIXES = {".py", ".js", ".ps1", ".html", ".css"}
SKIP_PARTS = {".venv", "__pycache__", "node_modules", "dist", "build"}


MODULE_GUIDES: dict[str, tuple[str, tuple[str, ...]]] = {
    "server.py": ("项目根目录的兼容启动包装器；把上一级入口转发到本地 Embedding 服务实现。", ("启动入口", "模块加载", "路径兼容")),
    "block_parsing.py": ("把 TXT、Markdown、JSON、PDF、PPTX、Python、C/C++ 的抽取文本转换为统一 DocumentBlock，并保留标题、符号、行号、页码、记录和幻灯片定位信息。", ("结构化解析", "DocumentBlock", "符号路径", "硬边界", "canonical_content", "embedding_content")),
    "chunking.py": ("在结构块内部执行流式长度分段、核心块语义合并、Token 上限控制和最终重叠添加。", ("语义分块", "核心块", "重叠", "Token 限制", "硬边界")),
    "cleaning.py": ("对大文本流做 Unicode、换行、空白和 Markdown 行级规范化，避免一次性加载全文。", ("文本清洗", "流式", "Unicode", "换行", "空白")),
    "cli.py": ("定义 knowledge_search 的命令行参数、子命令、索引/搜索/RAG/数据库管理流程和终端输出。", ("CLI", "argparse", "索引", "搜索", "问答", "退出码")),
    "database.py": ("封装 SQLite 文档表、结构化 chunks、三套 FTS/Token 索引、Embedding 缓存、向量候选和健康检查。", ("SQLite", "FTS5", "jieba", "Embedding 缓存", "事务", "增量索引")),
    "dataset_reader.py": ("将 Hugging Face、Parquet、JSONL 和 GZIP 数据集流式读取并统一为记录字典，再转换为独立 DocumentBlock。", ("数据集", "Hugging Face", "Parquet", "JSONL", "适配器", "流式读取")),
    "embedding.py": ("定义 Embedding 配置、稳定输入模板、向量校验及远程 Qwen3/OpenAI 兼容服务客户端。", ("Embedding", "Qwen3", "向量校验", "远程 HTTP", "revision", "归一化")),
    "extractors.py": ("按后缀抽取 TXT/Markdown、PDF 文本层、PPTX 形状文字，并计算文件元数据与 SHA-256。", ("文件抽取", "TXT", "Markdown", "PDF", "PPTX", "SHA-256")),
    "highlighting.py": ("把用户查询拆为安全关键词并用于 FTS5 查询和结果高亮。", ("关键词", "FTS5", "转义", "高亮")),
    "indexer.py": ("发现、排除、去重输入文件，串联抽取、清洗、结构解析、分块、Embedding 和 SQLite 原子替换。", ("增量索引", "文件发现", "排除规则", "进度", "单文件隔离")),
    "json_parser.py": ("实现配置驱动的有限 JSONPath、过滤、JSON Lines/数组流式记录读取、超大记录原文转发和结构扫描。", ("JSON", "JSONPath", "流式解析", "记录边界", "超大记录", "字段过滤")),
    "logging_config.py": ("配置控制台与文件日志格式、级别和 UTF-8 输出。", ("日志", "脱敏边界", "文件日志")),
    "models.py": ("定义文档、结构块、分段、搜索结果、数据库健康和索引进度等不可变数据契约。", ("数据模型", "dataclass", "数据契约")),
    "tokenization.py": ("使用 jieba 优先、字符级回退的方式生成中文检索词，并构造安全的 FTS5 AND 查询。", ("中文分词", "jieba", "字符回退", "FTS5")),
    "vector_search.py": ("提供 sqlite-vec KNN 和 NumPy 回退两种向量检索实现，并按模型配置同步向量派生表。", ("向量检索", "sqlite-vec", "NumPy", "KNN", "余弦相似度")),
    "answer.py": ("编排检索、严格上下文 Prompt、LLM 调用、引用合法性校验、拒答和脱敏审计日志。", ("RAG", "引用校验", "拒答", "Prompt", "审计日志")),
    "llm_client.py": ("通过 OpenAI 兼容 chat/completions HTTP 接口请求模型，解析答案与 token 用量并清理敏感配置。", ("LLM", "OpenAI 兼容", "HTTP", "token 用量", "API Key 脱敏")),
    "prompt.py": ("生成要求只依据检索上下文、把上下文视为不可信资料并逐句引用的聊天消息。", ("Prompt", "grounding", "引用", "拒答")),
    "retriever.py": ("把数据库搜索结果包装为可引用来源，按上下文字符预算合并相邻分段，并提供关键词/向量检索器。", ("RAG 检索", "来源", "引用 ID", "上下文预算", "相邻分段")),
    "app.py": ("提供标准库 ThreadingHTTPServer 的网页 API，覆盖统计、文档、搜索、问答、索引、删除和上传。", ("Web API", "HTTP", "上传", "安全边界", "并发")),
    "app.js": ("网页单页应用的交互层：标签切换、搜索、语义问答、文件上传、目录索引和文档删除。", ("前端", "Fetch API", "DOM", "搜索", "问答", "上传")),
    "index.html": ("网页单页应用的语义结构和表单骨架，定义搜索、问答、导入、文档管理视图及可访问性标记。", ("HTML", "网页结构", "表单", "可访问性")),
    "app.css": ("网页单页应用的视觉样式、布局、状态色、响应式断点和组件外观。", ("CSS", "布局", "响应式", "视觉状态")),
    "redox_ppt.js": ("使用 PptxGenJS 绘制氧化还原教学演示文稿，封装文本、形状、卡片、公式、页脚和过渡写入。", ("JavaScript", "PptxGenJS", "PPTX", "教学演示", "幻灯片")),
    "download_segmented.ps1": ("PowerShell 分段下载器：按 HTTP Range 下载大文件，校验每段大小后追加合并并支持断点续传。", ("PowerShell", "Range 下载", "断点续传", "文件校验")),
    "clean_rag_log.py": ("清洗 RAG 评估日志，核对事实、引用和消融结果并生成 JSONL 与 Markdown 报告。", ("评估", "日志清洗", "事实核对", "引用验证")),
    "probe_citation_failure.py": ("启动返回无引用答案的假 LLM 服务，验证引用校验会让 ask 失败且日志脱敏。", ("探针", "引用失败", "假服务", "回归验证")),
    "qwen_embedding_server.py": ("在 Transformers 服务端加载 Qwen Embedding，执行微批合并并暴露 /embed、OpenAI 兼容和 tokenizer 接口。", ("Embedding 服务", "Qwen", "Transformers", "微批", "FastAPI")),
    "run_rag_eval.py": ("按固定评估用例调用 ask 子进程并收集可复现的 RAG 评测日志。", ("RAG 评估", "子进程", "可复现")),
    "ablation_no_context.py": ("执行不提供检索上下文的消融实验，用于对比模型是否会凭空回答受控事实。", ("消融实验", "无上下文", "grounding")),
}

PATH_GUIDES: dict[str, tuple[str, tuple[str, ...]]] = {
    "personal_local_knowledge_base_v0/knowledge_search/__init__.py": ("知识库核心 Python 包的版本与公开包级说明。", ("包入口", "版本", "Python package")),
    "personal_local_knowledge_base_v0/knowledge_search/__main__.py": ("支持 `python -m knowledge_search` 的命令行模块入口，把退出码转交给 CLI。", ("模块入口", "CLI", "SystemExit")),
    "personal_local_knowledge_base_v0/knowledge_search/rag/__init__.py": ("RAG 子包的公开符号聚合入口，统一导出检索、回答和 LLM 客户端类型。", ("RAG", "包入口", "公开 API")),
    "personal_local_knowledge_base_v0/knowledge_search/web/__init__.py": ("网页子包公开入口，导出 KnowledgeWebApp、create_server 和 run_web。", ("Web", "包入口", "公开 API")),
    "personal_local_knowledge_base_v0/tests/__init__.py": ("测试包标记文件；不实现业务函数，只让 unittest 按包组织测试。", ("测试包", "unittest")),
}


@dataclass
class Entity:
    kind: str
    path: str
    qualified_name: str
    line_start: int
    line_end: int
    signature: str
    purpose: str
    docstring: str
    details: str
    keywords: list[str]
    calls: list[str]
    returns: list[str]
    raises: list[str]
    control_flow: list[str]
    side_effects: list[str]

    def as_dict(self) -> dict[str, Any]:
        return {
            "entity_id": f"{self.path}::{self.qualified_name}",
            "kind": self.kind,
            "file": self.path,
            "symbol": self.qualified_name,
            "line_start": self.line_start,
            "line_end": self.line_end,
            "signature": self.signature,
            "purpose": self.purpose,
            "docstring": self.docstring,
            "details": self.details,
            "keywords": self.keywords,
            "calls": self.calls,
            "returns": self.returns,
            "raises": self.raises,
            "control_flow": self.control_flow,
            "side_effects": self.side_effects,
        }


def relative(path: Path) -> str:
    return path.relative_to(PROJECT_DIR.parent).as_posix()


def short_node_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{short_node_name(node.value)}.{node.attr}"
    if isinstance(node, ast.Call):
        return short_node_name(node.func)
    return type(node).__name__


def expression_text(node: ast.AST | None, limit: int = 180) -> str:
    if node is None:
        return ""
    value = ast.unparse(node).replace("\n", " ")
    return value if len(value) <= limit else value[: limit - 1] + "…"


def name_words(name: str) -> list[str]:
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", name)
    return [part for part in re.split(r"[^A-Za-z0-9一-龥]+", name) if part]


def purpose_for(name: str, docstring: str, calls: list[str], kind: str) -> str:
    if docstring:
        return docstring.strip().split("\n\n", 1)[0].replace("\n", " ")
    if kind == "class":
        return f"定义 {name} 相关的状态、数据契约或协作接口。"
    if name.startswith("test_"):
        return f"回归测试：验证 {name[5:].replace('_', ' ')} 的预期行为、边界条件或错误处理。"
    if name == "__init__":
        return "初始化对象字段、运行配置和可复用的外部资源句柄。"
    if name == "__enter__":
        return "进入上下文管理器并返回可用的资源对象。"
    if name == "__exit__":
        return "退出上下文管理器，提交或关闭资源并按约定处理异常。"
    if name == "main":
        return "执行模块主流程，编排参数、业务调用、输出和进程退出码。"
    if name == "__new__":
        return "创建并初始化不可变值对象，同时附加结构化元数据。"
    exact = {
        "__post_init__": "执行 dataclass 配置校验，拒绝不满足范围、格式或不变量的参数。",
        "make": "根据正文和定位元数据创建稳定唯一的 DocumentBlock。",
        "fingerprint": "根据当前配置内容计算可比较、可缓存的哈希指纹。",
        "fingerprint_for": "把分块参数与 Embedding 后端配置组合为索引缓存指纹。",
        "append": "把相邻核心分块按分隔符合并，并更新合并块的边界和内容。",
        "first": "返回合并组中的第一个核心块，用于读取起始结构定位。",
        "last": "返回合并组中的最后一个核心块，用于读取结束结构定位。",
        "emit": "把当前解析或索引状态转换为一个可消费的记录/进度事件。",
        "report": "向回调或日志报告当前文件的索引进度和状态。",
        "counted_chunks": "包装分块迭代器并累计实际产生的分段数量。",
        "_same_structure": "比较两个核心块的标题、符号、记录或页面结构是否兼容。",
        "_crosses_hard_boundary": "判断合并是否会跨越代码、记录、页面或幻灯片硬边界。",
        "_located_block": "从合并核心组恢复带完整来源定位信息的结构块。",
        "_within_token_limit": "检查候选文本经 Embedding tokenizer 计算后是否不超过 Token 上限。",
        "_group_block_id": "根据合并组中的块 ID 生成稳定的最终分组标识。",
        "_capture": "记录流式 JSON 值的字符并在超过探测窗口时切换到临时文件。",
        "_advance": "推进 JSON 字符扫描状态机，处理字符串、转义和括号栈。",
        "_consume_first": "读取 JSON 记录首字符并初始化标量/容器扫描模式。",
        "_consume_next": "读取 JSON 记录后续字符并更新扫描状态。",
        "_flush_prefix": "把探测窗口内缓存的 JSON 前缀刷入临时文件。",
        "peek": "查看流式读取器的下一个字符但不消费它。",
        "peek_raw_character": "查看未跳过空白的原始下一个字符。",
        "take": "消费并返回流式读取器的下一个字符。",
        "take_raw_character": "消费并返回原始字符，保留 JSON 空白语义。",
        "skip_whitespace": "跳过当前输入中的空白字符并报告是否仍有数据。",
        "skip_string": "扫描并跳过带转义的 JSON 字符串，保持流位置正确。",
        "skip_value": "递归跳过一个 JSON 值而不物化其正文。",
        "expect": "校验下一个输入字符等于协议要求的字符，否则报告 JSON 格式错误。",
        "_resolve": "按有限 JSONPath 解析字段、数组索引或通配符，返回所有匹配值。",
        "_matches_filter": "按 equals/not_equals/in/exists 规则判断记录是否保留。",
        "_field_text": "从 JSON 记录抽取配置字段并拼接成可索引文本。",
        "_scalar_text": "把 JSON 标量、数组或对象规范化为可检索字符串。",
        "_source_text": "获取代码文档的完整源文本并处理缺失正文情况。",
        "_source_lines": "截取指定行号范围的源码，供结构块 canonical 内容使用。",
        "_source_comments": "提取源码行范围内的注释，作为函数或类的辅助语义。",
        "_arguments": "从 Python AST 函数节点展开位置参数、关键字参数和默认值信息。",
        "_python_items": "递归遍历 Python AST，产出模块、类、函数和方法的结构元数据。",
    }
    if name in exact:
        return exact[name]
    prefixes = (
        ("_parse_", "解析并转换"), ("parse_", "解析并转换"),
        ("_iter_", "以迭代器流式产生"), ("iter_", "以迭代器流式产生"),
        ("_load_", "加载并校验"), ("load_", "加载并校验"),
        ("_normalize", "规范化并适配"), ("normalize", "规范化并适配"),
        ("_build", "构造并返回"), ("build_", "构造并返回"),
        ("_validate", "校验并拒绝"), ("validate_", "校验并拒绝"),
        ("_search", "执行受约束的检索"), ("search", "执行检索"),
        ("close", "关闭并释放"), ("remove", "删除并清理"),
        ("save", "保存并持久化"), ("run", "启动并运行"),
    )
    for prefix, verb in prefixes:
        if name.startswith(prefix):
            subject = name[len(prefix):].replace("_", " ") or "内部资源"
            suffix = f"；内部调用 {', '.join(calls[:5])}" if calls else ""
            return f"{verb}{subject}{suffix}。"
    subject = name.replace("_", " ")
    suffix = f"，涉及 {', '.join(calls[:5])}" if calls else ""
    return f"执行 {subject}{suffix}。"


def collect_calls(node: ast.AST) -> list[str]:
    calls: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            name = short_node_name(child.func)
            if name not in calls:
                calls.append(name)
    return calls[:24]


def collect_returns(node: ast.AST) -> list[str]:
    values: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)) and child is not node:
            continue
        if isinstance(child, ast.Return):
            text = expression_text(child.value)
            if text and text not in values:
                values.append(text)
    return values[:8]


def collect_raises(node: ast.AST) -> list[str]:
    result: list[str] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Raise):
            text = expression_text(child.exc) or "裸 raise"
            if text not in result:
                result.append(text)
    return result[:8]


def infer_side_effects(calls: Iterable[str], source: str) -> list[str]:
    text = " ".join(calls) + " " + source
    effects: list[str] = []
    patterns = [
        ("SQLite/数据库写入或查询", r"sqlite|execute|commit|rollback|fts|KnowledgeBase"),
        ("文件系统读写", r"Path\.|\.open\(|read_text|write_text|write_bytes|TemporaryFile|File\."),
        ("网络 HTTP 请求", r"urlopen|urllib|Request\(|fetch\(|HTTPServer|requests"),
        ("日志输出", r"logger\.|logging|print\("),
        ("子进程或外部命令", r"subprocess|Start-Process|curl\.exe"),
        ("环境变量读取", r"os\.environ|getenv|dotenv"),
        ("模型/向量计算", r"Embedding|numpy|np\.|cosine|transformers|torch"),
    ]
    for label, pattern in patterns:
        if re.search(pattern, text, re.I):
            effects.append(label)
    return effects


def collect_python(path: Path, source: str, module_purpose: str, module_tags: tuple[str, ...]) -> list[Entity]:
    tree = ast.parse(source)
    lines = source.splitlines()
    entities: list[Entity] = []
    stack: list[str] = []

    class Visitor(ast.NodeVisitor):
        def visit_ClassDef(self, node: ast.ClassDef) -> None:
            qualified = ".".join(stack + [node.name])
            doc = ast.get_docstring(node) or ""
            entities.append(Entity(
                "class", relative(path), qualified, node.lineno, getattr(node, "end_lineno", node.lineno),
                f"class {node.name}", purpose_for(node.name, doc, [], "class"), doc,
                f"所属模块职责：{module_purpose}；类体包含 {sum(isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) for item in node.body)} 个直接方法。",
                list(dict.fromkeys([*module_tags, *name_words(node.name)])), [], [], [], ["类定义"], [],
            ))
            stack.append(node.name)
            self.generic_visit(node)
            stack.pop()

        def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
            self._function(node)

        def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
            self._function(node)

        def _function(self, node: ast.FunctionDef | ast.AsyncFunctionDef) -> None:
            qualified = ".".join(stack + [node.name])
            doc = ast.get_docstring(node) or ""
            calls = collect_calls(node)
            source_segment = ast.get_source_segment(source, node) or ""
            flow = []
            for label, typ in (("条件分支", (ast.If, ast.IfExp, ast.Match)), ("循环", (ast.For, ast.AsyncFor, ast.While)), ("异常处理", (ast.Try,)), ("上下文管理", (ast.With, ast.AsyncWith)), ("生成器 yield", (ast.Yield, ast.YieldFrom))):
                if any(isinstance(item, typ) for item in ast.walk(node)):
                    flow.append(label)
            if isinstance(node, ast.AsyncFunctionDef):
                flow.append("异步协程")
            args = ast.unparse(node.args)
            return_annotation = ast.unparse(node.returns) if node.returns else "未声明"
            signature = f"{'async ' if isinstance(node, ast.AsyncFunctionDef) else ''}def {node.name}({args}) -> {return_annotation}"
            returns = collect_returns(node)
            raises = collect_raises(node)
            details = (
                f"所属模块职责：{module_purpose}；输入参数：{args}；声明返回：{return_annotation}；"
                f"直接/间接调用：{', '.join(calls) if calls else '无明显函数调用'}；"
                f"返回表达式：{'; '.join(returns) if returns else '无显式 return（可能只产生副作用或通过 yield 输出）'}；"
                f"显式异常：{'; '.join(raises) if raises else '未发现显式 raise'}；"
                f"控制流：{', '.join(flow) if flow else '顺序执行'}。"
            )
            keywords = list(dict.fromkeys([*module_tags, *name_words(qualified), *calls, *flow]))
            entities.append(Entity(
                "function", relative(path), qualified, node.lineno, getattr(node, "end_lineno", node.lineno),
                signature, purpose_for(node.name, doc, calls, "function"), doc, details,
                keywords, calls, returns, raises, flow, infer_side_effects(calls, source_segment),
            ))
            stack.append(node.name)
            self.generic_visit(node)
            stack.pop()

        def visit_Lambda(self, node: ast.Lambda) -> None:
            """Index anonymous Python callbacks as first-class function records."""
            qualified = ".".join(stack + [f"lambda@{node.lineno}"])
            source_segment = ast.get_source_segment(source, node) or "lambda"
            calls = collect_calls(node)
            args = ast.unparse(node.args)
            returns = [expression_text(node.body)]
            flow = ["匿名函数"]
            details = (
                f"所属模块职责：{module_purpose}；这是匿名 lambda，输入参数：{args}；"
                f"返回表达式：{returns[0]}；调用：{', '.join(calls) if calls else '无明显函数调用'}；"
                "通常作为排序键、映射函数或事件回调传递给外部 API。"
            )
            entities.append(Entity(
                "function", relative(path), qualified, node.lineno, getattr(node, "end_lineno", node.lineno),
                f"lambda {args}", "匿名 lambda：接收参数并计算一个短表达式结果。", "", details,
                list(dict.fromkeys([*module_tags, "lambda", *calls])), calls, returns, [], flow,
                infer_side_effects(calls, source_segment),
            ))
            self.generic_visit(node)

    Visitor().visit(tree)
    return entities


def matching_brace(source: str, start: int) -> int:
    depth = 0
    quote: str | None = None
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if quote:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in "'\"`":
            quote = char
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
    return len(source) - 1


def collect_javascript(path: Path, source: str, module_purpose: str, module_tags: tuple[str, ...]) -> list[Entity]:
    entities: list[Entity] = []
    declaration = re.compile(r"(?m)^(\s*)(async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(([^\n]*)\)")
    arrow = re.compile(r"(?m)(?:(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*)?(async\s*)?(\([^\n()]*\)|[A-Za-z_$][\w$]*)\s*=>")
    seen: set[tuple[int, str]] = set()
    line_starts = [0]
    for match in re.finditer("\n", source):
        line_starts.append(match.end())

    def line_number(position: int) -> int:
        import bisect
        return bisect.bisect_right(line_starts, position)

    def add(name: str, start: int, end: int, signature: str, anonymous: bool = False) -> None:
        key = (start, name)
        if key in seen:
            return
        seen.add(key)
        segment = source[start : end + 1]
        calls = list(dict.fromkeys(re.findall(r"\b([A-Za-z_$][\w$]*)\s*\(", segment)))[:24]
        calls = [call for call in calls if call not in {"if", "for", "while", "switch", "catch", "function"}]
        flow = []
        if re.search(r"\bif\b|\?", segment): flow.append("条件分支")
        if re.search(r"\bfor\b|\.forEach\(|\.map\(", segment): flow.append("循环/集合遍历")
        if re.search(r"\btry\b|\bcatch\b", segment): flow.append("异常处理")
        if re.search(r"await\b", segment): flow.append("异步等待")
        purpose = "匿名回调：" if anonymous else ""
        purpose += purpose_for(name, "", calls, "function")
        details = (
            f"所属模块职责：{module_purpose}；JavaScript 输入签名：{signature}；"
            f"调用：{', '.join(calls) if calls else '无明显调用'}；"
            f"控制流：{', '.join(flow) if flow else '顺序执行'}；"
            "返回值由函数体决定，前端函数通常通过 DOM 更新、Fetch 请求或事件注册产生副作用。"
        )
        keywords = list(dict.fromkeys([*module_tags, *name_words(name), *calls, *flow, "JavaScript"]))
        entities.append(Entity(
            "function", relative(path), name, line_number(start), line_number(end), signature,
            purpose, "", details, keywords, calls, [], [], flow,
            infer_side_effects(calls, segment),
        ))

    for match in declaration.finditer(source):
        brace = source.find("{", match.end())
        end = matching_brace(source, brace) if brace >= 0 else match.end()
        add(match.group(3), match.start(), end, f"{'async ' if match.group(2) else ''}function {match.group(3)}({match.group(4).strip()})")
    for match in arrow.finditer(source):
        name = match.group(1) or f"anonymous_arrow@{line_number(match.start())}"
        brace = source.find("{", match.end())
        end = matching_brace(source, brace) if brace >= 0 else match.end()
        signature = f"{'async ' if match.group(2) else ''}{name} = {match.group(3).strip()} =>"
        add(name, match.start(), end, signature, anonymous=match.group(1) is None)
    return sorted(entities, key=lambda item: (item.line_start, item.qualified_name))


def script_entity(path: Path, source: str, purpose: str, tags: tuple[str, ...], language: str) -> Entity:
    commands = sorted(set(re.findall(r"\b(?:Get-Item|New-Item|Start-Process|curl\.exe|CopyTo|Move|File\.Delete|python|subprocess)\b", source, re.I)))
    details = f"脚本语言：{language}；无可声明的命名函数，主体按顺序执行。核心命令/操作：{', '.join(commands) if commands else '参数校验、文件处理和流程控制'}。"
    return Entity("script", relative(path), "<module>.__main__", 1, len(source.splitlines()), "module-level script", purpose, "", details, list(dict.fromkeys([*tags, language])), commands, [], [], ["条件分支", "循环"] if re.search(r"\bwhile\b|\bfor\b|\bif\b", source, re.I) else [], infer_side_effects(commands, source))


def render_markdown(records: list[dict[str, Any]]) -> str:
    files = [item for item in records if item["kind"] == "file"]
    by_file: dict[str, list[dict[str, Any]]] = {}
    for item in records:
        if item["kind"] != "file":
            by_file.setdefault(item["file"], []).append(item)
    lines = [
        "# 代码文件与函数语义索引",
        "",
        "> 本文件由 `scripts/generate_code_index.py` 从当前源码生成。每个文件、类、命名函数和 JavaScript 匿名箭头回调都有独立记录；行号以生成时源码为准。",
        "> JSONL 版本适合导入知识库：`docs/code-function-index.jsonl`。检索建议使用 `文件路径`、`symbol`、`关键词`、`调用`、`副作用` 和 `行号`。",
        "",
        f"覆盖文件：{len(files)}；实体记录：{len(records)}。",
        "",
    ]
    for file_record in files:
        path = file_record["file"]
        lines.extend([f"## {path}", "", f"**文件作用：** {file_record['purpose']}", "", f"**语言/关键词：** {', '.join(file_record['keywords'])}", "", f"**函数/类/脚本记录数：** {file_record['entity_count']}", ""])
        for item in by_file.get(path, []):
            lines.extend([
                f"### `{item['symbol']}` ({item['kind']}, L{item['line_start']}-L{item['line_end']})",
                "",
                f"**签名：** `{item['signature']}`",
                "",
                f"**作用：** {item['purpose']}",
                "",
                f"**详细语义：** {item['details']}",
                "",
                f"**关键词：** {', '.join(item['keywords']) or '无'}",
                "",
                f"**调用：** {', '.join(item['calls']) or '无明显调用'}；**返回：** {'; '.join(item['returns']) or '未记录'}；**异常：** {'; '.join(item['raises']) or '未发现显式 raise'}；**副作用：** {', '.join(item['side_effects']) or '未发现明显外部副作用'}。",
                "",
            ])
    return "\n".join(lines) + "\n"


def main() -> int:
    records: list[dict[str, Any]] = []
    paths = sorted(
        path for path in PROJECT_DIR.parent.rglob("*")
        if path.is_file() and path.suffix.lower() in CODE_SUFFIXES and not (set(path.parts) & SKIP_PARTS)
    )
    for path in paths:
        source = path.read_text(encoding="utf-8", errors="replace")
        guide_key = relative(path)
        purpose, tags = PATH_GUIDES.get(
            guide_key,
            MODULE_GUIDES.get(
                path.name,
            ("测试或辅助代码：通过可重复的输入、断言或运维流程验证项目行为。", ("代码", "回归", "辅助脚本")),
            ),
        )
        if "tests" in path.parts and path.name != "__init__.py":
            tested_name = path.stem.removeprefix("test_")
            tested_guide = MODULE_GUIDES.get(f"{tested_name}.py")
            if tested_guide:
                purpose = f"测试文件：验证 {tested_name} 模块的行为、边界和错误处理；{tested_guide[0]}"
                tags = (*tested_guide[1], "unittest", "回归测试")
            else:
                purpose = f"测试文件：验证 {tested_name} 相关功能的行为、边界和错误处理。"
                tags = (*tags, "unittest", "回归测试")
        language = {".py": "Python", ".js": "JavaScript", ".ps1": "PowerShell", ".html": "HTML", ".css": "CSS"}[path.suffix.lower()]
        try:
            if path.suffix.lower() == ".py":
                entities = collect_python(path, source, purpose, tags)
            elif path.suffix.lower() == ".js":
                entities = collect_javascript(path, source, purpose, tags)
            else:
                entities = [script_entity(path, source, purpose, tags, language)]
        except SyntaxError as exc:
            entities = [script_entity(path, source, f"源码解析失败，保留脚本级索引：{exc}", tags, language)]
        file_record = {
            "entity_id": f"{relative(path)}::<file>",
            "kind": "file",
            "file": relative(path),
            "symbol": "<file>",
            "line_start": 1,
            "line_end": len(source.splitlines()),
            "signature": f"{language} module",
            "purpose": purpose,
            "docstring": "",
            "details": f"源码文件共 {len(source.splitlines())} 行；包含 {len(entities)} 条可索引实体。文件级职责是：{purpose}",
            "keywords": list(dict.fromkeys([*tags, language, path.suffix.lower().lstrip(".")])),
            "calls": [],
            "returns": [],
            "raises": [],
            "control_flow": [],
            "side_effects": [],
            "entity_count": len(entities),
        }
        records.append(file_record)
        records.extend(entity.as_dict() for entity in entities)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    jsonl_path = OUTPUT_DIR / "code-function-index.jsonl"
    jsonl_path.write_text("\n".join(json.dumps(item, ensure_ascii=False, sort_keys=True) for item in records) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "code-function-index.md").write_text(render_markdown(records), encoding="utf-8")
    print(f"Wrote {len(records)} records for {len([r for r in records if r['kind'] == 'file'])} files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"use strict";

const $ = (selector) => document.querySelector(selector);
const $$ = (selector) => Array.from(document.querySelectorAll(selector));

const toastEl = $("#toast");
let toastTimer = null;

function toast(message, isError = false) {
  toastEl.textContent = message;
  toastEl.classList.toggle("is-error", isError);
  toastEl.hidden = false;
  if (toastTimer) clearTimeout(toastTimer);
  toastTimer = setTimeout(() => { toastEl.hidden = true; }, 3600);
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function formatBytes(bytes) {
  if (bytes == null) return "—";
  const units = ["B", "KB", "MB", "GB"];
  let value = Number(bytes);
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) { value /= 1024; unit += 1; }
  return `${value.toFixed(unit === 0 ? 0 : 1)} ${units[unit]}`;
}

async function api(path, options = {}) {
  const response = await fetch(path, {
    headers: options.body ? { "Content-Type": "application/json" } : {},
    ...options,
  });
  let payload = null;
  try { payload = await response.json(); } catch (e) { /* non-JSON error */ }
  if (!response.ok) {
    const message = payload && payload.error ? payload.error : `请求失败（${response.status}）`;
    throw new Error(message);
  }
  return payload;
}

// Tabs
$$(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    $$(".tab").forEach((t) => {
      const active = t === tab;
      t.classList.toggle("is-active", active);
      t.setAttribute("aria-selected", String(active));
    });
    $$(".panel").forEach((panel) => {
      panel.hidden = panel.id !== `panel-${tab.dataset.view}`;
    });
  });
});

// Stats
async function loadStats() {
  try {
    const stats = await api("/api/stats");
    $("#stat-documents").textContent = stats.documents;
    $("#stat-chunks").textContent = stats.chunks;
    const modeLabel = stats.search_mode === "semantic" ? "语义检索" : "关键词检索";
    $("#sidebar-note").textContent = stats.documents
      ? `${modeLabel}已启用，共 ${stats.documents} 篇文档。`
      : "数据库为空，请先导入文档。";
  } catch (err) {
    $("#sidebar-note").textContent = "无法读取统计信息。";
  }
}

// Search
$("#search-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const q = $("#search-q").value.trim();
  const box = $("#search-results");
  if (!q) { box.innerHTML = ""; return; }
  box.innerHTML = `<div class="empty"><span class="spinner"></span></div>`;
  try {
    const data = await api(`/api/search?q=${encodeURIComponent(q)}&limit=10&mode=semantic`);
    renderSearch(data.results);
  } catch (err) {
    box.innerHTML = `<div class="empty">搜索失败：${escapeHtml(err.message)}</div>`;
  }
});

function renderSearch(results) {
  const box = $("#search-results");
  if (!results.length) {
    box.innerHTML = `<div class="empty">没有找到匹配内容。</div>`;
    return;
  }
  box.innerHTML = results.map((result) => `
    <article class="result">
      <div class="result-head">
        <span class="result-title">${escapeHtml(result.filename)}</span>
        <span class="badge">${escapeHtml(result.file_type)}</span>
        <span class="result-meta">分段 ${result.chunk_index} · score ${Number(result.score).toFixed(3)}</span>
      </div>
      ${result.location ? `<div class="src-path">${escapeHtml(result.location)}</div>` : ""}
      <div class="result-content">${highlightedContent(result.highlighted)}</div>
    </article>
  `).join("");
}

function highlightedContent(html) {
  // The server emits <mark>...</mark>; sanitize by stripping any other tags.
  return String(html)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/&lt;mark&gt;/g, "<mark>")
    .replace(/&lt;\/mark&gt;/g, "</mark>");
}

// Ask
$("#ask-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const question = $("#ask-q").value.trim();
  const box = $("#ask-result");
  if (!question) { toast("请输入问题。", true); return; }
  box.innerHTML = `<div class="empty"><span class="spinner"></span> 正在检索并生成答案…</div>`;
  const button = event.submitter;
  button.disabled = true;
  try {
    const payload = {
      question,
      top_k: parseInt($("#ask-topk").value, 10) || 5,
      max_context_chars: parseInt($("#ask-context").value, 10) || 12000,
      temperature: parseFloat($("#ask-temperature").value) || 0,
      mode: "semantic",
    };
    const data = await api("/api/ask", { method: "POST", body: JSON.stringify(payload) });
    renderAnswer(data);
  } catch (err) {
    box.innerHTML = `<div class="answer-card"><div class="answer-text refused">${escapeHtml(err.message)}</div></div>`;
  } finally {
    button.disabled = false;
  }
});

function renderAnswer(data) {
  const box = $("#ask-result");
  if (data.error) {
    box.innerHTML = `<div class="answer-card"><div class="answer-text refused">${escapeHtml(data.error)}</div></div>`;
    return;
  }
  const refusedClass = data.refused ? " refused" : "";
  const sources = data.sources && data.sources.length
    ? `<div class="sources"><h3>引用来源</h3>${data.sources.map((source) => `
        <div class="source">
          <span class="cite">[${source.citation_id}]</span>
          <div class="src-info">
            <div class="src-name">${escapeHtml(source.filename)} · 分段 ${source.chunk_indexes.join("、")}</div>
            ${source.location ? `<div class="src-path">${escapeHtml(source.location)}</div>` : ""}
            <div class="src-path">${escapeHtml(source.path)}</div>
          </div>
        </div>`).join("")}</div>`
    : "";
  box.innerHTML = `
    <div class="answer-card">
      <div class="answer-text${refusedClass}">${escapeHtml(data.answer)}</div>
      <div class="answer-meta">
        <span>耗时 ${data.elapsed_ms} ms</span>
        <span>上下文 ${data.context_chars} 字符</span>
        <span>token ${data.usage.total_tokens}（输入 ${data.usage.prompt_tokens} / 输出 ${data.usage.completion_tokens}）</span>
      </div>
      ${sources}
    </div>`;
}

// Upload
const uploadZone = $("#upload-form");
const uploadInput = $("#upload-input");
uploadZone.addEventListener("click", () => uploadInput.click());
uploadZone.addEventListener("dragover", (event) => { event.preventDefault(); uploadZone.style.borderColor = "var(--accent)"; });
uploadZone.addEventListener("dragleave", () => { uploadZone.style.borderColor = ""; });
uploadZone.addEventListener("drop", (event) => {
  event.preventDefault();
  uploadZone.style.borderColor = "";
  if (event.dataTransfer.files.length) uploadFiles(event.dataTransfer.files);
});
uploadInput.addEventListener("change", () => {
  if (uploadInput.files.length) uploadFiles(uploadInput.files);
});

async function uploadFiles(files) {
  const progress = $("#import-progress");
  for (const file of files) {
    progress.innerHTML = `<span class="spinner"></span> 正在上传并索引 ${escapeHtml(file.name)}…`;
    const form = new FormData();
    form.append("file", file, file.name);
    try {
      const response = await fetch("/api/upload", { method: "POST", body: form });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || `上传失败（${response.status}）`);
      const idx = data.index;
      progress.innerHTML = `<span class="ok">✓</span> ${escapeHtml(data.filename)}：新增/更新 ${idx.indexed}，跳过 ${idx.skipped}，失败 ${idx.failed}`;
      await loadStats();
    } catch (err) {
      progress.innerHTML = `<span class="err">✕</span> ${escapeHtml(err.message)}`;
    }
  }
  uploadInput.value = "";
}

// Directory index
$("#dir-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const path = $("#dir-path").value.trim();
  const progress = $("#import-progress");
  if (!path) return;
  progress.innerHTML = `<span class="spinner"></span> 正在索引目录 ${escapeHtml(path)}…`;
  try {
    const data = await api("/api/index", {
      method: "POST",
      body: JSON.stringify({ paths: [path] }),
    });
    progress.innerHTML = `<span class="ok">✓</span> 发现 ${data.files_found}，新增/更新 ${data.indexed}，跳过 ${data.skipped}，失败 ${data.failed}`;
    await loadStats();
  } catch (err) {
    progress.innerHTML = `<span class="err">✕</span> ${escapeHtml(err.message)}`;
  }
});

// Documents
async function loadDocuments() {
  const box = $("#doc-list");
  box.innerHTML = `<div class="empty"><span class="spinner"></span></div>`;
  try {
    const data = await api("/api/documents");
    renderDocuments(data.documents);
  } catch (err) {
    box.innerHTML = `<div class="empty">加载失败：${escapeHtml(err.message)}</div>`;
  }
}

function renderDocuments(documents) {
  const box = $("#doc-list");
  if (!documents.length) {
    box.innerHTML = `<div class="empty">还没有已索引文档。</div>`;
    return;
  }
  box.innerHTML = documents.map((doc) => `
    <div class="doc-item" data-id="${doc.id}">
      <div class="doc-info">
        <div class="doc-name">${escapeHtml(doc.filename)} <span class="badge">${escapeHtml(doc.file_type)}</span></div>
        <div class="doc-meta">${formatBytes(doc.size)} · ${doc.chunks} 个分段 · ${escapeHtml(doc.indexed_at)}</div>
        <div class="doc-meta">${escapeHtml(doc.path)}</div>
      </div>
      <button class="btn btn-danger btn-remove" data-id="${doc.id}" data-name="${escapeHtml(doc.filename)}">
        <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M6 6l1 14h10l1-14"/></svg>
        移除
      </button>
    </div>
  `).join("");

  $$(".btn-remove").forEach((button) => {
    button.addEventListener("click", async () => {
      if (!confirm(`确定移除「${button.dataset.name}」的索引吗？`)) return;
      try {
        const data = await api("/api/remove", {
          method: "POST",
          body: JSON.stringify({ id: parseInt(button.dataset.id, 10) }),
        });
        toast(data.removed ? "已移除文档。" : "文档不存在。");
        await loadDocuments();
        await loadStats();
      } catch (err) {
        toast(err.message, true);
      }
    });
  });
}

// Load documents when switching to the manage tab.
$$(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    if (tab.dataset.view === "manage") loadDocuments();
  });
});

loadStats();

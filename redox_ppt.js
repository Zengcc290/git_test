const fs = require('fs');
const path = require('path');
const PptxGenJS = require('pptxgenjs');

const pptx = new PptxGenJS();
pptx.layout = 'LAYOUT_WIDE';
pptx.author = 'Codex';
pptx.company = 'OpenAI';
pptx.subject = '化学氧化还原反应';
pptx.title = '氧化还原反应：从电子转移到工业制硫酸';
pptx.lang = 'zh-CN';
pptx.theme = {
  headFontFace: 'Aptos Display',
  bodyFontFace: 'Microsoft YaHei',
  lang: 'zh-CN'
};
pptx.defineLayout({ name: 'WIDE_CUSTOM', width: 13.333, height: 7.5 });
pptx.layout = 'WIDE_CUSTOM';

const S = pptx.ShapeType;
const W = 13.333;
const H = 7.5;
const C = {
  bg: '08111F',
  panel: '101D31',
  panel2: '14253C',
  ink: 'F5F7FA',
  muted: '9FB2C8',
  line: '29415F',
  cyan: '51D9FF',
  cyan2: '9AEAFF',
  amber: 'FFC857',
  magenta: 'F06C9B',
  green: '63E6BE',
  purple: 'B68CFF',
  brown: 'C88754',
  red: 'FF6B6B',
  blue: '78A7FF'
};
const FONT = 'Microsoft YaHei';
const EQ = 'Aptos';

function addText(slide, text, x, y, w, h, opts = {}) {
  slide.addText(text, {
    x, y, w, h,
    fontFace: opts.fontFace || FONT,
    fontSize: opts.fontSize || 16,
    color: opts.color || C.ink,
    bold: opts.bold || false,
    italic: opts.italic || false,
    align: opts.align || 'left',
    valign: opts.valign || 'mid',
    margin: opts.margin === undefined ? 0 : opts.margin,
    breakLine: false,
    fit: 'shrink',
    charSpacing: opts.charSpacing,
    transparency: opts.transparency,
    rotate: opts.rotate,
    bullet: opts.bullet,
    paraSpaceAfterPt: opts.paraSpaceAfterPt,
    breakLine: opts.breakLine,
    isTextBox: true
  });
}

function rect(slide, x, y, w, h, fill, radius = true, line = null, transparency = 0) {
  slide.addShape(radius ? S.roundRect : S.rect, {
    x, y, w, h,
    rectRadius: 0.08,
    fill: { color: fill, transparency },
    line: line || { color: fill, transparency: 100 }
  });
}

function line(slide, x1, y1, x2, y2, color = C.line, width = 1.2, arrow = false, dash = 'solid') {
  slide.addShape(S.line, {
    x: x1, y: y1, w: x2 - x1, h: y2 - y1,
    line: {
      color,
      width,
      dashType: dash,
      beginArrowType: 'none',
      endArrowType: arrow ? 'triangle' : 'none'
    }
  });
}

function circle(slide, x, y, d, fill, lineColor = fill, transparency = 0) {
  slide.addShape(S.ellipse, {
    x, y, w: d, h: d,
    fill: { color: fill, transparency },
    line: { color: lineColor, transparency: lineColor === fill ? 100 : 0, width: 1 }
  });
}

function pill(slide, text, x, y, w, color, textColor = C.bg) {
  rect(slide, x, y, w, 0.34, color, true);
  addText(slide, text, x, y + 0.01, w, 0.30, { fontSize: 10, color: textColor, bold: true, align: 'center' });
}

function title(slide, kicker, heading, num) {
  addText(slide, kicker.toUpperCase(), 0.68, 0.32, 4.8, 0.24, { fontSize: 9, color: C.cyan, bold: true, charSpacing: 1.3 });
  addText(slide, heading, 0.68, 0.62, 10.7, 0.62, { fontSize: 25, bold: true, color: C.ink });
  addText(slide, String(num).padStart(2, '0'), 12.02, 0.37, 0.62, 0.32, { fontFace: EQ, fontSize: 13, color: C.cyan, bold: true, align: 'right' });
  line(slide, 0.68, 1.38, 12.64, 1.38, C.line, 0.8);
}

function footer(slide, label, num) {
  line(slide, 0.68, 7.10, 12.64, 7.10, C.line, 0.7);
  addText(slide, label, 0.68, 7.18, 7.0, 0.16, { fontSize: 8.5, color: C.muted });
  addText(slide, `${String(num).padStart(2, '0')}  /  氧化还原反应`, 10.1, 7.18, 2.54, 0.16, { fontSize: 8.5, color: C.muted, align: 'right' });
}

function note(slide, text) {
  slide.addNotes(text);
}

function addBg(slide, variant = 0) {
  slide.background = { color: C.bg };
  // Fine grid accents keep the deck visually alive without competing with the content.
  for (let i = 0; i < 8; i++) {
    circle(slide, 11.95 + (i % 2) * 0.17, 0.20 + i * 0.17, 0.035, variant % 2 ? C.amber : C.cyan, variant % 2 ? C.amber : C.cyan, 35);
  }
  for (let i = 0; i < 4; i++) {
    line(slide, 0.68, 6.73 + i * 0.08, 2.4, 6.73 + i * 0.08, C.line, 0.45, false, 'dash');
  }
}

function card(slide, x, y, w, h, opts = {}) {
  rect(slide, x, y, w, h, opts.fill || C.panel, true, opts.line ? { color: opts.line, width: opts.lineWidth || 1 } : null, opts.transparency || 0);
  if (opts.glow) {
    slide.addShape(S.line, { x: x + 0.14, y: y + 0.18, w: 0, h: h - 0.36, line: { color: opts.glow, width: 3 } });
  }
}

function formula(slide, text, x, y, w, h, color = C.ink, fs = 18, fill = C.panel2) {
  rect(slide, x, y, w, h, fill, true, { color: C.line, width: 0.6 });
  addText(slide, text, x + 0.12, y + 0.02, w - 0.24, h - 0.04, { fontFace: EQ, fontSize: fs, color, align: 'center', bold: true });
}

function dotLabel(slide, x, y, color, label, sub) {
  circle(slide, x, y + 0.06, 0.14, color);
  addText(slide, label, x + 0.25, y, 1.4, 0.24, { fontSize: 11, color: C.ink, bold: true });
  if (sub) addText(slide, sub, x + 0.25, y + 0.25, 1.7, 0.22, { fontSize: 9, color: C.muted });
}

// 1. Cover
{
  const slide = pptx.addSlide();
  addBg(slide, 0);
  // orbit illustration
  slide.addShape(S.ellipse, { x: 8.03, y: 0.82, w: 4.05, h: 4.05, fill: { color: C.bg, transparency: 100 }, line: { color: C.cyan, transparency: 65, width: 1 } });
  slide.addShape(S.ellipse, { x: 8.53, y: 1.33, w: 3.05, h: 3.05, rotate: 24, fill: { color: C.bg, transparency: 100 }, line: { color: C.amber, transparency: 72, width: 1 } });
  slide.addShape(S.ellipse, { x: 9.05, y: 1.86, w: 2.0, h: 2.0, rotate: -20, fill: { color: C.bg, transparency: 100 }, line: { color: C.magenta, transparency: 65, width: 1 } });
  circle(slide, 9.65, 2.46, 0.78, C.panel2, C.cyan);
  addText(slide, 'e⁻', 9.65, 2.60, 0.78, 0.30, { fontFace: EQ, fontSize: 23, color: C.cyan, bold: true, align: 'center' });
  circle(slide, 11.35, 1.10, 0.14, C.amber);
  circle(slide, 8.30, 3.72, 0.14, C.magenta);
  circle(slide, 10.92, 4.33, 0.14, C.green);
  addText(slide, 'CHEMISTRY / REDOX', 0.82, 1.08, 3.0, 0.25, { fontSize: 10, color: C.cyan, bold: true, charSpacing: 1.5 });
  addText(slide, '氧化还原\n反应', 0.80, 1.55, 5.8, 1.55, { fontSize: 43, bold: true, color: C.ink, valign: 'top' });
  addText(slide, '从电子转移到工业制硫酸', 0.84, 3.35, 5.6, 0.42, { fontSize: 19, color: C.cyan2, bold: true });
  addText(slide, '概念 · 判价 · 配平 · 强氧化剂 · 常见还原剂', 0.84, 3.92, 6.4, 0.28, { fontSize: 11, color: C.muted });
  pill(slide, '得电子 ＝ 还原', 0.84, 5.22, 1.75, C.cyan);
  pill(slide, '失电子 ＝ 氧化', 2.76, 5.22, 1.75, C.amber);
  formula(slide, 'MnO₄⁻  ⇌  Mn²⁺', 0.84, 5.92, 2.65, 0.55, C.cyan2, 18);
  formula(slide, 'H₂O₂：两面角色', 3.70, 5.92, 2.65, 0.55, C.amber, 16);
  addText(slide, '动态讲解版 · 适合课堂展示', 8.08, 5.92, 3.9, 0.28, { fontSize: 11, color: C.muted, align: 'right' });
  note(slide, '开场：先让学生看到“电子”是全章的主角。建议从“失电子/得电子”两个关键词切入，再进入后续流程。');
}

// 2. Map
{
  const slide = pptx.addSlide();
  addBg(slide, 1); title(slide, '01 | 先建立地图', '一条学习路径，串起整章', 2);
  const steps = [
    ['01', '识别', '是否发生化合价变化？', C.cyan],
    ['02', '判价', '谁升、谁降、谁得失电子？', C.amber],
    ['03', '配平', '用电子守恒把反应配准。', C.magenta],
    ['04', '介质', '酸性 / 中性 / 碱性决定产物。', C.green],
    ['05', '迁移', '工业、滴定与生活中的应用。', C.purple]
  ];
  steps.forEach((s, i) => {
    const x = 0.76 + i * 2.43;
    card(slide, x, 2.02, 2.02, 2.22, { fill: i % 2 ? C.panel2 : C.panel, glow: s[3] });
    circle(slide, x + 0.24, 2.28, 0.45, s[3]);
    addText(slide, s[0], x + 0.24, 2.39, 0.45, 0.16, { fontFace: EQ, fontSize: 10, color: C.bg, bold: true, align: 'center' });
    addText(slide, s[1], x + 0.24, 2.93, 1.55, 0.34, { fontSize: 20, color: s[3], bold: true });
    addText(slide, s[2], x + 0.24, 3.43, 1.50, 0.50, { fontSize: 10.5, color: C.muted, valign: 'top' });
    if (i < steps.length - 1) line(slide, x + 2.04, 3.12, x + 2.38, 3.12, s[3], 1.4, true);
  });
  card(slide, 0.76, 4.86, 11.82, 1.05, { fill: C.panel2, line: C.line });
  addText(slide, '本课高频物质', 1.02, 5.10, 1.42, 0.24, { fontSize: 11, color: C.muted, bold: true });
  pill(slide, 'KMnO₄', 2.62, 5.06, 1.25, C.purple, C.ink);
  pill(slide, 'H₂O₂', 4.04, 5.06, 1.12, C.cyan, C.bg);
  pill(slide, 'SO₂ / SO₃', 5.34, 5.06, 1.50, C.amber, C.bg);
  pill(slide, 'Fe²⁺ / Fe³⁺', 7.02, 5.06, 1.52, C.magenta, C.ink);
  addText(slide, '把“物质”放进“电子流动”里理解，记忆会更牢。', 8.82, 5.10, 3.35, 0.26, { fontSize: 10.5, color: C.cyan2, align: 'right' });
  footer(slide, '学习路径', 2);
  note(slide, '本页是导航页。每个步骤对应后面的一组视觉化页面，讲解时可以逐个点击推进。');
}

// 3. Core rule
{
  const slide = pptx.addSlide();
  addBg(slide, 0); title(slide, '02 | 核心概念', '一条规则，贯穿全章', 3);
  card(slide, 0.78, 1.82, 3.38, 3.45, { fill: '20192A', line: C.amber, glow: C.amber });
  addText(slide, '氧化', 1.10, 2.16, 1.6, 0.46, { fontSize: 29, color: C.amber, bold: true });
  addText(slide, '失电子\n化合价升高', 1.10, 2.86, 2.2, 0.72, { fontSize: 19, color: C.ink, bold: true, valign: 'top' });
  addText(slide, '还原剂在这里“交出”电子', 1.10, 4.18, 2.45, 0.26, { fontSize: 10.5, color: C.muted });
  circle(slide, 3.45, 2.18, 0.42, C.amber);
  addText(slide, 'e⁻', 3.45, 2.29, 0.42, 0.18, { fontFace: EQ, fontSize: 12, color: C.bg, bold: true, align: 'center' });
  card(slide, 9.17, 1.82, 3.38, 3.45, { fill: '172437', line: C.cyan, glow: C.cyan });
  addText(slide, '还原', 9.49, 2.16, 1.6, 0.46, { fontSize: 29, color: C.cyan, bold: true });
  addText(slide, '得电子\n化合价降低', 9.49, 2.86, 2.2, 0.72, { fontSize: 19, color: C.ink, bold: true, valign: 'top' });
  addText(slide, '氧化剂在这里“接收”电子', 9.49, 4.18, 2.45, 0.26, { fontSize: 10.5, color: C.muted });
  circle(slide, 11.84, 2.18, 0.42, C.cyan);
  addText(slide, 'e⁻', 11.84, 2.29, 0.42, 0.18, { fontFace: EQ, fontSize: 12, color: C.bg, bold: true, align: 'center' });
  // electron transfer rail
  line(slide, 4.43, 3.42, 8.72, 3.42, C.cyan2, 2.2, true);
  circle(slide, 6.48, 3.13, 0.58, C.panel2, C.cyan);
  addText(slide, 'e⁻', 6.48, 3.28, 0.58, 0.20, { fontFace: EQ, fontSize: 18, color: C.cyan, bold: true, align: 'center' });
  addText(slide, '电子从还原剂流向氧化剂', 5.05, 4.10, 3.2, 0.27, { fontSize: 11, color: C.cyan2, align: 'center', bold: true });
  formula(slide, 'Zn + Cu²⁺ → Zn²⁺ + Cu', 3.14, 5.72, 7.05, 0.65, C.ink, 20);
  addText(slide, 'Zn：还原剂        Cu²⁺：氧化剂', 3.40, 6.53, 6.5, 0.24, { fontSize: 11, color: C.muted, align: 'center' });
  footer(slide, '电子转移', 3);
  note(slide, '这里要反复强调：氧化剂自己被还原，還原剂自己被氧化。可以用Zn与Cu²⁺的置换反应做口头互动。');
}

// 4. Oxidation number
{
  const slide = pptx.addSlide();
  addBg(slide, 1); title(slide, '03 | 先判价，再找电子', '化合价是氧化还原反应的“雷达”', 4);
  const rules = [
    ['0', '单质', '单质中元素化合价为0', C.cyan],
    ['电荷', '离子', '单原子离子化合价＝所带电荷', C.amber],
    ['−2', '氧通常', 'O通常为−2价', C.green],
    ['−1', '过氧化物', 'H₂O₂ / Na₂O₂中O为−1价', C.magenta],
    ['+1', '氢通常', 'H通常为+1价，金属氢化物例外', C.purple],
    ['Σ', '代数和', '化合物和为0，离子和等于电荷', C.blue]
  ];
  rules.forEach((r, i) => {
    const x = 0.78 + (i % 3) * 3.98;
    const y = 1.78 + Math.floor(i / 3) * 1.32;
    card(slide, x, y, 3.55, 1.02, { fill: C.panel, line: C.line, glow: r[3] });
    addText(slide, r[0], x + 0.24, y + 0.15, 0.62, 0.38, { fontFace: EQ, fontSize: 22, color: r[3], bold: true, align: 'center' });
    addText(slide, r[1], x + 1.02, y + 0.16, 1.36, 0.22, { fontSize: 12, color: C.ink, bold: true });
    addText(slide, r[2], x + 1.02, y + 0.48, 2.20, 0.28, { fontSize: 9.4, color: C.muted, valign: 'top' });
  });
  addText(slide, '快速扫描：高频物质的关键价态', 0.80, 4.62, 3.3, 0.25, { fontSize: 11, color: C.cyan2, bold: true });
  const scan = [
    ['KMnO₄', 'Mn +7', C.purple],
    ['H₂O₂', 'O −1', C.cyan],
    ['SO₂', 'S +4', C.amber],
    ['Fe²⁺ → Fe³⁺', '升1价', C.magenta]
  ];
  scan.forEach((r, i) => {
    const x = 0.80 + i * 3.0;
    card(slide, x, 5.05, 2.62, 1.02, { fill: '0E192B', line: r[2] });
    addText(slide, r[0], x + 0.16, 5.25, 2.30, 0.23, { fontFace: EQ, fontSize: 15, color: r[2], bold: true, align: 'center' });
    addText(slide, r[1], x + 0.16, 5.62, 2.30, 0.18, { fontSize: 10, color: C.muted, align: 'center' });
  });
  footer(slide, '化合价判断', 4);
  note(slide, '建议把本页作为“随时回看”的速查卡。重点提醒H₂O₂中的氧是−1价，这是后面双重角色的根源。');
}

// 5. Redox or not
{
  const slide = pptx.addSlide();
  addBg(slide, 0); title(slide, '04 | 一眼识别', '反应发生了，不代表一定是氧化还原', 5);
  card(slide, 0.78, 1.86, 5.70, 3.98, { fill: '18273B', line: C.cyan, glow: C.cyan });
  pill(slide, '有化合价变化', 1.08, 2.16, 1.58, C.cyan);
  addText(slide, '氧化还原反应', 1.08, 2.72, 3.6, 0.34, { fontSize: 22, color: C.ink, bold: true });
  formula(slide, 'Zn + Cu²⁺ → Zn²⁺ + Cu', 1.08, 3.42, 4.95, 0.66, C.cyan2, 17, '0D1A2B');
  dotLabel(slide, 1.12, 4.48, C.amber, 'Zn：0 → +2', '失电子，被氧化');
  dotLabel(slide, 3.46, 4.48, C.cyan, 'Cu：+2 → 0', '得电子，被还原');
  addText(slide, '结论：必须追踪“谁升、谁降”。', 1.08, 5.45, 4.8, 0.22, { fontSize: 10.5, color: C.muted });
  card(slide, 6.86, 1.86, 5.70, 3.98, { fill: '211B2A', line: C.magenta, glow: C.magenta });
  pill(slide, '无化合价变化', 7.16, 2.16, 1.58, C.magenta, C.ink);
  addText(slide, '非氧化还原反应', 7.16, 2.72, 3.6, 0.34, { fontSize: 22, color: C.ink, bold: true });
  formula(slide, 'HCl + NaOH → NaCl + H₂O', 7.16, 3.42, 4.95, 0.66, 'FFD5E1', 17, '2A1624');
  dotLabel(slide, 7.20, 4.48, C.magenta, '复分解', '主要是离子重新组合');
  dotLabel(slide, 9.54, 4.48, C.muted, '价态不变', '没有电子转移');
  addText(slide, '结论：先看价态，再看反应类型。', 7.16, 5.45, 4.8, 0.22, { fontSize: 10.5, color: C.muted });
  rect(slide, 3.75, 6.24, 5.82, 0.54, C.amber, true);
  addText(slide, '判断开关：化合价有没有变化？', 3.75, 6.36, 5.82, 0.22, { fontSize: 15, color: C.bg, bold: true, align: 'center' });
  footer(slide, '反应识别', 5);
  note(slide, '用左右两类对照纠正常见误区：有气体、沉淀或水生成，并不能单独说明是氧化还原反应。');
}

// 6. Balancing
{
  const slide = pptx.addSlide();
  addBg(slide, 1); title(slide, '05 | 配平', '让电子守恒：从半反应到总反应', 6);
  addText(slide, '示例：酸性条件下 MnO₄⁻ 氧化 Fe²⁺', 0.82, 1.68, 5.0, 0.25, { fontSize: 12, color: C.cyan2, bold: true });
  const steps = [
    ['01', '锁定变化', 'Mn：+7 → +2\n得5e⁻', C.purple],
    ['02', '补齐原子', 'O用H₂O\nH用H⁺', C.cyan],
    ['03', '守恒电荷', 'Fe²⁺ → Fe³⁺\n每个失1e⁻', C.amber]
  ];
  steps.forEach((s, i) => {
    const x = 0.82 + i * 2.08;
    card(slide, x, 2.08, 1.78, 1.46, { fill: C.panel, line: s[3], glow: s[3] });
    addText(slide, s[0], x + 0.16, 2.27, 0.40, 0.18, { fontFace: EQ, fontSize: 10, color: s[3], bold: true });
    addText(slide, s[1], x + 0.16, 2.57, 1.42, 0.22, { fontSize: 11, color: C.ink, bold: true });
    addText(slide, s[2], x + 0.16, 2.94, 1.42, 0.42, { fontFace: EQ, fontSize: 10, color: C.muted, valign: 'top' });
    if (i < 2) line(slide, x + 1.82, 2.78, x + 2.02, 2.78, s[3], 1.3, true);
  });
  card(slide, 7.56, 1.92, 4.98, 2.06, { fill: '0D1B2D', line: C.line });
  addText(slide, '两个半反应', 7.88, 2.16, 2.0, 0.24, { fontSize: 11, color: C.muted, bold: true });
  addText(slide, 'MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O', 7.88, 2.62, 4.25, 0.28, { fontFace: EQ, fontSize: 14, color: C.purple, bold: true });
  addText(slide, 'Fe²⁺ → Fe³⁺ + e⁻', 7.88, 3.14, 4.25, 0.28, { fontFace: EQ, fontSize: 14, color: C.amber, bold: true });
  addText(slide, '电子总数：5 = 5', 7.88, 3.60, 4.25, 0.20, { fontSize: 10.5, color: C.green, bold: true });
  addText(slide, '合并后的离子方程式', 0.82, 4.40, 2.6, 0.25, { fontSize: 11, color: C.muted, bold: true });
  formula(slide, 'MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 0.82, 4.86, 11.72, 0.76, C.ink, 18, '132B40');
  pill(slide, '原子守恒', 1.14, 6.10, 1.18, C.green, C.bg);
  pill(slide, '电荷守恒', 2.54, 6.10, 1.18, C.cyan, C.bg);
  pill(slide, '电子守恒', 3.94, 6.10, 1.18, C.amber, C.bg);
  addText(slide, '配平不是“凑系数”，而是把电子数对齐。', 6.05, 6.14, 5.8, 0.22, { fontSize: 11, color: C.cyan2, align: 'right' });
  footer(slide, '半反应法', 6);
  note(slide, '配平页建议逐步点击：先出现价态变化，再出现半反应，最后出现总反应。课件通过连续视觉区块模拟逐步动画。');
}

// 7. Sulfuric acid process
{
  const slide = pptx.addSlide();
  addBg(slide, 0); title(slide, '06 | 工业应用', '现代制硫酸：接触法的三段推进', 7);
  addText(slide, 'SO₂  →  SO₃  →  H₂SO₄', 0.82, 1.67, 5.0, 0.34, { fontFace: EQ, fontSize: 22, color: C.cyan2, bold: true });
  const xs = [0.82, 4.46, 8.10];
  const colors = [C.amber, C.cyan, C.green];
  const headers = ['① 制 SO₂', '② 氧化 SO₂', '③ 吸收 SO₃'];
  const eqs = [
    'S + O₂ → SO₂\n或\n4FeS₂ + 11O₂ → 2Fe₂O₃ + 8SO₂',
    '2SO₂ + O₂ ⇌ 2SO₃',
    'SO₃ + H₂SO₄ → H₂S₂O₇\nH₂S₂O₇ + H₂O → 2H₂SO₄'
  ];
  const subs = [
    '焙烧硫或黄铁矿',
    'V₂O₅，400～500 ℃\n关键氧化步骤',
    '先成发烟硫酸\n再加水稀释'
  ];
  xs.forEach((x, i) => {
    card(slide, x, 2.28, 3.02, 3.20, { fill: i === 1 ? '10283A' : C.panel, line: colors[i], glow: colors[i] });
    circle(slide, x + 0.25, 2.55, 0.42, colors[i]);
    addText(slide, String(i + 1), x + 0.25, 2.67, 0.42, 0.16, { fontFace: EQ, fontSize: 10, color: C.bg, bold: true, align: 'center' });
    addText(slide, headers[i], x + 0.82, 2.57, 1.90, 0.26, { fontSize: 15, color: colors[i], bold: true });
    addText(slide, eqs[i], x + 0.24, 3.25, 2.54, i === 0 ? 0.94 : 0.78, { fontFace: EQ, fontSize: i === 0 ? 11 : 15, color: C.ink, bold: true, valign: 'top' });
    line(slide, x + 0.24, 4.44, x + 2.78, 4.44, C.line, 0.7);
    addText(slide, subs[i], x + 0.24, 4.66, 2.54, 0.48, { fontSize: 10, color: C.muted, valign: 'top' });
    if (i < 2) line(slide, x + 3.10, 3.86, x + 3.48, 3.86, colors[i], 2, true);
  });
  rect(slide, 0.82, 5.88, 11.72, 0.65, '2A1D18', true, { color: C.amber, width: 0.8 });
  addText(slide, '为什么不直接用水吸收SO₃？', 1.10, 6.08, 2.55, 0.20, { fontSize: 11, color: C.amber, bold: true });
  addText(slide, 'SO₃ + H₂O 反应过于剧烈，会形成酸雾；工业上先吸收成H₂S₂O₇，再加水。', 4.05, 6.08, 7.98, 0.20, { fontSize: 10.5, color: C.ink });
  footer(slide, '接触法制硫酸', 7);
  note(slide, '重点讲第二步：S(+4)被氧化为S(+6)，O₂被还原。第三步是工艺上的“控雾”设计，不是新的硫价态变化。');
}

// 8. Permanganate by medium
{
  const slide = pptx.addSlide();
  addBg(slide, 1); title(slide, '07 | 强氧化剂', '高锰酸钾：介质决定“落点”', 8);
  addText(slide, '同一个MnO₄⁻，在不同介质中会走向不同的还原产物。', 0.82, 1.66, 6.5, 0.24, { fontSize: 11.5, color: C.muted });
  const cols = [
    { x: 0.82, color: C.purple, name: '酸性', product: 'Mn²⁺', visual: '紫色 → 近无色', eq: 'MnO₄⁻ + 8H⁺ + 5e⁻\n→ Mn²⁺ + 4H₂O', use: 'Fe²⁺、C₂O₄²⁻、H₂O₂滴定' },
    { x: 4.46, color: C.brown, name: '中性 / 弱碱性', product: 'MnO₂↓', visual: '紫色 → 棕褐色', eq: 'MnO₄⁻ + 2H₂O + 3e⁻\n→ MnO₂↓ + 4OH⁻', use: '氧化SO₃²⁻、Fe²⁺等' },
    { x: 8.10, color: C.green, name: '强碱性', product: 'MnO₄²⁻', visual: '紫色 → 绿色', eq: 'MnO₄⁻ + e⁻\n→ MnO₄²⁻', use: '特定碱性体系中的还原' }
  ];
  cols.forEach((c) => {
    card(slide, c.x, 2.10, 3.02, 3.82, { fill: C.panel, line: c.color, glow: c.color });
    addText(slide, c.name, c.x + 0.24, 2.38, 2.5, 0.25, { fontSize: 15, color: c.color, bold: true });
    circle(slide, c.x + 0.24, 2.94, 0.52, c.color);
    addText(slide, 'Mn', c.x + 0.24, 3.09, 0.52, 0.16, { fontFace: EQ, fontSize: 12, color: C.bg, bold: true, align: 'center' });
    addText(slide, '→', c.x + 1.00, 3.05, 0.38, 0.22, { fontFace: EQ, fontSize: 18, color: C.muted, bold: true, align: 'center' });
    addText(slide, c.product, c.x + 1.54, 3.03, 1.20, 0.25, { fontFace: EQ, fontSize: 17, color: C.ink, bold: true });
    addText(slide, c.visual, c.x + 0.24, 3.74, 2.48, 0.25, { fontSize: 11, color: C.cyan2, bold: true });
    formula(slide, c.eq, c.x + 0.24, 4.22, 2.54, 0.76, C.ink, 11.5, '0C1728');
    addText(slide, '用途：' + c.use, c.x + 0.24, 5.28, 2.50, 0.35, { fontSize: 9.6, color: C.muted, valign: 'top' });
  });
  addText(slide, '实验提醒：酸性高锰酸钾通常用稀H₂SO₄酸化，避免Cl⁻被同步氧化。', 0.84, 6.32, 11.6, 0.24, { fontSize: 10.5, color: C.amber, bold: true, align: 'center' });
  footer(slide, 'KMnO₄的介质效应', 8);
  note(slide, '本页适合做“颜色动画”讲解：先看紫色MnO₄⁻，再依次出现酸性、中性、强碱性三种落点。');
}

// 9. Titration use
{
  const slide = pptx.addSlide();
  addBg(slide, 0); title(slide, '08 | 典型用途', 'KMnO₄滴定：紫色本身就是信号灯', 9);
  // burette
  card(slide, 0.90, 1.82, 2.25, 4.54, { fill: '0E1B2C', line: C.line });
  addText(slide, '滴定管', 1.18, 2.10, 1.6, 0.25, { fontSize: 12, color: C.muted, bold: true });
  rect(slide, 1.72, 2.58, 0.38, 2.24, 'DCE7F2', true, { color: 'FFFFFF', width: 0.8 });
  rect(slide, 1.78, 2.70, 0.26, 1.12, C.purple, true);
  line(slide, 1.91, 4.83, 1.91, 5.13, C.purple, 1.2, true);
  circle(slide, 1.86, 5.30, 0.10, C.purple);
  circle(slide, 1.86, 5.67, 0.10, C.purple);
  addText(slide, 'MnO₄⁻', 1.20, 5.96, 1.60, 0.28, { fontFace: EQ, fontSize: 18, color: C.purple, bold: true, align: 'center' });
  // flask
  card(slide, 3.56, 1.82, 4.42, 4.54, { fill: C.panel, line: C.cyan });
  addText(slide, '锥形瓶：待测Fe²⁺', 3.90, 2.10, 2.8, 0.24, { fontSize: 12, color: C.muted, bold: true });
  rect(slide, 5.12, 2.72, 0.72, 1.28, 'DCE7F2', true, { color: 'FFFFFF', width: 0.8 });
  slide.addShape(S.trapezoid, { x: 4.47, y: 3.78, w: 2.02, h: 1.58, fill: { color: '193A4A' }, line: { color: C.cyan, width: 1.1 } });
  slide.addShape(S.arc, { x: 4.60, y: 4.49, w: 1.76, h: 0.46, line: { color: C.purple, width: 2 }, fill: { color: C.purple, transparency: 78 } });
  line(slide, 5.48, 4.02, 5.48, 4.46, C.purple, 1.4, true);
  circle(slide, 5.43, 4.30, 0.10, C.purple);
  addText(slide, '终点：浅紫红色\n30秒不褪', 4.88, 5.72, 1.22, 0.46, { fontSize: 11, color: C.purple, bold: true, align: 'center', valign: 'top' });
  // steps
  card(slide, 8.38, 1.82, 4.16, 4.54, { fill: C.panel2, line: C.line });
  addText(slide, '课堂中的三帧动态', 8.72, 2.10, 2.8, 0.24, { fontSize: 12, color: C.muted, bold: true });
  const frames = [['滴加', '紫色进入溶液', C.purple], ['反应', '颜色迅速褪去', C.cyan], ['终点', '浅紫红色留存', C.amber]];
  frames.forEach((f, i) => {
    const y = 2.72 + i * 0.88;
    circle(slide, 8.74, y, 0.34, f[2]);
    addText(slide, String(i + 1), 8.74, y + 0.10, 0.34, 0.14, { fontFace: EQ, fontSize: 10, color: C.bg, bold: true, align: 'center' });
    addText(slide, f[0], 9.30, y + 0.02, 0.68, 0.20, { fontSize: 12, color: f[2], bold: true });
    addText(slide, f[1], 10.10, y + 0.02, 1.85, 0.20, { fontSize: 10, color: C.ink });
    if (i < 2) line(slide, 8.91, y + 0.38, 8.91, y + 0.75, C.line, 1.2, true);
  });
  formula(slide, 'MnO₄⁻ + 5Fe²⁺ + 8H⁺ → Mn²⁺ + 5Fe³⁺ + 4H₂O', 8.72, 5.52, 3.48, 0.60, C.ink, 10.5, '0D1726');
  footer(slide, '氧化还原滴定', 9);
  note(slide, '说明KMnO₄滴定的“自身指示”特点。强调反应介质和滴定终点现象，避免把紫色褪去误认为所有高锰酸钾反应的共同现象。');
}

// 10. Hydrogen peroxide dual role
{
  const slide = pptx.addSlide();
  addBg(slide, 1); title(slide, '09 | 双氧水', 'H₂O₂：同一个分子，两个角色', 10);
  circle(slide, 5.36, 2.28, 2.55, C.panel2, C.cyan);
  circle(slide, 5.63, 2.55, 2.01, C.bg, C.line);
  addText(slide, 'H₂O₂', 5.66, 2.92, 1.95, 0.46, { fontFace: EQ, fontSize: 32, color: C.ink, bold: true, align: 'center' });
  addText(slide, 'O：−1价', 5.88, 3.60, 1.55, 0.25, { fontFace: EQ, fontSize: 14, color: C.cyan2, bold: true, align: 'center' });
  card(slide, 0.82, 1.90, 3.66, 3.98, { fill: '172437', line: C.cyan, glow: C.cyan });
  pill(slide, '作氧化剂', 1.12, 2.20, 1.25, C.cyan);
  addText(slide, '得电子', 1.12, 2.82, 1.5, 0.32, { fontSize: 22, color: C.cyan2, bold: true });
  addText(slide, 'O：−1 → −2', 1.12, 3.28, 2.2, 0.25, { fontFace: EQ, fontSize: 14, color: C.ink, bold: true });
  formula(slide, 'H₂O₂ + 2I⁻ + 2H⁺\n→ I₂ + 2H₂O', 1.12, 3.86, 2.96, 0.80, C.ink, 13, '0D1726');
  addText(slide, '把I⁻氧化成I₂', 1.12, 5.10, 2.3, 0.20, { fontSize: 10.5, color: C.muted });
  card(slide, 8.86, 1.90, 3.66, 3.98, { fill: '2A2117', line: C.amber, glow: C.amber });
  pill(slide, '作还原剂', 9.16, 2.20, 1.25, C.amber);
  addText(slide, '失电子', 9.16, 2.82, 1.5, 0.32, { fontSize: 22, color: C.amber, bold: true });
  addText(slide, 'O：−1 → 0', 9.16, 3.28, 2.2, 0.25, { fontFace: EQ, fontSize: 14, color: C.ink, bold: true });
  formula(slide, 'Cl₂ + H₂O₂\n→ 2HCl + O₂', 9.16, 3.86, 2.96, 0.80, C.ink, 13, '201A12');
  addText(slide, '把Cl₂还原成Cl⁻', 9.16, 5.10, 2.3, 0.20, { fontSize: 10.5, color: C.muted });
  line(slide, 4.54, 3.41, 5.24, 3.41, C.cyan, 1.8, true);
  line(slide, 8.72, 3.41, 8.02, 3.41, C.amber, 1.8, true);
  rect(slide, 3.42, 6.04, 6.50, 0.56, C.panel2, true, { color: C.green, width: 0.8 });
  addText(slide, '歧化：2H₂O₂ → 2H₂O + O₂↑   （同一物质内部一升一降）', 3.42, 6.18, 6.50, 0.21, { fontFace: EQ, fontSize: 13, color: C.green, bold: true, align: 'center' });
  footer(slide, 'H₂O₂的双重角色', 10);
  note(slide, '双氧水是本章最适合用“左右分叉动画”讲解的物质。核心不是背两个方程式，而是看它的氧从−1价走向−2或0。');
}

// 11. Common reducing agents
{
  const slide = pptx.addSlide();
  addBg(slide, 0); title(slide, '10 | 还原剂矩阵', '常见还原剂：它们都在“交出电子”', 11);
  addText(slide, '还原剂本身发生氧化；被它还原的对象才发生还原。', 0.82, 1.67, 5.6, 0.24, { fontSize: 11.5, color: C.muted });
  const items = [
    ['H₂', 'CuO + H₂ → Cu + H₂O', '非金属还原剂', C.cyan],
    ['CO', 'Fe₂O₃ + 3CO → 2Fe + 3CO₂', '炼铁核心还原剂', C.amber],
    ['Zn', 'Zn + Cu²⁺ → Zn²⁺ + Cu', '活泼金属', C.green],
    ['H₂S', 'H₂S + I₂ → S + 2HI', '硫化氢还原性', C.magenta],
    ['SO₂', 'SO₂ + Br₂ + 2H₂O → H₂SO₄ + 2HBr', 'S(+4)继续升价', C.purple],
    ['Fe²⁺ / I⁻', '2Fe²⁺ + Cl₂ → 2Fe³⁺ + 2Cl⁻', '常见离子还原剂', C.blue]
  ];
  items.forEach((it, i) => {
    const x = 0.82 + (i % 3) * 4.03;
    const y = 2.15 + Math.floor(i / 3) * 1.80;
    card(slide, x, y, 3.56, 1.40, { fill: i % 2 ? C.panel2 : C.panel, line: it[3], glow: it[3] });
    addText(slide, it[0], x + 0.22, y + 0.19, 0.95, 0.30, { fontFace: EQ, fontSize: 20, color: it[3], bold: true, align: 'center' });
    line(slide, x + 1.38, y + 0.23, x + 1.38, y + 1.16, C.line, 0.8);
    addText(slide, it[1], x + 1.60, y + 0.22, 1.70, 0.54, { fontFace: EQ, fontSize: 11.2, color: C.ink, bold: true, valign: 'top' });
    addText(slide, it[2], x + 1.60, y + 0.93, 1.70, 0.18, { fontSize: 9.4, color: C.muted });
  });
  rect(slide, 0.82, 6.10, 11.70, 0.54, '211B2A', true, { color: C.magenta, width: 0.8 });
  addText(slide, '记忆方向：还原剂 → 失电子 → 化合价升高', 0.82, 6.24, 11.70, 0.20, { fontSize: 14, color: 'FFD5E1', bold: true, align: 'center' });
  footer(slide, '常见还原剂', 11);
  note(slide, '矩阵页可以按“物质类别”逐列出现。讲解时让学生先预测还原剂的价态变化，再核对方程式。');
}

// 12. Challenge
{
  const slide = pptx.addSlide();
  addBg(slide, 1); title(slide, '11 | 课堂互动', '三秒判断：谁是氧化剂？谁是还原剂？', 12);
  addText(slide, '先遮住答案，只看化合价变化。', 0.82, 1.68, 4.5, 0.24, { fontSize: 11.5, color: C.muted });
  const qs = [
    ['A', '2Fe²⁺ + Cl₂ → 2Fe³⁺ + 2Cl⁻', '判断两种角色', C.cyan],
    ['B', '2H₂O₂ → 2H₂O + O₂', '判断特殊类型', C.amber],
    ['C', 'SO₂ + 2H₂S → 3S + 2H₂O', '判断价态归宿', C.magenta]
  ];
  qs.forEach((q, i) => {
    const y = 2.25 + i * 1.24;
    card(slide, 1.08, y, 11.16, 0.90, { fill: C.panel, line: q[3], glow: q[3] });
    circle(slide, 1.38, y + 0.20, 0.46, q[3]);
    addText(slide, q[0], 1.38, y + 0.33, 0.46, 0.14, { fontFace: EQ, fontSize: 12, color: C.bg, bold: true, align: 'center' });
    addText(slide, q[1], 2.12, y + 0.20, 6.35, 0.26, { fontFace: EQ, fontSize: 17, color: C.ink, bold: true });
    addText(slide, q[2], 9.25, y + 0.26, 2.30, 0.20, { fontSize: 10.5, color: C.muted, align: 'right' });
  });
  rect(slide, 2.22, 6.22, 8.88, 0.56, C.cyan, true);
  addText(slide, '提示：先找“升价者”和“降价者”，再命名角色。', 2.22, 6.36, 8.88, 0.20, { fontSize: 14, color: C.bg, bold: true, align: 'center' });
  footer(slide, '课堂互动', 12);
  note(slide, '互动页建议停留几秒让学生作答。下一页给出答案和解析，形成点击推进的动态效果。');
}

// 13. Answers
{
  const slide = pptx.addSlide();
  addBg(slide, 0); title(slide, '12 | 互动解析', '答案不是重点，变化路径才是重点', 13);
  const ans = [
    ['A', 'Cl₂是氧化剂；Fe²⁺是还原剂', 'Fe²⁺：+2 → +3；Cl₂：0 → −1', C.cyan],
    ['B', '歧化反应', '一部分O：−1 → −2；另一部分O：−1 → 0', C.amber],
    ['C', '归中反应', 'S(+4)与S(−2)共同走向S(0)', C.magenta]
  ];
  ans.forEach((a, i) => {
    const x = 0.82 + i * 4.03;
    card(slide, x, 2.02, 3.56, 3.68, { fill: C.panel, line: a[3], glow: a[3] });
    circle(slide, x + 0.26, 2.33, 0.50, a[3]);
    addText(slide, a[0], x + 0.26, 2.47, 0.50, 0.16, { fontFace: EQ, fontSize: 13, color: C.bg, bold: true, align: 'center' });
    addText(slide, a[1], x + 0.26, 3.18, 2.92, 0.48, { fontSize: 16, color: C.ink, bold: true, valign: 'top' });
    line(slide, x + 0.26, 4.06, x + 3.30, 4.06, C.line, 0.8);
    addText(slide, a[2], x + 0.26, 4.40, 2.92, 0.52, { fontFace: EQ, fontSize: 11.5, color: a[3], bold: true, valign: 'top' });
    addText(slide, '核心：化合价轨迹', x + 0.26, 5.25, 2.92, 0.20, { fontSize: 10, color: C.muted });
  });
  rect(slide, 2.05, 6.18, 9.22, 0.54, '10283A', true, { color: C.green, width: 0.8 });
  addText(slide, '升价者＝还原剂　｜　降价者＝氧化剂　｜　同一元素一升一降＝歧化', 2.05, 6.32, 9.22, 0.20, { fontSize: 12.5, color: C.green, bold: true, align: 'center' });
  footer(slide, '互动解析', 13);
  note(slide, '解析时不要只公布答案，要带学生说出每个元素“从几价到几价”。这一步决定学生能否迁移到陌生反应。');
}

// 14. Recap flow
{
  const slide = pptx.addSlide();
  addBg(slide, 1); title(slide, '13 | 反应链复盘', '把零散方程式，收束成一张“电子地图”', 14);
  const nodes = [
    { x: 1.02, y: 2.60, d: 1.25, c: C.amber, t: '还原剂', s: '失 e⁻' },
    { x: 3.58, y: 2.60, d: 1.25, c: C.cyan, t: '氧化剂', s: '得 e⁻' },
    { x: 6.14, y: 2.60, d: 1.25, c: C.purple, t: '介质', s: '决定产物' },
    { x: 8.70, y: 2.60, d: 1.25, c: C.green, t: '应用', s: '工业 / 滴定' }
  ];
  nodes.forEach((n, i) => {
    circle(slide, n.x, n.y, n.d, C.panel2, n.c);
    addText(slide, n.t, n.x - 0.20, n.y + 0.35, n.d + 0.40, 0.22, { fontSize: 13, color: n.c, bold: true, align: 'center' });
    addText(slide, n.s, n.x - 0.20, n.y + 0.70, n.d + 0.40, 0.18, { fontSize: 9.5, color: C.muted, align: 'center' });
    if (i < nodes.length - 1) line(slide, n.x + n.d + 0.16, n.y + 0.62, nodes[i + 1].x - 0.20, nodes[i + 1].y + 0.62, n.c, 1.8, true);
  });
  addText(slide, '典型链条', 1.02, 4.50, 1.5, 0.24, { fontSize: 11, color: C.muted, bold: true });
  formula(slide, 'SO₂(+4)  →  SO₃(+6)  →  H₂SO₄(+6)', 1.02, 4.92, 5.22, 0.68, C.ink, 17, '172437');
  formula(slide, 'KMnO₄(+7)  →  Mn²⁺ / MnO₂ / MnO₄²⁻', 6.52, 4.92, 5.72, 0.68, C.ink, 16, '201A2A');
  addText(slide, '同一知识框架，也能解释：H₂O₂的双重角色、Fe²⁺滴定、Cl₂消毒和金属冶炼。', 1.02, 6.16, 11.3, 0.24, { fontSize: 11, color: C.cyan2, align: 'center' });
  footer(slide, '知识迁移', 14);
  note(slide, '复盘页把内容收束为“还原剂—氧化剂—介质—应用”四个节点，帮助学生建立框架，而非只记单个方程式。');
}

// 15. Final summary
{
  const slide = pptx.addSlide();
  addBg(slide, 0); title(slide, '14 | 带走四句话', '最后只记住这四个开关', 15);
  const takeaways = [
    ['01', '先判价', '化合价变了，才是氧化还原。', C.cyan],
    ['02', '看电子', '升价失电子；降价得电子。', C.amber],
    ['03', '看介质', 'KMnO₄的产物随酸碱环境改变。', C.purple],
    ['04', '看对象', 'H₂O₂、SO₂等物质的角色取决于对手。', C.green]
  ];
  takeaways.forEach((t, i) => {
    const x = 0.82 + (i % 2) * 6.03;
    const y = 1.95 + Math.floor(i / 2) * 1.42;
    card(slide, x, y, 5.45, 1.10, { fill: i % 2 ? C.panel2 : C.panel, line: t[3], glow: t[3] });
    circle(slide, x + 0.26, y + 0.30, 0.48, t[3]);
    addText(slide, t[0], x + 0.26, y + 0.44, 0.48, 0.14, { fontFace: EQ, fontSize: 10, color: C.bg, bold: true, align: 'center' });
    addText(slide, t[1], x + 0.98, y + 0.20, 1.4, 0.25, { fontSize: 16, color: t[3], bold: true });
    addText(slide, t[2], x + 0.98, y + 0.58, 3.95, 0.20, { fontSize: 11, color: C.ink });
  });
  formula(slide, '氧化还原 ＝ 电子转移 ＝ 化合价升降', 1.10, 5.20, 11.08, 0.76, C.ink, 22, '132B40');
  addText(slide, '安全提醒：强氧化剂与可燃物、浓酸或不明还原剂混合可能剧烈反应。', 1.10, 6.30, 11.08, 0.23, { fontSize: 10.5, color: C.amber, align: 'center' });
  footer(slide, '总结', 15);
  note(slide, '收尾可以让学生用自己的话复述四个开关，并把任意一个新反应带入框架判断。');
}

async function writeAndAddTransitions() {
  const out = path.join(__dirname, 'redox_reactions_dynamic.pptx');
  await pptx.writeFile({ fileName: out, compression: true });
  // PptxGenJS does not expose transitions directly. Add a valid fade transition
  // to each slide XML so the deck has a built-in dynamic feel in PowerPoint/WPS.
  const JSZip = require('jszip');
  const zip = await JSZip.loadAsync(fs.readFileSync(out));
  const slideNames = Object.keys(zip.files)
    .filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))
    .sort((a, b) => Number(a.match(/\d+/)[0]) - Number(b.match(/\d+/)[0]));
  for (let i = 0; i < slideNames.length; i++) {
    const name = slideNames[i];
    const xml = await zip.file(name).async('string');
    if (!xml.includes('<p:transition')) {
      const transition = i === 0
        ? '<p:transition spd="slow" advClick="1"><p:fade/></p:transition>'
        : '<p:transition spd="med" advClick="1"><p:fade/></p:transition>';
      const anchor = xml.includes('</p:clrMapOvr>') ? '</p:clrMapOvr>' : '</p:cSld>';
      const updated = xml.replace(anchor, anchor + transition);
      zip.file(name, updated);
    }
  }
  const data = await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE' });
  fs.writeFileSync(out, data);
  console.log(out);
}

writeAndAddTransitions().catch((err) => {
  console.error(err);
  process.exit(1);
});

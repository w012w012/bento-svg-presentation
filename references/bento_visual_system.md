# Bento Grid 高保真 SVG 视觉设计规范与微组件系统 (Design System 2.0)

> 本规范基于 Sandun（三顿）顶级 PPT 设计案例（《分层架构设计》、《AIoT智能家居》、《Dify企业介绍》等）反向工程提炼，旨在解决大模型手搓 SVG 容易退化为“黑底白字文本列表”和“彩虹色看板”的致命缺陷。

---

## 一、 顶尖质感三大铁律 (Hard Rules)

### 1. 单主色克制原则 (Single Accent Color Restraint)
* **严禁滥用多杂色**：禁止同一屏中红、黄、蓝、绿、紫同时出现！
* **单主色闭环**：全局有且仅能选择**一种核心品牌强调色**（默认推荐：电光青 `#00F2FE`，备选：科技蓝 `#38BDF8`、极客绿 `#10B981` 或橙黄 `#F59E0B`）。
* **全图严格四级色阶**：
  1. **背景底色**：深度沉浸黑蓝 `#080C14`
  2. **卡片底色**：略亮半透明暗灰蓝 `#0F172A`（透明度 0.6~0.85）
  3. **次级文字**：低对比度冷灰蓝 `#64748B` / `#94A3B8`
  4. **视觉焦点**：纯白加粗 `#FFFFFF`（大标题）+ 核心强调色（单主色，用于边缘光条、标签、微缩组件与大数字）

---

### 2. 左右平衡与“微缩视觉 Token”原则 (No Pure Text Lists)
* **严禁纯文本列表**：卡片内部禁止连续堆砌带有实心圆点的文字句子。
* **卡片必须具备“左右或上下双重重心”**：
  - **左侧/上侧（语义层）**：分类小胶囊标签（Pill Tag）+ 卡片标题 + 1~2 行精炼结论（主谓宾短语，禁止长句）。
  - **右侧/下侧（几何 Token 层）**：必须渲染一个**轻量抽象但具象化的微缩几何图形**，平衡视觉重心。

---

### 3. 虚实与深度层级 (Depth & Elevation)
* **背景网格 (Tech Grid)**：必须铺设间距 24px 或 30px 的极细正方形网格（opacity: 0.15~0.25），消除纯色空洞感。
* **卡片左边缘光条 (Left Accent Border)**：重要卡片左侧必须放置一条 `width="3"` 或 `width="4"` 的垂直强调色亮条，作为章节导引。
* **虚线沙箱 (Dashed Perimeter)**：外部系统、安全隔离层、监控层必须使用强调色虚线描边（`stroke-dasharray="5,4"`）。

---

## 二、 四大微缩视觉组件库 (Micro-Diagram Tokens)

模型在生成卡片右侧视觉重心时，必须从以下 4 种微缩组件中选择一种渲染：

### 1. 节点流水线组件 (Pipeline Token)
适用于：数据处理流、业务阶段递进、生命周期。
```xml
<!-- 示例：横向 3 节点流水线 -->
<g transform="translate(x, y)">
  <line x1="10" y1="20" x2="150" y2="20" stroke="#00F2FE" stroke-width="1.5" opacity="0.6"/>
  <!-- Node 1 -->
  <circle cx="10" cy="20" r="12" fill="#0F172A" stroke="#00F2FE" stroke-width="1.5"/>
  <text x="10" y="24" text-anchor="middle" fill="#00F2FE" font-size="10" font-weight="700">1</text>
  <!-- Node 2 -->
  <circle cx="80" cy="20" r="12" fill="#0F172A" stroke="#00F2FE" stroke-width="1.5"/>
  <text x="80" y="24" text-anchor="middle" fill="#00F2FE" font-size="10" font-weight="700">2</text>
  <!-- Node 3 -->
  <circle cx="150" cy="20" r="12" fill="#00F2FE"/>
  <text x="150" y="24" text-anchor="middle" fill="#080C14" font-size="10" font-weight="800">3</text>
</g>
```

### 2. 芯片微徽章组件 (Chip Group Token)
适用于：底层能力、技术底座、硬件模块、多模型生态。
```xml
<!-- 示例：2~3 个紧凑排列的深色倒角芯片容器 -->
<g transform="translate(x, y)">
  <rect x="0" y="0" width="48" height="28" rx="6" fill="#1E293B" stroke="#334155" stroke-width="1"/>
  <text x="24" y="18" text-anchor="middle" fill="#E2E8F0" font-size="11" font-weight="700">LLM</text>
  
  <rect x="56" y="0" width="48" height="28" rx="6" fill="#1E293B" stroke="#00F2FE" stroke-width="1" stroke-opacity="0.8"/>
  <text x="80" y="18" text-anchor="middle" fill="#00F2FE" font-size="11" font-weight="700">VDB</text>
</g>
```

### 3. 微型发光柱状/趋势图 (Mini Metric Chart Token)
适用于：销量对比、增长率、量化成果。
```xml
<!-- 示例：带上升趋势箭头的高亮渐变柱体 -->
<g transform="translate(x, y)">
  <rect x="0" y="40" width="16" height="50" rx="3" fill="#1E293B"/>
  <rect x="26" y="20" width="16" height="70" rx="3" fill="#0284C7"/>
  <rect x="52" y="5" width="16" height="85" rx="3" fill="#00F2FE"/>
  <!-- 趋势折线与箭头 -->
  <path d="M 8 35 Q 34 15 58 2" fill="none" stroke="#FFFFFF" stroke-width="1.5" stroke-dasharray="3,2"/>
  <polygon points="58,0 63,4 58,6" fill="#FFFFFF"/>
</g>
```

### 4. 拓扑容器与控制块 (DSL / Topology Token)
适用于：可视化编排、调度引擎、协议。
```xml
<!-- 示例：虚线矩形框内的控制单元 -->
<g transform="translate(x, y)">
  <rect x="0" y="0" width="90" height="40" rx="6" fill="#0F172A" stroke="#00F2FE" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="45" y="24" text-anchor="middle" fill="#00F2FE" font-size="12" font-weight="700" letter-spacing="1">DSL 引擎</text>
</g>
```

# Bento Grid 高保真 SVG 视觉设计规范与微组件系统 (Design System 2.1)

> 本规范基于 Sandun（三顿）顶级 PPT 设计案例（《分层架构设计》、《AIoT智能家居》、《Dify企业介绍》等）反向工程提炼，旨在解决大模型手搓 SVG 容易退化为“黑底白字文本列表”和“五彩斑斓杂色看板”的致命缺陷。

---

## 一、 顶尖质感四大铁律 (Hard Rules)

### 1. 颜色克制系统（主品牌色 80% + 受控语义色 20%）
* **主品牌色闭环（占核心视觉焦点 80%）**：全局统一选择**一种核心品牌强调色**（默认推荐：电光青 `#00F2FE`，备选：科技蓝 `#38BDF8`、极客绿 `#10B981` 或活力橙 `#FF6900`）。用于主光标、核心卡片高亮线、大指标数字、常规微缩 Token。
* **业务语义辅助色（严格限定 20%，需具备明确业务含义）**：
  - 危机 / 警示 / 断档 / 亏损：胭脂红 `#F43F5E` / 猩红 `#EF4444`；
  - 突破 / 增长 / 达标 / 正向：极客绿 `#10B981`；
  - 异动 / 关注 / 增量渠道：活力橙 `#F97316`；
  - **红线**：严禁毫无业务逻辑的“彩虹色看板”（例如把 4 个平级卡片各涂成红黄蓝绿）。
* **全图清晰五级色阶体系**：
  1. **背景底色**：深度沉浸黑蓝 `#070C18` 或 `#080C14`；
  2. **卡片底色**：微透暗夜灰蓝 `#0F172A` 或 `#111827`（搭配 `1px` 极细暗边框 `#1E293B`）；
  3. **次级与说明文字**：冷灰蓝 `#64748B` / `#94A3B8`；
  4. **标题与主文本**：纯白加粗 `#F8FAFC`；
  5. **焦点高光**：品牌主色与语义色。

---

### 2. 左右平衡与“微缩视觉 Token”原则 (No Pure Text Lists)
* **严禁纯文本列表**：卡片内部禁止只有带有实心圆点 `•` 的文字堆砌。
* **卡片必须具备“左右或上下双重重心”**：
  - **语义层（左侧 / 上侧）**：分类胶囊微标签（Pill Tag）+ 卡片标题 + 1~2 行精炼业务论据（字数严控，禁止大段 Word 搬家）。
  - **几何 Token 层（右侧 / 下侧）**：必须渲染一个**轻量抽象但具象化的微缩几何图形**，平衡视觉重心。

---

### 3. 虚实与工程深度 (Depth & Elevation)
* **背景网格 (Tech Grid)**：铺设间距 24px 或 28px 的极细正方形网格（opacity: 0.15~0.3），消除纯色空洞感。
* **卡片左边缘光条 (Left Accent Border)**：重要卡片左侧放置一条 `width="3"` 或 `width="4"` 的垂直强调色亮条，作为章节导引。
* **虚线沙箱 (Dashed Perimeter)**：外部系统、安全隔离层、监控层使用强调色虚线描边（`stroke-dasharray="5,4"`）。

---

### 4. Office 2016+ 原生矢量打散（Convert to Shape）安全红线
* **内联呈现属性优先**：所有几何元素使用内联属性（如 `fill="#00F2FE" stroke="#1E293B"`），避免在 `<style>` 标签内使用复杂 CSS 选择器，确保 Office 导入解析器 100% 识别。
* **渐变规范**：使用标准的 2 节点 `<linearGradient>`（`stop-color`），Office 完美转换为原生 Shape Gradient。
* **滤镜慎用原则**：`<filter>`（如 `feGaussianBlur` 外发光或 `feDropShadow`）在部分早期 Office 2016/2019 版本中执行“转换为形状”时，会导致该卡片被强制栅格化为位图图片。**若需纯净打散为原生 Office 形状，建议使用叠层透明度矩形模拟阴影与发光效果**。

---

## 二、 八大微缩视觉组件库 (Micro-Diagram Tokens 2.1)

大模型在生成每张 Bento 卡片的几何重心时，必须根据该卡片的业务属性，从以下 8 种微缩组件中选择一种渲染：

### 1. 节点流水线组件 (Pipeline Token)
适用于：数据处理流、业务阶段递进、生命周期。
```xml
<!-- 横向 3 节点流水线 -->
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
<!-- 紧凑排列的深色倒角芯片容器 -->
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
<!-- 带上升趋势箭头的高亮渐变柱体 -->
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
适用于：可视化编排、调度引擎、接口网关、协议。
```xml
<!-- 虚线矩形框内的控制单元 -->
<g transform="translate(x, y)">
  <rect x="0" y="0" width="90" height="40" rx="6" fill="#0F172A" stroke="#00F2FE" stroke-width="1.2" stroke-dasharray="4,3"/>
  <text x="45" y="24" text-anchor="middle" fill="#00F2FE" font-size="12" font-weight="700" letter-spacing="1">DSL 引擎</text>
</g>
```

### 5. 核心 KPI 环比增长胶囊 (Growth Capsule Token)
适用于：财务指标、环比/同比大幅变动、业务爆发点展示。
```xml
<!-- 涨跌幅胶囊与对比指标 -->
<g transform="translate(x, y)">
  <rect x="0" y="0" width="88" height="28" rx="14" fill="#064E3B" stroke="#10B981" stroke-width="1"/>
  <polygon points="12,17 18,9 24,17" fill="#10B981"/>
  <text x="30" y="18" fill="#34D399" font-size="12" font-weight="800">+34.8%</text>
  <text x="44" y="42" text-anchor="middle" fill="#64748B" font-size="10">YoY 净增长</text>
</g>
```

### 6. 紧凑环形占比仪表 (Donut / Radial Progress Token)
适用于：大盘份额占比、目标完成率、健康度评分。
```xml
<!-- 紧凑环形完成度图表 -->
<g transform="translate(x, y)">
  <circle cx="36" cy="36" r="28" fill="none" stroke="#1E293B" stroke-width="7"/>
  <!-- stroke-dasharray="周长(175.9) * 比例, 周长" -->
  <circle cx="36" cy="36" r="28" fill="none" stroke="#00F2FE" stroke-width="7"
          stroke-linecap="round" stroke-dasharray="123 176" transform="rotate(-90 36 36)"/>
  <text x="36" y="40" text-anchor="middle" fill="#F8FAFC" font-size="13" font-weight="800">70%</text>
  <text x="36" y="52" text-anchor="middle" fill="#64748B" font-size="8">占比</text>
</g>
```

### 7. 特性矩阵判定块 (Feature Matrix Token)
适用于：技术选型对比、方案对比、合规性检视。
```xml
<!-- 2x2 对比判定微矩阵 -->
<g transform="translate(x, y)">
  <rect x="0" y="0" width="84" height="48" rx="6" fill="#0B1120" stroke="#1E293B" stroke-width="1"/>
  <circle cx="20" cy="16" r="6" fill="#064E3B"/><text x="20" y="19" text-anchor="middle" fill="#34D399" font-size="9" font-weight="900">✓</text>
  <text x="32" y="19" fill="#94A3B8" font-size="10">高可用</text>
  <circle cx="20" cy="34" r="6" fill="#064E3B"/><text x="20" y="37" text-anchor="middle" fill="#34D399" font-size="9" font-weight="900">✓</text>
  <text x="32" y="37" fill="#94A3B8" font-size="10">自运维</text>
</g>
```

### 8. 阶段里程碑与旗标 (Milestone Timeline Token)
适用于：项目排期、季度 OKR 里程碑、战略落地节奏。
```xml
<!-- 里程碑指示旗标 -->
<g transform="translate(x, y)">
  <line x1="0" y1="24" x2="80" y2="24" stroke="#334155" stroke-width="2" stroke-dasharray="3,2"/>
  <polygon points="12,6 36,6 30,16 36,24 12,24" fill="#00F2FE"/>
  <text x="20" y="18" fill="#080C14" font-size="9" font-weight="800">M1</text>
  <circle cx="70" cy="24" r="5" fill="#1E293B" stroke="#00F2FE" stroke-width="1.5"/>
</g>
```

---
name: bento-svg-presentation
description: Creates executive-ready presentation slide decks using Bento Grid layouts and editable full-page vector SVG (Office 2016+ compatible). Use when the user wants to create, design, plan, or export presentations, pitch decks, slide decks, business reviews, or technical architecture slides.
version: 2.1.0
author: Sandun (Methodology) & Hermes
license: MIT
platforms: [linux, macos, windows]
---

# Bento SVG Presentation (便当网格矢量幻灯片工作流)

将非结构化业务与技术内容转化为高质感、结构化的 Bento Grid 幻灯片。
核心理念：**策划与视觉解耦，以卡片容器承载信息，输出可直接导入 Office 2016+ 无损打散编辑的原生矢量 SVG。**

---

## 执行流水线 (SOP)

必须严格遵循以下四阶段流水线，禁止跳过策划阶段直接套用模板：

```
[输入主题/文档]
       │
       ▼
1. 需求调研与逻辑大纲 (金字塔大纲) ────► 确认受众与目标，生成 JSON 大纲
       │
       ▼
2. 定点事实与数据填充 (事实检索)   ────► 补齐关键定量指标、同比/环比与技术事实
       │
       ▼
3. 容器权重与 Token 规划 (策划稿)   ────► 选定 Bento 栅格版式，为每张卡片分配微缩视觉 Token
       │
       ▼
4. SVG 渲染与排版自愈 (视觉呈现)   ────► 注入 defs 规范，输出 SVG 并执行排版自愈校验
```

### 阶段 1：需求调研与大纲搭建
1. 明确核心受众（高管汇报/技术方案/商业竞演）与演示目标。
2. 依据 `references/outline_prompt.md` 输出金字塔原理结构的 JSON 大纲，向用户确认后方可进入下一阶段。

### 阶段 2：事实与数据检索
逐页检查核心论点，确保量化数据真实可查，禁止模糊空话。

### 阶段 3：版式映射与 Token 分配
1. 根据每页信息形态（对比/架构/问题/路线），从 `references/data_layout_mapping.md` 和 `references/bento_grid_specs.md` 选择适配的 1280x720 拓扑容器。
2. 为每张卡片明确分配对应的几何微缩组件（如流水线、芯片组、趋势柱、环比胶囊等）。

### 阶段 4：SVG 生成与校验自愈
1. 载入生成规范 `references/bento_svg_prompt.md` 与视觉系统 `references/bento_visual_system.md`。
2. 注入标准预制定义 `templates/bento_defs_template.svg`。
3. 逐页生成 `slide_XX.svg` 并执行自动校验与修复：
   ```bash
   python scripts/validate_svg.py slide_01.svg --fix
   ```

---

## 核心设计铁律 (Design Invariants)

1. **色彩克制系统**
   - **主品牌色（80% 焦点）**：全局统一使用一种高饱和度主色（如电光青 `#00F2FE` 或科技蓝 `#38BDF8`），底层统一步调暗夜灰蓝 `#0F172A`。
   - **语义辅助色（20% 受控）**：仅用于明确业务归因（警示 `#F43F5E`、增长 `#10B981`、异动 `#F97316`），严禁无语义彩虹色。

2. **左右平衡与微缩视觉 Token**
   - **严禁纯文字列表卡片**：避免在卡片中堆砌只有项目符号 `•` 的大段文本。
   - 每张卡片必须形成“左侧语义结论 + 右侧几何微缩 Token”的双重心结构，从 `references/bento_visual_system.md` 的 8 大 Token 库中选择渲染。

3. **Office 2016+ 原生打散（Convert to Shape）兼容保障**
   - 形状均使用内联属性（`fill`、`stroke` 等），确保 Office 解析器 100% 识别。
   - 使用两节点 `<linearGradient>` 渐变；核心图形避免依赖复杂 `<filter>`，改用多层透明度矩形营造光影与深度。

---

## 交付与工具链

1. **排版自愈与合规校验**：
   ```bash
   python scripts/validate_svg.py slide_01.svg --fix
   ```
2. **多页串联预览器（纯前端无依赖）**：
   ```bash
   python scripts/build_deck.py --dir ./slides --title "演示文稿标题"
   ```
   - 快捷键：`←` / `→` 翻页（或触屏滑动）、`F` 全屏放映、`N` 演讲备注、`O` 九宫格全景、`C` 复制单页 SVG 源码、`E` 导出 1080P PNG。
3. **打包 PPTX 演示文稿**：
   ```bash
   python scripts/build_deck.py --dir ./slides --pptx output.pptx
   ```

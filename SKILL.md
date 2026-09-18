---
name: bento-svg-presentation
description: Creates executive-ready presentation slide decks using Bento Grid layouts and editable full-page vector SVG (Office 2016+ compatible). Use when the user wants to create, design, plan, or export presentations, pitch decks, slide decks, business reviews, or technical architecture slides.
version: 2.1.0
author: Sandun (Methodology) & Hermes
license: MIT
platforms: [linux, macos, windows]
---

# Bento SVG Presentation (便当网格矢量幻灯片工作流)

将非结构化业务与技术内容转化为高质感、结构化的 Bento Grid 演示文稿。
核心理念：**策划与视觉解耦，以卡片容器承载信息，并落盘生成可直接演示的交互 HTML 播放器与导入 Office 2016+ 无损打散编辑的原生矢量 PPTX。**

---

## 执行流水线 (SOP)

必须严格遵循以下五阶段流水线。**严禁仅在对话窗口输出 SVG 代码块**，必须落盘写入文件并执行构建闭环：

```
[输入主题/文档]
       │
       ▼
1. 需求调研与逻辑大纲 (金字塔大纲) ────► 确认受众与目标，生成 JSON 大纲并向用户确认
       │
       ▼
2. 定点事实与数据填充 (事实检索)   ────► 补齐关键定量指标、同比/环比与技术事实
       │
       ▼
3. 容器权重与 Token 规划 (策划稿)   ────► 选定 Bento 栅格版式，为每张卡片分配微缩视觉 Token
       │
       ▼
4. SVG 渲染与文件落地 (必须写入文件) ──► 将每页 slide_XX.svg 写入磁盘，并执行排版自愈校验
       │
       ▼
5. 最终打包交付 (生成 HTML 与 PPTX) ──► 运行 build_deck.py，产出 preview_deck.html 与 presentation.pptx
```

### 阶段 1：需求调研与大纲搭建
1. 明确核心受众（高管汇报/技术方案/商业竞演）与演示目标。
2. 依据 `references/outline_prompt.md` 输出金字塔原理结构的 JSON 大纲，向用户确认后方可进入下一阶段。

### 阶段 2：事实与数据检索
逐页检查核心论点，确保量化数据真实可查，禁止模糊空话。

### 阶段 3：版式映射与 Token 分配
1. 根据每页信息形态（对比/架构/问题/路线），从 `references/data_layout_mapping.md` 和 `references/bento_grid_specs.md` 选择适配的 1280x720 拓扑容器。
2. 为每张卡片明确分配对应的几何微缩组件（如流水线、芯片组、趋势柱、环比胶囊等）。

### 阶段 4：SVG 逐页渲染与落盘写入
1. 载入生成规范 `references/bento_svg_prompt.md` 与视觉系统 `references/bento_visual_system.md`。
2. 注入标准预制定义 `templates/bento_defs_template.svg`。
3. **必须使用写文件工具真实创建并保存文件**（如创建 `./slides/slide_01.svg`、`slide_02.svg`...），严禁只在聊天窗口展示代码块。
4. 逐页执行自动排版校验与自愈：
   ```bash
   python scripts/validate_svg.py ./slides/slide_01.svg --fix
   ```

### 阶段 5：最终构建交付（必须执行）
每页 SVG 落盘后，**必须调用构建脚本完成最终交付产物**：
```bash
python scripts/build_deck.py --dir ./slides --title "演示文稿标题"
```
该脚本将自动产出两项核心交付物：
1. `preview_deck.html`：本地全屏交互演示播放器（支持 `←`/`→` 翻页、`F` 全屏、`N` 演讲备注、`O` 九宫格概览、`C` 复制 SVG 源码、`E` 导出 1080P PNG）。
2. `presentation.pptx`：原生矢量演示文稿。内嵌 1080P 预览，且内嵌 `image/svg+xml` 原生矢量与 `asvg:svgBlip` 标记，支持在 PowerPoint 2016+ / 365 中直接右键**“转换为形状 (Convert to Shape)”**无损打散为原生矢量形状和文本框二次编辑！

在最终回复中，向用户提供上述文件的绝对路径与操作指引。

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

## 完成验收标准 (Checklist)
任务完成前，必须核对以下交付项全部存在：
- [ ] 目标目录下已生成所有 `slide_*.svg` 独立矢量文件
- [ ] 目标目录下已生成 `preview_deck.html` 交互播放器
- [ ] 目标目录下已生成 `presentation.pptx` 矢量演示文稿
- [ ] 已向用户明确提供文件路径及打开/导入 PowerPoint 说明

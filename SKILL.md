---
name: bento-svg-presentation
description: Use when designing Bento Grid PPT slides with editable SVG.
version: 2.0.0
author: Sandun (Methodology) & Hermes
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [ppt, presentation, slides, bento-grid, svg, gemini, office]
    category: productivity
    related_skills: [powerpoint, docx, web-design]
---

# Bento SVG Presentation Skill (顶级 PPT 专家流水线 2.0)

基于 Linux.do 顶级 PPT 设计专家（Sandun，前 1W+/页商业 PPT 定制公司策划师）总结的实战方法论。
核心思想：**彻底摈弃死板模板与“一键生成”，将内容策划与视觉设计深度解耦，采用卡片式便当盒（Bento Grid）网格语言，生成可直接导入 Office 2016+ 无损打散编辑的整页矢量 SVG 幻灯片。**

---

## 核心原则：作者原版方法论为下限（Baseline）

在执行本技能时，**严禁自作主张删减步骤或简化流程**。作者沉淀的 4 步专家工作流是不可逾越的底线：
```
[用户主题输入]
       │
       ▼
【阶段 1: 需求调研与提问】 ──── 逆向提问调研背景 ──► 运用金字塔原理输出 JSON 结构大纲（数字便利贴）
       │
       ▼
【阶段 2: 深度事实检索】   ──── 逐页大纲定点搜索 ──► 为骨架填充真实数据与案例（推荐 Grok / 搜索接口）
       │
       ▼
【阶段 3: 策划稿制作】     ──── 版式结构与视觉解耦 ──► 规划 Bento 容器权重，并显式指定右侧几何 Token
       │
       ▼
【阶段 4: Bento Grid 设计】──── 单主色克制原则 ──► 注入 Tech Grid、光条与微缩 Token，输出顶级矢量 SVG
```

---

## 2.0 升级规范：如何达到原作者案例的顶尖高级感？

### 1. 颜色克制法则（单主色原则）
* **严禁使用彩虹杂色**！禁止在一屏中同时使用红、黄、蓝、绿等多色。
* **单主色锁定**：全局仅允许一种高饱和度强调色（电光青 `#00F2FE`、科技蓝 `#38BDF8` 或品牌橙 `#FF6900`），其余全为暗夜蓝灰与纯白文字。

### 2. 拒绝纯文本卡片（微缩视觉 Token）
* 卡片内部严禁只有 `•` 文本列表。
* 必须采用“左侧文字结论 + 右侧几何微缩组件”的平衡结构。右侧根据业务从四类 Token 中选取：
  - **流水线节点 (Pipeline)**：3 节点连线；
  - **芯片组 (Chips)**：底座/硬件徽章；
  - **微型趋势图 (Mini Chart)**：带上升虚线箭头的渐变发光柱；
  - **拓扑控制块 (Topology)**：虚线控制框。

### 3. 光影与工程深度 (Depth & Elevation)
* 必须引入 `templates/bento_defs_template.svg` 中预制的数字化正方形网格（Tech Grid）。
* 核心卡片左侧添加 `3px` 垂直光条，外部关联系统使用虚线沙箱框。

---

## 四阶段标准作业程序 (SOP)

### 阶段 1：需求提问与大纲搭建
1. 先反问核心诉求（受众是谁？核心目的？）。
2. 调用 `references/outline_prompt.md` 输出金字塔原理 JSON 大纲并向用户确认。

### 阶段 2：逐页深度检索
针对确认的每一页大纲，检索客观数据与技术事实，绝不凭空捏造。

### 阶段 3：策划稿制作（版式与 Token 规划）
1. 确定每页的 Bento 栅格结构（1200x550 区域内）。
2. **显式规划**：指定该页各卡片右侧放置何种微缩 Token（流水线/芯片/趋势柱/拓扑框）。

### 阶段 4：Bento Grid 高保真 SVG 渲染
1. 完整加载 `references/bento_svg_prompt.md` 与 `references/bento_visual_system.md`。
2. 注入标准 `<defs>` 模板 `templates/bento_defs_template.svg`。
3. 逐页生成 SVG 并保存为 `slide_XX.svg`。

---

## 辅助工具库 (Scripts)

1. **SVG 语法与排版校验**：
   ```bash
   python scripts/validate_svg.py slide_01.svg
   ```
2. **多页串联本地交互播放器**：
   ```bash
   python scripts/build_deck.py --dir ./slides --title "演示文稿标题"
   ```
   在 Hermes 桌面端直接调用：
   ```text
   ::preview{file="/path/to/slides/preview_deck.html"}
   ```
3. **打包 PPTX**：
   ```bash
   python scripts/build_deck.py --dir ./slides --pptx output.pptx
   ```

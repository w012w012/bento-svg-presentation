# Bento SVG Presentation (顶级 PPT 专家流水线 2.1)

> **基于便当网格（Bento Grid）与整页矢量 SVG 的高保真 AI 演示文稿生成框架与 Agent 技能库。**  
> 告别死板模板、告别粗糙排版，生成可直接拖入 **PowerPoint 2016+ 取消组合打散编辑** 的硅谷发布会级演示文稿。

---

## 致谢与开源溯源 (Special Thanks)

本项目的核心方法论与设计哲学，源自 **Linux.do 社区顶尖 PPT 设计专家 Sandun（三顿）** 的重磅分享：
* **核心思路出处**：[应该是目前最强的PPT Agent，附上完整思路分享 (Linux.do)](https://linux.do/t/topic/1782304)
* **前作设计参考**：[把小米379页的年报转为可视化网页，附完整提示词 (Linux.do)](https://linux.do/t/topic/604327)

> **致敬原作者**：  
> 三顿老师拥有 7 年 PPT 定制与培训经验（曾任职于单页报价 1W+ 的国内顶尖 PPT 定制公司），他在帖中倡导的 **“金字塔策划大纲与视觉排版解耦”、“Bento Grid 语义卡片容器” 以及 “整页 SVG 矢量打散编辑”**，为整个 AI PPT 领域指明了摆脱“玩具套模板”的破局之路。  
> 
> 本仓库是在原作者公开的方法论与 Prompt 骨架基础上，由开源社区进一步完成**工程化、系统级封装与微观设计系统升级**的产物。我们承诺原作者的方法论是本项目的绝对下限。

---

## 为什么选择 Bento Grid + 整页矢量 SVG？

| 对比维度 | 传统 python-pptx 脚本 | 市面商业 AI PPT 工具 (Web) | **Bento SVG Presentation (本项目 2.1)** |
| :--- | :--- | :--- | :--- |
| **排版质感** | 极度死板、生硬，缺乏呼吸感 | 模版痕迹重，容易内容假大空 | **硅谷极客/Apple 发布会级 Dark Bento 风格** |
| **可编辑性** | 原生可编辑，但调样式极度痛苦 | 封闭平台，导出常需付费或为图片 | **拖入 Office 2016+ 直接打散为原生矢量形状** |
| **逻辑解耦** | 混在一起，模型常常顾此失彼 | 一键直出，无法人工精调 | **需求调研 ➔ 深度检索 ➔ 策划稿 ➔ 视觉稿四步解耦** |
| **微观视觉** | 纯文字项目符号列表 | 拼凑插画，逻辑割裂 | **8 大微缩几何组件 Token (流水线/芯片/图表/矩阵等)** |
| **大模型稳定性** | 易出现坐标重叠、换行截断 | 闭源黑盒 | **单主色克制 + 词法感知排版自愈引擎 (`--fix`)** |

---

## 2.1 工业级升级核心特性

在继承原作者四步专家流水线的基础上，本项目经过全面工程重构与升级：

1. **单主色基调 + 受控语义色谱 (Color System 2.1)**：
   - 全局锁定单一高饱和度主强调色（80% 视觉焦点，如电光青 `#00F2FE` 或科技蓝 `#38BDF8`）。
   - 规范引入 20% 受控业务语义色（危机红 `#F43F5E`、增长绿 `#10B981`、异动橙 `#F97316`），既避免了“五彩斑斓的大杂烩”，又完美满足经营分析与多维对比。
2. **8 大微缩视觉组件积木库 (Micro-Diagram Tokens)**：
   - 彻底打破大模型输出带有 `•` 的纯文本列表惯性。为模型预制 8 种高频参数化微缩几何 Token：
     - **流水线节点 (Pipeline)**、**芯片徽章组 (Chips)**、**微型发光趋势图 (Mini Chart)**、**拓扑控制块 (Topology)**；
     - **新增：核心 KPI 环比增长胶囊 (Growth Capsule)**、**紧凑环形占比仪表 (Donut Progress)**、**特性核对矩阵 (Feature Matrix)**、**阶段里程碑旗标 (Milestone Flag)**。
3. **词法感知排版自愈引擎 (`scripts/validate_svg.py --fix`)**：
   - 动态提取 `font-size` 自适应计算行高（`dy = round(font_size * 1.35)`），杜绝大标题换行重影；
   - 智能识别中英文字词边界与 XML 实体保护，避免半截断词；
   - 增加未定义 `url(#id)` 静态引用缺失检查与 Office 形状转换兼容性检测。
4. **全功能交互播放器 2.1 (`templates/preview_deck.html`)**：
   - 纯原生零依赖。全屏放映（`F`）、展开演讲者说辞抽屉（`N`）、Canvas 导出 1080P PNG（`E`）；
   - **新增九宫格全景缩略图总览（`O` / `G`）**，方便快速把握全篇节奏；
   - **新增一键复制当前页 SVG 矢量源码（`C`）**，方便快速粘入设计工具；
   - 支持移动端与触屏设备的左右滑动翻页。
5. **Office 2016+ 原生形状转换兼容性规范**：
   - 梳理 Office 矢量解析器红线，指导使用内联样式与安全渐变，确保打散时 100% 转换为 Office 可编辑形状。

---

## 目录结构

```text
bento-svg-presentation/
├── SKILL.md                          # Hermes / Claude / OpenCode 标准技能入口规范 (2.1)
├── references/                       # 核心设计规范与 Prompt 资产库
│   ├── outline_prompt.md            # 阶段 1：金字塔大纲架构师 Prompt (原作者原版)
│   ├── bento_svg_prompt.md          # 阶段 4：2.1 大师级 Bento Grid SVG 生成 Prompt
│   ├── bento_visual_system.md       # 单主色+语义色体系与 8 大微缩 Token 规范
│   ├── bento_grid_specs.md          # 6 大便当盒几何比例与留白规范
│   ├── data_layout_mapping.md       # 5 大业务数据形态到 Bento 拓扑映射指南
│   └── html_bento_alternative.md    # 备选单文件 HTML 网页版卡片规范
├── templates/
│   ├── bento_defs_template.svg      # 预制标准网格底纹、渐变 (含警示/增长) 与滤镜库
│   └── preview_deck.html            # 支持全览(O)、复制SVG(C)、备注(N)与1080P(E)的播放器
├── scripts/
│   ├── validate_svg.py              # 带 --fix 智能词法断行与引用检查的自愈引擎
│   └── build_deck.py                # 多页 SVG 串联、备注注入与 PPTX 打包工具
└── examples/                         # 真实实战案例 (包含家电微蒸烤全渠道经营分析)
    └── steamer_channel_analysis/
        ├── preview_deck.html
        ├── slide_01.svg ~ slide_06.svg
```

---

## 快速上手与使用工作流

### 步骤 1：金字塔大纲策划 (提问与调研)
使用 `references/outline_prompt.md`，输入你的主题与背景信息。AI 将运用金字塔原理输出严格的 JSON 结构大纲（数字便利贴）。

### 步骤 2：生成单页高保真 SVG
加载 `references/bento_svg_prompt.md` 与 `references/bento_visual_system.md`，将每页内容转化为 `slide_01.svg`。

### 步骤 3：文本排版自愈与合规检查
```bash
# 自动检测并修复长文本溢出、检查资源引用完整性
python scripts/validate_svg.py slides/slide_01.svg --fix
```

### 步骤 4：串联本地全屏交互演示器
```bash
python scripts/build_deck.py --dir ./slides --title "我的高管汇报"
```
打开生成的 `preview_deck.html`：
- 按 `←` / `→`：翻页（支持手机/触屏左右滑动）
- 按 `F`：进入全屏播放
- 按 `N`：呼出演讲者汇报说辞
- 按 `O` 或 `G`：开启九宫格全景缩略图总览
- 按 `C`：一键复制当前页 SVG 矢量源码
- 按 `E`：一键通过 Canvas 导出 1080P 高清 PNG

### 步骤 5：导入 PowerPoint 二次编辑
将生成的 `.svg` 文件直接拖拽进 **Microsoft PowerPoint 2016 或更新版本**，鼠标右键点击图片选择 **“转换为形状 (Convert to Shape)”**，即可完全打散为原生 Office 形状和文本，自由二次调整！

---

## 许可证 (License)

本项目采用 [MIT License](LICENSE)。欢迎自由使用、集成至个人 Agent、修改或用于商业演示文稿制作。

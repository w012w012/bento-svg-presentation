#!/usr/bin/env python3
"""
validate_svg.py - Bento Grid SVG 演示文稿排版规范与 Office 兼容性校验自愈引擎
功能：
1. XML 静态语法、命名空间 (xmlns) 与 1280x720 (16:9) 视口比例校验；
2. 资源引用完整性校验（检测 fill/stroke/filter 中的 url(#id) 是否在 <defs> 或文档中已定义）；
3. Office 2016+ 转换为形状（Convert to Shape）兼容性安全提示；
4. 【--fix 模式】：智能文本折行排版自愈：
   - 动态识别 font-size 并计算自适应行距 (dy = round(font_size * 1.35))，防止重影或行距过大；
   - 词法边界保护（CJK字符与英文单词断词、XML实体 &amp; / &lt; 保护）；
   - 尊重 text-anchor 对齐方式与相对坐标定位。
"""
import sys
import os
import xml.etree.ElementTree as ET
import re

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def estimate_display_units(text):
    """计算文本的等效视觉长度单位（中文字符计 1.0，西文字符计 0.55）"""
    units = 0.0
    for ch in text:
        if ord(ch) > 127:
            units += 1.0
        else:
            units += 0.55
    return units

def smart_tokenize(text):
    """将文本切分为不可拆分的词法单元（保护英文单词、连续数字、XML转义实体、中文字符）"""
    # 匹配: XML 实体 | 连续英文/数字/下划线/连字符 | 单个空白符 | 单个其他字符（如中文字符、标点）
    pattern = re.compile(r'(&[a-zA-Z0-9#]+;)|([a-zA-Z0-9_\-\.]+)|(\s+)|(.)')
    tokens = []
    for match in pattern.finditer(text):
        token = match.group(0)
        tokens.append(token)
    return tokens

def wrap_text_tokens(tokens, max_units=22.0):
    """根据视觉宽度将词法单元切分为多行，避免在单词中截断"""
    lines = []
    current_line = ""
    current_units = 0.0

    for token in tokens:
        t_units = estimate_display_units(token)
        # 如果当前行加上此 token 超出限制，且当前行非空
        if current_units + t_units > max_units and current_line.strip():
            lines.append(current_line.strip())
            current_line = token.lstrip()
            current_units = estimate_display_units(current_line)
        else:
            current_line += token
            current_units += t_units

    if current_line.strip():
        lines.append(current_line.strip())

    return lines if lines else [text]

def parse_and_validate(file_path, auto_fix=False):
    issues = []
    warnings = []
    infos = []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        print(f"[FAIL] 无法读取文件 {file_path}: {e}")
        return False

    # 1. 基础 XML 解析
    try:
        ET.register_namespace("", "http://www.w3.org/2000/svg")
        root = ET.fromstring(content)
    except ET.ParseError as e:
        issues.append(f"XML 语法解析失败 (标签未闭合或未转义字符): {e}")
        return print_report(file_path, issues, warnings, infos)

    # 2. 检查根节点
    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag.lower() != "svg":
        issues.append(f"根节点不是 <svg>，而是 <{tag}>")

    # 3. 检查 xmlns（Office 导入打散硬性要求）
    xmlns = root.attrib.get("xmlns", "")
    if "http://www.w3.org/2000/svg" not in xmlns and "http://www.w3.org/2000/svg" not in root.tag:
        issues.append("缺失 xmlns=\"http://www.w3.org/2000/svg\"，Office 无法识别为原生矢量形状")

    # 4. 检查 viewBox
    viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if not viewbox:
        warnings.append("未定义 viewBox 属性，建议设置 viewBox=\"0 0 1280 720\"")
    else:
        parts = viewbox.replace(",", " ").split()
        if len(parts) == 4:
            try:
                w, h = float(parts[2]), float(parts[3])
                ratio = w / h if h > 0 else 0
                if abs(ratio - 16 / 9) > 0.05:
                    warnings.append(f"当前画布比例 ({parts[2]}x{parts[3]}) 不是标准的 16:9 (建议 1280x720)")
            except ValueError:
                pass

    # 5. 校验资源引用完整性 (检查所有 url(#id) 是否都有对应定义的 id)
    defined_ids = set(re.findall(r'\bid=[\"\x27]([^\s\"\x27]+)[\"\x27]', content))
    referenced_urls = set(re.findall(r'url\(#([^\s\)\"\x27]+)\)', content))
    missing_ids = referenced_urls - defined_ids
    if missing_ids:
        for mid in missing_ids:
            issues.append(f"引用了未定义的资源: url(#{mid})，会导致形状变黑或渲染缺失")

    # 6. Office 2016+ 打散兼容性检查 (filter 与 image 提示)
    has_filters = "<filter" in content or "filter=" in content
    if has_filters:
        infos.append("检测到 <filter> 滤镜（发光/阴影）：Office 转换为形状时可能将滤镜对象栅格化为图片。若需 100% 矢量打散，建议使用多层透明度矩形模拟。")

    has_images = "<image" in content
    if has_images:
        warnings.append("检测到内嵌 <image> 元素：Office 转换为形状时无法矢量化位图图片。")

    # 7. 文本溢出检测与智能自愈
    fixed_count = 0
    text_pattern = re.compile(r'(<text\b([^>]*)>)(.*?)(</text>)', re.DOTALL)

    def replacer(match):
        nonlocal fixed_count, warnings
        full_match = match.group(0)
        start_tag = match.group(1)
        attrs = match.group(2)
        inner = match.group(3).strip()
        end_tag = match.group(4)

        # 已经包含子标签（如已有 tspan）则不重复处理
        if "<" in inner:
            return full_match

        # 解析 font-size 与 y 坐标判断上下文
        fs_match = re.search(r'\bfont-size=[\"\x27](\d+(?:\.\d+)?)[\"\x27]', attrs)
        if not fs_match:
            fs_style = re.search(r'font-size:\s*(\d+(?:\.\d+)?)px', attrs)
            font_size = float(fs_style.group(1)) if fs_style else 14.0
        else:
            font_size = float(fs_match.group(1))

        y_match = re.search(r'\by=[\"\x27](\d+(?:\.\d+)?)[\"\x27]', attrs)
        y_val = float(y_match.group(1)) if y_match else 0.0

        # 根据排版位置与字号动态设定容量阈值：
        # 1. 顶部 Header 大标题 (y <= 90 且 font-size >= 24)：拥有横跨全屏宽度的空间 (~1000px)，允许约 30~34 字符
        # 2. 卡片内部大字号标题 (y > 90 且 font-size >= 20)：卡片宽度有限 (~380-580px)，阈值设为 16~18
        # 3. 常规卡片正文 (font-size <= 16)：标准卡片单行约 22~24 字符
        if font_size >= 24 and y_val <= 90:
            max_units = 32.0
        elif font_size >= 20:
            max_units = 18.0
        else:
            max_units = 24.0

        units = estimate_display_units(inner)
        if units > max_units and "dy=" not in attrs:
            warnings.append(f"长文本可能溢出 ({units:.1f}单位 / 字号{font_size}px): \"{inner[:20]}...\"")

            if auto_fix:
                tokens = smart_tokenize(inner)
                lines = wrap_text_tokens(tokens, max_units=max_units)

                if len(lines) > 1:
                    # 提取 x 坐标
                    x_match = re.search(r'\bx=[\"\x27]([^\s\"\x27]+)[\"\x27]', attrs)
                    base_x = x_match.group(1) if x_match else None
                    line_height = round(font_size * 1.35)

                    tspan_str = ""
                    for idx, line in enumerate(lines):
                        x_attr = f'x="{base_x}" ' if base_x is not None else ''
                        dy = '0' if idx == 0 else str(line_height)
                        tspan_str += f'<tspan {x_attr}dy="{dy}">{line}</tspan>'

                    fixed_count += 1
                    return f"{start_tag}{tspan_str}{end_tag}"

        return full_match

    new_content = text_pattern.sub(replacer, content)
    if auto_fix and fixed_count > 0:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"[FIX] 已基于字号动态行高重构 {fixed_count} 处超长文本为自愈多行 <tspan>！")

    return print_report(file_path, issues, warnings, infos)

def print_report(file_path, issues, warnings, infos):
    print(f"--- 校验报告: {file_path} ---")
    for i in infos:
        print(f"  [INFO] {i}")
    for w in warnings:
        print(f"  [WARN] {w}")
    for err in issues:
        print(f"  [ERR]  {err}")

    if not issues and not warnings:
        print("[PASS] SVG 完全符合 Bento Grid 与 Office 原生矢量兼容规范！")

    return len(issues) == 0

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("用法: python validate_svg.py <slide.svg> [--fix]")
        sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"] else 1)

    fix_mode = "--fix" in sys.argv
    target_file = [a for a in sys.argv[1:] if a != "--fix"][0]
    ok = parse_and_validate(target_file, auto_fix=fix_mode)
    sys.exit(0 if ok else 1)

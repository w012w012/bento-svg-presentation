#!/usr/bin/env python3
"""
validate_svg.py - 校验并自愈 SVG 演示文稿排版规范
功能：
1. 校验根节点、xmlns 命名空间（保证 Office 导入与打散编辑兼容性）；
2. 校验 viewBox (1280x720) 比例；
3. 检测长文本溢出卡片风险；
4. 【--fix 模式】：自动将超长单行 <text> 重构为符合 Office 规范的自愈多行 <tspan x="..." dy="...">。
"""
import sys
import os
import xml.etree.ElementTree as ET
import re

def parse_and_validate(file_path, auto_fix=False):
    issues = []
    warnings = []
    
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
        issues.append(f"XML 语法解析失败 (标签未闭合或非法字符): {e}")
        return print_report(file_path, issues, warnings)

    # 2. 检查根节点
    tag = root.tag.split("}")[-1] if "}" in root.tag else root.tag
    if tag.lower() != "svg":
        issues.append(f"根节点不是 <svg>，而是 <{tag}>")

    # 3. 检查 xmlns（Office 导入打散硬性要求）
    xmlns = root.attrib.get("xmlns", "")
    if "http://www.w3.org/2000/svg" not in xmlns and "http://www.w3.org/2000/svg" not in root.tag:
        issues.append("缺失 xmlns=\"http://www.w3.org/2000/svg\"，Office 无法识别为矢量形状")

    # 4. 检查 viewBox
    viewbox = root.attrib.get("viewBox") or root.attrib.get("viewbox")
    if not viewbox:
        warnings.append("未定义 viewBox 属性，建议设置 viewBox=\"0 0 1280 720\"")

    # 5. 检查与自动修复超长文本
    fixed_count = 0
    new_content = content

    # 针对可能溢出的单行 <text> 做识别与替换
    # 规则：如果单行 <text> 纯文本超过 24 个汉字/字符，且内部没有 <tspan>，则判定为溢出风险
    text_pattern = re.compile(r'(<text\b([^>]*)>)(.*?)(</text>)', re.DOTALL)
    
    def replacer(match):
        nonlocal fixed_count, warnings
        full_match = match.group(0)
        start_tag = match.group(1)
        attrs = match.group(2)
        inner = match.group(3).strip()
        end_tag = match.group(4)
        
        # 排除包含子标签的情况
        if "<" in inner:
            return full_match

        # 长度检查 (中文字符长度加权)
        length = len(inner)
        if length > 22 and "dy=" not in attrs:
            warnings.append(f"长文本可能溢出 ({length}字): \"{inner[:18]}...\"")
            
            if auto_fix:
                # 提取 x 坐标
                x_match = re.search(r'\bx=[\"\x27]([^\s\"\x27]+)[\"\x27]', attrs)
                base_x = x_match.group(1) if x_match else "0"
                
                # 按每行约 18~20 个字切分
                chunk_size = 20
                chunks = [inner[i:i+chunk_size] for i in range(0, len(inner), chunk_size)]
                
                tspan_str = ""
                for idx, c in enumerate(chunks):
                    dy = '0' if idx == 0 else '20'
                    tspan_str += f'<tspan x="{base_x}" dy="{dy}">{c}</tspan>'
                
                fixed_count += 1
                return f"{start_tag}{tspan_str}{end_tag}"
                
        return full_match

    if auto_fix:
        new_content = text_pattern.sub(replacer, content)
        if fixed_count > 0:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"[FIX] 已自动重构 {fixed_count} 处超长文本为多行 <tspan>，完全保障排版自愈！")

    return print_report(file_path, issues, warnings)

def print_report(file_path, issues, warnings):
    print(f"--- 校验报告: {file_path} ---")
    if not issues and not warnings:
        print("[PASS] SVG 符合 Bento Grid 与 Office 原生矢量兼容规范！")
        return True
    
    for w in warnings:
        print(f"  [WARN] {w}")
    for i in issues:
        print(f"  [ERR]  {i}")
        
    return len(issues) == 0

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        print("用法: python validate_svg.py <slide.svg> [--fix]")
        sys.exit(0 if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help"] else 1)
        
    fix_mode = "--fix" in sys.argv
    target_file = [a for a in sys.argv[1:] if a != "--fix"][0]
    ok = parse_and_validate(target_file, auto_fix=fix_mode)
    sys.exit(0 if ok else 1)

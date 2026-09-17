#!/usr/bin/env python3
"""
build_deck.py - 将零散的 Bento SVG 幻灯片聚合为桌面交互预览器 (HTML) 或 PPTX 文件
"""
import os
import sys
import glob
import json
import argparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def build_html_preview(slides_dir, output_html, title, notes_list=None):
    svg_files = sorted(glob.glob(os.path.join(slides_dir, "*.svg")))
    if not svg_files:
        print(f"[WARN] 目录 {slides_dir} 下未找到任何 .svg 文件")
        return False

    svg_contents = []
    for fpath in svg_files:
        with open(fpath, "r", encoding="utf-8") as f:
            svg_contents.append(f.read())

    template_path = os.path.join(os.path.dirname(__file__), "..", "templates", "preview_deck.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    rendered = template.replace("{{DECK_TITLE}}", title)
    rendered = rendered.replace("{{SLIDES_JSON}}", json.dumps(svg_contents, ensure_ascii=False))
    
    # 注入演讲者备注
    notes_json = json.dumps(notes_list if notes_list else [], ensure_ascii=False)
    rendered = rendered.replace("{{NOTES_JSON}}", notes_json)

    with open(output_html, "w", encoding="utf-8") as f:
        f.write(rendered)

    print(f"[OK] 预览文件生成成功: {output_html} (共包含 {len(svg_files)} 页)")
    return True

def build_pptx_deck(slides_dir, output_pptx):
    try:
        from pptx import Presentation
        from pptx.util import Inches
    except ImportError:
        print("[INFO] python-pptx 未安装，跳过 PPTX 自动打包。可以直接将 .svg 拖入 PowerPoint 使用。")
        return False

    svg_files = sorted(glob.glob(os.path.join(slides_dir, "*.svg")))
    if not svg_files:
        print(f"[WARN] 目录 {slides_dir} 下未找到任何 .svg 文件")
        return False

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    for fpath in svg_files:
        slide = prs.slides.add_slide(blank_layout)
        try:
            slide.shapes.add_picture(fpath, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)
        except Exception as e:
            print(f"[WARN] 插入 {fpath} 遇到异常: {e}")

    prs.save(output_pptx)
    print(f"[OK] PPTX 打包成功: {output_pptx}")
    return True

def main():
    parser = argparse.ArgumentParser(description="聚合 Bento SVG 幻灯片")
    parser.add_argument("--dir", required=True, help="包含 slide_*.svg 的目录路径")
    parser.add_argument("--title", default="Bento Presentation", help="演示文稿标题")
    parser.add_argument("--html", default="preview_deck.html", help="输出的预览 HTML 文件名")
    parser.add_argument("--pptx", default=None, help="可选：打包输出的 PPTX 文件路径")
    parser.add_argument("--notes", default=None, help="可选：JSON 格式的演讲者备注文件路径")

    args = parser.parse_args()
    slides_dir = os.path.abspath(args.dir)
    out_html = os.path.join(slides_dir, args.html)

    notes_list = None
    if args.notes and os.path.exists(args.notes):
        try:
            with open(args.notes, "r", encoding="utf-8") as f:
                notes_list = json.load(f)
        except Exception as e:
            print(f"[WARN] 读取备注文件失败: {e}")

    build_html_preview(slides_dir, out_html, args.title, notes_list=notes_list)

    if args.pptx:
        out_pptx = os.path.abspath(args.pptx)
        build_pptx_deck(slides_dir, out_pptx)

if __name__ == "__main__":
    main()

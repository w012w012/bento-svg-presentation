#!/usr/bin/env python3
"""
build_deck.py - 将零散的 Bento SVG 幻灯片聚合为桌面交互预览器 (HTML) 与原生矢量 PPTX 文件
功能：
1. 聚合 slide_*.svg 生成单文件全屏交互播放器 (preview_deck.html)；
2. 打包生成原生矢量 PPTX 演示文稿 (presentation.pptx)：
   - 双重架构：内嵌高清 1080P 预览图与原生 image/svg+xml 矢量数据；
   - 注入 asvg:svgBlip 扩展标签，支持 Office 2016+ / 365 鼠标右键“转换为形状”打散二次编辑。
"""
import os
import sys
import glob
import json
import io
import argparse

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def render_svg_to_png(svg_path):
    """尝试将 SVG 渲染为 1920x1080 高清 PNG 兜底预览。支持 Playwright、CairoSVG 或 PIL 降级"""
    # 1. 优先尝试 Playwright (Chromium 引擎，渲染效果 100% 像素级保真)
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page(viewport={'width': 1920, 'height': 1080})
            url = 'file:///' + os.path.abspath(svg_path).replace('\\', '/')
            page.goto(url)
            screenshot_bytes = page.screenshot()
            browser.close()
            if screenshot_bytes:
                return screenshot_bytes
    except Exception:
        pass

    # 2. 尝试 CairoSVG
    try:
        import cairosvg
        png_data = cairosvg.svg2png(url=svg_path, output_width=1920, output_height=1080)
        if png_data:
            return png_data
    except Exception:
        pass

    # 3. 兜底方案：使用 Pillow 生成深色高质量占位图（确保 PPTX 结构合法且 Office 正常打开）
    try:
        from PIL import Image
        buf = io.BytesIO()
        Image.new('RGB', (1920, 1080), (8, 12, 20)).save(buf, format='PNG')
        return buf.getvalue()
    except Exception:
        return b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15c4\x00\x00\x00\rIDATx\x9cc\xf8\xff\xff?\x00\x05\xfe\x02\xfe\r\xef\x8f\xa7\x00\x00\x00\x00IEND\xaeB`\x82'

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
        from pptx.oxml import parse_xml
        from pptx.opc.package import Part
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

    print(f"[INFO] 正在将 {len(svg_files)} 页 SVG 打包嵌入原生矢量 PPTX...")

    for fpath in svg_files:
        slide = prs.slides.add_slide(blank_layout)
        try:
            # 1. 渲染或获取 1080P 预览 PNG
            png_bytes = render_svg_to_png(fpath)
            png_buf = io.BytesIO(png_bytes)

            # 2. 插入图像形状作为基底
            pic = slide.shapes.add_picture(png_buf, Inches(0), Inches(0), width=prs.slide_width, height=prs.slide_height)

            # 3. 读取原始 SVG 并作为原生矢量资源嵌入 PPTX OpenXML 包体
            with open(fpath, "rb") as f:
                svg_data = f.read()

            svg_partname = prs.part.package.next_image_partname('svg')
            svg_part = Part(svg_partname, 'image/svg+xml', prs.part.package, svg_data)
            rId_svg = slide.part.relate_to(svg_part, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/image')

            # 4. 注入 asvg:svgBlip 扩展标签（Office 2016+ / 365 识别原生矢量与右键打散的核心）
            blip = pic._element.blipFill.blip
            extLst_xml = f'''<a:extLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <a:ext uri="{{96DAC542-7B16-43E4-950E-E5F64E334241}}">
    <asvg:svgBlip xmlns:asvg="http://schemas.microsoft.com/office/drawing/2016/SVG/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" r:embed="{rId_svg}"/>
  </a:ext>
</a:extLst>'''
            blip.append(parse_xml(extLst_xml))

        except Exception as e:
            print(f"[WARN] 嵌入 {fpath} 遇到异常: {e}")

    prs.save(output_pptx)
    print(f"[OK] PPTX 演示文稿生成成功: {output_pptx} (支持 Office 2016+ 右键转换为形状无损打散编辑)")
    return True

def main():
    parser = argparse.ArgumentParser(description="聚合 Bento SVG 幻灯片为 HTML 交互播放器与 PPTX 文件")
    parser.add_argument("--dir", required=True, help="包含 slide_*.svg 的目录路径")
    parser.add_argument("--title", default="Bento Presentation", help="演示文稿标题")
    parser.add_argument("--html", default="preview_deck.html", help="输出的预览 HTML 文件名")
    parser.add_argument("--pptx", default=None, help="可选：指定输出的 PPTX 文件路径（默认自动生成 presentation.pptx）")
    parser.add_argument("--no-pptx", action="store_true", help="显式指定跳过生成 PPTX")
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

    # 1. 生成 HTML 预览器
    build_html_preview(slides_dir, out_html, args.title, notes_list=notes_list)

    # 2. 默认生成 PPTX 演示文稿（除非指定 --no-pptx）
    if not args.no_pptx:
        out_pptx = os.path.abspath(args.pptx) if args.pptx else os.path.join(slides_dir, "presentation.pptx")
        build_pptx_deck(slides_dir, out_pptx)

if __name__ == "__main__":
    main()

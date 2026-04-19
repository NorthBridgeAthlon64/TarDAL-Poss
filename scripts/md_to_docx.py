# -*- coding: utf-8 -*-
"""将项目根目录下的 Markdown 转为 Word（.docx）。依赖：pip install markdown html2docx"""
import sys
from pathlib import Path

import markdown
from html2docx import html2docx


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    md_name = "主要测试-过程结果与技术指标.md"
    md_path = root / md_name
    if not md_path.is_file():
        print("找不到:", md_path, file=sys.stderr)
        return 1
    text = md_path.read_text(encoding="utf-8")
    html = markdown.markdown(
        text,
        extensions=["tables", "nl2br", "sane_lists"],
    )
    title = "主要测试：过程、结果与技术指标"
    buf = html2docx(html, title)
    out_path = md_path.with_suffix(".docx")
    out_path.write_bytes(buf.getvalue())
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

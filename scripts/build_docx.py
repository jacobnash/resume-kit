#!/usr/bin/env python3
"""
build_docx.py - the same resume/cover letter as a plain, ATS-friendly Word file.

    python3 scripts/build_docx.py my-career/output/core/resume.md
    python3 scripts/build_docx.py resume.md --paper a4

Some application forms ask for .docx, and some ATS parsers read Word more
reliably than PDF. Single column, real headings, standard fonts, dates on the
right using a tab stop (not a table). Paper size follows my-career/profile.md.
"""

import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mdlite  # noqa: E402
from build_pdf import PAPERS, guess_kind, pip_install, profile_settings  # noqa: E402

ACCENT = {"modern": "1F4E79", "classic": "111111", "minimal": "444444", "warm": "B5592C"}
FONT = {"modern": "Calibri", "classic": "Georgia", "minimal": "Calibri", "warm": "Calibri"}


def _docx():
    try:
        import docx  # noqa: F401
    except ImportError:
        pip_install("python-docx")
    import docx
    return docx


def _bottom_border(paragraph, color):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    ppr = paragraph._p.get_or_add_pPr()
    bdr = OxmlElement("w:pBdr")
    b = OxmlElement("w:bottom")
    b.set(qn("w:val"), "single")
    b.set(qn("w:sz"), "6")
    b.set(qn("w:space"), "1")
    b.set(qn("w:color"), color)
    bdr.append(b)
    ppr.append(bdr)


def _hyperlink(paragraph, url, text, size, font):
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    r_id = paragraph.part.relate_to(
        url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink",
        is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = OxmlElement("w:r")
    rpr = OxmlElement("w:rPr")
    sz = OxmlElement("w:sz")
    sz.set(qn("w:val"), str(int(size * 2)))
    rpr.append(sz)
    rf = OxmlElement("w:rFonts")
    rf.set(qn("w:ascii"), font)
    rf.set(qn("w:hAnsi"), font)
    rpr.append(rf)
    run.append(rpr)
    t = OxmlElement("w:t")
    t.text = text
    t.set(qn("xml:space"), "preserve")
    run.append(t)
    link.append(run)
    paragraph._p.append(link)


def _runs(paragraph, text, size, font, color=None, italic=False, bold=False):
    from docx.shared import Pt, RGBColor
    lines = text.split("\n")
    for n, line in enumerate(lines):
        for t, st in mdlite.spans(line):
            if st.get("link") and not st["link"].startswith("mailto:"):
                _hyperlink(paragraph, st["link"], t, size, font)
                continue
            r = paragraph.add_run(t)
            r.font.size = Pt(size)
            r.font.name = font
            r.bold = bold or bool(st.get("bold"))
            r.italic = italic or bool(st.get("italic"))
            if color:
                r.font.color.rgb = RGBColor.from_string(color)
        if n < len(lines) - 1:
            paragraph.add_run().add_break()


def build(md_path, theme=None, paper=None, out=None):
    docx = _docx()
    from docx.enum.text import WD_TAB_ALIGNMENT
    from docx.shared import Inches, Pt, RGBColor

    md_path = os.path.abspath(md_path)
    with open(md_path, encoding="utf-8") as f:
        blocks = mdlite.parse(f.read())
    prefs = profile_settings(md_path)
    theme = theme or prefs.get("theme") or "modern"
    paper = (paper or prefs.get("paper") or "letter").lower()
    kind = guess_kind(md_path)
    accent, font = ACCENT.get(theme, "1F4E79"), FONT.get(theme, "Calibri")
    base = 10.5

    d = docx.Document()
    sec = d.sections[0]
    _, w_pt, h_pt = PAPERS[paper]
    sec.page_width, sec.page_height = Pt(w_pt), Pt(h_pt)
    sec.left_margin = sec.right_margin = Inches(0.75)
    sec.top_margin = sec.bottom_margin = Inches(0.6)
    text_width = sec.page_width - sec.left_margin - sec.right_margin

    normal = d.styles["Normal"]
    normal.font.name = font
    normal.font.size = Pt(base)
    normal.paragraph_format.space_after = Pt(2)
    normal.paragraph_format.space_before = Pt(0)

    title = mdlite.title_of(blocks)
    d.core_properties.title = title
    d.core_properties.author = title

    in_header, prev = False, None
    for k, payload in blocks:
        if k == "h1":
            p = d.add_paragraph()
            _runs(p, payload, base * 2, font, bold=True)
            p.paragraph_format.space_after = Pt(2)
            in_header = True
        elif k == "p":
            p = d.add_paragraph()
            if in_header:
                _runs(p, payload, base * 0.9, font, color="555555")
            elif prev == "h3":
                _runs(p, payload, base, font, color="555555", italic=True)
            else:
                _runs(p, payload, base, font)
                if kind == "letter":
                    p.paragraph_format.space_after = Pt(9)
        elif k == "h2":
            if in_header and d.paragraphs:
                d.paragraphs[-1].paragraph_format.space_after = Pt(6)
            in_header = False
            # a real Heading style, so parsers can find sections
            p = d.add_heading(level=1)
            r = p.add_run(mdlite.plain(payload).upper() if theme != "warm" else mdlite.plain(payload))
            r.font.size = Pt(base * 1.1)
            r.font.name = font
            r.font.bold = True
            r.font.italic = theme == "warm"
            r.font.color.rgb = RGBColor.from_string(accent)
            p.paragraph_format.space_before = Pt(10)
            p.paragraph_format.space_after = Pt(3)
            p.paragraph_format.keep_with_next = True
            _bottom_border(p, "BBBBBB")
        elif k == "h3":
            in_header = False
            left, right = payload
            p = d.add_paragraph()
            p.paragraph_format.space_before = Pt(5)
            p.paragraph_format.keep_with_next = True
            _runs(p, left, base, font, bold=True)
            if right:
                p.paragraph_format.tab_stops.add_tab_stop(text_width, WD_TAB_ALIGNMENT.RIGHT)
                p.add_run("\t")
                _runs(p, right, base, font, color="555555")
        elif k == "ul":
            in_header = False
            for item in payload:
                p = d.add_paragraph(style="List Bullet")
                p.paragraph_format.space_after = Pt(1)
                _runs(p, item, base, font)
        elif k == "hr":
            p = d.add_paragraph()
            _bottom_border(p, "CCCCCC")
        elif k == "pagebreak":
            d.add_page_break()
        prev = k

    out = out or os.path.splitext(md_path)[0] + ".docx"
    d.save(out)
    return out


def main():
    ap = argparse.ArgumentParser(description="Markdown resume / cover letter -> .docx")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--theme", choices=list(ACCENT))
    ap.add_argument("--paper", choices=list(PAPERS))
    a = ap.parse_args()
    status = 0
    for md in a.files:
        if not os.path.isfile(md):
            print(f"NOT FOUND  {md}")
            status = 1
            continue
        try:
            print(f"OK        {build(md, a.theme, a.paper)}")
        except Exception as e:  # noqa: BLE001
            print(f"FAILED     {md}\n  {e}")
            status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())

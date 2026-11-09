"""
pdf_reportlab.py - last-resort PDF renderer for build_pdf.py.

Used only when no browser engine is available. Pure Python (ReportLab), so it
works in bare sandboxes. Visually simpler than the browser themes, but keeps
the same structure: one column, real selectable text, standard headings.
"""

import html

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4, LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (HRFlowable, KeepTogether, ListFlowable, ListItem, PageBreak,
                                Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

import mdlite

THEME = {
    "modern": {"body": "Helvetica", "bold": "Helvetica-Bold", "ital": "Helvetica-Oblique",
               "head": "Helvetica-Bold", "accent": "#1f4e79", "muted": "#57606a", "upper": True},
    "classic": {"body": "Times-Roman", "bold": "Times-Bold", "ital": "Times-Italic",
                "head": "Times-Bold", "accent": "#111111", "muted": "#444444", "upper": True},
    "minimal": {"body": "Helvetica", "bold": "Helvetica-Bold", "ital": "Helvetica-Oblique",
                "head": "Helvetica-Bold", "accent": "#555555", "muted": "#666666", "upper": True},
    "warm": {"body": "Helvetica", "bold": "Helvetica-Bold", "ital": "Helvetica-Oblique",
             "head": "Times-Italic", "accent": "#b5592c", "muted": "#6b625a", "upper": False},
}

# core PDF fonts only cover Latin-1; map common typography to safe equivalents
_SAFE = {"—": "-", "–": "–", "‘": "'", "’": "'", "“": '"',
         "”": '"', "•": "•", " ": " ", "→": "->"}


def _safe(t):
    out = []
    for ch in t:
        ch = _SAFE.get(ch, ch)
        try:
            ch.encode("cp1252")
            out.append(ch)
        except UnicodeEncodeError:
            out.append("?")
    return "".join(out)


def _rl(text, th):
    if "\n" in text:
        return "<br/>".join(_rl(t, th) for t in text.split("\n"))
    parts = []
    for t, st in mdlite.spans(text):
        h = html.escape(_safe(t))
        if st.get("italic"):
            h = f'<font name="{th["ital"]}">{h}</font>'
        if st.get("bold"):
            h = f'<font name="{th["bold"]}">{h}</font>'
        if st.get("link"):
            h = f'<link href="{html.escape(st["link"], quote=True)}">{h}</link>'
        parts.append(h)
    return "".join(parts)


def render(blocks, pdf_path, theme="modern", paper="letter", size_pt=10.0, kind="resume"):
    th = THEME.get(theme, THEME["modern"])
    accent = colors.HexColor(th["accent"])
    muted = colors.HexColor(th["muted"])
    s = size_pt
    lead = s * (1.5 if kind == "letter" else 1.35)
    body = ParagraphStyle("body", fontName=th["body"], fontSize=s, leading=lead, alignment=TA_LEFT,
                          spaceAfter=s * (0.8 if kind == "letter" else 0.15))
    name = ParagraphStyle("name", parent=body, fontName=th["bold"], fontSize=s * 2, leading=s * 2.3,
                          spaceAfter=s * 0.2)
    contact = ParagraphStyle("contact", parent=body, fontSize=s * 0.9, textColor=muted, spaceAfter=0)
    h2 = ParagraphStyle("h2", parent=body, fontName=th["head"], fontSize=s * 1.05, textColor=accent,
                        spaceBefore=s * 0.9, spaceAfter=s * 0.1)
    h3 = ParagraphStyle("h3", parent=body, fontName=th["bold"], spaceBefore=s * 0.5, spaceAfter=0)
    h3r = ParagraphStyle("h3r", parent=body, textColor=muted, alignment=2)
    meta = ParagraphStyle("meta", parent=body, fontName=th["ital"], textColor=muted)
    bullet = ParagraphStyle("bullet", parent=body, spaceAfter=s * 0.1)

    pagesize = LETTER if paper == "letter" else A4
    margin = 0.6 * inch if s >= 9.7 else 0.5 * inch
    doc = SimpleDocTemplate(pdf_path, pagesize=pagesize, leftMargin=margin + 0.1 * inch,
                            rightMargin=margin + 0.1 * inch, topMargin=margin, bottomMargin=margin,
                            title=mdlite.title_of(blocks), author=mdlite.title_of(blocks))
    width = pagesize[0] - 2 * (margin + 0.1 * inch)

    story = []
    in_header = False
    prev = None
    for k, payload in blocks:
        if k == "h1":
            story.append(Paragraph(_rl(payload, th), name))
            story.append(HRFlowable(width="100%", thickness=1.2, color=accent, spaceAfter=s * 0.3))
            in_header = True
        elif k == "p":
            st = contact if in_header else (meta if prev == "h3" else body)
            story.append(Paragraph(_rl(payload, th), st))
        elif k == "h2":
            if in_header:
                story.append(Spacer(1, s * 0.4))
            in_header = False
            text = _safe(mdlite.plain(payload))
            text = text.upper() if th["upper"] else text
            story.append(KeepTogether([Paragraph(html.escape(text), h2),
                                       HRFlowable(width="100%", thickness=0.5,
                                                  color=colors.HexColor("#c9c9cf"),
                                                  spaceAfter=s * 0.25)]))
        elif k == "h3":
            in_header = False
            left, right = payload
            if right:
                t = Table([[Paragraph(_rl(left, th), h3),
                            Paragraph(html.escape(_safe(mdlite.plain(right))), h3r)]],
                          colWidths=[width * 0.72, width * 0.28])
                t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                                       ("LEFTPADDING", (0, 0), (-1, -1), 0),
                                       ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                                       ("TOPPADDING", (0, 0), (-1, -1), 0),
                                       ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
                story.append(t)
            else:
                story.append(Paragraph(_rl(left, th), h3))
        elif k == "ul":
            in_header = False
            items = [ListItem(Paragraph(_rl(i, th), bullet), leftIndent=s * 1.2) for i in payload]
            story.append(ListFlowable(items, bulletType="bullet", start="•",
                                      leftIndent=s * 1.2, bulletFontSize=s * 0.8))
        elif k == "hr":
            story.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#c9c9cf")))
        elif k == "pagebreak":
            story.append(PageBreak())
        prev = k
    doc.build(story)

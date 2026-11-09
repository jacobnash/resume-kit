"""
mdlite.py - the tiny Markdown dialect resume-kit documents are written in.

Deliberately small and dependency-free so it runs anywhere Python 3.8+ runs
(a stranger's Mac, the Cowork sandbox) without installing anything.

Supported:
  # Name                         -> document title (the person's name)
  ## Section                     -> section heading (Experience, Education, ...)
  ### Left part | Right part     -> entry heading; the last " | " segment is shown
                                    right-aligned (usually dates)
  plain lines                    -> paragraphs; a single line break is kept as a
                                    line break (handy for Skills and contact lines)
  - item / * item                -> bullet list
  ---                            -> thin rule
  <!--pagebreak-->               -> page break
  **bold**  *italic*  [text](url)  `code`

Everything renders from one block list, so the PDF, the DOCX and the ATS
checker all agree on what the document says.
"""

import html
import re

PAGEBREAK = "<!--pagebreak-->"


def parse(md: str):
    """Return a list of blocks: (kind, payload).

    kinds: h1, h2, h3, p, ul, hr, pagebreak
    h3 payload is (left, right_or_None); ul payload is a list of strings.
    """
    blocks = []
    para = []
    items = None

    def flush():
        nonlocal para, items
        if para:
            blocks.append(("p", "\n".join(s.strip() for s in para)))
            para = []
        if items is not None:
            blocks.append(("ul", items))
            items = None

    for raw in md.replace("\r\n", "\n").split("\n"):
        line = raw.rstrip()
        s = line.strip()

        # strip HTML comments other than the page-break marker
        if s.startswith("<!--") and s.endswith("-->") and s != PAGEBREAK:
            continue
        if s == PAGEBREAK:
            flush()
            blocks.append(("pagebreak", None))
            continue
        if re.fullmatch(r"-{3,}|\*{3,}|_{3,}", s):
            flush()
            blocks.append(("hr", None))
            continue
        m = re.match(r"^(#{1,3})\s+(.*)$", s)
        if m:
            flush()
            level = len(m.group(1))
            text = m.group(2).strip()
            if level == 3:
                parts = [p.strip() for p in text.split(" | ")]
                if len(parts) > 1:
                    blocks.append(("h3", (" | ".join(parts[:-1]), parts[-1])))
                else:
                    blocks.append(("h3", (text, None)))
            else:
                blocks.append((f"h{level}", text))
            continue
        m = re.match(r"^[-*+]\s+(.*)$", s)
        if m and not s.startswith("**"):
            if para:
                blocks.append(("p", "\n".join(x.strip() for x in para)))
                para = []
            if items is None:
                items = []
            items.append(m.group(1).strip())
            continue
        if s == "":
            flush()
            continue
        # continuation of a bullet (indented line right after an item)
        if items is not None and raw.startswith(("  ", "\t")):
            items[-1] += " " + s
            continue
        if items is not None:
            flush()
        para.append(s)
    flush()
    return blocks


# ---------------------------------------------------------------- inline ---

_INLINE = re.compile(
    r"\*\*(?P<b>.+?)\*\*"
    r"|(?<![\w*])\*(?P<i>[^*\s][^*]*?)\*(?![\w*])"
    r"|\[(?P<lt>[^\]]+)\]\((?P<lu>[^)\s]+)\)"
    r"|`(?P<c>[^`]+)`"
    r"|(?P<url>(?:https?://|mailto:)[^\s)|]+)"
)


def spans(text: str):
    """Split inline markdown into (text, style) runs.

    style is a dict with optional keys: bold, italic, link, code.
    Nested bold-inside-link etc. is intentionally not supported.
    """
    out = []
    pos = 0
    for m in _INLINE.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], {}))
        if m.group("b") is not None:
            for t, st in spans(m.group("b")):
                out.append((t, {**st, "bold": True}))
        elif m.group("i") is not None:
            out.append((m.group("i"), {"italic": True}))
        elif m.group("lt") is not None:
            out.append((m.group("lt"), {"link": m.group("lu")}))
        elif m.group("c") is not None:
            out.append((m.group("c"), {"code": True}))
        else:
            out.append((m.group("url"), {"link": m.group("url")}))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], {}))
    return out


def plain(text: str) -> str:
    """Inline markdown -> the plain text a reader (or an ATS) sees."""
    return "".join(t for t, _ in spans(text))


def inline_html(text: str) -> str:
    if "\n" in text:
        return "<br>".join(inline_html(t) for t in text.split("\n"))
    parts = []
    for t, st in spans(text):
        h = html.escape(t)
        if st.get("code"):
            h = f"<code>{h}</code>"
        if st.get("italic"):
            h = f"<em>{h}</em>"
        if st.get("bold"):
            h = f"<strong>{h}</strong>"
        if st.get("link"):
            h = f'<a href="{html.escape(st["link"], quote=True)}">{h}</a>'
        parts.append(h)
    return "".join(parts)


# ------------------------------------------------------------------ html ---

def to_html_body(blocks) -> str:
    out = []
    in_header = False  # contact lines right after the name
    for kind, payload in blocks:
        if kind == "h1":
            out.append('<header class="masthead">')
            out.append(f"<h1>{inline_html(payload)}</h1>")
            in_header = True
            continue
        if in_header and kind != "p":
            out.append("</header>")
            in_header = False
        if kind == "p":
            cls = ' class="contact"' if in_header else ""
            out.append(f"<p{cls}>{inline_html(payload)}</p>")
        elif kind == "h2":
            out.append(f"<h2>{inline_html(payload)}</h2>")
        elif kind == "h3":
            left, right = payload
            if right:
                out.append(
                    f'<h3><span class="what">{inline_html(left)}</span>'
                    f' <span class="sep">|</span> '
                    f'<span class="when">{inline_html(right)}</span></h3>'
                )
            else:
                out.append(f'<h3><span class="what">{inline_html(left)}</span></h3>')
        elif kind == "ul":
            lis = "".join(f"<li>{inline_html(i)}</li>" for i in payload)
            out.append(f"<ul>{lis}</ul>")
        elif kind == "hr":
            out.append("<hr>")
        elif kind == "pagebreak":
            out.append('<div class="page-break"></div>')
    if in_header:
        out.append("</header>")
    return "\n".join(out)


def title_of(blocks, fallback="Resume") -> str:
    for kind, payload in blocks:
        if kind == "h1":
            return plain(payload)
    return fallback


def plain_lines(blocks):
    """Every visible line of text, in reading order (used by the ATS check)."""
    lines = []
    for kind, payload in blocks:
        if kind in ("h1", "h2"):
            lines.append(plain(payload))
        elif kind == "p":
            lines.extend(plain(t) for t in payload.split("\n"))
        elif kind == "h3":
            left, right = payload
            lines.append(plain(left))
            if right:
                lines.append(plain(right))
        elif kind == "ul":
            lines.extend(plain(i) for i in payload)
    return [l for l in lines if l.strip()]

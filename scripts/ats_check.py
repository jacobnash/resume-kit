#!/usr/bin/env python3
"""
ats_check.py - read a resume PDF back the way an applicant tracking system (ATS) does,
and report anything that could get it mangled or filtered out.

    python3 scripts/ats_check.py my-career/output/core/resume.pdf
    python3 scripts/ats_check.py resume.pdf --md resume.md --keywords my-career/targets/positioning.md

If --md is not given, the .md next to the PDF is used. If --keywords is not given,
the nearest my-career/targets/positioning.md is used (if there is one).

Writes <name>-ats-report.md next to the PDF and prints a plain-language summary.
Exit code: 0 = pass (warnings allowed), 1 = something failed.

Keyword list format (in positioning.md), any bullets under these headings:
    ## ATS keywords
    ### Must have
    - SQL
    - stakeholder management / stakeholder communication     <- " / " separates synonyms
    ### Nice to have
    - Looker
"""

import argparse
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mdlite  # noqa: E402

STANDARD_HEADINGS = {
    "summary", "professional summary", "profile", "professional profile", "about", "objective",
    "experience", "work experience", "professional experience", "employment", "employment history",
    "work history", "relevant experience", "career history", "additional experience",
    "education", "education and training", "education & training",
    "skills", "technical skills", "core skills", "key skills", "skills and tools", "skills & tools",
    "core competencies", "competencies", "areas of expertise",
    "certifications", "certificates", "licenses", "licenses and certifications",
    "licenses & certifications", "certifications and licenses", "certifications & licenses",
    "projects", "selected projects", "key projects", "publications", "patents", "awards",
    "honors", "awards and honors", "honors and awards", "awards & honors", "achievements",
    "volunteer experience", "volunteering", "volunteer work", "community involvement",
    "leadership", "leadership experience", "languages", "interests", "training",
    "professional development", "affiliations", "professional affiliations", "memberships",
    "speaking", "research", "teaching", "portfolio", "military service", "references",
}

ODD_CHARS = {
    "ﬀ": "ff ligature", "ﬁ": "fi ligature", "ﬂ": "fl ligature",
    "ﬃ": "ffi ligature", "ﬄ": "ffl ligature", "�": "unreadable character",
}

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
PHONE = re.compile(r"(?:\+?\d{1,3}[\s.-]?)?(?:\(\d{2,4}\)|\d{2,4})[\s.-]?\d{3,4}[\s.-]?\d{3,4}")

DATE_STYLES = [
    ("Mon YYYY", re.compile(r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)\.? \d{4}\b")),
    ("Month YYYY", re.compile(r"\b(?:January|February|March|April|June|July|August|September|"
                              r"October|November|December) \d{4}\b")),
    ("MM/YYYY", re.compile(r"\b(?:0?[1-9]|1[0-2])/\d{4}\b")),
    ("YYYY-MM", re.compile(r"\b\d{4}-(?:0[1-9]|1[0-2])\b")),
]


def norm(s):
    s = unicodedata.normalize("NFKC", s).lower()
    s = s.replace("–", "-").replace("—", "-").replace("’", "'")
    return re.sub(r"\s+", " ", s).strip()


def extract(pdf_path):
    try:
        from pypdf import PdfReader
    except ImportError:
        sys.path.insert(0, HERE)
        from build_pdf import pip_install
        pip_install("pypdf")
        from pypdf import PdfReader
    r = PdfReader(pdf_path)
    pages = [(p.extract_text() or "") for p in r.pages]
    return pages


def find_upward(start, rel):
    d = os.path.abspath(start)
    for _ in range(8):
        cand = os.path.join(d, rel)
        if os.path.isfile(cand):
            return cand
        parent = os.path.dirname(d)
        if parent == d:
            return None
        d = parent
    return None


def load_keywords(path):
    """Return {"must": [[syn, syn], ...], "nice": [...]}."""
    out = {"must": [], "nice": []}
    if not path or not os.path.isfile(path):
        return out
    with open(path, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"(?ims)^##\s+ATS keywords.*?$(.*?)(?=^##\s|\Z)", text)
    if not m:
        return out
    bucket = "must"
    for line in m.group(1).splitlines():
        s = line.strip()
        if s.startswith("###"):
            bucket = "nice" if re.search(r"nice|bonus|plus|optional", s, re.I) else "must"
            continue
        mm = re.match(r"^[-*]\s+(.*)", s)
        if mm:
            term = re.sub(r"\(.*?\)|\*|`", "", mm.group(1)).strip()
            term = term.split(" - ")[0].split(" — ")[0]
            syns = [t.strip() for t in term.split(" / ") if t.strip()]
            if syns:
                out[bucket].append(syns)
    return out


def has_term(text_norm, term):
    t = norm(term)
    pattern = r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])"
    return re.search(pattern, text_norm) is not None


def check(pdf_path, md_path=None, kw_path=None, max_pages=None, kind=None):
    results = []  # (level, title, detail)

    def add(level, title, detail=""):
        results.append((level, title, detail))

    pages = extract(pdf_path)
    full = "\n".join(pages)
    full_n = norm(full)
    if kind is None:
        kind = "letter" if re.search(r"cover|letter", os.path.basename(pdf_path), re.I) else "resume"
    if max_pages is None:
        max_pages = 1 if kind == "letter" else 2

    # 1. text is real text
    if len(full.strip()) < 200:
        add("FAIL", "Text can't be read",
            "Almost no text came out of the PDF. It may be an image or scan; an ATS would see a blank page.")
        return results, {"pages": len(pages)}
    add("PASS", "Text is selectable", f"{len(full.split())} words extracted.")

    # 2. page count
    if len(pages) > max_pages:
        add("FAIL", "Too long", f"{len(pages)} pages; the limit for this document is {max_pages}.")
    else:
        add("PASS", "Length", f"{len(pages)} page(s), limit {max_pages}.")

    # 3. contact details on page 1
    p1 = pages[0]
    email = EMAIL.search(p1)
    phone = PHONE.search(p1)
    if email and phone:
        add("PASS", "Contact details on page 1", f"{email.group(0)}, {phone.group(0).strip()}")
    elif kind == "resume":
        missing = [n for n, ok in (("email", email), ("phone", phone)) if not ok]
        add("WARN" if email else "FAIL", "Contact details",
            "Missing on page 1 as plain text: " + ", ".join(missing) + ".")

    # 4. odd characters
    odd = sorted({ODD_CHARS.get(c, f"U+{ord(c):04X}") for c in full
                  if c in ODD_CHARS or 0xE000 <= ord(c) <= 0xF8FF})
    if odd:
        add("WARN", "Unusual characters", "These can scramble in some systems: " + ", ".join(odd))
    else:
        add("PASS", "No unusual characters")

    blocks = None
    if md_path and os.path.isfile(md_path):
        with open(md_path, encoding="utf-8") as f:
            blocks = mdlite.parse(f.read())

    if blocks:
        # 5. name at the top
        name = mdlite.title_of(blocks, "")
        first = norm(" ".join(p1.strip().splitlines()[:3]))
        if name and norm(name) in first:
            add("PASS", "Name is first", name)
        elif name:
            add("WARN", "Name is not the first thing read",
                f"Expected '{name}' at the top of page 1.")

        # 6. headings
        if kind == "resume":
            heads = [mdlite.plain(p) for k, p in blocks if k == "h2"]
            odd_h = [h for h in heads if norm(h).rstrip(":") not in STANDARD_HEADINGS]
            if odd_h:
                add("WARN", "Non-standard section names",
                    "ATS software looks for familiar names (Experience, Education, Skills). "
                    "Consider renaming: " + ", ".join(f"'{h}'" for h in odd_h))
            elif heads:
                add("PASS", "Standard section names", ", ".join(heads))

        # 7. nothing lost, nothing out of order
        lines = mdlite.plain_lines(blocks)
        lost, disorder = [], 0
        cursor = 0
        flat = re.sub(r"\s+", "", full_n)
        for line in lines:
            probe = re.sub(r"\s+", "", norm(line))[:40]
            if len(probe) < 6:
                continue
            idx = flat.find(probe, cursor)
            if idx == -1:
                if flat.find(probe) == -1:
                    lost.append(line)
                else:
                    disorder += 1
            else:
                cursor = idx
        if lost:
            add("FAIL", "Text lost in the PDF",
                "These lines did not come through: " + "; ".join(f"'{l[:60]}'" for l in lost[:5]))
        else:
            add("PASS", "Every line came through")
        if disorder > 2:
            add("WARN", "Reading order", f"{disorder} lines were read out of order. "
                "Avoid side-by-side columns or text boxes.")
        elif not lost:
            add("PASS", "Reading order is top to bottom")

    # 8. date styles
    styles = [n for n, rx in DATE_STYLES if rx.search(full)]
    if len(styles) > 1:
        add("WARN", "Mixed date formats", "Pick one style. Found: " + ", ".join(styles))
    elif styles:
        add("PASS", "Consistent dates", styles[0])

    # 9. keywords
    kw = load_keywords(kw_path)
    stats = {"pages": len(pages)}
    if kw["must"] or kw["nice"]:
        def cover(group):
            hit, miss = [], []
            for syns in group:
                (hit if any(has_term(full_n, s) for s in syns) else miss).append(syns[0])
            return hit, miss
        mh, mm = cover(kw["must"])
        nh, nm = cover(kw["nice"])
        stats.update(must_hit=len(mh), must_total=len(kw["must"]), nice_hit=len(nh),
                     nice_total=len(kw["nice"]))
        if kw["must"]:
            pct = 100 * len(mh) // len(kw["must"])
            level = "PASS" if pct >= 80 else ("WARN" if pct >= 60 else "FAIL")
            detail = f"{len(mh)}/{len(kw['must'])} must-have terms found ({pct}%)."
            if mm:
                detail += " Missing: " + ", ".join(mm) + \
                    ". Add only the ones that are true for you, using the employer's wording."
            add(level, "Must-have keywords", detail)
        if kw["nice"]:
            detail = f"{len(nh)}/{len(kw['nice'])} found."
            if nm:
                detail += " Not found: " + ", ".join(nm) + "."
            add("PASS" if len(nh) * 2 >= len(kw["nice"]) else "WARN", "Nice-to-have keywords", detail)
    return results, stats


def report(pdf_path, results, kw_path):
    fails = [r for r in results if r[0] == "FAIL"]
    warns = [r for r in results if r[0] == "WARN"]
    if fails:
        verdict = f"Needs fixing: {len(fails)} problem(s) an ATS would trip on."
    elif warns:
        verdict = f"Good to go, with {len(warns)} thing(s) worth a look."
    else:
        verdict = "Clean. An ATS will read this exactly as written."
    icon = {"PASS": "PASS", "WARN": "WARN", "FAIL": "FAIL"}
    lines = [f"# ATS check: {os.path.basename(pdf_path)}", "", f"**{verdict}**", ""]
    if kw_path:
        lines += [f"Keywords from: `{os.path.relpath(kw_path, os.path.dirname(pdf_path))}`", ""]
    for level, title, detail in sorted(results, key=lambda r: ["FAIL", "WARN", "PASS"].index(r[0])):
        lines.append(f"- **{icon[level]}** {title}" + (f": {detail}" if detail else ""))
    return verdict, "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Check a resume PDF the way an ATS reads it")
    ap.add_argument("pdf")
    ap.add_argument("--md", help="source markdown (default: same name, .md)")
    ap.add_argument("--keywords", help="positioning.md with an '## ATS keywords' section")
    ap.add_argument("--max-pages", type=int)
    ap.add_argument("--kind", choices=["resume", "letter"])
    a = ap.parse_args()

    pdf = os.path.abspath(a.pdf)
    if not os.path.isfile(pdf):
        print(f"NOT FOUND  {pdf}")
        return 1
    md = a.md or os.path.splitext(pdf)[0] + ".md"
    kw = a.keywords or find_upward(os.path.dirname(pdf), os.path.join("targets", "positioning.md")) \
        or find_upward(os.path.dirname(pdf), os.path.join("my-career", "targets", "positioning.md"))
    results, _ = check(pdf, md if os.path.isfile(md) else None, kw, a.max_pages, a.kind)
    verdict, text = report(pdf, results, kw)
    out = os.path.splitext(pdf)[0] + "-ats-report.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write(text)
    print(text)
    print(f"(saved to {out})")
    return 1 if any(r[0] == "FAIL" for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())

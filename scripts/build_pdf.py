#!/usr/bin/env python3
"""
build_pdf.py - turn a resume or cover letter (.md) into a polished, ATS-safe PDF.

    python3 scripts/build_pdf.py my-career/output/acme-pm/resume.md
    python3 scripts/build_pdf.py resume.md cover-letter.md --theme warm --paper a4
    python3 scripts/build_pdf.py --doctor          # what can render PDFs on this machine?

Defaults come from my-career/profile.md when it exists ("Paper size:", "Theme:"),
otherwise US Letter + the "modern" theme. The PDF is written next to the .md.

Rendering, best first (the first that works wins):
  1. Chrome / Chromium / Edge / Brave already on the computer (headless print)
  2. Playwright for Python, if installed
  3. WeasyPrint, if installed
  4. ReportLab (pure Python; installed automatically if nothing else works)

If the document runs past its page limit (2 for resumes, 1 for cover letters)
the text is shrunk a little at a time, never below a readable size. If it
still doesn't fit, the script says so: the fix is to cut content, not font.
"""

import argparse
import glob
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import mdlite  # noqa: E402

THEMES_DIR = os.path.join(HERE, "themes")
THEMES = ["modern", "classic", "minimal", "warm"]
PAPERS = {"letter": ("Letter", 8.5 * 72, 11 * 72), "a4": ("A4", 595.28, 841.89)}

# body font sizes (pt) tried in order when shrinking to fit
SCALES = [10.0, 9.7, 9.4, 9.1]
LETTER_SCALES = [11.0, 10.5, 10.0]
MARGINS = {11.0: "0.9in 1in", 10.5: "0.8in 0.9in", 10.0: "0.6in 0.7in", 9.7: "0.55in 0.65in", 9.4: "0.5in 0.6in", 9.1: "0.45in 0.55in"}


def say(msg):
    print(msg, flush=True)


# ------------------------------------------------------------- settings ---

def find_profile(start):
    d = os.path.abspath(start)
    for _ in range(8):
        for cand in (os.path.join(d, "my-career", "profile.md"), os.path.join(d, "profile.md")):
            if os.path.isfile(cand):
                return cand
        parent = os.path.dirname(d)
        if parent == d:
            break
        d = parent
    return None


def profile_settings(md_path):
    prof = find_profile(os.path.dirname(md_path))
    out = {}
    if not prof:
        return out
    with open(prof, encoding="utf-8") as f:
        text = f.read()
    m = re.search(r"(?im)^\W*paper(?: size)?\W*:\s*\**\s*(letter|a4)", text)
    if m:
        out["paper"] = m.group(1).lower()
    m = re.search(r"(?im)^\W*(?:resume )?theme\W*:\s*\**\s*(" + "|".join(THEMES) + ")", text)
    if m:
        out["theme"] = m.group(1).lower()
    return out


def guess_kind(md_path):
    name = os.path.basename(md_path).lower()
    if "cover" in name or "letter" in name:
        return "letter"
    return "resume"


# ----------------------------------------------------------------- html ---

def read_css(theme):
    with open(os.path.join(THEMES_DIR, "base.css"), encoding="utf-8") as f:
        base = f.read()
    path = os.path.join(THEMES_DIR, theme + ".css")
    if not os.path.isfile(path):
        raise SystemExit(f"Unknown theme '{theme}'. Choose one of: {', '.join(THEMES)}")
    with open(path, encoding="utf-8") as f:
        return base + "\n" + f.read()


def build_html(blocks, theme, paper, size_pt, kind):
    page_name = PAPERS[paper][0]
    css = read_css(theme)
    css += (
        f"\n@page {{ size: {page_name}; margin: {MARGINS[size_pt]}; }}"
        f"\nhtml {{ font-size: {size_pt}pt; }}\n"
    )
    title = mdlite.title_of(blocks)
    body_cls = "letter" if kind == "letter" else "resume"
    return (
        "<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
        f"<title>{title}</title><style>{css}</style></head>"
        f"<body class=\"{body_cls}\">\n{mdlite.to_html_body(blocks)}\n</body></html>"
    )


# ------------------------------------------------------------ renderers ---

def chrome_candidates():
    c = []
    for pattern in ("~/Library/Caches/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell",
                    "~/.cache/ms-playwright/chromium_headless_shell-*/*/chrome-headless-shell",
                    "/opt/pw-browsers/chromium_headless_shell-*/*/chrome-headless-shell"):
        c += sorted(glob.glob(os.path.expanduser(pattern)), reverse=True)
    if platform.system() == "Darwin":
        for app in ("Google Chrome", "Google Chrome Canary", "Chromium", "Microsoft Edge",
                    "Brave Browser", "Arc"):
            exe = app if app != "Arc" else "Arc"
            c.append(f"/Applications/{app}.app/Contents/MacOS/{exe}")
            c.append(os.path.expanduser(f"~/Applications/{app}.app/Contents/MacOS/{exe}"))
        c += glob.glob(os.path.expanduser(
            "~/Library/Caches/ms-playwright/chromium-*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium"))
    elif platform.system() == "Windows":
        for base in (os.environ.get("PROGRAMFILES", ""), os.environ.get("PROGRAMFILES(X86)", ""),
                     os.environ.get("LOCALAPPDATA", "")):
            c.append(os.path.join(base, "Google", "Chrome", "Application", "chrome.exe"))
            c.append(os.path.join(base, "Microsoft", "Edge", "Application", "msedge.exe"))
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser",
                 "microsoft-edge", "brave-browser", "chrome"):
        p = shutil.which(name)
        if p:
            c.append(p)
    for pattern in ("~/.cache/ms-playwright/chromium-*/chrome-linux*/chrome",
                    "/opt/pw-browsers/chromium-*/chrome-linux*/chrome",
                    "/ms-playwright/chromium-*/chrome-linux*/chrome"):
        c += sorted(glob.glob(os.path.expanduser(pattern)), reverse=True)
    seen, out = set(), []
    for p in c:
        if p and p not in seen and os.path.isfile(p) and os.access(p, os.X_OK):
            seen.add(p)
            out.append(p)
    return out


def _pdf_complete(path):
    try:
        if os.path.getsize(path) < 500:
            return False
        with open(path, "rb") as f:
            f.seek(-1024, os.SEEK_END)
            return b"%%EOF" in f.read()
    except OSError:
        return False


def _stop(proc):
    """Stop Chrome and every helper process it started."""
    import signal
    if os.name != "nt":
        for sig in (signal.SIGTERM, signal.SIGKILL):
            try:
                os.killpg(proc.pid, sig)
            except (ProcessLookupError, PermissionError, OSError):
                break
            try:
                proc.wait(3)
                break
            except subprocess.TimeoutExpired:
                continue
    elif proc.poll() is None:
        proc.kill()


def _run_chrome(args, pdf_path, timeout=45):
    """Run headless Chrome. Some builds write the PDF and then never exit,
    so watch for a finished file and stop Chrome ourselves."""
    import time
    err = tempfile.TemporaryFile()
    try:
        proc = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=err,
                                start_new_session=(os.name != "nt"))
    except OSError as e:
        return False, str(e)
    start = time.time()
    try:
        while time.time() - start < timeout:
            if proc.poll() is not None:
                break
            if _pdf_complete(pdf_path):
                time.sleep(0.3)
                break
            time.sleep(0.2)
    finally:
        _stop(proc)
    if _pdf_complete(pdf_path):
        return True, ""
    err.seek(0)
    return False, err.read().decode("utf-8", "replace")[-300:].strip() or "timed out"


def render_chrome(html_doc, pdf_path):
    exes = chrome_candidates()
    if not exes:
        raise RuntimeError("no Chrome/Chromium/Edge found")
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, "doc.html")
        with open(src, "w", encoding="utf-8") as f:
            f.write(html_doc)
        last = ""
        for exe in exes:
            for headless in ("--headless", "--headless=new"):
                args = [exe, headless, "--disable-gpu", "--disable-background-networking",
                        "--disable-component-update", "--disable-sync", "--disable-extensions", "--no-first-run", "--no-default-browser-check",
                        "--no-pdf-header-footer", "--print-to-pdf-no-header",
                        "--run-all-compositor-stages-before-draw",
                        f"--print-to-pdf={pdf_path}", "file://" + src]
                if platform.system() == "Linux" or (hasattr(os, "geteuid") and os.geteuid() == 0):
                    args.insert(2, "--no-sandbox")
                if os.path.exists(pdf_path):
                    os.remove(pdf_path)
                ok, last = _run_chrome(args, pdf_path)
                if ok:
                    return f"chrome ({os.path.basename(exe)})"
        raise RuntimeError("Chrome could not print: " + last.strip())


def render_playwright(html_doc, pdf_path):
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise RuntimeError("playwright (python) not installed")
    with sync_playwright() as p:
        try:
            browser = p.chromium.launch()
        except Exception:  # noqa: BLE001  (browser not downloaded for this version)
            exes = chrome_candidates()
            if not exes:
                raise RuntimeError("playwright has no browser installed")
            browser = p.chromium.launch(executable_path=exes[0])
        page = browser.new_page()
        page.set_content(html_doc, wait_until="load")
        page.pdf(path=pdf_path, prefer_css_page_size=True, print_background=True)
        browser.close()
    return "playwright"


def render_weasyprint(html_doc, pdf_path):
    try:
        from weasyprint import HTML
    except Exception:  # ImportError or missing system libs (OSError)
        raise RuntimeError("weasyprint not available")
    HTML(string=html_doc).write_pdf(pdf_path)
    return "weasyprint"


def render_reportlab(blocks, pdf_path, theme, paper, size_pt, kind):
    try:
        import reportlab  # noqa: F401
    except ImportError:
        pip_install("reportlab")
    import pdf_reportlab
    pdf_reportlab.render(blocks, pdf_path, theme=theme, paper=paper, size_pt=size_pt, kind=kind)
    return "reportlab"


def pip_install(pkg):
    say(f"  (one-time setup: installing {pkg}...)")
    for extra in ([], ["--user"], ["--user", "--break-system-packages"], ["--break-system-packages"]):
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", *extra, pkg],
                           capture_output=True, text=True)
        if r.returncode == 0:
            import importlib
            import site
            importlib.invalidate_caches()
            try:
                sys.path.append(site.getusersitepackages())
            except Exception:  # noqa: BLE001
                pass
            return
    raise RuntimeError(f"could not install {pkg}")


# ---------------------------------------------------------------- pages ---

def count_pages(pdf_path):
    try:
        from pypdf import PdfReader
        return len(PdfReader(pdf_path).pages)
    except Exception:  # noqa: BLE001
        with open(pdf_path, "rb") as f:
            data = f.read()
        return max(1, len(re.findall(rb"/Type\s*/Page(?![s\w])", data)))


ORDER = ["chrome", "playwright", "weasyprint", "reportlab"]


def render_once(blocks, pdf_path, theme, paper, size_pt, kind, renderers):
    html_doc = build_html(blocks, theme, paper, size_pt, kind)
    errors = []
    for name in renderers:
        try:
            if name == "chrome":
                return render_chrome(html_doc, pdf_path)
            if name == "playwright":
                return render_playwright(html_doc, pdf_path)
            if name == "weasyprint":
                return render_weasyprint(html_doc, pdf_path)
            if name == "reportlab":
                return render_reportlab(blocks, pdf_path, theme, paper, size_pt, kind)
        except Exception as e:  # noqa: BLE001
            errors.append(f"{name}: {e}")
    raise RuntimeError("Could not make a PDF on this computer.\n  " + "\n  ".join(errors))


def build(md_path, theme=None, paper=None, max_pages=None, renderer="auto", out=None, kind=None):
    md_path = os.path.abspath(md_path)
    with open(md_path, encoding="utf-8") as f:
        blocks = mdlite.parse(f.read())
    prefs = profile_settings(md_path)
    theme = theme or prefs.get("theme") or "modern"
    paper = (paper or prefs.get("paper") or "letter").lower()
    kind = kind or guess_kind(md_path)
    if max_pages is None:
        max_pages = 1 if kind == "letter" else 2
    pdf_path = out or os.path.splitext(md_path)[0] + ".pdf"
    renderers = ORDER if renderer == "auto" else [renderer]

    # once a renderer works, keep using it for the shrink passes
    used, pages = None, None
    for size in (LETTER_SCALES if kind == "letter" else SCALES):
        used = render_once(blocks, pdf_path, theme, paper, size, kind,
                           renderers if used is None else [used.split(" ")[0]])
        pages = count_pages(pdf_path)
        if pages <= max_pages:
            break
    fits = pages <= max_pages
    return {"pdf": pdf_path, "pages": pages, "max_pages": max_pages, "fits": fits,
            "theme": theme, "paper": PAPERS[paper][0], "renderer": used, "font_pt": size}


def doctor():
    say("PDF makers available on this computer:")
    ex = chrome_candidates()
    say(f"  chrome:     {'yes - ' + ex[0] if ex else 'no'}")
    for mod, label in (("playwright.sync_api", "playwright"), ("weasyprint", "weasyprint"),
                       ("reportlab", "reportlab")):
        try:
            __import__(mod)
            ok = "yes"
        except Exception:  # noqa: BLE001
            ok = "no" + (" (will be installed automatically if needed)" if label == "reportlab" else "")
        say(f"  {label + ':':<11} {ok}")
    for mod in ("pypdf", "docx"):
        try:
            __import__(mod)
            ok = "yes"
        except Exception:  # noqa: BLE001
            ok = "no (installed automatically when needed)"
        say(f"  {mod + ':':<11} {ok}")


def open_file(path):
    try:
        if platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        elif platform.system() == "Windows":
            os.startfile(path)  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:  # noqa: BLE001
        pass


def main():
    ap = argparse.ArgumentParser(description="Markdown resume / cover letter -> PDF")
    ap.add_argument("files", nargs="*", help=".md files to convert")
    ap.add_argument("--theme", choices=THEMES)
    ap.add_argument("--paper", choices=list(PAPERS))
    ap.add_argument("--max-pages", type=int)
    ap.add_argument("--kind", choices=["resume", "letter"], help="default: guessed from file name")
    ap.add_argument("--renderer", default="auto", choices=["auto"] + ORDER)
    ap.add_argument("--open", action="store_true", help="open the PDF when done")
    ap.add_argument("--doctor", action="store_true", help="show which PDF makers are available")
    a = ap.parse_args()

    if a.doctor:
        doctor()
        return 0
    if not a.files:
        ap.print_help()
        return 1

    status = 0
    for md in a.files:
        if not os.path.isfile(md):
            say(f"NOT FOUND  {md}")
            status = 1
            continue
        try:
            r = build(md, a.theme, a.paper, a.max_pages, a.renderer, kind=a.kind)
        except Exception as e:  # noqa: BLE001
            say(f"FAILED     {md}\n  {e}")
            status = 1
            continue
        tag = "OK        " if r["fits"] else "TOO LONG  "
        say(f"{tag}{r['pdf']}\n  {r['pages']} page(s) (limit {r['max_pages']}), {r['paper']}, "
            f"theme {r['theme']}, body {r['font_pt']}pt, made with {r['renderer']}")
        if not r["fits"]:
            say("  Still over the limit at the smallest readable size. Cut or tighten content, "
                "then build again.")
            status = 2
        if a.open:
            open_file(r["pdf"])
    return status


if __name__ == "__main__":
    sys.exit(main())

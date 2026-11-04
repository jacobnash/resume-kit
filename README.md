# Resume Kit

A free, guided resume coach that runs inside Claude (Cowork or Claude Code). No app, no
account, no prompt engineering. Someone who has never used AI unzips a folder, opens it in
Claude, says "hi", and comes out with an ATS-safe, genuinely strong resume (and cover letters).

**New here? Read [START-HERE.md](START-HERE.md).**

## How it works

| Step | Skill | What happens |
|---|---|---|
| 0 | `resume-coach` | Front door. Works out where you are, does setup, routes everything else |
| 1 | `resume-intake` | Reads your "super resume" and other files, then walks through every job **line by line**, asking for specifics and real numbers, and builds a deep, honest bullet pool in `my-career/roles/` |
| 2 | `target-roles` | You give 3 ideal next jobs. It extracts requirements and ATS keywords, rates fit, and decides what to lead with, trim and cut (`targets/positioning.md`) |
| 3 | `resume-build` | Writes the resume, self-checks it, gets independent recruiter and hiring-manager reviews, then gets your approval in plain language |
| 4 | `resume-export` | Builds a designed PDF and a .docx, then reads the PDF back like an ATS and reports problems |
| + | `cover-letter` | Company research, one clear argument, strict quality checks, matching PDF |

Design rules that run through every skill: Claude drives and the person only answers. It
never invents facts. Plain language throughout. Every message ends with a numbered next step.
Progress is saved, so "hi" resumes where you left off.

## The tools (`scripts/`)
Plain Python 3.8+. Nothing to install up front.

```bash
python3 scripts/build_pdf.py my-career/output/core/resume.md      # -> resume.pdf
python3 scripts/build_pdf.py resume.md --theme warm --paper a4
python3 scripts/build_pdf.py --doctor                             # what can make PDFs here?
python3 scripts/ats_check.py my-career/output/core/resume.pdf     # ATS read-back report
python3 scripts/build_docx.py my-career/output/core/resume.md     # -> resume.docx
python3 scripts/selftest.py                                       # build + check the example
```

- **PDF makers**, in order: Chrome/Chromium/Edge already on the machine (or Playwright's
  headless shell), Playwright for Python, WeasyPrint, then ReportLab (pure Python,
  auto-installed). The first one that works wins.
- **Themes**: `modern` (default), `classic`, `minimal`, `warm`. All single-column with
  standard headings and real text.
- **Fit to page**: resumes are capped at 2 pages and cover letters at 1. Text shrinks
  slightly (10pt to 9.1pt) before the tool tells you to cut content.
- **ATS check**: confirms the text is extractable, the name and contact details come first,
  section names are standard, every line survives in reading order, dates are consistent,
  there are no ligatures or icon glyphs, and the target-job keywords are covered.
- **Defaults** are read from `my-career/profile.md` (`Paper size:`, `Theme:`). US Letter
  unless set.

## Install options
- **Folder (recommended for non-technical users):** download the ZIP, unzip it, open the
  folder in Claude Cowork, and say hi. `CLAUDE.md` and `.claude/skills/` drive everything.
- **Plugin:** `/plugin marketplace add jacobnash/resume-kit`, then
  `/plugin install resume-kit@resume-kit`. The skills are namespaced `resume-kit:*`. Your data
  goes in `my-career/` in whatever folder you open.

## Keeping your own resume in git
`my-career/` is gitignored in the kit so nobody commits personal data by accident. To keep
your career notes in your own private repo, copy the kit there and remove the `my-career`
lines from `.gitignore`. (See `jacobnash/about-chelsey` for an example.)

## Example
`examples/sample-person/` is a fictional, fully worked example (Jordan Rivera, ops analyst
moving into product analytics). It's used by `scripts/selftest.py` and CI.

## Origin
Distilled from `jacobnash/about-cait` and `jacobnash/about-me` (hand-tuned resume-tailor
skills used in a real job search) and `jacobnash/lagom` (an app version whose prompts for the
career walkthrough, dream-job extraction and profile merging live on here).

MIT licensed. Free forever. Share it with anyone job hunting.

---
name: resume-export
description: Turns an approved resume or cover letter into a polished, ATS-safe PDF (and a Word .docx when useful) using resume-kit's own tools. It checks the result the way screening software reads it, fixes problems, and lets the person pick a look. Use after the person approves resume text, when they want a different design, a Word version or A4 paper, or when a PDF looks wrong.
---

# Making the PDF

**Follow `../resume-coach/reference/how-to-talk.md`.** The person sees results, not commands.
KIT is the kit's `scripts/` folder (see the resume-coach skill, step 0).

## Step 1: Pick a look (first time only)
If `profile.md` has no `Theme:` yet, offer the four looks in one message:

> "Last step: pick a look. All four are built to pass screening software. Only the style changes.
> 1) **Modern**: clean, with a navy accent. A safe pick for most jobs, especially tech and business.
> 2) **Classic**: serif type, black and white. Law, finance, government, academia.
> 3) **Minimal**: quiet grays, lots of breathing room.
> 4) **Warm**: serif headings with a terracotta accent. Design, research, creative and people roles.
> Not sure? Go with 1."

If they want to compare, build all four and show the first page of each. Save the choice to
`profile.md` (`- Theme: modern`).

## Step 2: Build and check
```bash
python3 KIT/build_pdf.py my-career/output/core/resume.md
python3 KIT/ats_check.py my-career/output/core/resume.pdf
python3 KIT/build_docx.py my-career/output/core/resume.md
```
Paper size and theme come from `profile.md` automatically. Override with `--paper a4` or
`--theme classic` if needed.

What the output means:
- `OK ... made with chrome/playwright/weasyprint/reportlab`: built. Chrome looks best. ReportLab
  is a plainer fallback that's still ATS-safe. If ReportLab was used and the person is on a Mac
  without Chrome, mention once: "Installing the free Google Chrome browser would give you a
  nicer-looking PDF. Totally optional."
- `TOO LONG`: the content doesn't fit even at the smallest readable size. Go back and cut
  (weakest and oldest bullets first) with the person's OK, then rebuild. Never ship over-length.
- `FAILED`: run `python3 KIT/build_pdf.py --doctor`, read the output, and fix it yourself.
  Try `--renderer reportlab`, which installs itself. Only ask the person for help as a last
  resort, with one exact instruction.
- ATS report FAIL: fix the source .md (or the person's content with their OK) and rebuild.
  WARN: fix it if it's easy and honest, otherwise mention it in plain words.

## Step 3: Look at it yourself
Before showing the person, look at the PDF yourself. If you can render a page to an image
(e.g. `pdftoppm -png -r 80`) or view the PDF, check:
- nothing cut off, no orphan heading at the bottom of a page, no near-empty last page
  (if page 2 has only 2-3 lines, cut a bullet so it fits on 1 page, or add substance)
- dates aligned, names spelled right, links readable

## Step 4: Hand it over
Show or link the PDF (in Cowork, it appears as a file they can click). Say where it is in
plain words, plus the two-line ATS summary:

> "Here's your resume: **resume.pdf** (in my-career/output/core). It passed every screening
> check, and it covers 13 of the 15 key terms from your target jobs. The two it doesn't
> (Looker, SaaS) aren't things you've done, so we left them out on purpose. There's also a
> Word version if a form asks for one.
>
> 1) Perfect 2) Change something 3) Try a different look"

Then update `_progress.md` and offer the "What next" menu from the resume-coach skill
(tailor to a real posting, cover letter, LinkedIn, ...).

## File naming for applications
For tailored applications, also save a copy named for the employer to see, like
`Jordan-Rivera-Resume.pdf` (and `Jordan-Rivera-Cover-Letter.pdf`), in the same folder. File
names show up in recruiters' downloads. Never use `resume-final-v3.pdf`.

## Combined upload
If an application form has only one upload field and they want a cover letter included, make
`combined.md` with the cover letter first, then `<!--pagebreak-->`, then the resume. Build it with
`--max-pages 3`.

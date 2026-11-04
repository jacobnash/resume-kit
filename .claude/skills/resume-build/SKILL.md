---
name: resume-build
description: Writes the actual resume from the person's career notes (my-career/roles/, extras.md) and target-job positioning (my-career/targets/positioning.md). It self-checks against ATS and writing rules, gets independent recruiter and hiring-manager reviews, and walks the person through approving it in plain language. Builds a core resume aimed at their 3 target jobs, or a version tailored to one specific posting. Use when targets are done and there's no resume yet, or when the person wants a resume for a specific job.
---

# Writing the resume

**Follow `../resume-coach/reference/how-to-talk.md`.** Also read before writing:
- `../resume-coach/reference/writing-rules.md`
- `../resume-coach/reference/ats-rules.md`
- `../resume-coach/reference/resume-format.md` (the exact format the PDF tools need)
- `../resume-coach/reference/regional-norms.md` (check `Job market:` in `profile.md`)

The person doesn't need to do anything until Step 5. Tell them: "Writing your resume now.
I'll check it carefully and get a second opinion before I show you. Give me a minute."

## Two modes
- **Core** (default, first time): aimed at all 3 targets. Write to `my-career/output/core/resume.md`.
- **Tailored** (they're applying to a specific posting): write to
  `my-career/output/<company-role>/resume.md`. Start from the core resume. Re-pick and reorder
  bullets from the full career notes using that posting's target file. Never just find-and-replace
  the company name. Put an `## ATS keywords` section in that posting's target file so the
  check uses it.

## Step 1: Select (don't write yet)
From `positioning.md` (and the specific target, if tailored):
1. Pick the roles to include. Leave out roles under 6 months unless they were contracts. Roles
   older than ~15 years become one line under "Earlier experience" unless they're relevant.
2. For each role, pick bullets from the **approved** pool. Recent and relevant roles get 4-6,
   older ones 2-3, and the oldest get 1-2 or a single line. Start with the "Lead with" items.
3. Order the bullets in each role by relevance to the targets, most relevant first.
4. Pick skills: confirmed items from `extras.md` Skills inventory that match the targets'
   keywords, grouped into 2-4 labelled lines (e.g. **Analysis:**, **Tools:**, **Clinical:**).
5. Decide the section order. Usually Summary, Experience, Education, then Certifications,
   Skills, and others. Early-career or a big pivot: Education or Projects can go above Experience.

Only use `[approved]` bullets. If a key point only exists as `[draft]`, ask about it in Step 5.

## Step 2: Write
- Header: name, then one contact line from `profile.md` (city/state, email, phone, LinkedIn,
  portfolio). Nothing in `Never mention:`.
- Summary: 2-3 sentences built from "The through-line" and the differentiator, with one or
  two real numbers. No adjectives without evidence.
- You may tighten wording and swap in the employers' exact keywords **where the meaning stays
  the same** ("worked with" -> "partnered with stakeholders in"). You may not change facts,
  numbers or scope. If a tightened bullet drifts from the approved one, it needs re-approval.
- Fit the length: 1 page under ~8 years of experience, otherwise 2 pages max. Check by
  building a draft PDF (Step 4 does this).

## Step 3: Self-check. Fix before anyone sees it.
Go through each check and fix failures:
1. **Requirement mapping.** For every Must-have in the target(s), which bullet or skill line proves it?
   If none, can an approved bullet honestly be reframed? If not, it's a known gap (leave it out).
2. **Buried lead.** Is the most target-relevant bullet first in each role?
3. **Six-second test.** Do the name, the most recent title, the summary and the first two bullets
   make the case on their own?
4. **Every bullet**: strong verb, result, real number where one exists, no banned words, one to
   two lines, no repeats across roles.
5. **Style**: no em-dashes in prose, no semicolons, consistent tense, one date style.
6. **Honesty**: every claim traces back to an approved bullet or confirmed fact. Spot-check 5.
7. **Tailored only, the same-bullet test**: if there are other tailored resumes for the same
   company, the bullets shouldn't be identical across them.

## Step 4: Draft build and ATS check (silently)
Run the tools. KIT is the kit's `scripts/` folder; see the resume-coach skill, step 0.
```bash
python3 KIT/build_pdf.py my-career/output/core/resume.md
python3 KIT/ats_check.py my-career/output/core/resume.pdf
```
- `TOO LONG`: cut the weakest bullets (oldest and least relevant first), then rebuild. Never
  shrink fonts by hand.
- Any FAIL in the ATS report: fix and re-run.
- Keyword coverage under 80%: find honest places to use the employer's wording (Step 2 rule).
  Don't add claims to hit a number.

## Step 5: Independent review
Run the two reviewers exactly as `../resume-coach/reference/reviewers.md` describes, in
parallel if you can start agents, and without your notes. Fix the clear issues. A PASS gut call
from the recruiter blocks: revise and re-run. Keep a short list of taste calls for the person.

## Step 6: Show it and get approval (the read-and-approve gate)
Show the full resume **in the chat**, formatted so it reads like the document. Then, briefly:
- The 2-3 strongest things about it.
- Anything you're unsure about, or a reviewer disagreement, as a numbered choice.
- Any `[draft]` facts you used that need their OK.

> "Here's your resume. Read it like a stranger would. Does every line sound like you, and is
> every fact right?
> 1) Looks great, make the PDF 2) A few changes (just tell me in your own words)"

Make their changes, re-run Steps 3-4 for anything changed, and show the changed parts again.
**Don't make the final PDF until they clearly approve the text.** "Looks good" counts. Silence
or an unrelated message doesn't.

Record approval in `_progress.md` ("Core resume approved 2026-11-04"), then hand off to
**resume-export**.

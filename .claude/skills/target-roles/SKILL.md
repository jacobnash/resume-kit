---
name: target-roles
description: Takes the 3 jobs a person would love to have next (job posting links, pasted text, PDFs or just descriptions) and works out what those employers care about. It extracts the requirements and ATS keywords, rates fit, and decides which parts of the person's career notes to lead with, trim or cut. Writes my-career/targets/. Use after the career walkthrough, when the person shares ideal or dream jobs, or when they want to change direction.
---

# Target jobs: deciding what matters

The career notes say everything the person has done. The 3 target jobs decide what the
resume should *say*. This step turns "here are 3 jobs I like" into a clear positioning
plan and a keyword list the ATS check uses later.

**Follow `../resume-coach/reference/how-to-talk.md`.** ATS background is in
`../resume-coach/reference/ats-rules.md`.

## Step 1: Collect the 3 jobs

Ask:
> "Tell me about 3 jobs you'd love next. Real postings work best, so paste a link or the
> text. Not sure where to look? Tell me the job title and the kind of company and I'll
> work from typical postings for that role. They can be a stretch!"

For each:
- **Link**: fetch it. Many job sites (LinkedIn, Workday, Greenhouse, Lever, Ashby) load the
  posting with JavaScript or need a login. If the fetch comes back empty or blocked, say
  "That site won't let me read it. Could you copy the job description text and paste it here?"
- **Text or PDF**: use as given.
- **Just a description** ("product analyst at a health tech startup"): say you'll use what
  similar postings typically ask for. If you can search the web, find 2-3 real current
  postings for that title and blend them. Mark the target file `Source: composite`.

If they give more than 3, that's fine. Use them all, but ask which 3 matter most.
If the 3 are wildly different (nurse, data analyst, chef), say so gently and ask whether
they want one resume per direction, or which direction comes first.

## Step 2: Break down each posting

Write `my-career/targets/<company-role-slug>.md`. Extraction only, no interpretation:

```markdown
# Senior Product Analyst, Acme Health
- Source: <url or "pasted 2026-11-04" or "composite">
- Seniority: Senior IC
- Location / remote: Remote (US)
- Salary range: $130k-$155k (if listed)

## Must have
- 4+ years in analytics
- Advanced SQL
- ...
## Responsibilities
- ...
## Nice to have
- ...
## Their words
Phrases that show what they value, quoted exactly: "comfortable with ambiguity",
"partner closely with product managers", "tell stories with data"
## Full posting text
<paste, so later steps don't need the link to still work>
```

Only include sections the posting actually covers. Never guess.

## Step 3: Positioning (the important part)

Read all targets plus every file in `my-career/roles/` and `extras.md`. Write
`my-career/targets/positioning.md`:

```markdown
# Positioning

## The through-line
One or two sentences: who this person is *for these jobs*. This becomes the backbone of the
summary. E.g. "An operations analyst who already does product-analytics work (experiments,
self-serve dashboards, forecasting) in a healthcare setting, moving to a product team."

## What all 3 want (ranked)
1. SQL + Python analysis (all 3, hard requirement)
2. Experimentation / A/B testing (all 3)
3. Stakeholder storytelling (2 of 3)
...

## Fit
| Requirement | Fit | Evidence (from career notes) |
|---|---|---|
| Advanced SQL | STRONG | 2021 Front Range: dbt/Snowflake data model |
| A/B testing | PARTIAL | 1 test (text reminders, -17% no-shows); no product experiments |
| Looker | GAP | used Tableau, Power BI |

## Differentiator
The single thing most competing candidates won't have. E.g. "Real healthcare operations
context plus shipped experimentation. Health-tech product teams struggle to hire that."

## Lead with / Keep / Trim / Cut
- **Lead with:** forecasting model (2021), A/B test (2019), dashboards (2021)
- **Keep:** dbt data model, mentoring, carrier cost analysis (reframe as negotiation support)
- **Trim to one line:** Summit Logistics role
- **Cut:** floor-lead training, Epic migration (not relevant to the targets)

## Gaps and how to handle them
- Looker: transferable from Tableau. Put "BI tools (Tableau, Power BI)" in skills, and let
  the cover letter say it's learnable. Don't claim Looker.
- "Product" experience: frame the clinic network as the product and patients as users,
  but only in honest terms.

## Questions to ask
Things the targets care about that the notes don't cover yet. Ask before writing.
- "Have you ever worked directly with software engineers or a product team?"

## ATS keywords
### Must have
- SQL
- Python
- A/B testing / experimentation / experiments
- product analytics
- stakeholder management / stakeholders
### Nice to have
- Looker
- cohort analysis
```

Keyword rules:
- Use the **employers' exact wording**. Put synonyms after ` / `. The first term is the
  preferred one.
- Must have = appears in 2+ targets *or* is a hard requirement in any. Typically 8-15 terms.
- Include tools, methods, domain terms, and key title words ("product analyst").
- Leave out soft fluff ("team player", "fast-paced").
- **Don't list keywords the person can't honestly claim** under Must have. Put true gaps in
  the Gaps section instead. The ATS check measures coverage of this list, so it should be
  a list of things to *say*, not a wish list.

## Step 4: Ask the gap questions, then walk them through it

First ask the "Questions to ask" (2-3 at a time). New material goes back into the role files
as `[approved]` bullets, same as intake.

Then explain the plan in plain words, briefly:
> "Here's what I learned from your 3 jobs. They all want strong SQL and Python, testing ideas
> with experiments, and someone who can explain data to non-technical people. You're strong on
> the first and third. The forecasting model is your best story, and we'll lead with it.
> Your healthcare background is a real advantage for 2 of them. One gap: they use Looker and
> you've used Tableau. We'll say 'BI tools' honestly, not claim Looker.
>
> 1) Sounds right, write my resume 2) I'd change something"

Update `_progress.md` and hand off to **resume-build**.

## Later: a new real posting
When they bring a specific job they're about to apply for, write its target file the same
way, add a `## Tailoring for <company>` section to `positioning.md` covering only what's
different from the core plan, then go to resume-build in tailored mode.

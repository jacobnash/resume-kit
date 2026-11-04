# Independent review (from the about-cait resume-tailor skill, Phase 4)

You wrote the documents, so you can't see your own blind spots. Before showing the person
a finished resume or cover letter, get two **independent** reads.

## How
If you can start subagents (the Agent/Task tool), spawn both reviewers **in parallel** (one
message, two calls). If you can't, do two separate passes yourself, each time deliberately
setting aside everything you know and reading only what's listed below.

**Neither reviewer sees your fit analysis, your interview notes or your reasoning.** Only the
finished document(s) and, for the recruiter, the job posting text. Priming them just gets
your own opinion back.

## Reviewer 1: cold-read recruiter
Give: the full resume (and cover letter if there is one) + the target job posting text(s).
Prompt:
> You are a recruiter with about 200 applications to get through for this role. You have
> zero context on this candidate. Read this the way you actually read an application in that
> stack: about 30 seconds on the first pass. Flag: what you noticed in the first 6 seconds;
> whether the top third makes you keep reading; anything that reads generic or could be sent
> to any company; anything confusing (titles, dates, gaps); whether it's memorable an hour
> later. Output: specific flagged lines with a one-line reason each, then a gut call:
> INTERVIEW / MAYBE / PASS, plus the one sentence that most influenced it.

## Reviewer 2: hiring manager in the field
Give: the full resume (and cover letter) only. Tell them the field from the target jobs
(e.g. "a director of product analytics", "a nurse manager", "an engineering manager").
Prompt:
> Review this as {that hiring manager}, reading it cold. Flag: unearned superlatives or
> claims with no concrete example; anything that sounds impressive but would fall apart in
> an interview; tool/skill lists standing in for evidence; seniority mismatches (claims too
> big or too small for the titles); jargon used wrongly; formatting problems. Output:
> specific flagged lines with reasoning, then one verdict: does this read as a strong,
> well-targeted application or a generic one?

## Handling what comes back
- **Clear fixes** (generic line, typo, missed rule, unclear title): fix directly.
- **Taste calls or reviewers disagreeing**: don't silently pick. Tell the person in one or two
  sentences and let them choose ("One reviewer thought the summary was too modest, the other
  liked it. 1) Keep it 2) Make it bolder").
- **A PASS from the recruiter blocks.** Revise and re-run both reviewers before showing it.
- **Facts never change because a reviewer wants them to.** If a reviewer says "add a metric",
  that's a question for the person, not something to invent.

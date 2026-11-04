---
name: resume-intake
description: Walks a person through their whole career history one job and one line at a time, turning a messy "super resume", old CVs, LinkedIn exports, reviews and plain conversation into a deep, honest set of career notes (my-career/roles/ and extras.md) that every resume and cover letter is built from. Use after resume-kit setup, when the person adds new files or a new job, says "I forgot to mention...", or when _progress.md shows the walkthrough isn't finished.
---

# Career walkthrough (intake)

Goal: by the end, `my-career/` holds everything true and useful about this person's career,
better worded than they could have done alone, with real numbers wherever they exist. This
material is the asset. Resumes are just selections from it. Breadth and depth beat polish.

**Follow `../resume-coach/reference/how-to-talk.md` throughout.** File formats are in
`../resume-coach/reference/file-layout.md`. Bullet quality rules are in
`../resume-coach/reference/writing-rules.md`.

## Step 1: Read everything in the inbox (silently, then a short summary)

Read every file in `my-career/00-inbox/` (PDF, DOCX, text, images of documents). For each
job, degree, cert, project, award or anything else you find, merge it into the notes:
- One file per job in `my-career/roles/` named `YYYY-company-slug.md` (start year).
  Promotions at the same company: one file per title.
- Everything else into `my-career/extras.md` under clear headings (Education, Certifications,
  Projects, Awards, Volunteering, Publications, Languages, Skills inventory).
- **Merge, never overwrite.** If two sources describe the same job, combine the details into
  one file. Keep every distinct fact. If sources conflict (different dates or titles), keep
  both and flag it as a question for the person.
- Every bullet starts as `[draft]`, with `source:` saying which file it came from.
- Put anything that doesn't fit yet under `## Raw notes`. Nothing gets thrown away.

Then tell the person what you found, briefly:

> I've read everything. I found 5 jobs going back to 2012, a degree, 2 certifications and
> some great material in your 2023 review. A couple of things to check: your old resume says
> you started at Summit in 2017, LinkedIn says 2016. Which is right?
>
> Next we'll go through your jobs one at a time, newest first. Each takes about 10-15
> minutes. 1) Start with Front Range Health 2) Start somewhere else

Update `_progress.md` with the list of jobs to walk through.

If there's no inbox material, build each job by conversation instead: title, company, dates,
what the company does, what they were hired to do, then the questions below.

## Step 2: One job at a time

For the job you're on, first confirm the facts in one message: title, dates, location, what
the company does in a phrase, team size / who they reported to. Then go **line by line**
through what exists (their existing bullets in order), then dig for what's missing.

### For each existing line
1. Show it, in their words.
2. Ask at most 2-3 short questions that would make it stronger. Pick from:
   - **The specific moment.** "Can you think of one specific time this happened? What was going on?"
   - **The result.** "What changed because of this? What would have happened if you hadn't?"
   - **The number.** Only if the line is genuinely vague. "Roughly how many people / customers / dollars / hours?
     A ballpark is fine, and 'I don't know' is fine too."
   - **What made it hard.** "What made this harder than it sounds?"
   - **Their part.** For "we/team" work: "What part was yours specifically?"
3. Write **up to 3 options** that differ in *angle*, not just wording, such as:
   - impact/outcome first
   - leadership/ownership
   - technical/craft depth

   Mark the one you'd pick and say why in five words.
4. They pick, tweak in their own words, or say "skip". Save the result as `[approved]`, with the
   source. Keep the story they told under Raw notes, even the parts that didn't make the bullet.

Don't ask about the number when one is already there. Most well-quantified lines need
**zero** questions: just offer a polish or confirm it. The bar is "this reads as vague or
generic", not "a more precise number exists somewhere".

### Then dig for what's missing (the gold is usually here)
Ask these 2-3 at a time, adapting to the job and the field:
- "What are you proudest of from this job that isn't on your resume yet?"
- "What did people come to you for? What would have broken if you'd left?"
- "Did you get any awards, shout-outs, promotions or great review comments here?"
- "Did you train, mentor or manage anyone? Fix a process? Save money or time? Win or keep a customer?"
- "What tools, systems, methods or certifications did you use day to day?" (Collect these for Skills.)
- For technical work: "What did you build or run? What was it built with? How many users or how much load? What went wrong and how did you handle it?"
- For people-facing work: "How many customers / patients / students a day? Any measures you were judged on (satisfaction scores, quotas, retention)?"

Turn good answers into new bullets the same way: options, then pick, then save.

### Translating plain words into the right terms
People describe their work in everyday language. You know the vocabulary of their field.
Offer the professional term and **confirm it's accurate**:
> "When you say you 'kept the servers running', would it be fair to call that *site
> reliability* or *on-call incident response*? Did you use anything like PagerDuty, Datadog
> or Kubernetes?"

Only use a term once they agree it's true. Record confirmed tools and skills in
`extras.md` under `## Skills inventory`, noting where each was used.

### Close out the job
- Aim for a pool of **8-20 approved bullets** for recent and relevant jobs, 3-6 for older ones.
  It's a pool. The resume will use only the best few.
- Read back the top 3 bullets for the job. "That's [Company] done. These three are the
  strongest. Nice work." Keep the praise to one sentence and make it honest.
- Update `_progress.md` (mark the job done, note the next one, add a "Last session" line).
- Offer: "1) Next job: [name] 2) Take a break, just say hi when you're back".

## Step 3: Extras

After the jobs, walk through `extras.md` the same way, but faster. Confirm details for education,
certifications (with year), projects, volunteering, awards, languages (with level), and
publications or patents. Ask about anything that might be missing: "Any side projects, volunteer
roles, or courses we haven't covered?"

## Step 4: Gaps and sensitive things

If there are gaps longer than about 6 months, a short stint, or a career change, raise it once and
kindly:
> "I noticed a gap from 2019 to 2020. Totally normal. Do you want it to show as something
> (caregiving, study, travel, a project) or just leave the dates as they are?"

Record the answer in `profile.md` under Notes. Never invent cover stories.

## Step 5: Hand off

Mark the walkthrough done in `_progress.md`. Then:
> "Your career notes are done. Honestly, this is the hard part, and you never have to do it
> again. We'll just add to it. Next: tell me about 3 jobs you'd love to have next. Real postings
> are best (paste a link or the text), but a description works too."

Hand off to **target-roles**.

## Update mode (later visits)
When they bring something new (a new job, a review, an award, "I forgot..."), drop the files in
`00-inbox/`, merge them into the right role or extras file, and run Step 2 just for the new
material. Mention which existing resumes might want refreshing.

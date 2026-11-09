---
name: cover-letter
description: Writes a specific, human-sounding one-page cover letter for a particular job. It researches the company, builds one clear argument from the person's career notes, runs strict quality checks and independent reviews, then exports a matching PDF. Use when the person asks for a cover letter, a letter of interest, or an answer to "why do you want to work here?" on an application form.
---

# Cover letter

A good cover letter makes one argument: *why this person, for this job, at this company.*
It sounds like a person talking, not a list of adjectives. It only works when it's specific,
so research comes first.

**Follow `../resume-coach/reference/how-to-talk.md`.** Rules are in
`../resume-coach/reference/writing-rules.md`. The format is in
`../resume-coach/reference/resume-format.md` (cover letter section).

## Step 1: The job
If there's no target file for this posting yet, collect it the way the target-roles skill
does (link or pasted text) and save `my-career/targets/<company-role>.md`. Work in
`my-career/output/<company-role>/`.

## Step 2: Research (silently, ~a few minutes)
If you can browse or search, read:
- the company's About/mission page and what they actually sell or do
- 1-3 recent news items, blog posts, product launches or annual-report highlights
- the hiring team or manager's name if it's public (for the greeting)
- the application form itself, if reachable: separate cover letter upload or a single
  combined field? Any custom questions ("Why are you interested?")?

Save it to `research.md`: facts, quotes of their own language, and the form details.
If you can't browse, ask the person one question: "What drew you to this company in the
first place?" Their answer is often the best opening anyway.

## Step 3: Fit and argument (internal)
Rate each must-have: STRONG / PARTIAL / GAP, using career notes. Pick:
- **The argument**: one sentence. "I've already done the core of this job (X) in a setting
  that gives me Y, which your team needs because Z."
- **2 proof stories** from approved bullets or raw notes, each with a number if one exists.
- **The gap to address** (if a big one is obvious) and how: a short, confident line about
  how they'd close it, never an apology.
- Anything specific from the research to connect to.

If there's no strong, concrete reason they want *this* company, ask: "What excites you
about this one specifically? Even a small reason helps."

## Step 4: Write (250-350 words, 1 page)
1. **Opening (2-3 sentences)**: something specific to this company and the person's
   connection to it, then the argument. Not "I am writing to apply for...".
2. **Proof (1-2 short paragraphs)**: the 2 stories, told as small concrete moments with
   outcomes. No skill lists.
3. **Why here (2-3 sentences)**: connect their experience to something real from the research.
4. **Close (1-2 sentences)**: confident and warm. Say what they'd like to talk about. Never "I would be honored".
Sign-off: "Best regards," then their name.

## Step 5: Checks. Fix every failure before showing anything.
1. **Swap test**: remove the company name from the first sentence. Could it go to a competitor?
   If yes, rewrite it.
2. **Adjective audit**: passionate, dedicated, experienced, skilled, strong, proven, motivated,
   enthusiastic, innovative, excited. Replace each with a fact or cut it.
3. **Argument test**: is it one argument, or a list of qualities? If it's a list, restructure.
4. **Voice test**: would each sentence sound normal said out loud over dinner? Watch for
   stacked tool or skill lists in a single clause. Those belong on the resume.
5. **Metric count**: at least 2 real numbers. If a number sounds too extreme, use a before/after.
6. **Closing test**: confident, not grovelling, and gives them a reason to reach out.
7. **Length**: 1 page in the PDF.
8. **Honesty**: every claim traces back to career notes.

Then run the two reviewers from `../resume-coach/reference/reviewers.md` on the letter **and**
the resume together (recruiter gets the posting too). A recruiter PASS blocks.

## Step 6: Approve, then export
Show the letter in the chat. Ask "Does this sound like you?" with numbered choices. Edit
from their own words. Only after clear approval:
```bash
python3 KIT/build_pdf.py my-career/output/<company-role>/cover-letter.md
python3 KIT/build_docx.py my-career/output/<company-role>/cover-letter.md
```
The tools give the letter the same look as the resume, and a 1-page limit, automatically
(the file name contains "cover"). Follow the resume-export skill's naming and combined-upload
rules.

## Application form answers
For "Why do you want to work here?" style fields: 150-200 words, written fresh for that
field (not pasted from the letter), with the same voice and checks. Save to `notes.md` and get
approval. Never answer sponsorship, salary or legal questions for them. Ask, and use their
exact answer. If you're filling a web form for them, **never click the final Submit**. Tell
them it's ready for their review.

## Regional notes
Check `Job market:` in `profile.md`. For example, in Sweden a cover letter (personligt brev)
is expected even when it's optional, the tone is understated and team-oriented, and you state
the relocation plan plainly. See `../resume-coach/reference/regional-norms.md`.

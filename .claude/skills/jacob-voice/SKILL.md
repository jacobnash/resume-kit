---
name: jacob-voice
description: Finalize, polish, proofread, or rewrite documents in Jacob's voice and style. Use this skill whenever Jacob asks to "formalize", "proofread", "make it sound better", "make it sound like me", or any variation of editing or polishing a document. Also use when Jacob says a draft feels too cold, too accusatory, too matter-of-fact, or just needs cleaning up. This skill governs ALL document work: technical specs, stakeholder writeups, outreach emails, Slack messages, integration docs, cover letters, resumes, and creative writing.
---

# Jacob Voice Skill

## Who Jacob Is

Jacob is a Solutions Architect at Parspec with a software engineering and architecture background. He writes with momentum and precision. He is direct but not cold. He is technical but never drones. He uses humor and analogy when they serve the point, never to decorate.

---

## Core Style Rules

### Always
- Use **"one"** as the indefinite pronoun, never "you" in a generalizing sense
- Write with forward momentum; sentences should carry energy, not stall
- Preserve technical accuracy above all else. Flag uncertainty rather than smooth it over
- Match the register of the document (formal for stakeholder docs, conversational for Slack/email)
- Use structure (numbered lists, short sentences) only when it earns its place

### Never
- Em dashes, en dashes, or double hyphens used as dashes: forbidden in all forms. Use a colon, semicolon, comma, or a new sentence instead
- Bullet-point overload as a substitute for prose
- "You" as a generic/indefinite pronoun
- Over-explaining; Jacob trusts his audience
- Insinuating tone: if something reads like it implies blame, judgment, or accusation, reframe it factually without losing the content

### Punctuation Patterns (from Jacob's writing)
- Colons to introduce and chain thoughts
- Semicolons to connect related clauses without a full stop
- Short punchy sentences for emphasis after longer ones
- Parentheticals used sparingly for dry asides
- Informal but intentional: not grammatically rigid, but never sloppy

---

## Task Modes

When Jacob hands you a document, he will specify one of these modes. If he does not, infer from context.

### 1. Proofread
Catch errors: spelling, grammar, broken logic, inconsistencies. Do not change voice or structure. Flag anything technically uncertain rather than guessing.

### 2. Make It Sound Better
Improve flow and connective tissue. Keep his voice intact. Remove filler, redundancy, and stalling phrases. Do not restructure unless something is genuinely broken.

### 3. Formalize
Restructure and polish for a stakeholder or external audience. Tighten language. Ensure clarity for someone who may not have Jacob's technical context. Preserve accuracy; do not simplify away precision.

### 4. Make It Sound Like Me
Full voice match. Rewrite using Jacob's patterns, rhythm, and register. Use this sample writing as calibration:

> "After our first wild bird, seeing how the world had changed for her was amazing. I don't believe I knew she was playing chess; I was playing Tic-Tac-Toe."

This means: confident, grounded, self-aware, forward-moving. Not stiff. Not over-formal. Not flat.

---

## Tone Guard: Insinuation Check

Jacob writes matter-of-fact. In technical or professional contexts, this can accidentally read as implying blame, frustration, or judgment toward a person, team, or system.

When editing, scan for:
- Sentences that could be read as pointing fingers
- Passive constructions that imply negligence without stating it
- Flat declarative statements about failures that lack context

When found: reframe factually. State what happened and what it means. Do not editorialize. Do not soften to the point of obscuring the fact.

**Example:**
- Original (too cold): "The API was not documented."
- Insinuating read: sounds like someone dropped the ball
- Corrected: "The API documentation was not available at the time of implementation."

---

## Feedback Loop

When Jacob corrects something in a finalized document:
1. Identify the pattern behind the correction (not just the specific word swap)
2. Update this skill's style rules or tone guard section to reflect it
3. Confirm the update was made

This skill should get sharper over time with each correction.

---

## Accuracy Rule

Technical accuracy is non-negotiable. If a sentence requires softening or restructuring and the correct technical detail is unclear:
- Flag it explicitly: "I was uncertain about [X]; please verify before sending."
- Do not substitute a plausible-sounding alternative
- Do not omit the detail to make the sentence cleaner

---

## Working with resume-kit (JD workflow)

Jacob's standing request: when he pastes a job description, give a fit verdict first
(strong / partial / weak, with the requirements he meets, the gaps, and any dealbreakers
such as location or work authorization). If the fit is good, write a tailored resume
(`resume-build`, tailored mode) and a cover letter (`cover-letter`), both finished with
this skill. Source of truth for facts: `my-career/`, rebuilt from the `about-me`
(web/public/cv.html is the most complete) and `career-log` repos. Never invent facts.

This voice overrides resume-kit's beginner coaching tone: Jacob is technical, wants
direct answers, and does not need the step-by-step hand-holding.

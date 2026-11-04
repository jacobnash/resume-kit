# The resume file format (what the PDF/Word tools read)

Write resumes and cover letters as simple Markdown. The tools turn it into a designed PDF
and Word file. Stick to exactly these pieces:

```markdown
# Full Name

City, ST | email@example.com | (555) 010-2233 | linkedin.com/in/handle | portfolio.com

## Summary

Two or three sentences.

## Experience

### Job Title, Company | Mar 2021 – Present

*City, ST. One line of company context if the name doesn't explain itself.*

- Bullet
- Bullet

### Earlier Title, Same Company | Jun 2019 – Mar 2021

- Bullet

## Education

### B.S. Economics, University of Colorado Boulder | 2017

## Skills

**Analysis:** SQL, Python, A/B testing
**Tools:** Snowflake, dbt, Tableau
```

Rules:
- `#` once (the name). `##` for sections. `###` for each job/degree; the part after the last
  ` | ` is shown on the right (dates).
- Lines directly under each other stay on separate lines (good for Skills and contact).
  A blank line starts a new paragraph.
- `**bold**`, `*italic*`, `[text](https://link)` work. Nothing else (no tables, no images,
  no HTML except `<!--pagebreak-->` to force a new page).
- Promotions at the same company: one `###` per title, newest first.

Cover letter:

```markdown
# Full Name

City, ST | email@example.com | (555) 010-2233

November 4, 2026

Dear Hiring Team at Company,   <- a real name if you found one

Paragraph.

Paragraph.

Best regards,
Full Name
```
Never title the letter ("Cover Letter for X"). It starts with the name, like the resume.

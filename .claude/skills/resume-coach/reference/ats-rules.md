# ATS rules: getting through the software companies use to screen resumes

Most mid-size and large employers run every resume through an applicant tracking system
(ATS: Workday, Greenhouse, Lever, Ashby, iCIMS, Taleo...). It turns the file into text,
splits it into sections, and recruiters search or filter it by keywords. A beautiful resume
the ATS can't read is a blank resume. The kit's PDF builder already handles the format side.
Your job is the content side.

## Format (handled by the kit's tools, don't fight them)
- One column. No tables, text boxes, side bars, icons, graphics, skill bars or photos.
- Real, selectable text. Never an image or scan.
- Name first, then contact details as plain text on page 1 (not in a page header/footer).
- Standard fonts and standard bullets.
- PDF is the default. Also produce .docx when a form asks for Word or the person is
  applying through an older ATS (Taleo, some Workday setups) or a staffing agency.

## Section names: use the familiar ones
Summary, Experience (or Work Experience), Education, Skills, Certifications, Projects,
Awards, Volunteer Experience, Publications, Languages. Creative names ("My Journey",
"Toolbox", "Where I've Made Impact") confuse parsers. `ats_check.py` warns about these.

## Each job entry
`### Job Title, Company | Mon YYYY – Mon YYYY` (or `– Present`)
Optional next line in italics: location and one line of context about the company
("Regional network of 14 clinics") when the company name alone doesn't explain it.
Title and company on the same line, dates right-aligned, is the most reliably parsed layout.

## Keywords: the part that actually decides who gets seen
- Recruiters search for the **exact words in the job posting**. Use the employer's wording
  when it's true: if they say "stakeholder management" and the person did it, say
  "stakeholder management", not only "worked with partners".
- Include both the acronym and the long form once where it matters:
  "search engine optimization (SEO)", "electronic health records (EHR)".
- Put the most important keywords in **context** (inside bullets that prove them), and
  also list hard skills/tools in the **Skills** section for exact-match searches.
- Job titles matter: if their official title was odd ("Data Ninja II") but the work was
  "Data Analyst", it's fine to write "Data Analyst (official title: Data Ninja II)" once.
- **Never** keyword-stuff, hide white text, or list skills they don't have. Modern ATS
  and every human reviewer catch it, and it ends applications.
- Target: the resume covers ~80% of the "must have" terms in `targets/positioning.md`
  *that are true for the person*. `ats_check.py` reports coverage. Below that, find honest
  places to use the employer's words, or accept the gap and say so.

## Things that silently break parsing (the tools check these)
- Contact info only in a header/footer.
- Ligatures (fi, fl) and private-use symbol fonts (icons).
- Mixed date formats ("2019-03", "March 2019", "3/19").
- Dates on a separate line far from the job title.
- Two-column layouts, where the ATS reads straight across both columns.

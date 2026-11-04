# Where things live

All the person's material lives in `my-career/` inside the folder they opened.
(Create it if it doesn't exist. In plugin mode the open folder may be empty: that's fine.)

```
my-career/
  00-inbox/              # anything they drop in: old resumes, LinkedIn PDF, reviews, awards,
                         # project write-ups, job descriptions. Never delete from here.
  profile.md             # contact details, job market, paper size, theme, name form,
                         # work authorization, preferences, things to never mention
  roles/                 # one file per job: YYYY-company-slug.md (YYYY = start year)
  extras.md              # education, certifications, projects, volunteering, awards,
                         # publications, languages, skills inventory
  _progress.md           # where we are; read FIRST every session
  targets/
    <slug>.md            # one per ideal job (the 3 targets, plus real postings later)
    positioning.md       # what matters across the targets + ATS keyword list
  output/
    core/                # the main resume aimed at all 3 targets
      resume.md / .pdf / .docx / -ats-report.md
    <company-role>/      # tailored versions for specific postings
      resume.md / cover-letter.md / research.md / ...
```

## roles/YYYY-company.md format

```markdown
# Job title, Company
- Dates: Mar 2021 – Present
- Location: Denver, CO (hybrid)
- Company context: regional network of 14 outpatient clinics, 1,100 staff
- Team / reports to: 4 analysts, reported to VP Operations
- Why they left (private, never on the resume): ...

## Bullet pool
<!-- status: approved | draft | cut. source: where the fact came from -->
- [approved] Built a patient-volume forecasting model in Python that drove staffing for all 14 clinics, cutting overtime 22% ($410K a year) in its first year
  - source: super resume line 14 + interview 2026-11-04 (number from their annual review)
  - tags: forecasting, python, cost savings, executive-facing
- [draft] ...

## Raw notes
Everything else they said about this job, in their own words. Stories, context, numbers,
names of tools. Nothing gets thrown away. This is the material future tailoring pulls from.
```

## _progress.md format

```markdown
# Progress
- [x] Setup (name, contact, job market)
- [x] Read inbox (3 files)
- [ ] Walk through jobs: 2 of 5 done
  - [x] 2021 Front Range Health (12 approved bullets)
  - [x] 2019 Front Range Health (6 approved bullets)
  - [ ] 2017 Summit Logistics  <- NEXT: start here
- [ ] Extras (education, certs...)
- [ ] 3 ideal jobs
- [ ] Core resume
- [ ] PDF
- [ ] Cover letter (optional)

## Last session (2026-11-04)
Finished the 2019 role. They mentioned an award at Summit; ask about it.
```

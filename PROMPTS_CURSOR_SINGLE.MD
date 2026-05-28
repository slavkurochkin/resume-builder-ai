# Cursor — Single Job

1. Open Cursor prompt (`Cmd+L` or `Cmd+I`)
2. Replace `@DOCS/jobs/COMPANY.md` with the actual job file, e.g. `@DOCS/jobs/stripe.md`
3. Replace `COMPANY_resume.txt` in the output line with the same slug, e.g. `stripe_resume.txt`
4. Paste and send

---

You are an expert technical recruiter and ATS optimization specialist.

Generate a tailored resume using the documents below.

Base resume: @ENG_ATS.md
Job description: @DOCS/jobs/COMPANY.md
Skills reference: @SKILLS_BASE.md

Instructions:
- Optimize for ATS parsing and human readability
- Align experience, bullet points, and keywords directly to the job description
- Only include skills, tools, and experiences that exist in the Skills reference
    - Do not invent or exaggerate experience
- Rephrase bullet points using action verbs, measurable impact, and role-relevant keywords
- Prioritize relevant technologies, responsibilities, and domain knowledge
- De-emphasize or remove content not relevant to the target role

Constraints:
- 3–4 pages maximum
- Plain text only — no Markdown, no #, *, **, _, backticks, or symbols
- Standard headings and bullet points, ATS-friendly

Output:
- Save the resume as DOCS/resumes/COMPANY_resume.txt
- Move the job file to DOCS/archives/jobs/
- Update DOCS/status_log.csv: set resume_created=yes for this company
- No explanations before or after — resume content only
- After saving, list the keywords from the job description that were matched

# Cursor — All Pending Jobs (Batch)

1. Open Cursor prompt (`Cmd+L` or `Cmd+I`)
2. Paste as-is — no edits needed
3. Send

---

You are an expert technical recruiter and ATS optimization specialist.

Process every .md file inside @DOCS/jobs/ — generate one tailored resume per job.

For each job file found, use:
- Base resume: @ENG_ATS.md
- Skills reference: @SKILLS_BASE.md

For each job, follow these instructions:
- Optimize for ATS parsing and human readability
- Align experience, bullet points, and keywords directly to the job description
- Only include skills, tools, and experiences that exist in the Skills reference
    - Do not invent or exaggerate experience
- Rephrase bullet points using action verbs, measurable impact, and role-relevant keywords
- Prioritize relevant technologies, responsibilities, and domain knowledge
- De-emphasize or remove content not relevant to the target role

Constraints (apply to every resume):
- 3–4 pages maximum
- Plain text only — no Markdown, no #, *, **, _, backticks, or symbols
- Standard headings and bullet points, ATS-friendly

For each job file, do all of the following in order:
1. Generate the tailored resume
2. Save it to DOCS/resumes/<company-slug>_resume.txt
3. Move the job file to DOCS/archives/jobs/
4. Update DOCS/status_log.csv: set resume_created=yes for that company
5. Print the matched keywords for that job

After all jobs are processed, print a summary: how many resumes were created.

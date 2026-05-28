# Resume Agent

Generates tailored, ATS-optimized resumes from job postings.
Two ways to run: **Python agent** (automated) or **Cursor** (manual, one at a time).

---

## Folder structure

```
DOCS/
  jobs/            ← drop job postings here (.md files)
  resumes/         ← generated resumes land here (.txt files)
  archives/jobs/   ← processed job files are moved here automatically
  status_log.csv   ← tracks resume_created and applied per company
ENG_ATS.md         ← your base resume (source of truth for structure)
SKILLS_BASE.md     ← your skills reference (source of truth for content)
PROMPTS.MD         ← prompt template used by the Python agent
PROMPTS_CURSOR.MD  ← prompt template used in Cursor
resume_agent.py    ← the agent script
```

---

## Adding a job

Save the job posting as a `.md` file in `DOCS/jobs/`. The filename becomes the company slug.

```
DOCS/jobs/stripe.md
DOCS/jobs/datadog.md
```

Use a `# Company Name` heading as the first line — the agent uses it to fill in the company name in the prompt.

---

## Option 1 — Python agent

Best for: processing multiple jobs at once, fully automated.

### First-time setup

```bash
# 1. Create and activate a virtual environment (Python 3.13)
python3.13 -m venv .venv
source .venv/bin/activate

# 2. Install dependency
pip install openai

# 3. Set your OpenAI API key
export OPENAI_API_KEY=sk-...
```

> Each new terminal session requires `source .venv/bin/activate` and `export OPENAI_API_KEY=sk-...`

### Running

```bash
# Preview pending jobs — no API call, free
python resume_agent.py --dry-run

# Process all pending jobs
python resume_agent.py

# Process one specific job
python resume_agent.py --job stripe.md
```

### What happens automatically

1. Any new job files not yet in `status_log.csv` are registered
2. Jobs already marked `resume_created=yes` are skipped
3. Resume saved to `DOCS/resumes/stripe_resume.txt`
4. Job file moved to `DOCS/archives/jobs/stripe.md`
5. `status_log.csv` updated: `resume_created=yes`
6. Matched keywords printed to console

### Marking a job as applied

Open `DOCS/status_log.csv` and flip `applied` to `yes` manually — this column is never touched by the agent.

---

## Option 2 — Cursor

Best for: when you want to review output before saving, or don't want to use the terminal.
Supports two modes: single job or all pending jobs at once.

### Single job

1. Drop the job file into `DOCS/jobs/`, e.g. `DOCS/jobs/stripe.md`
2. Open `PROMPTS_CURSOR_SINGLE.MD` in Cursor
3. Open the prompt window (`Cmd+L` for chat, `Cmd+I` for inline)
4. Replace `COMPANY.md` with your actual file and send

### All pending jobs (batch)

1. Drop all job files into `DOCS/jobs/`
2. Open `PROMPTS_CURSOR_BATCH.MD` in Cursor
3. Open the prompt window (`Cmd+L` or `Cmd+I`)
4. Paste as-is — no edits needed — and send

Cursor will for each job:
- Write the resume to `DOCS/resumes/<slug>_resume.txt`
- Move the job file to `DOCS/archives/jobs/`
- Update `status_log.csv`
- Print matched keywords

At the end it prints a summary of how many resumes were created.

---

## Comparison

| | Python agent | Cursor |
|---|---|---|
| Best for | Batch processing | One at a time |
| File handling | Fully automatic | Cursor does it, you confirm |
| CSV update | Automatic | Manual |
| Requires | `OPENAI_API_KEY` env var | Cursor with file access |
| Command | `python resume_agent.py` | Cmd+L or Cmd+I |

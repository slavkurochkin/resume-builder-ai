# Resume Builder AI

An AI-powered resume builder that generates tailored, ATS-optimized resumes from job postings. Collect a job description with one click, run the agent, and get a resume aligned to that role's exact keywords and requirements.

---

## The workflow

```
Job posting (browser)
        │
        ▼
 copy-agent extension          ← click to collect job fields, save as .md
        │
        ▼
  DOCS/jobs/stripe.md          ← job file lands here automatically
        │
        ▼
 resume_agent.py  OR  Cursor   ← reads job + your base resume + skills
        │
        ▼
  DOCS/resumes/stripe_resume.txt  ← ATS-optimized resume, ready to submit
```

**Step 1 — Collect** job descriptions from any site using the [copy-agent Chrome extension](https://github.com/slavkurochkin/copy-agent). It clicks through the page fields you configure and saves the result as a `.md` file directly into `DOCS/jobs/`.

**Step 2 — Generate** a tailored resume by running the Python agent (batch) or using Cursor (one at a time). The AI rewrites your base resume to match the job's keywords, responsibilities, and required skills — without inventing anything not in your skills file.

**Step 3 — Submit** the resume from `DOCS/resumes/` and mark the job as `applied=yes` in `DOCS/status_log.csv`.

---

## Getting started

### 1. One-time setup

```bash
# Clone the repo
git clone https://github.com/YOUR-USERNAME/resume-builder-ai
cd resume-builder-ai

# Create and activate a virtual environment (Python 3.13+)
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install openai

# Set your OpenAI API key
export OPENAI_API_KEY=sk-...
```

### 2. Fill in your resume files

Edit these two files with your own information before running anything:

**`ENG_ATS.md`** — your base resume. The AI uses this as the structural source of truth: it preserves your section order, approximate length, and formatting while rewriting the content for each job.

**`SKILLS_BASE.md`** — your skills and experience reference. The AI only includes skills, tools, and experiences listed here — it never invents or exaggerates content. Keep this accurate and up-to-date.

Both files contain placeholder text (`YOUR_NAME`, `YOUR_EMAIL`, etc.) to guide you.

### 3. Set up the copy-agent extension

Install the [copy-agent Chrome extension](https://github.com/slavkurochkin/copy-agent) locally:

1. Clone or download the copy-agent repo
2. Open `chrome://extensions` → enable **Developer mode** → **Load unpacked** → select the folder
3. Pin the extension to your toolbar

Then configure a recipe for the job sites you use (LinkedIn, Greenhouse, Lever, company career pages, etc.):

1. Click the extension icon → **⚙ Site Recipes** → **+ New Recipe**
2. Set the **URL pattern** to match the job posting URL (e.g. `linkedin.com/jobs/view`)
3. Add fields: **Job Title**, **Company**, **Job Description** — use Record mode to click each element and capture its selector automatically
4. Enable **Include source URL** so the source link is saved with every file
5. Set the save folder to `DOCS/jobs/` inside this project

Now on any job posting: click the extension → **Collect** → **Save as .md** — the file lands directly in `DOCS/jobs/` ready for the agent.

> **File naming:** use a short company slug as the filename (e.g. `stripe.md`, `datadog.md`). The agent uses the filename as the company identifier in `status_log.csv`.

### 4. Generate a resume

**Option A — Python agent** (best for processing multiple jobs at once):

```bash
python resume_agent.py --dry-run        # preview pending jobs, no API call
python resume_agent.py                  # process all pending jobs
python resume_agent.py --job stripe.md  # process one specific job
```

The agent automatically:
- Registers any new job files in `status_log.csv`
- Skips jobs already marked `resume_created=yes`
- Saves the resume to `DOCS/resumes/stripe_resume.txt`
- Archives the job file to `DOCS/archives/jobs/stripe.md`
- Updates `status_log.csv`

**Option B — Cursor** (best when you want to review output before saving):

1. Open `PROMPTS_CURSOR_SINGLE.MD` in Cursor for one job, or `PROMPTS_CURSOR_BATCH.MD` for all pending jobs
2. Open the prompt window (`Cmd+L` for chat, `Cmd+I` for inline) and send
3. Cursor writes the resume, archives the job file, and updates the CSV

### 5. Track your applications

Open `DOCS/status_log.csv` and flip `applied` to `yes` after submitting. The agent never touches the `applied` column — only `resume_created`.

---

## File structure

```
DOCS/
  jobs/            ← job postings land here (from copy-agent or manual)
  resumes/         ← generated resumes saved here
  archives/jobs/   ← processed job files moved here automatically
  status_log.csv   ← tracks resume_created and applied per company
ENG_ATS.md         ← your base resume (structural source of truth)
SKILLS_BASE.md     ← your skills reference (content source of truth)
PROMPTS.MD         ← prompt template used by the Python agent
PROMPTS_CURSOR_SINGLE.MD  ← Cursor prompt for one job at a time
PROMPTS_CURSOR_BATCH.MD   ← Cursor prompt for all pending jobs
resume_agent.py    ← the agent script
```

---

## Requirements

- Python 3.13+
- OpenAI API key (`OPENAI_API_KEY` env var)
- [copy-agent Chrome extension](https://github.com/slavkurochkin/copy-agent) (optional but recommended for fast job collection)
- Job postings as `.md` files with a `# Company Name` heading as the first line

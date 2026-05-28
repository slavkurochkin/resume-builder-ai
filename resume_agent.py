#!/usr/bin/env python3
"""
Resume Agent — Automatically generates tailored resumes for job postings.

Usage:
    python resume_agent.py              # Process all pending jobs
    python resume_agent.py --dry-run    # Preview what would be processed
    python resume_agent.py --job aveshka-inc.md  # Process one specific job
"""

import argparse
import csv
import os
import re
import shutil
from pathlib import Path

from openai import OpenAI

# ── Paths ──────────────────────────────────────────────────────────────────
ROOT         = Path(__file__).parent
JOBS_DIR     = ROOT / "DOCS" / "jobs"
ARCHIVE_DIR  = ROOT / "DOCS" / "archives" / "jobs"
RESUMES_DIR  = ROOT / "DOCS" / "resumes"
STATUS_LOG   = ROOT / "DOCS" / "status_log.csv"
PROMPT_FILE  = ROOT / "PROMPTS.MD"
BASE_RESUME  = ROOT / "ENG_ATS.md"
SKILLS_FILE  = ROOT / "SKILLS_BASE.md"

MODEL = "gpt-4o"


# ── Status log helpers ─────────────────────────────────────────────────────

def load_status_log() -> dict[str, dict]:
    """Return {slug: {resume_created, applied}} from status_log.csv."""
    if not STATUS_LOG.exists():
        return {}
    with open(STATUS_LOG, newline="") as f:
        return {
            row["company"].strip(): {
                "resume_created": row.get("resume_created", "no").strip(),
                "applied":        row.get("applied",         "no").strip(),
            }
            for row in csv.DictReader(f)
        }


def save_status_log(entries: dict[str, dict]) -> None:
    with open(STATUS_LOG, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["company", "resume_created", "applied"])
        writer.writeheader()
        for company, data in sorted(entries.items()):
            writer.writerow({
                "company":        company,
                "resume_created": data["resume_created"],
                "applied":        data["applied"],
            })


def auto_register_jobs(jobs: list[Path], status: dict) -> dict:
    """Add rows for any job files not yet in status_log.csv."""
    new_entries = [j for j in jobs if slug(j) not in status]
    if new_entries:
        for job in new_entries:
            print(f"  [+] Registering new job in status_log: {slug(job)}")
            status[slug(job)] = {"resume_created": "no", "applied": "no"}
        save_status_log(status)
    return status


# ── Job file helpers ───────────────────────────────────────────────────────

def slug(job_file: Path) -> str:
    """aveshka-inc.md → 'aveshka-inc'"""
    return job_file.stem


def company_name(job_file: Path) -> str:
    """Read first # heading from the job file; fall back to title-cased slug."""
    text = job_file.read_text(encoding="utf-8")
    match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return job_file.stem.replace("-", " ").replace(",", "").title()


def pending_jobs(status: dict) -> list[Path]:
    """Return all .md files in Jobs/ whose resume_created != 'yes'."""
    return [
        f for f in sorted(JOBS_DIR.glob("*.md"))
        if status.get(slug(f), {}).get("resume_created", "no").lower() != "yes"
    ]


# ── Resume generation ──────────────────────────────────────────────────────

def build_prompt(job_file: Path, company: str) -> str:
    template   = PROMPT_FILE.read_text(encoding="utf-8")
    job_text   = job_file.read_text(encoding="utf-8")
    base       = BASE_RESUME.read_text(encoding="utf-8")
    skills     = SKILLS_FILE.read_text(encoding="utf-8")

    return (
        template
        .replace("{JOB_DESCRIPTION}", job_text)
        .replace("{BASE_RESUME}",     base)
        .replace("{SKILLS_BASE}",     skills)
        .replace("{COMPANY_NAME}",    company)
    )


def call_openai(client: OpenAI, prompt: str) -> tuple[str, str]:
    """Call gpt-4o and return (resume_markdown, keywords_string)."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
    )
    text = response.choices[0].message.content or ""

    resume_m   = re.search(r"<resume>(.*?)</resume>",     text, re.DOTALL)
    keywords_m = re.search(r"<keywords>(.*?)</keywords>", text, re.DOTALL)

    resume   = resume_m.group(1).strip()   if resume_m   else text.strip()
    keywords = keywords_m.group(1).strip() if keywords_m else ""
    return resume, keywords


# ── Main pipeline ──────────────────────────────────────────────────────────

def process_job(job_file: Path, status: dict, client: OpenAI) -> bool:
    company = company_name(job_file)
    job_slug = slug(job_file)
    print(f"\n  Company : {company}")
    print(f"  File    : {job_file.name}")

    prompt = build_prompt(job_file, company)

    print(f"  → Calling OpenAI ({MODEL})…")
    try:
        resume_text, keywords = call_openai(client, prompt)
    except Exception as exc:
        print(f"  ✗ OpenAI error: {exc}")
        return False

    # Save resume
    RESUMES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = RESUMES_DIR / f"{job_slug}_resume.txt"
    out_path.write_text(resume_text, encoding="utf-8")
    print(f"  ✓ Resume  → {out_path.relative_to(ROOT)}")

    if keywords:
        preview = keywords[:120] + ("…" if len(keywords) > 120 else "")
        print(f"  ✓ Keywords: {preview}")

    # Archive job file
    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    shutil.move(str(job_file), ARCHIVE_DIR / job_file.name)
    print(f"  ✓ Archived → DOCS/Jobs/archive/{job_file.name}")

    # Update status log
    status[job_slug]["resume_created"] = "yes"
    save_status_log(status)
    print(f"  ✓ status_log.csv updated")

    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Resume generation agent")
    parser.add_argument("--dry-run", action="store_true",
                        help="List pending jobs without calling OpenAI")
    parser.add_argument("--job", metavar="FILENAME",
                        help="Process a single job file (name only, e.g. aveshka-inc.md)")
    args = parser.parse_args()

    if not args.dry_run and not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("✗  OPENAI_API_KEY is not set. Add it to .env or export it.")

    client = OpenAI() if not args.dry_run else None  # reads OPENAI_API_KEY automatically

    print("═══ Resume Agent ═══")
    status = load_status_log()

    # Determine job list
    if args.job:
        job_path = JOBS_DIR / args.job
        if not job_path.exists():
            raise SystemExit(f"✗  Job file not found: {job_path}")
        jobs = [job_path]
    else:
        jobs = pending_jobs(status)

    if not jobs:
        print("✓ No pending jobs — nothing to do.")
        return

    print(f"\nFound {len(jobs)} pending job(s):")
    for j in jobs:
        print(f"  • {j.name}")

    # Auto-register any new files in the CSV
    status = auto_register_jobs(jobs, status)

    if args.dry_run:
        print("\n[dry-run] Would process the jobs listed above. Re-run without --dry-run to proceed.")
        return

    # Process each job
    passed, failed = 0, 0
    for job_file in jobs:
        print(f"\n{'─' * 40}")
        ok = process_job(job_file, status, client)
        if ok:
            passed += 1
        else:
            failed += 1

    print(f"\n{'═' * 40}")
    print(f"Finished — {passed} resume(s) created, {failed} failed.")


if __name__ == "__main__":
    main()

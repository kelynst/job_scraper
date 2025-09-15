# 💼 job_scraper
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python job scraper using **Requests** to pull live listings from the Remote OK public API and export clean CSV files for analysis.

---

## 📌 Features
- Scrapes **real job listings** from a public API (no brittle HTML)
- Optional **tag** filter (e.g., `python`, `designer`, `marketing`)
- Choose **row limit** and **output file**
- Exports tidy **CSV** with: position, company, location, tags, salary (if available), URL, and posted date (UTC)

---

## 📦 Installation
```bash
git clone https://github.com/kelynst/job_scraper.git
cd job_scraper
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\Activate      # Windows PowerShell
pip install -r requirements.txt
```

---

## ▶️ Usage

**Default (all jobs, max 200 rows):**
```bash
python scrape_jobs.py
```

**Filter by tag (e.g., Python) and save to a custom file:**
```bash
python scrape_jobs.py --tag python --limit 300 --out python_jobs.csv
```

**Design roles, 100 rows:**
```bash
python scrape_jobs.py --tag designer --limit 100 --out design_jobs.csv
```

**Marketing, no limit:**
```bash
python scrape_jobs.py --tag marketing --limit 0 --out marketing_all.csv
```

---

## 📝 Example Output (`python_jobs.csv`)
```
id,position,company,location,salary,url,company_url,logo,tags,posted_utc
123456,Senior Python Engineer,Acme Corp,Remote,$150k–$180k,https://remoteok.com/remote-jobs/123456,https://acme.example,,python, backend, aws,2025-09-01T12:34:56+00:00
...
```

---

## ⚠️ Notes
- Data comes from **Remote OK public API** (`/api` or `/api/{tag}`).
- CSV outputs are ignored in this repo (`.gitignore`).
- Be polite with usage; don’t hammer endpoints.

---

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
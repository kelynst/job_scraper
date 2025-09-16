# job_scraper

job_scraper is a Python command-line tool that fetches remote job listings from the Remote OK public API and saves them to a CSV file for analysis. It demonstrates how to use Python for APIs, filtering, and CSV export, making it a good portfolio project.

It uses the Remote OK API endpoint (https://remoteok.com/api). You can filter results with --tag (for example python, designer, marketing), filter by posting date with --since DAYS, and set a row limit with --limit N (default is 200, 0 means unlimited). Results are exported to a CSV file with columns: id, position, company, location, salary, url, company_url, logo, tags, and posted_utc.

## ✅ Features
- Scrapes **real job listings** from Remote OK’s public API
- Optional filters:  
  - `--tag` (e.g. python, designer, marketing)  
  - `--since DAYS` (limit to recent postings)  
  - `--limit N` (rows, 0 = unlimited)
- Exports clean CSV with columns:  
  `id, position, company, location, salary, url, company_url, logo, tags, posted_utc`
- Lightweight, no HTML parsing — uses the official API
- Beginner-friendly but extendable for portfolio or freelance work

Requirements: Python 3.10+, pip, and the requests package. A virtual environment is recommended. Your requirements.txt file should contain: requests.

Installation steps:
1. Clone the repository:  
   git clone https://github.com/kelynst/job_scraper.git
2. Navigate into the project folder:  
   cd job_scraper  
   This moves you into the directory where all the files live, so the next commands (like creating the virtual environment and installing dependencies) affect this project only.
3. Create and activate a virtual environment:  
   python3 -m venv .venv  
   This makes a self-contained Python environment inside the folder called `.venv` so the packages you install won’t interfere with other projects on your computer.  
To activate:
   - On macOS/Linux:  
     source .venv/bin/activate  
   - On Windows (PowerShell):  
     .venv\Scripts\Activate  

   When activated, your terminal will show `(.venv)` at the start of the line, meaning Python and pip will use this environment.

4. Install dependencies:  
   pip install -r requirements.txt  
   This installs the Python packages your project needs. In this case, only the `requests` library is required. If someone else clones your repo, this makes sure they get the exact packages needed to run the script.

Usage: run the scraper with
python scrape_jobs.py [--tag TAG] [--limit N] [--since DAYS] [--out FILE]

Arguments:
--tag TAG : filter by tag (e.g. python, designer, marketing)
--limit N : maximum number of rows (default 200, 0 = unlimited)
--since DAYS : only include jobs posted in the last N days (default 0 = no filter)
--out FILE : output CSV filename (default jobs.csv)

Examples:
python scrape_jobs.py
python scrape_jobs.py --tag python --since 7 --limit 100 --out python_week.csv
python scrape_jobs.py --tag designer --limit 50 --out design_sample.csv
python scrape_jobs.py --since 3 --limit 0 --out recent_jobs.csv

Output: the script writes a CSV file with the following columns: id, position, company, location, salary, url, company_url, logo, tags, posted_utc.

Example CSV row:
123456,Senior Python Engineer,Acme Corp,Remote,$150k–$180k,https://remoteok.com/remote-jobs/123456,https://acme.example,,python, backend, aws,2025-09-01T12:34:56+00:00

Notes: The API returns a metadata object as the first element, which is skipped automatically. Tag filtering is handled locally. CSVs, .venv, and cache files are ignored via .gitignore. Use responsibly and don’t send excessive requests.

License: MIT License — see LICENSE.
import csv
import argparse
import requests
from datetime import datetime, timezone, timedelta

API_URL = "https://remoteok.com/api"
USER_AGENT = "KelynJobScraper/1.1 (+https://github.com/kelynst)"  # safe, professional UA


def fetch_jobs(tag: str | None) -> list[dict]:
    """
    Fetch jobs from the Remote OK public API (single endpoint) and
    optionally filter by tag locally.
    """
    r = requests.get(API_URL, headers={"User-Agent": USER_AGENT}, timeout=30)
    r.raise_for_status()
    data = r.json()

    # First element is API metadata; jobs follow
    if isinstance(data, list) and data and isinstance(data[0], dict) and "legal" in data[0]:
        jobs = data[1:]
    else:
        jobs = data if isinstance(data, list) else []

    if tag:
        needle = tag.lower()

        def matches(j: dict) -> bool:
            tags = j.get("tags") or []
            tags_lower = [str(x).lower() for x in tags] if isinstance(tags, list) else [str(tags).lower()]
            # Also allow a loose match in position/description as a fallback
            text = f"{j.get('position', '')} {j.get('description', '')}".lower()
            return (needle in tags_lower) or (needle in text)

        jobs = [j for j in jobs if matches(j)]

    return jobs


def parse_iso_to_utc(date_str: str) -> datetime | None:
    """Parse API date string to timezone-aware UTC datetime."""
    if not date_str:
        return None
    try:
        # e.g. "2025-08-15T12:34:56+00:00" or "...Z"
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        return dt.astimezone(timezone.utc)
    except Exception:
        return None


def normalize_job(job: dict) -> dict:
    """Pick and normalize a few useful fields for CSV output."""
    def get(key, default=""):
        val = job.get(key, default)
        return "" if val is None else val

    posted_utc_dt = parse_iso_to_utc(get("date"))
    posted_iso = posted_utc_dt.isoformat() if posted_utc_dt else get("date")

    tags = job.get("tags") or []
    tags_str = ", ".join(tags) if isinstance(tags, list) else str(tags)

    return {
        "id": get("id"),
        "position": get("position"),
        "company": get("company"),
        "location": get("location"),
        "salary": get("salary"),
        "url": get("url"),
        "company_url": get("company_url"),
        "logo": get("logo"),
        "tags": tags_str,
        "posted_utc": posted_iso,
    }


def main():
    ap = argparse.ArgumentParser(description="Scrape Remote OK jobs to CSV (uses public API).")
    ap.add_argument("--tag", default="", help="Filter by tag, e.g. 'python', 'designer', 'marketing'. Empty = all.")
    ap.add_argument("--limit", type=int, default=200, help="Max rows to write (0 = unlimited).")
    ap.add_argument("--since", type=int, default=0,
                    help="Only include jobs posted in the last N days (0 = no date filter).")
    ap.add_argument("--out", default="jobs.csv", help="Output CSV filename.")
    args = ap.parse_args()

    tag = args.tag.strip().lower() or None
    limit = max(0, args.limit)
    days = max(0, args.since)

    print(f"Fetching jobs from Remote OK (tag={tag or 'ALL'})…")
    jobs = fetch_jobs(tag)
    print(f"Fetched {len(jobs)} job rows from API")

    # Optional date cutoff
    cutoff_utc = None
    if days:
        cutoff_utc = datetime.now(timezone.utc) - timedelta(days=days)
        print(f"Filtering to jobs posted since {cutoff_utc.isoformat()} (last {days} days)")

    written = 0
    fieldnames = [
        "id", "position", "company", "location", "salary",
        "url", "company_url", "logo", "tags", "posted_utc"
    ]

    with open(args.out, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for job in jobs:
            # Date filter if requested
            if cutoff_utc is not None:
                posted_dt = parse_iso_to_utc(job.get("date", ""))
                if not posted_dt or posted_dt < cutoff_utc:
                    continue

            writer.writerow(normalize_job(job))
            written += 1
            if limit and written >= limit:
                break

    print(f"Done. Wrote {written} rows to {args.out}")


if __name__ == "__main__":
    main()
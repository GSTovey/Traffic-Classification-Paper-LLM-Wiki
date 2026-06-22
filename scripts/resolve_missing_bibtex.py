#!/usr/bin/env python3
"""
resolve_missing_bibtex.py
=========================
Resolve the 33 papers that CrossRef couldn't find, using DBLP API.
DBLP is the authoritative source for CS conference/journal metadata.

Usage:
  python3 scripts/resolve_missing_bibtex.py
"""

import json
import subprocess
import sys
import time
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
BIB_FILE = VAULT_ROOT / "bibliography.json"
DBLP_DELAY = 0.3  # seconds between requests


def dblp_search(title: str, year: int) -> dict:
    """Search DBLP for a paper by title."""
    # Clean title for search
    import re
    clean = re.sub(r'[^\w\s]', ' ', title).strip()
    clean = re.sub(r'\s+', '+', clean)

    url = f"https://dblp.org/search/publ/api?q={clean}&format=json&h=3"

    try:
        result = subprocess.run(
            ["curl", "-s", "-f", "--max-time", "15", url],
            capture_output=True, text=True, timeout=20
        )
        if result.returncode != 0 or not result.stdout:
            return None

        data = json.loads(result.stdout)
        hits = data.get("result", {}).get("hits", {}).get("hit", [])
        if not hits:
            return None

        # Find best match by title similarity + year
        title_lower = title.lower().strip()
        best = None
        best_score = 0

        for hit in hits:
            info = hit.get("info", {})
            item_title = info.get("title", "").lower().strip().rstrip(".")
            item_year = int(info.get("year", "0"))

            # Title word overlap
            words1 = set(re.findall(r'\w+', title_lower))
            words2 = set(re.findall(r'\w+', item_title))
            if not words1:
                continue
            overlap = len(words1 & words2) / max(len(words1), 1)

            # Year match bonus
            year_match = 1.0 if item_year == year else 0.5

            score = overlap * year_match

            if score > best_score:
                best_score = score
                best = info

        if best and best_score >= 0.5:
            return best
        return None

    except Exception as e:
        print(f"    DBLP error: {e}")
        return None


def dblp_to_fields(info: dict) -> dict:
    """Convert DBLP info to bibliography fields."""
    import re
    result = {}

    # Authors
    authors_data = info.get("authors", {}).get("author", [])
    if isinstance(authors_data, dict):
        authors_data = [authors_data]
    authors = []
    for a in authors_data:
        name = a.get("text", "")
        # Remove numeric suffix (e.g., "Tao Wang 0012" → "Tao Wang")
        name = re.sub(r'\s+\d{4,}$', '', name)
        # Convert "First Last" to "Last, First"
        parts = name.strip().split()
        if len(parts) >= 2:
            authors.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
        elif parts:
            authors.append(parts[0])
    if authors:
        result["authors"] = authors

    # Venue → booktitle
    venue = info.get("venue", "")
    if venue:
        result["booktitle"] = venue

    # Pages
    pages = info.get("pages", "")
    if pages:
        result["pages"] = pages

    # Entry type
    pub_type = info.get("type", "")
    if "Conference" in pub_type or "Workshop" in pub_type:
        result["entry_type"] = "inproceedings"
    elif "Journal" in pub_type:
        result["entry_type"] = "article"
        result["journal"] = venue
        result.pop("booktitle", None)

    # URL (prefer DBLP ee link which is usually the official page)
    url = info.get("ee", "")
    if url:
        result["url"] = url

    return result


def main():
    bib = json.loads(BIB_FILE.read_text(encoding="utf-8"))

    missing = [i for i, entry in enumerate(bib) if entry.get("metadata_source") == "note"]
    print(f"Resolving {len(missing)} papers via DBLP...")

    resolved = 0
    still_missing = []

    for idx in missing:
        entry = bib[idx]
        title = entry.get("title", "")
        year = entry.get("year", 0)

        print(f"  [{idx+1}] {title[:60]}...")

        info = dblp_search(title, year)
        time.sleep(DBLP_DELAY)

        if info:
            fields = dblp_to_fields(info)
            for key, value in fields.items():
                if key == "authors":
                    entry["authors"] = value
                elif key == "entry_type":
                    if value != "misc":
                        entry["entry_type"] = value
                elif not entry.get(key):
                    entry[key] = value

            # If we got a booktitle/journal from DBLP, also try to get DOI via CrossRef
            if not entry.get("doi"):
                # Try DBLP DOI
                dblp_url = info.get("ee", "")
                if "doi.org" in dblp_url:
                    entry["doi"] = dblp_url.replace("https://doi.org/", "")

            entry["metadata_source"] = "dblp"
            resolved += 1
            print(f"    → RESOLVED via DBLP: {info.get('venue', '')}, pages={info.get('pages', '')}")
        else:
            still_missing.append(entry)
            print(f"    → NOT FOUND in DBLP")

    # Write back
    with open(BIB_FILE, "w", encoding="utf-8") as f:
        json.dump(bib, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"DBLP RESOLUTION SUMMARY")
    print(f"{'='*50}")
    print(f"Resolved:        {resolved}/{len(missing)}")
    print(f"Still missing:   {len(still_missing)}")

    if still_missing:
        print(f"\nPapers still needing manual review:")
        for entry in still_missing:
            print(f"  - {entry['source_file']}: {entry['title'][:60]}")


if __name__ == "__main__":
    main()

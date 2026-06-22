#!/usr/bin/env python3
"""
generate_bibliography.py
========================
Generate bibliography.json for all papers in the Traffic_Papers knowledge base.

Strategy:
  Pass 1: Extract structured metadata from paper note YAML frontmatter
  Pass 2: Enrich via CrossRef API (official publisher-verified data)
  Pass 3: Extract abstracts from parsed markdown (fallback)
  Pass 4: Merge and write bibliography.json

CrossRef is the authoritative source for:
  - pages, volume, number, publisher
  - official booktitle (conference proceedings name)
  - official journal name
  - DOI resolution and URL

Usage:
  python scripts/generate_bibliography.py [--dry-run] [--skip-api]
"""

import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

# --- Configuration ---
VAULT_ROOT = Path(__file__).resolve().parent.parent
NOTES_DIR = VAULT_ROOT / "03-paper-notes"
PARSED_DIR = VAULT_ROOT / "02-parsed-markdown"
OUTPUT_FILE = VAULT_ROOT / "bibliography.json"

CROSSREF_BASE = "https://api.crossref.org"
CROSSREF_MAILTO = "traffic-papers-kb@research.local"  # polite pool
CROSSREF_DELAY = 0.1  # seconds between requests (polite pool allows 50/s, we use 10/s to be safe)
MAX_RETRIES = 2

# --- Venue classification ---
# Tier 1 conferences → entry_type = "inproceedings"
CONFERENCE_KEYWORDS = [
    "CCS", "S&P", "USENIX", "NDSS", "SIGCOMM", "INFOCOM", "AAAI", "NeurIPS",
    "NIPS", "ICML", "WWW", "KDD", "SIGKDD", "IMC", "IWQoS", "ICASSP",
    "HPCC", "ICMLA", "CNSM", "INCAS", "EITCE", "ICAACE"
]

# Journals → entry_type = "article"
JOURNAL_KEYWORDS = [
    "TIFS", "TSC", "TDSC", "TON", "TNET", "COMST", "TNSM", "TBD",
    "JPDC", "JCN", "JIoT", "JKSU", "JNSM", "ESWA", "CCPE", "CS"
]


def classify_entry_type(venue_str: str) -> str:
    """Classify venue as inproceedings (conference) or article (journal)."""
    v = venue_str.upper()
    for kw in JOURNAL_KEYWORDS:
        if kw.upper() in v:
            return "article"
    for kw in CONFERENCE_KEYWORDS:
        if kw.upper() in v:
            return "inproceedings"
    # Default: if venue contains "conference", "symposium", "workshop" → inproceedings
    if any(w in v for w in ["CONFERENCE", "SYMPOSIUM", "WORKSHOP", "ARXIV"]):
        return "misc"
    return "inproceedings"  # default for unknown


def generate_citation_key(authors: list, year: int, title: str) -> str:
    """Generate citation key: {firstauthor_last}{year}{first_keyword}"""
    if not authors:
        lastname = "unknown"
    else:
        # Handle "First Last" or "Last, First" format
        name = authors[0].strip()
        if "," in name:
            lastname = name.split(",")[0].strip().lower()
        else:
            parts = name.split()
            lastname = parts[-1].lower() if parts else "unknown"

    # Clean lastname: only alphanumeric
    lastname = re.sub(r'[^a-z]', '', lastname)

    # First meaningful word from title (skip articles/prepositions)
    stop_words = {"a", "an", "the", "on", "in", "of", "for", "to", "with", "and", "by", "from"}
    title_words = re.findall(r'[a-zA-Z]+', title)
    keyword = "paper"
    for w in title_words:
        if w.lower() not in stop_words and len(w) > 2:
            keyword = w.lower()
            break

    key = f"{lastname}{year}{keyword}"

    # Truncate if too long
    if len(key) > 40:
        key = key[:40]

    return key


def normalize_doi(doi: str) -> str:
    """Normalize DOI to bare form (no URL prefix)."""
    if not doi or doi.lower() in ("unknown", "", "none"):
        return ""
    doi = doi.strip()
    doi = re.sub(r'^https?://(dx\.)?doi\.org/', '', doi, flags=re.IGNORECASE)
    return doi


# ============================================================
# Pass 1: Extract from paper note frontmatter
# ============================================================

def parse_yaml_frontmatter(filepath: Path) -> dict:
    """Parse YAML frontmatter from a markdown file (simple parser, no PyYAML needed)."""
    text = filepath.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}

    end = text.find("---", 3)
    if end == -1:
        return {}

    yaml_text = text[3:end].strip()
    result = {}
    current_key = None
    current_list = None

    for line in yaml_text.split("\n"):
        line_stripped = line.strip()

        # List item
        if line_stripped.startswith("- ") and current_key:
            if current_list is None:
                current_list = []
            item = line_stripped[2:].strip().strip('"').strip("'")
            current_list.append(item)
            result[current_key] = current_list
            continue

        # Key-value pair
        if ":" in line_stripped and not line_stripped.startswith("- "):
            # Save any pending list
            current_list = None

            colon_pos = line_stripped.index(":")
            key = line_stripped[:colon_pos].strip()
            value = line_stripped[colon_pos + 1:].strip()

            current_key = key

            if value == "" or value == "[]":
                result[key] = []
                current_list = []
            elif value.startswith("[") and value.endswith("]"):
                # Inline list
                items = value[1:-1].split(",")
                result[key] = [i.strip().strip('"').strip("'") for i in items if i.strip()]
            else:
                result[key] = value.strip('"').strip("'")
                current_list = None

    return result


def pass1_extract_notes() -> dict:
    """Extract metadata from all paper notes."""
    papers = {}
    note_files = sorted(NOTES_DIR.glob("*.md"))

    print(f"Pass 1: Extracting metadata from {len(note_files)} paper notes...")

    for fpath in note_files:
        meta = parse_yaml_frontmatter(fpath)
        if not meta or meta.get("type") != "paper":
            continue

        filename = fpath.stem
        title = meta.get("title_original", "")
        authors = meta.get("authors", [])
        if isinstance(authors, str):
            authors = [a.strip() for a in authors.split(",")]

        year = int(meta.get("year", 0)) if str(meta.get("year", "0")).isdigit() else 0
        venue = meta.get("venue", "")
        doi = normalize_doi(meta.get("doi", ""))
        url = meta.get("url", "")
        if url and url.lower() in ("unknown", ""):
            url = ""

        entry_type = classify_entry_type(venue)
        citation_key = generate_citation_key(authors, year, title)

        papers[filename] = {
            "citation_key": citation_key,
            "entry_type": entry_type,
            "title": title,
            "authors": authors,
            "year": year,
            "venue_raw": venue,
            "doi": doi,
            "url": url,
            "booktitle": None,   # will be filled by CrossRef
            "journal": None,     # will be filled by CrossRef
            "pages": None,
            "volume": None,
            "number": None,
            "publisher": None,
            "abstract": "",
            "source_file": f"{filename}.pdf",
            "note_file": f"{filename}.md",
            "metadata_source": "note",
            "crossref_status": "pending"
        }

    print(f"  → Extracted {len(papers)} papers")
    doi_count = sum(1 for p in papers.values() if p["doi"])
    print(f"  → {doi_count} have DOI, {len(papers) - doi_count} need title search")
    return papers


# ============================================================
# Pass 2: CrossRef API enrichment
# ============================================================

def crossref_get(url: str) -> dict:
    """Make a CrossRef API request using curl (subprocess) with polite header."""
    for attempt in range(MAX_RETRIES + 1):
        try:
            result = subprocess.run(
                [
                    "curl", "-s", "-f", "--max-time", "30",
                    "-H", f"User-Agent: TrafficPapersKB/1.0 (mailto:{CROSSREF_MAILTO})",
                    "-H", "Accept: application/json",
                    url
                ],
                capture_output=True, text=True, timeout=35
            )
            if result.returncode == 0 and result.stdout:
                return json.loads(result.stdout)
            if result.returncode == 22:  # HTTP error (404 etc.)
                return None
            if attempt < MAX_RETRIES:
                time.sleep(1)
                continue
            return None
        except (subprocess.TimeoutExpired, json.JSONDecodeError) as e:
            if attempt < MAX_RETRIES:
                time.sleep(1)
                continue
            print(f"    Error: {e}")
            return None
    return None


def extract_crossref_item(item: dict) -> dict:
    """Extract BibTeX-relevant fields from a CrossRef work item."""
    result = {}

    # Entry type
    item_type = item.get("type", "")
    if item_type in ("proceedings-article", "conference-paper"):
        result["entry_type"] = "inproceedings"
    elif item_type in ("journal-article",):
        result["entry_type"] = "article"
    elif item_type in ("book-chapter",):
        result["entry_type"] = "incollection"
    else:
        result["entry_type"] = "misc"

    # Title
    titles = item.get("title", [])
    if titles:
        result["title"] = titles[0]

    # Authors
    authors = []
    for author in item.get("author", []):
        family = author.get("family", "")
        given = author.get("given", "")
        if family:
            authors.append(f"{family}, {given}" if given else family)
    if authors:
        result["authors"] = authors

    # Year
    pub_date = item.get("published-print") or item.get("published-online") or item.get("created")
    if pub_date:
        date_parts = pub_date.get("date-parts", [[]])[0]
        if date_parts:
            result["year"] = date_parts[0]

    # Container (booktitle or journal)
    container = item.get("container-title", [])
    if container:
        if result.get("entry_type") == "article":
            result["journal"] = container[0]
        else:
            result["booktitle"] = container[0]

    # Pages
    pages = item.get("page", "")
    if pages:
        result["pages"] = pages

    # Volume / Number
    volume = item.get("volume", "")
    if volume:
        result["volume"] = str(volume)
    number = item.get("issue", "")
    if number:
        result["number"] = str(number)

    # Publisher
    publisher = item.get("publisher", "")
    if publisher:
        result["publisher"] = publisher

    # DOI
    doi = item.get("DOI", "")
    if doi:
        result["doi"] = doi

    # URL
    result["url"] = item.get("URL", f"https://doi.org/{doi}") if doi else ""

    # Abstract
    abstract = item.get("abstract", "")
    if abstract:
        # Strip HTML tags
        abstract = re.sub(r'<[^>]+>', '', abstract).strip()
        result["abstract"] = abstract

    return result


def search_crossref_by_doi(doi: str) -> dict:
    """Search CrossRef by DOI."""
    url = f"{CROSSREF_BASE}/works/{urllib.parse.quote(doi, safe='')}"
    data = crossref_get(url)
    if data and "message" in data:
        return extract_crossref_item(data["message"])
    return None


def search_crossref_by_title(title: str, year: int) -> dict:
    """Search CrossRef by title (+ year filter for precision)."""
    # Clean title for search
    clean_title = re.sub(r'[^\w\s]', ' ', title).strip()
    clean_title = re.sub(r'\s+', ' ', clean_title)

    params = {
        "query.title": clean_title,
        "rows": "3",
        "select": "DOI,title,author,type,container-title,published-print,published-online,page,volume,issue,publisher,URL,abstract"
    }
    if year > 0:
        params["filter"] = f"from-pub-date:{year},until-pub-date:{year}"

    url = f"{CROSSREF_BASE}/works?{urllib.parse.urlencode(params)}"
    data = crossref_get(url)

    if not data or "message" not in data:
        return None

    items = data["message"].get("items", [])
    if not items:
        return None

    # Find best match by title similarity
    title_lower = title.lower().strip()
    best = None
    best_score = 0

    for item in items:
        item_titles = item.get("title", [])
        if not item_titles:
            continue
        item_title = item_titles[0].lower().strip()

        # Simple similarity: ratio of shared words
        words1 = set(re.findall(r'\w+', title_lower))
        words2 = set(re.findall(r'\w+', item_title))
        if not words1:
            continue
        overlap = len(words1 & words2) / max(len(words1), 1)

        if overlap > best_score:
            best_score = overlap
            best = item

    if best and best_score >= 0.6:  # 60% word overlap threshold
        return extract_crossref_item(best)

    return None


def pass2_crossref_enrichment(papers: dict) -> dict:
    """Enrich paper metadata via CrossRef API."""
    total = len(papers)
    doi_papers = {k: v for k, v in papers.items() if v["doi"]}
    search_papers = {k: v for k, v in papers.items() if not v["doi"]}

    print(f"\nPass 2: CrossRef API enrichment...")
    print(f"  → {len(doi_papers)} papers with DOI (direct lookup)")
    print(f"  → {len(search_papers)} papers without DOI (title search)")

    enriched = 0
    failed = 0

    # Phase 2a: DOI lookup
    print(f"\n  Phase 2a: DOI lookup ({len(doi_papers)} papers)...")
    for i, (filename, paper) in enumerate(doi_papers.items()):
        result = search_crossref_by_doi(paper["doi"])
        time.sleep(CROSSREF_DELAY)

        if result:
            _merge_crossref_result(paper, result)
            paper["crossref_status"] = "resolved"
            enriched += 1
        else:
            paper["crossref_status"] = "doi_not_found"
            failed += 1

        if (i + 1) % 10 == 0:
            print(f"    {i + 1}/{len(doi_papers)} processed (enriched: {enriched})")

    print(f"  Phase 2a done: {enriched} enriched, {failed} not found")

    # Phase 2b: Title search for papers without DOI
    title_enriched = 0
    title_failed = 0
    print(f"\n  Phase 2b: Title search ({len(search_papers)} papers)...")
    for i, (filename, paper) in enumerate(search_papers.items()):
        result = search_crossref_by_title(paper["title"], paper["year"])
        time.sleep(CROSSREF_DELAY)

        if result:
            _merge_crossref_result(paper, result)
            paper["crossref_status"] = "title_matched"
            title_enriched += 1
        else:
            paper["crossref_status"] = "not_found"
            title_failed += 1

        if (i + 1) % 10 == 0:
            print(f"    {i + 1}/{len(search_papers)} processed (enriched: {title_enriched})")

    print(f"  Phase 2b done: {title_enriched} enriched, {title_failed} not found")

    total_enriched = enriched + title_enriched
    total_failed = failed + title_failed
    print(f"\n  Pass 2 summary: {total_enriched}/{total} enriched, {total_failed} need manual review")

    return papers


def _merge_crossref_result(paper: dict, result: dict):
    """Merge CrossRef result into paper dict (only fill None/empty fields)."""
    for field in ["booktitle", "journal", "pages", "volume", "number", "publisher"]:
        if result.get(field) and not paper.get(field):
            paper[field] = result[field]

    # Always update DOI if CrossRef found one and we don't have it
    if result.get("doi") and not paper["doi"]:
        paper["doi"] = result["doi"]

    # Update URL
    if result.get("url") and not paper["url"]:
        paper["url"] = result["url"]

    # Update entry_type if CrossRef has a better classification
    if result.get("entry_type") and result["entry_type"] != "misc":
        paper["entry_type"] = result["entry_type"]

    # Update abstract if we don't have one
    if result.get("abstract") and not paper["abstract"]:
        paper["abstract"] = result["abstract"]

    # Update authors if CrossRef has them (they're usually more standardized)
    if result.get("authors"):
        paper["authors"] = result["authors"]


# ============================================================
# Pass 3: Extract abstracts from parsed markdown
# ============================================================

def extract_abstract_from_md(text: str) -> str:
    """Extract abstract from parsed markdown text."""
    # Try multiple patterns
    patterns = [
        r'(?:^|\n)\s*(?:Abstract|ABSTRACT)\s*[-–—:]\s*\n?(.*?)(?:\n\s*(?:#|Keywords|KEYWORDS|Introduction|INTRODUCTION|1\s*[\.\)]\s*Introduction|I\.\s*Introduction))',
        r'(?:^|\n)\s*#\s*(?:Abstract|ABSTRACT)\s*\n(.*?)(?:\n\s*#)',
        r'(?:^|\n)\s*Abstract\s*[-–—]\s*(.*?)(?:\n\s*\n)',
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            abstract = match.group(1).strip()
            # Clean up
            abstract = re.sub(r'\s+', ' ', abstract)
            abstract = abstract.strip('- –—')
            if len(abstract) > 50:  # minimum reasonable abstract length
                return abstract

    return ""


def pass3_extract_abstracts(papers: dict) -> dict:
    """Extract abstracts from parsed markdown for papers still missing them."""
    missing = {k: v for k, v in papers.items() if not v["abstract"]}
    print(f"\nPass 3: Extracting abstracts from parsed markdown ({len(missing)} papers)...")

    found = 0
    for filename, paper in missing.items():
        parsed_file = PARSED_DIR / f"{filename}.md"
        if not parsed_file.exists():
            continue

        text = parsed_file.read_text(encoding="utf-8")
        abstract = extract_abstract_from_md(text)
        if abstract:
            paper["abstract"] = abstract
            found += 1

    print(f"  → Found {found} abstracts from parsed markdown")
    return papers


# ============================================================
# Pass 4: Generate output
# ============================================================

def generate_citation_keys(papers: dict) -> dict:
    """Ensure all citation keys are unique."""
    seen = {}
    for filename, paper in papers.items():
        key = paper["citation_key"]
        if key in seen:
            # Add filename suffix to disambiguate
            seen[key] += 1
            paper["citation_key"] = f"{key}_{seen[key]}"
        else:
            seen[key] = 1
    return papers


def pass4_write_output(papers: dict):
    """Write bibliography.json."""
    papers = generate_citation_keys(papers)

    # Convert to list sorted by year (desc) then first author
    entries = list(papers.values())
    entries.sort(key=lambda p: (-p["year"], p["authors"][0] if p["authors"] else ""))

    # Remove internal tracking fields from output
    output = []
    for entry in entries:
        out = {k: v for k, v in entry.items() if k != "venue_raw" and k != "crossref_status"}
        output.append(out)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\nPass 4: Written {len(output)} entries to {OUTPUT_FILE}")

    # Summary statistics
    crossref_resolved = sum(1 for p in papers.values() if p["crossref_status"] in ("resolved", "title_matched"))
    crossref_notfound = sum(1 for p in papers.values() if p["crossref_status"] in ("not_found", "doi_not_found"))
    has_abstract = sum(1 for p in papers.values() if p["abstract"])
    has_doi = sum(1 for p in papers.values() if p["doi"])
    has_pages = sum(1 for p in papers.values() if p["pages"])
    has_publisher = sum(1 for p in papers.values() if p["publisher"])
    has_booktitle = sum(1 for p in papers.values() if p.get("booktitle"))
    has_journal = sum(1 for p in papers.values() if p.get("journal"))

    print(f"\n{'='*50}")
    print(f"BIBLIOGRAPHY GENERATION SUMMARY")
    print(f"{'='*50}")
    print(f"Total entries:          {len(output)}")
    print(f"CrossRef enriched:      {crossref_resolved}")
    print(f"CrossRef not found:     {crossref_notfound} (need manual review)")
    print(f"With DOI:               {has_doi}")
    print(f"With abstract:          {has_abstract}")
    print(f"With pages:             {has_pages}")
    print(f"With publisher:         {has_publisher}")
    print(f"With booktitle (conf):  {has_booktitle}")
    print(f"With journal:           {has_journal}")
    print(f"{'='*50}")

    if crossref_notfound > 0:
        print(f"\nPapers needing manual review:")
        for filename, paper in papers.items():
            if paper["crossref_status"] in ("not_found", "doi_not_found"):
                print(f"  - {filename}: {paper['title'][:60]}...")

    return output


# ============================================================
# Main
# ============================================================

def main():
    dry_run = "--dry-run" in sys.argv
    skip_api = "--skip-api" in sys.argv

    if dry_run:
        print("[DRY RUN] Will not write output file")

    # Pass 1
    papers = pass1_extract_notes()

    # Pass 2
    if not skip_api:
        papers = pass2_crossref_enrichment(papers)
    else:
        print("\nPass 2: SKIPPED (--skip-api flag)")

    # Pass 3
    papers = pass3_extract_abstracts(papers)

    # Pass 4
    if not dry_run:
        pass4_write_output(papers)
    else:
        print(f"\n[DRY RUN] Would write {len(papers)} entries")
        # Still print summary
        pass4_write_output(papers)


if __name__ == "__main__":
    main()

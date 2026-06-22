#!/usr/bin/env python3
"""Resolve missing BibTeX entries via OpenAlex API."""
import json, subprocess, sys, time, re, urllib.parse
from pathlib import Path

VAULT_ROOT = Path(__file__).resolve().parent.parent
BIB_FILE = VAULT_ROOT / "bibliography.json"

def openalex_search(title: str, year: int):
    clean = re.sub(r'[^\w\s]', ' ', title).strip()
    url = f"https://api.openalex.org/works?search={urllib.parse.quote(clean)}&per_page=3"
    try:
        r = subprocess.run(["curl","-s","-f","--max-time","15",url], capture_output=True, text=True, timeout=20)
        if r.returncode != 0 or not r.stdout: return None
        data = json.loads(r.stdout)
        results = data.get("results", [])
        if not results: return None
        # Find best match
        title_lower = title.lower().strip()
        best, best_score = None, 0
        for item in results:
            item_title = (item.get("title") or "").lower().strip()
            w1 = set(re.findall(r'\w+', title_lower))
            w2 = set(re.findall(r'\w+', item_title))
            if not w1: continue
            overlap = len(w1 & w2) / max(len(w1), 1)
            yr = item.get("publication_year", 0)
            score = overlap * (1.0 if yr == year else 0.6)
            if score > best_score:
                best_score = score
                best = item
        if best and best_score >= 0.5:
            return best
        return None
    except: return None

def extract_openalex(item: dict) -> dict:
    r = {}
    # DOI
    doi = item.get("doi", "")
    if doi:
        r["doi"] = doi.replace("https://doi.org/", "")

    # Authors
    authorships = item.get("authorships", [])
    authors = []
    for a in authorships:
        name = a.get("author", {}).get("display_name", "")
        if name:
            parts = name.strip().split()
            if len(parts) >= 2:
                authors.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
            elif parts:
                authors.append(parts[0])
    if authors:
        r["authors"] = authors

    # Venue: primary_location
    loc = item.get("primary_location", {})
    if loc:
        source = loc.get("source", {})
        if source:
            source_name = source.get("display_name", "")
            if source_name:
                r["booktitle"] = source_name

    # Abstract from inverted index
    abstract_idx = item.get("abstract_inverted_index")
    if abstract_idx:
        word_positions = []
        for word, positions in abstract_idx.items():
            for pos in positions:
                word_positions.append((pos, word))
        word_positions.sort()
        r["abstract"] = " ".join(w for _, w in word_positions)

    # Pages
    biblio = item.get("biblio", {})
    if biblio:
        first_page = biblio.get("first_page", "")
        last_page = biblio.get("last_page", "")
        if first_page:
            r["pages"] = f"{first_page}-{last_page}" if last_page else first_page
        vol = biblio.get("volume", "")
        if vol:
            r["volume"] = str(vol)
        iss = biblio.get("issue", "")
        if iss:
            r["number"] = str(iss)

    # Entry type
    t = item.get("type", "")
    if "journal" in t:
        r["entry_type"] = "article"
    elif "proceedings" in t or "conference" in t:
        r["entry_type"] = "inproceedings"

    return r

def main():
    bib = json.loads(BIB_FILE.read_text(encoding="utf-8"))
    missing = [i for i, e in enumerate(bib) if e.get("metadata_source") == "note"]
    print(f"Resolving {len(missing)} papers via OpenAlex...")

    resolved = 0
    still_missing = []
    for idx in missing:
        entry = bib[idx]
        title, year = entry.get("title",""), entry.get("year",0)
        print(f"  [{idx+1}] {title[:60]}...")
        item = openalex_search(title, year)
        time.sleep(0.3)
        if item:
            fields = extract_openalex(item)
            for k, v in fields.items():
                if k == "authors":
                    entry["authors"] = v
                elif k == "entry_type":
                    if v != "misc": entry["entry_type"] = v
                elif not entry.get(k):
                    entry[k] = v
            entry["metadata_source"] = "openalex"
            resolved += 1
            info_parts = []
            if fields.get("booktitle"): info_parts.append(fields["booktitle"])
            if fields.get("doi"): info_parts.append(f"doi={fields['doi'][:30]}")
            if fields.get("pages"): info_parts.append(f"pp.{fields['pages']}")
            print(f"    → RESOLVED: {', '.join(info_parts)}")
        else:
            still_missing.append(entry)
            print(f"    → NOT FOUND")

    with open(BIB_FILE, "w", encoding="utf-8") as f:
        json.dump(bib, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print(f"OPENALEX RESOLUTION: {resolved}/{len(missing)} resolved, {len(still_missing)} still missing")
    if still_missing:
        print(f"\nStill missing:")
        for e in still_missing:
            print(f"  - {e['source_file']}: {e['title'][:60]}")

if __name__ == "__main__":
    main()

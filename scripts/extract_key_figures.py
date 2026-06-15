#!/usr/bin/env python3
"""
Key Figure Extractor
====================
Scans MinerU output for all 93 papers, scores each image using a three-layer
heuristic (caption keywords, sub-type signal, bbox area), selects the top 1-2
"framework / architecture" figures per paper, copies them to a unified gallery,
and generates a summary Markdown file.

Incremental: a manifest.json tracks which papers have been processed.
Deleting a figure from the Markdown prevents it from being re-added on re-run.

Pure-Python stdlib — no third-party dependencies.
"""

from __future__ import annotations

import json
import logging
import os
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

# ─── Paths ────────────────────────────────────────────────────────────────────

VAULT_ROOT = Path(__file__).resolve().parent.parent
MINERU_DIR = VAULT_ROOT / "01-mineru-output"
OUTPUT_DIR = VAULT_ROOT / "10-outputs" / "key-figures"
IMAGES_DIR = OUTPUT_DIR / "images"
MARKDOWN   = OUTPUT_DIR / "all-key-figures.md"
MANIFEST   = OUTPUT_DIR / "manifest.json"

# ─── Scoring weights ──────────────────────────────────────────────────────────

# Layer 1: Caption keyword matching
HIGH_KEYWORDS   = [
    "framework", "architecture", "overview", "pipeline",
    "proposed method", "proposed framework", "proposed architecture",
    "system overview", "method overview", "model overview",
    "overall architecture", "overall framework", "overall pipeline",
]
MID_KEYWORDS    = [
    "design of", "workflow", "structure of", "schematic",
    "illustration of", "high-level", "high level",
    "end-to-end", "network architecture",
]
LOW_KEYWORDS    = [
    "model architecture", "the model", "block", "layer", "module",
    "diagram", "approach", "network", "transformer", "encoder",
    "decoder", "attention", "embedding",
]

HIGH_SCORE = 10
MID_SCORE  = 7
LOW_SCORE  = 4

# Layer 2: Sub-type signal
SUB_TYPE_SCORES = {
    "flowchart":     3,
    "natural_image": -2,
    "text_image":    -5,
}

# Layer 3: Bbox area thresholds
AREA_THRESHOLDS = [
    (100_000, 2),
    (50_000,  1),
    (5_000,   0),
    (0,      -3),
]

SCORE_THRESHOLD = 5
MAX_FIGURES_PER_PAPER = 2

# ─── Logging ──────────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─── Helpers ──────────────────────────────────────────────────────────────────


def find_content_list(paper_dir: Path) -> Path | None:
    """Return the v1 *_content_list.json path (not _v2)."""
    candidates = sorted(paper_dir.glob("*_content_list.json"))
    for c in candidates:
        if "_content_list_v2" not in c.name:
            return c
    return None


def bbox_area(bbox: list[float]) -> float:
    """Compute area from [x1, y1, x2, y2]."""
    if len(bbox) != 4:
        return 0
    x1, y1, x2, y2 = bbox
    return max(0, x2 - x1) * max(0, y2 - y1)


def score_caption(caption_parts: list[str]) -> int:
    """Layer 1: Score based on caption keyword presence."""
    text = " ".join(caption_parts).lower()
    if not text.strip():
        return 0
    best = 0
    for kw in HIGH_KEYWORDS:
        if kw in text:
            best = max(best, HIGH_SCORE)
    for kw in MID_KEYWORDS:
        if kw in text:
            best = max(best, MID_SCORE)
    for kw in LOW_KEYWORDS:
        if kw in text:
            best = max(best, LOW_SCORE)
    return best


def score_sub_type(sub_type: str | None) -> int:
    """Layer 2: Score based on MinerU sub_type classification."""
    if not sub_type:
        return 0
    return SUB_TYPE_SCORES.get(sub_type, 0)


def score_area(bbox: list[float]) -> int:
    """Layer 3: Score based on bbox area."""
    area = bbox_area(bbox)
    for threshold, score in AREA_THRESHOLDS:
        if area >= threshold:
            return score
    return AREA_THRESHOLDS[-1][1]


def compute_score(item: dict) -> int:
    """Three-layer composite score for a single image entry."""
    s1 = score_caption(item.get("image_caption", []))
    s2 = score_sub_type(item.get("sub_type"))
    s3 = score_area(item.get("bbox", []))
    return s1 + s2 + s3


def extract_figure_label(caption_parts: list[str]) -> str:
    """Extract 'Figure N' or 'Fig. N' label from caption, if present."""
    text = " ".join(caption_parts).strip()
    m = re.match(r"(Fig(?:ure|\.)\s*\d+[a-z]?)", text, re.IGNORECASE)
    return m.group(1) if m else "Figure"


def extract_caption_text(caption_parts: list[str]) -> str:
    """Return cleaned caption text (strip Figure N prefix)."""
    text = " ".join(caption_parts).strip()
    # Remove leading "Figure N:" or "Fig. N:" prefix
    text = re.sub(r"^(Fig(?:ure|\.)\s*\d+[a-z]?\s*[:\-–—]\s*)", "", text, flags=re.IGNORECASE)
    return text.strip()


def unique_image_name(paper_name: str, figure_label: str, img_path: str) -> str:
    """Generate a unique, readable filename for the copied image."""
    # Use the original hash filename to avoid collisions
    original_name = Path(img_path).stem  # e.g. "c283ff368d8dd..."
    # Sanitize paper name for filesystem
    safe_paper = re.sub(r"[^\w\-]", "_", paper_name)[:80]
    safe_label = re.sub(r"[^\w]", "_", figure_label)
    return f"{safe_paper}__{safe_label}__{original_name[:16]}.jpg"

# ─── Core logic ───────────────────────────────────────────────────────────────


def process_paper(paper_dir: Path) -> list[dict]:
    """
    Process a single paper directory.

    Returns a list of selected figure dicts:
        [{"img_path", "original_path", "caption", "figure_label", "score"}, ...]
    """
    content_list_path = find_content_list(paper_dir)
    if not content_list_path:
        log.warning("No content_list.json found in %s", paper_dir.name)
        return []

    with open(content_list_path, encoding="utf-8") as f:
        data = json.load(f)

    # Filter to image entries only
    images = [item for item in data if item.get("type") == "image"]
    if not images:
        return []

    # Score all images
    scored = []
    for img in images:
        score = compute_score(img)
        scored.append((score, img))

    # Sort by score descending, then by area descending as tiebreaker
    scored.sort(key=lambda x: (x[0], bbox_area(x[1].get("bbox", []))), reverse=True)

    # Select top figures with score >= threshold
    selected = []
    for score, img in scored:
        if len(selected) >= MAX_FIGURES_PER_PAPER:
            break
        if score >= SCORE_THRESHOLD:
            selected.append({
                "img_path": img.get("img_path", ""),
                "original_path": str(paper_dir / img.get("img_path", "")),
                "caption": img.get("image_caption", []),
                "figure_label": extract_figure_label(img.get("image_caption", [])),
                "sub_type": img.get("sub_type"),
                "score": score,
            })

    # Fallback 1: if no candidates >= threshold, pick largest flowchart
    if not selected:
        flowcharts = [
            (score, img) for score, img in scored
            if img.get("sub_type") == "flowchart"
        ]
        if flowcharts:
            flowcharts.sort(key=lambda x: bbox_area(x[1].get("bbox", [])), reverse=True)
            _, img = flowcharts[0]
            selected.append({
                "img_path": img.get("img_path", ""),
                "original_path": str(paper_dir / img.get("img_path", "")),
                "caption": img.get("image_caption", []),
                "figure_label": extract_figure_label(img.get("image_caption", [])),
                "sub_type": img.get("sub_type"),
                "score": score,
            })

    # Fallback 2: if still nothing, pick the largest image
    if not selected:
        by_area = sorted(images, key=lambda x: bbox_area(x.get("bbox", [])), reverse=True)
        if by_area:
            img = by_area[0]
            selected.append({
                "img_path": img.get("img_path", ""),
                "original_path": str(paper_dir / img.get("img_path", "")),
                "caption": img.get("image_caption", []),
                "figure_label": extract_figure_label(img.get("image_caption", [])),
                "sub_type": img.get("sub_type"),
                "score": 0,
            })

    return selected


def load_manifest() -> dict:
    """Load existing manifest or return empty structure."""
    if MANIFEST.exists():
        with open(MANIFEST, encoding="utf-8") as f:
            return json.load(f)
    return {"generated": "", "papers": {}}


def save_manifest(manifest: dict) -> None:
    """Write manifest to disk."""
    with open(MANIFEST, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)


def read_existing_markdown() -> set[str]:
    """Parse existing Markdown to find which image paths are still present."""
    if not MARKDOWN.exists():
        return set()
    text = MARKDOWN.read_text(encoding="utf-8")
    # Match image references like ![...](images/...)
    return set(re.findall(r"!\[.*?\]\((images/[^)]+)\)", text))


def build_markdown(papers_data: list[dict], existing_images: set[str]) -> str:
    """
    Build the full Markdown gallery.

    papers_data: list of {"paper_name", "figures": [{...}]}
    existing_images: set of image paths already in the Markdown (for deletions)
    """
    today = datetime.now().strftime("%Y-%m-%d")
    total_papers = len(papers_data)

    lines = [
        "---",
        f"title: Key Framework & Architecture Figures",
        f"generated: {today}",
        f"paper_count: {total_papers}",
        "---",
        "",
        "# Key Framework & Architecture Figures",
        "",
        "> 自动生成的关键框架图/方法流程图集合。删除不需要的图后，再次运行不会重复添加。",
        "> 每篇论文选取 1-2 张核心框架图，基于 caption 关键词、图片类型和尺寸三层评分筛选。",
        "",
        "---",
        "",
    ]

    for entry in papers_data:
        paper_name = entry["paper_name"]
        figures = entry["figures"]

        lines.append(f"## {paper_name}")
        lines.append("")

        for fig in figures:
            img_rel = fig["dest_rel"]  # e.g. "images/xxx.jpg"
            figure_label = fig["figure_label"]
            caption_text = extract_caption_text(fig["caption"])

            if caption_text:
                lines.append(f"**{figure_label}** — {caption_text}")
            else:
                lines.append(f"**{figure_label}**")
            lines.append(f"![{paper_name} {figure_label}]({img_rel})")
            lines.append("")

        lines.append("---")
        lines.append("")

    return "\n".join(lines)


def main() -> None:
    """Main entry point."""
    # Ensure output directories exist
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)

    # Load manifest for incremental tracking
    manifest = load_manifest()
    processed_papers = manifest.get("papers", {})

    # Read existing Markdown to detect user deletions
    existing_images = read_existing_markdown()

    # Discover all paper directories
    paper_dirs = sorted([d for d in MINERU_DIR.iterdir() if d.is_dir()])
    log.info("Found %d paper directories in %s", len(paper_dirs), MINERU_DIR.name)

    new_count = 0
    skip_count = 0
    all_paper_entries = []

    for paper_dir in paper_dirs:
        paper_name = paper_dir.name

        # Check if already processed (incremental)
        if paper_name in processed_papers:
            skip_count += 1
            # Re-add to gallery, checking for user deletions
            manifest_entry = processed_papers[paper_name]
            figures = manifest_entry.get("figures", [])
            kept_figures = []
            for fig in figures:
                img_rel = fig.get("dest_rel", "")
                # If user deleted the image reference from Markdown, respect that
                if existing_images and img_rel not in existing_images:
                    log.info("  User-deleted figure skipped: %s", img_rel)
                    continue
                kept_figures.append(fig)
            if kept_figures:
                all_paper_entries.append({
                    "paper_name": paper_name,
                    "figures": kept_figures,
                })
            continue

        # Process new paper
        log.info("Processing: %s", paper_name)
        selected = process_paper(paper_dir)

        if not selected:
            log.warning("  No suitable figures found for %s", paper_name)
            # Still record in manifest so we don't re-process
            processed_papers[paper_name] = {
                "processed_at": datetime.now().isoformat(),
                "figures": [],
            }
            new_count += 1
            continue

        # Copy images and build figure entries
        figure_entries = []
        for fig in selected:
            src = Path(fig["original_path"])
            if not src.exists():
                log.warning("  Image not found: %s", src)
                continue

            dest_name = unique_image_name(paper_name, fig["figure_label"], fig["img_path"])
            dest_path = IMAGES_DIR / dest_name
            shutil.copy2(src, dest_path)

            figure_entries.append({
                "img_path": fig["img_path"],
                "figure_label": fig["figure_label"],
                "caption": fig["caption"],
                "sub_type": fig["sub_type"],
                "score": fig["score"],
                "dest_name": dest_name,
                "dest_rel": f"images/{dest_name}",
            })

        processed_papers[paper_name] = {
            "processed_at": datetime.now().isoformat(),
            "figures": figure_entries,
        }

        if figure_entries:
            all_paper_entries.append({
                "paper_name": paper_name,
                "figures": figure_entries,
            })

        new_count += 1

    # Sort by paper name (chronological by convention)
    all_paper_entries.sort(key=lambda x: x["paper_name"])

    # Build and write Markdown
    markdown_text = build_markdown(all_paper_entries, existing_images)
    MARKDOWN.write_text(markdown_text, encoding="utf-8")

    # Save manifest
    manifest["generated"] = datetime.now().isoformat()
    manifest["papers"] = processed_papers
    save_manifest(manifest)

    # Summary
    total_figures = sum(len(e["figures"]) for e in all_paper_entries)
    log.info("=" * 60)
    log.info("Done!")
    log.info("  New papers processed: %d", new_count)
    log.info("  Skipped (already done): %d", skip_count)
    log.info("  Total papers in gallery: %d", len(all_paper_entries))
    log.info("  Total figures in gallery: %d", total_figures)
    log.info("  Output: %s", MARKDOWN)
    log.info("  Images: %s", IMAGES_DIR)


if __name__ == "__main__":
    main()

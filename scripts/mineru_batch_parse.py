#!/usr/bin/env python3
"""
MinerU Batch PDF Parser
=======================
Calls MinerU's official precision parsing API to batch-convert PDFs into Markdown.
Token is read exclusively from environment variable MINERU_API_TOKEN.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
import zipfile
from datetime import datetime
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


def make_session() -> requests.Session:
    """Create a requests session with automatic retries for transient errors."""
    s = requests.Session()
    retries = Retry(
        total=5,
        backoff_factor=1.5,
        status_forcelist=[502, 503, 504],
        allowed_methods=["GET", "POST", "PUT"],
    )
    adapter = HTTPAdapter(max_retries=retries)
    s.mount("https://", adapter)
    s.mount("http://", adapter)
    return s


SESSION = make_session()

# ─── Constants ────────────────────────────────────────────────────────────────

API_BASE        = "https://mineru.net/api/v4"
BATCH_URL_API   = f"{API_BASE}/file-urls/batch"
BATCH_RESULT_API = f"{API_BASE}/extract-results/batch"

MAX_BATCH_SIZE  = 50
POLL_INTERVAL   = 10        # seconds between polls
POLL_TIMEOUT    = 1800      # 30 minutes max wait per batch


# ─── Logging Setup ───────────────────────────────────────────────────────────

def setup_logging(log_dir: Path) -> logging.Logger:
    """Create a logger that writes to both console and a timestamped log file."""
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file  = log_dir / f"mineru_parse_{timestamp}.log"

    logger = logging.getLogger("mineru")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter(
        "[%(asctime)s] %(levelname)-7s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    logger.info(f"Log file: {log_file}")
    return logger


# ─── Token Handling ──────────────────────────────────────────────────────────

def get_api_token() -> str:
    """Read MinerU API token from environment variable. Exit if missing."""
    token = os.environ.get("MINERU_API_TOKEN", "").strip()
    if not token:
        print("ERROR: Environment variable MINERU_API_TOKEN is not set.", file=sys.stderr)
        print("Please configure it first:", file=sys.stderr)
        print("  macOS / Linux : export MINERU_API_TOKEN='your-token-here'", file=sys.stderr)
        print("  Windows       : setx MINERU_API_TOKEN \"your-token-here\"", file=sys.stderr)
        sys.exit(1)
    print("已检测到 MINERU_API_TOKEN")
    return token


# ─── Argument Parser ─────────────────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Batch-parse PDFs via MinerU API and output structured Markdown."
    )
    p.add_argument("--input",      default="00-inbox/PDFs",       help="PDF input directory")
    p.add_argument("--output",     default="01-mineru-output",    help="MinerU raw output directory")
    p.add_argument("--parsed",     default="02-parsed-markdown",  help="Parsed Markdown directory")
    p.add_argument("--model-version", default="vlm",              help="Model version (default: vlm)")
    p.add_argument("--language",   default="ch",                  help="Document language (default: ch)")
    p.add_argument("--batch-size", type=int, default=10,          help="Max PDFs per API batch (default: 10, max 50)")
    p.add_argument("--ocr",        action="store_true",           help="Enable OCR")
    p.add_argument("--page-ranges",default=None,                  help='Page ranges, e.g. "1-5" or "2,4-6"')
    p.add_argument("--force",      action="store_true",           help="Re-parse PDFs even if Markdown already exists")
    return p.parse_args()


# ─── Helpers ─────────────────────────────────────────────────────────────────

def find_pdfs(directory: Path, logger: logging.Logger) -> list[Path]:
    """Recursively find all PDF files in directory."""
    pdfs = sorted(directory.rglob("*.pdf"))
    logger.info(f"Found {len(pdfs)} PDF(s) in {directory}")
    return pdfs


def filter_already_parsed(
    pdfs: list[Path], parsed_dir: Path, force: bool, logger: logging.Logger
) -> tuple[list[Path], int]:
    """Remove PDFs that already have a corresponding Markdown file (unless --force)."""
    if force:
        logger.info("--force enabled: will re-parse all PDFs")
        return pdfs, 0

    remaining = []
    skipped   = 0
    for pdf in pdfs:
        md_path = parsed_dir / f"{pdf.stem}.md"
        if md_path.exists():
            skipped += 1
            logger.debug(f"Skipped (already parsed): {pdf.name}")
        else:
            remaining.append(pdf)

    return remaining, skipped


def upload_file(upload_url: str, pdf_path: Path, logger: logging.Logger) -> bool:
    """Upload a single PDF to the presigned URL via PUT."""
    try:
        with open(pdf_path, "rb") as f:
            resp = SESSION.put(
                upload_url,
                data=f,
                timeout=300,
            )
        if resp.status_code == 200:
            logger.debug(f"Uploaded: {pdf_path.name}")
            return True
        else:
            logger.error(f"Upload failed for {pdf_path.name}: HTTP {resp.status_code}")
            return False
    except Exception as e:
        logger.error(f"Upload exception for {pdf_path.name}: {e}")
        return False


def poll_batch(
    batch_id: str, token: str, logger: logging.Logger
) -> dict | None:
    """
    Poll the batch extract-results endpoint until all tasks finish or timeout.
    Returns the final JSON response, or None on timeout/error.
    """
    url     = f"{BATCH_RESULT_API}/{batch_id}"
    headers = {"Authorization": f"Bearer {token}"}
    start   = time.time()

    while True:
        elapsed = time.time() - start
        if elapsed > POLL_TIMEOUT:
            logger.error(f"Polling timeout ({POLL_TIMEOUT}s) for batch {batch_id}")
            return None

        try:
            resp = SESSION.get(url, headers=headers, timeout=60)
            if resp.status_code != 200:
                logger.warning(f"Poll HTTP {resp.status_code}, retrying...")
                time.sleep(POLL_INTERVAL)
                continue

            data     = resp.json()
            extract  = data.get("data", {}).get("extract_result", [])
            if extract is None:
                extract = []

            total    = len(extract)
            done     = sum(1 for r in extract if r.get("state") in ("done", "failed"))
            pending  = total - done

            if total > 0:
                logger.info(f"  Batch {batch_id[:8]}... progress: {done}/{total} done, {pending} pending")

            if pending == 0 and total > 0:
                return data

        except Exception as e:
            logger.warning(f"Poll error: {e}")

        time.sleep(POLL_INTERVAL)


def download_and_extract(
    zip_url: str, dest_dir: Path, pdf_stem: str, logger: logging.Logger
) -> Path | None:
    """Download the result ZIP, extract it, and return the path to full.md (or None)."""
    import subprocess

    dest_dir.mkdir(parents=True, exist_ok=True)
    zip_path = dest_dir / f"{pdf_stem}.zip"

    # Try downloading with requests first, then fallback to curl
    downloaded = False

    # Use curl (bypass proxy, more reliable for CDN SSL)
    for attempt in range(3):
        try:
            result = subprocess.run(
                ["curl", "-fsSL", "--noproxy", "*", "-o", str(zip_path), zip_url],
                capture_output=True, text=True, timeout=600,
            )
            if result.returncode == 0 and zip_path.exists() and zip_path.stat().st_size > 0:
                downloaded = True
                logger.debug(f"Downloaded: {zip_path}")
                break
            else:
                logger.warning(f"curl attempt {attempt+1}/3 failed: {result.stderr[:200]}")
        except Exception as e:
            logger.warning(f"curl attempt {attempt+1}/3 exception: {e}")
        if attempt < 2:
            time.sleep(3 * (attempt + 1))

    # Fallback: requests with proxy bypass
    if not downloaded:
        logger.info(f"Trying requests fallback for {pdf_stem}...")
        try:
            resp = SESSION.get(zip_url, timeout=600, stream=True, proxies={"http": None, "https": None})
            if resp.status_code == 200:
                with open(zip_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)
                downloaded = True
                logger.debug(f"Downloaded via requests: {zip_path}")
            else:
                logger.error(f"requests download failed: HTTP {resp.status_code}")
                return None
        except Exception as e:
            logger.error(f"requests download exception: {e}")
            return None

    if not downloaded:
        return None

    # Extract
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            zf.extractall(dest_dir)
        logger.debug(f"Extracted to: {dest_dir}")
    except Exception as e:
        logger.error(f"ZIP extraction failed: {e}")
        return None
    finally:
        zip_path.unlink(missing_ok=True)

    # Find full.md
    full_md = dest_dir / "full.md"
    if full_md.exists():
        return full_md

    # Fallback: search recursively
    for candidate in dest_dir.rglob("full.md"):
        return candidate

    logger.error(f"full.md not found in extracted content: {dest_dir}")
    return None


# ─── Core Processing ─────────────────────────────────────────────────────────

def process_batch(
    pdfs: list[Path],
    token: str,
    args: argparse.Namespace,
    output_dir: Path,
    parsed_dir: Path,
    logger: logging.Logger,
) -> tuple[int, int, list[tuple[str, str]]]:
    """
    Process one batch of PDFs.
    Returns (success_count, fail_count, failures: list of (filename, reason)).
    """
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    # 1. Request upload URLs
    name_list = [pdf.name for pdf in pdfs]
    payload: dict = {
        "files":             [{"name": name, "is_ocr": args.ocr} for name in name_list],
        "enable_formula":    True,
        "enable_table":      True,
        "language":          args.language,
        "model_version":     args.model_version,
    }
    if args.page_ranges:
        payload["page_ranges"] = args.page_ranges

    logger.info(f"Requesting upload URLs for {len(pdfs)} PDF(s)...")
    resp = None
    for attempt in range(3):
        try:
            resp = SESSION.post(BATCH_URL_API, json=payload, headers=headers, timeout=60)
            break
        except Exception as e:
            logger.warning(f"API request attempt {attempt+1}/3 failed: {e}")
            if attempt < 2:
                time.sleep(3 * (attempt + 1))
    if resp is None:
        logger.error("Failed to request upload URLs after 3 attempts")
        return 0, len(pdfs), [(p.name, "API request failed after retries") for p in pdfs]

    if resp.status_code != 200:
        msg = f"HTTP {resp.status_code}: {resp.text[:200]}"
        logger.error(f"Batch upload URL request failed: {msg}")
        return 0, len(pdfs), [(p.name, msg) for p in pdfs]

    resp_data = resp.json()
    if resp_data.get("code") != 0:
        msg = resp_data.get("msg", "Unknown API error")
        logger.error(f"API error: {msg}")
        return 0, len(pdfs), [(p.name, msg) for p in pdfs]

    batch_id     = resp_data["data"]["batch_id"]
    file_urls    = resp_data["data"].get("file_urls", [])
    logger.info(f"Batch ID: {batch_id}")

    # 2. Upload each PDF
    failures: list[tuple[str, str]] = []
    upload_map: dict[str, Path] = {}   # pdf_name -> pdf_path

    for idx, pdf in enumerate(pdfs):
        if idx >= len(file_urls):
            logger.error(f"No upload URL for {pdf.name} (index {idx} out of range)")
            failures.append((pdf.name, "No upload URL returned"))
            continue
        url = file_urls[idx]
        if not url:
            logger.error(f"Empty upload URL for {pdf.name}")
            failures.append((pdf.name, "Empty upload URL"))
            continue
        success = upload_file(url, pdf, logger)
        if success:
            upload_map[pdf.name] = pdf
        else:
            failures.append((pdf.name, "Upload failed"))

    if not upload_map:
        return 0, len(pdfs), failures

    # 3. Poll for results
    logger.info(f"Polling batch {batch_id} ...")
    result_data = poll_batch(batch_id, token, logger)

    if result_data is None:
        for name in upload_map:
            failures.append((name, "Polling timeout or error"))
        return 0, len(pdfs), failures

    # 4. Process results
    success_count = 0
    extract_results = result_data.get("data", {}).get("extract_result", [])
    if extract_results is None:
        extract_results = []

    # Build a lookup by name
    result_by_name: dict[str, dict] = {}
    for r in extract_results:
        result_by_name[r.get("file_name", "")] = r

    for pdf_name, pdf_path in upload_map.items():
        r = result_by_name.get(pdf_name)
        if r is None:
            failures.append((pdf_name, "Result not found in response"))
            continue

        state = r.get("state", "")
        if state == "failed":
            err = r.get("err_msg", "Unknown error")
            logger.error(f"Parse failed for {pdf_name}: {err}")
            failures.append((pdf_name, f"Parse failed: {err}"))
            continue

        if state != "done":
            failures.append((pdf_name, f"Unexpected state: {state}"))
            continue

        zip_url = r.get("full_zip_url", "")
        if not zip_url:
            failures.append((pdf_name, "No download URL in result"))
            continue

        # Download, extract, copy
        pdf_stem    = pdf_path.stem
        dest_dir    = output_dir / pdf_stem
        full_md     = download_and_extract(zip_url, dest_dir, pdf_stem, logger)

        if full_md is None:
            failures.append((pdf_name, "Download/extract failed or full.md missing"))
            continue

        # Copy full.md -> parsed_dir/xxx.md
        parsed_md = parsed_dir / f"{pdf_stem}.md"
        try:
            import shutil
            shutil.copy2(full_md, parsed_md)
            logger.info(f"Saved: {parsed_md}")
            success_count += 1
        except Exception as e:
            logger.error(f"Failed to copy {full_md} -> {parsed_md}: {e}")
            failures.append((pdf_name, f"Copy failed: {e}"))

    return success_count, len(pdfs), failures


# ─── Main ────────────────────────────────────────────────────────────────────

def main() -> None:
    args = parse_args()
    args.batch_size = min(args.batch_size, MAX_BATCH_SIZE)

    # Resolve paths relative to vault root (parent of scripts/)
    vault_root   = Path(__file__).resolve().parent.parent
    input_dir    = vault_root / args.input
    output_dir   = vault_root / args.output
    parsed_dir   = vault_root / args.parsed
    log_dir      = vault_root / "99-logs"

    # Setup logging
    logger = setup_logging(log_dir)
    logger.info("=" * 60)
    logger.info("MinerU Batch Parse Started")
    logger.info("=" * 60)
    logger.info(f"Input  : {input_dir}")
    logger.info(f"Output : {output_dir}")
    logger.info(f"Parsed : {parsed_dir}")
    logger.info(f"Model  : {args.model_version}")
    logger.info(f"Language: {args.language}")
    logger.info(f"OCR    : {args.ocr}")
    logger.info(f"Formula: True")
    logger.info(f"Table  : True")
    logger.info(f"Batch  : {args.batch_size}")
    if args.page_ranges:
        logger.info(f"Pages  : {args.page_ranges}")

    # Validate input directory
    if not input_dir.exists():
        logger.error(f"Input directory does not exist: {input_dir}")
        sys.exit(1)

    # Get token (exit if missing)
    token = get_api_token()

    # Ensure output directories exist
    output_dir.mkdir(parents=True, exist_ok=True)
    parsed_dir.mkdir(parents=True, exist_ok=True)

    # Scan and filter PDFs
    all_pdfs = find_pdfs(input_dir, logger)
    if not all_pdfs:
        logger.warning("No PDF files found. Nothing to do.")
        sys.exit(0)

    pdfs_to_process, skipped = filter_already_parsed(all_pdfs, parsed_dir, args.force, logger)

    logger.info(f"To process: {len(pdfs_to_process)}, Skipped: {skipped}")

    if not pdfs_to_process:
        logger.info("All PDFs already parsed. Use --force to re-parse.")
        sys.exit(0)

    # Process in batches
    total_success = 0
    total_fail    = 0
    all_failures: list[tuple[str, str]] = []

    for i in range(0, len(pdfs_to_process), args.batch_size):
        batch     = pdfs_to_process[i : i + args.batch_size]
        batch_num = i // args.batch_size + 1
        total_batches = (len(pdfs_to_process) + args.batch_size - 1) // args.batch_size
        logger.info(f"--- Batch {batch_num}/{total_batches} ({len(batch)} PDFs) ---")

        ok, count, fails = process_batch(
            batch, token, args, output_dir, parsed_dir, logger
        )
        total_success += ok
        total_fail    += len(fails)
        all_failures.extend(fails)

    # ── Summary ────────────────────────────────────────────────────────────────
    logger.info("=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Total PDFs found     : {len(all_pdfs)}")
    logger.info(f"Skipped (parsed)     : {skipped}")
    logger.info(f"Successfully parsed  : {total_success}")
    logger.info(f"Failed               : {total_fail}")

    if all_failures:
        logger.info("")
        logger.info("Failure details:")
        for fname, reason in all_failures:
            logger.info(f"  - {fname}: {reason}")

    logger.info("=" * 60)
    logger.info("Done.")


if __name__ == "__main__":
    main()

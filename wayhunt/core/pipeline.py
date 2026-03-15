"""
WayHunt Pipeline

Coordinates the complete WayHunt scanning workflow.

Phases:
1. Subdomain discovery
2. Wayback archive enumeration
3. Snapshot filtering
4. Snapshot streaming
5. Secret detection (scanner callback)
6. Finding intelligence & risk scoring
7. Security reporting
8. Historical exposure intelligence
"""

import json
import os
from datetime import datetime
from typing import List, Tuple

from tqdm import tqdm

from wayhunt.core.logger import get_logger, is_verbose
from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import DEFAULT_OUTPUT_DIR, SUBPATHS

from wayhunt.discovery.subdomains import enumerate_subdomains

from wayhunt.archive.snapshot_collector import collect_snapshots
from wayhunt.archive.snapshot_filter import filter_snapshots

from wayhunt.streaming.snapshot_stream import stream_snapshots
from wayhunt.scanning.scanner_engine import scan_snapshot

from wayhunt.intelligence.intelligence_engine import generate_intelligence

from wayhunt.reporting.report_generator import (
    load_findings,
    aggregate_findings
)

from wayhunt.reporting.markdown_report import generate_markdown_report
from wayhunt.reporting.dashboard_generator import generate_dashboard
from wayhunt.reporting.llm_report import generate_llm_analysis

from wayhunt.analysis.secret_timeline import generate_secret_timeline
from wayhunt.analysis.sensitive_files import detect_sensitive_files
from wayhunt.analysis.endpoint_timeline import analyze_endpoint_evolution

logger = get_logger()

Snapshot = Tuple[str, str, str]


def make_run_dir(domain: str) -> str:
    """
    Build a unique output directory for this run.
    Format: output/<domain_with_underscores>_YYYYMMDD_HHMMSS
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_domain = domain.replace(".", "_")
    return os.path.join(DEFAULT_OUTPUT_DIR, f"{safe_domain}_{timestamp}")


def print_stage(msg: str) -> None:
    """Print a stage header — always shown regardless of verbose mode."""
    print(f"\n{msg}")


def run_pipeline(
    domain: str,
    years: int,
    threads: int,
    dashboard: bool = False,
    llm: dict | None = None
) -> None:

    # --------------------------------
    # Create isolated run directory
    # --------------------------------

    run_dir = make_run_dir(domain)
    ensure_directory(run_dir)

    print(f"[WayHunt] Run directory: {run_dir}")
    logger.info("Initializing WayHunt pipeline...")

    # --------------------------------
    # Phase 1 — Subdomain Discovery
    # --------------------------------

    print_stage("Stage 1/6: Subdomain discovery...")

    subdomains = enumerate_subdomains(domain, run_dir)

    print(f"  Found {len(subdomains)} subdomains")

    # --------------------------------
    # Phase 2 — Wayback Enumeration
    # --------------------------------

    print_stage("Stage 2/6: Wayback archive enumeration...")

    if not is_verbose():
        with tqdm(total=len(subdomains), desc="  Querying Wayback", unit="host",
                  bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} hosts") as pbar:
            snapshots = collect_snapshots(subdomains, years, progress_callback=lambda: pbar.update(1))
    else:
        snapshots = collect_snapshots(subdomains, years)

    snapshots = filter_snapshots(snapshots)

    print(f"  {len(snapshots)} snapshots after filtering")

    save_snapshots(snapshots, run_dir)

    # --------------------------------
    # Phase 3 — Snapshot Streaming
    # --------------------------------

    print_stage("Stage 3/6: Streaming and scanning snapshots...")

    stream_snapshots(
        snapshots,
        threads,
        scanner_callback=lambda ts, url, c: scan_snapshot(ts, url, c, run_dir)
    )

    # --------------------------------
    # Phase 4 — Load Raw Findings
    # --------------------------------

    raw_findings_path = os.path.join(run_dir, SUBPATHS["raw_findings"])
    raw_findings = load_findings(raw_findings_path)

    if not raw_findings:
        print("\n[WayHunt] No findings detected.")
        return

    print(f"  {len(raw_findings)} raw findings collected")

    # --------------------------------
    # Phase 5 — Finding Intelligence
    # --------------------------------

    print_stage("Stage 4/6: Generating finding intelligence...")

    intelligence_findings = generate_intelligence(raw_findings, run_dir)

    print(f"  Collapsed to {len(intelligence_findings)} unique findings")

    # --------------------------------
    # Phase 6 — Reporting
    # --------------------------------

    print_stage("Stage 5/6: Generating security reports...")

    summary = aggregate_findings(intelligence_findings)

    generate_markdown_report(
        intelligence_findings,
        summary,
        domain,
        years,
        run_dir
    )

    print(f"  Markdown report  → {run_dir}/reports/security_report.md")

    if dashboard:
        generate_dashboard(intelligence_findings, summary, run_dir)
        print(f"  Dashboard        → {run_dir}/reports/dashboard/index.html")

    if llm:
        generate_llm_analysis(intelligence_findings, llm, run_dir)
        print(f"  LLM analysis     → {run_dir}/reports/llm_analysis.md")

    # --------------------------------
    # Phase 7 — Historical Intelligence
    # --------------------------------

    print_stage("Stage 6/6: Historical exposure analysis...")

    secret_timeline = generate_secret_timeline(intelligence_findings, run_dir)
    sensitive_files = detect_sensitive_files(intelligence_findings, run_dir)
    endpoint_timeline = analyze_endpoint_evolution(intelligence_findings, run_dir)

    print(f"  Secret timelines : {len(secret_timeline)}")
    print(f"  Sensitive files  : {len(sensitive_files)}")
    print(f"  Endpoints tracked: {len(endpoint_timeline)}")

    print(f"\n[WayHunt] Pipeline completed. Output: {run_dir}\n")


def save_snapshots(snapshots: List[Snapshot], run_dir: str) -> None:
    """Save snapshot metadata to disk for reproducibility."""

    path = os.path.join(run_dir, SUBPATHS["snapshots"])
    ensure_directory(os.path.dirname(path))

    data = [
        {"timestamp": ts, "url": url, "status": status}
        for ts, url, status in snapshots
    ]

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logger.info(f"Snapshots saved to {path}")

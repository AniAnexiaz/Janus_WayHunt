import os
from typing import List, Dict

from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import SUBPATHS


def generate_markdown_report(
    findings: List[Dict],
    summary: Dict,
    target: str,
    years: int,
    run_dir: str
):

    path = os.path.join(run_dir, SUBPATHS["report_md"])
    ensure_directory(os.path.dirname(path))

    with open(path, "w", encoding="utf-8") as f:

        f.write("# WayHunt Historical Exposure Report\n\n")

        f.write(f"Target: {target}\n")
        f.write(f"Scan Window: last {years} years\n\n")

        f.write("## Summary\n\n")

        f.write(f"Total findings: {summary['total_findings']}\n")
        f.write(f"Unique URLs: {summary['unique_urls']}\n")
        f.write(f"Endpoints discovered: {summary['unique_endpoints']}\n\n")

        f.write("## Finding Types\n\n")

        for k, v in summary["type_counts"].items():
            f.write(f"- {k}: {v}\n")

        f.write("\n## Timeline of Exposure\n\n")

        for finding in findings:
            # Use first_seen — intelligence findings don't carry 'timestamp'
            f.write(
                f"{finding.get('first_seen', 'N/A')} -> {finding['type']} -> {finding['url']}\n"
            )

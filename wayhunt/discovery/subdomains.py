"""
Subdomain aggregation module.

Collects results from multiple passive sources and produces
a unified set of discovered subdomains.
"""

import os
from typing import Set

from wayhunt.core.logger import get_logger, is_verbose
from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import SUBPATHS

from .crtsh import fetch_crtsh
from .otx import fetch_otx
from .threatcrowd import fetch_threatcrowd
from .wayback_hosts import fetch_wayback_hosts

logger = get_logger()


def enumerate_subdomains(domain: str, run_dir: str) -> Set[str]:
    """
    Enumerate subdomains from passive sources.

    Args:
        domain: target domain
        run_dir: isolated output directory for this run

    Returns:
        set of unique subdomains
    """

    logger.info("Enumerating subdomains...")

    results = set()

    sources = [
        ("crt.sh", fetch_crtsh),
        ("OTX", fetch_otx),
        ("ThreatCrowd", fetch_threatcrowd),
        ("Wayback hosts", fetch_wayback_hosts),
    ]

    for name, func in sources:
        try:
            data = func(domain)
            # Per-source counts only shown in verbose mode
            if is_verbose():
                print(f"  {name}: {len(data)} results")
            logger.info(f"{name} returned: {len(data)}")
            results.update(data)
        except Exception:
            logger.warning(f"Warning: {name} source failed")

    logger.info(f"Total unique subdomains: {len(results)}")

    save_subdomains(results, run_dir)

    return results


def save_subdomains(subdomains: Set[str], run_dir: str) -> None:
    """Save discovered subdomains to disk."""

    path = os.path.join(run_dir, SUBPATHS["subdomains"])
    ensure_directory(os.path.dirname(path))

    with open(path, "w", encoding="utf-8") as f:
        for sub in sorted(subdomains):
            f.write(sub + "\n")

    logger.info(f"Subdomains saved to {path}")

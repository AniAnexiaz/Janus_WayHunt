"""
Snapshot collection module.
"""

from typing import List, Tuple, Set, Callable, Optional

from wayhunt.core.logger import get_logger
from .wayback_api import query_wayback

logger = get_logger()

Snapshot = Tuple[str, str, str]


def collect_snapshots(
    subdomains: Set[str],
    years: int,
    progress_callback: Optional[Callable] = None
) -> List[Snapshot]:
    """
    Collect Wayback snapshots for all discovered subdomains.

    Args:
        subdomains: discovered hosts
        years: archive window
        progress_callback: optional callable invoked after each host
                           (used by pipeline to advance tqdm bar)

    Returns:
        list of snapshot metadata
    """

    logger.info("Collecting Wayback snapshots...")

    all_snaps: List[Snapshot] = []

    for host in sorted(subdomains):

        try:
            snaps = query_wayback(host, years)

            logger.info(f"{host} -> {len(snaps)} snapshots")

            all_snaps.extend(snaps)

        except Exception:
            logger.warning(f"Warning: Wayback query failed for {host}")

        if progress_callback:
            progress_callback()

    logger.info(f"Total snapshots collected: {len(all_snaps)}")

    return all_snaps

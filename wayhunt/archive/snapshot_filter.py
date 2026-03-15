"""
Snapshot filtering utilities.
"""

from typing import List, Tuple
from urllib.parse import urlparse

Snapshot = Tuple[str, str, str]

IGNORE_EXTENSIONS = (
    ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico",
    ".css", ".mp4", ".mp3",
    ".woff", ".woff2", ".ttf"
)


def filter_snapshots(snapshot_list: List[Snapshot]) -> List[Snapshot]:
    """
    Remove unwanted snapshot URLs and deduplicate.

    Args:
        snapshot_list: raw snapshot list

    Returns:
        filtered snapshot list
    """

    seen_urls = set()
    filtered: List[Snapshot] = []

    for ts, url, status in snapshot_list:

        parsed = urlparse(url)
        path = parsed.path.lower()

        if path.endswith(IGNORE_EXTENSIONS):
            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        filtered.append((ts, url, status))

    return filtered
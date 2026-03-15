"""
Load snapshot metadata from Phase 3.
"""

import json
from typing import List, Tuple

Snapshot = Tuple[str, str, str]


def load_snapshots(path: str) -> List[Snapshot]:
    """
    Load snapshots.json into tuple format.

    Args:
        path: path to snapshot file

    Returns:
        list of (timestamp, url, status)
    """

    with open(path, "r") as f:
        data = json.load(f)

    snapshots: List[Snapshot] = []

    for entry in data:
        snapshots.append(
            (
                entry["timestamp"],
                entry["url"],
                entry["status"]
            )
        )

    return snapshots
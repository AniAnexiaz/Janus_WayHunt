"""
Secret exposure timeline analysis.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Tuple

from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import SUBPATHS


def _parse_date(ts: str) -> datetime | None:
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        try:
            return datetime.strptime(ts[:10], "%Y-%m-%d")
        except Exception:
            return None


def generate_secret_timeline(findings: List[Dict], run_dir: str) -> List[Dict]:
    """
    Group secrets by (value + URL) and calculate exposure windows.
    """

    groups: Dict[Tuple[str, str], Dict] = {}

    for f in findings:

        if f.get("type") == "ENDPOINT":
            continue

        value = f.get("value")
        url = f.get("url")
        ts = f.get("first_seen")

        if not value or not url or not ts:
            continue

        key = (value, url)

        dt = _parse_date(ts)
        if not dt:
            continue

        if key not in groups:

            groups[key] = {
                "secret_type": f.get("type"),
                "value": value,
                "url": url,
                "first_seen": dt,
                "last_seen": dt
            }

        else:

            if dt < groups[key]["first_seen"]:
                groups[key]["first_seen"] = dt

            if dt > groups[key]["last_seen"]:
                groups[key]["last_seen"] = dt

    results: List[Dict] = []

    for g in groups.values():

        exposure = (g["last_seen"] - g["first_seen"]).days

        results.append({
            "secret_type": g["secret_type"],
            "value": g["value"],
            "url": g["url"],
            "first_seen": g["first_seen"].date().isoformat(),
            "last_seen": g["last_seen"].date().isoformat(),
            "exposure_days": exposure
        })

    path = os.path.join(run_dir, SUBPATHS["secret_timeline"])
    ensure_directory(os.path.dirname(path))

    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results

"""
Endpoint evolution analysis.
"""

import json
import os
from datetime import datetime
from typing import List, Dict

from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import SUBPATHS


def _parse_date(ts: str):
    try:
        return datetime.fromisoformat(ts)
    except Exception:
        try:
            return datetime.strptime(ts[:10], "%Y-%m-%d")
        except Exception:
            return None


def analyze_endpoint_evolution(findings: List[Dict], run_dir: str) -> List[Dict]:

    endpoints: Dict[str, Dict] = {}

    for f in findings:

        if f.get("type") != "ENDPOINT":
            continue

        endpoint = f.get("value")
        ts = f.get("first_seen")

        dt = _parse_date(ts)
        if not endpoint or not dt:
            continue

        if endpoint not in endpoints:

            endpoints[endpoint] = {
                "first_seen": dt,
                "last_seen": dt,
                "count": 1
            }

        else:

            endpoints[endpoint]["count"] += 1

            if dt < endpoints[endpoint]["first_seen"]:
                endpoints[endpoint]["first_seen"] = dt

            if dt > endpoints[endpoint]["last_seen"]:
                endpoints[endpoint]["last_seen"] = dt

    results = []

    for ep, data in endpoints.items():

        results.append({
            "endpoint": ep,
            "first_seen": data["first_seen"].date().isoformat(),
            "last_seen": data["last_seen"].date().isoformat(),
            "occurrences": data["count"]
        })

    path = os.path.join(run_dir, SUBPATHS["endpoint_timeline"])
    ensure_directory(os.path.dirname(path))

    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results

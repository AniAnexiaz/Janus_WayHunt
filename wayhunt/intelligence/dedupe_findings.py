"""
Collapse duplicate findings across multiple snapshots.
"""

from datetime import datetime
from typing import List, Dict, Tuple


def _parse_date(ts: str):

    try:
        return datetime.fromisoformat(ts)
    except Exception:
        try:
            return datetime.strptime(ts[:10], "%Y-%m-%d")
        except Exception:
            return None


def collapse_duplicate_findings(findings: List[Dict]) -> List[Dict]:

    groups: Dict[Tuple[str, str, str], Dict] = {}

    for f in findings:

        key = (
            f.get("type"),
            f.get("value"),
            f.get("url")
        )

        ts = _parse_date(f.get("timestamp", ""))

        if key not in groups:

            groups[key] = {
                "type": f.get("type"),
                "value": f.get("value"),
                "url": f.get("url"),
                "first_seen": ts,
                "last_seen": ts,
                "occurrences": 1
            }

        else:

            groups[key]["occurrences"] += 1

            if ts:
                # FIX: guard against None stored from a previous unparseable timestamp
                if groups[key]["first_seen"] is None or ts < groups[key]["first_seen"]:
                    groups[key]["first_seen"] = ts

                if groups[key]["last_seen"] is None or ts > groups[key]["last_seen"]:
                    groups[key]["last_seen"] = ts

    results = []

    for g in groups.values():

        results.append({
            "type": g["type"],
            "value": g["value"],
            "url": g["url"],
            "first_seen": g["first_seen"].date().isoformat() if g["first_seen"] else None,
            "last_seen": g["last_seen"].date().isoformat() if g["last_seen"] else None,
            "occurrences": g["occurrences"]
        })

    return results

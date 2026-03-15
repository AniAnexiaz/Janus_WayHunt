import json
from collections import defaultdict
from typing import List, Dict


def load_findings(path: str) -> List[Dict]:
    """Load findings JSON file."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return []


def aggregate_findings(findings: List[Dict]) -> Dict:
    """Aggregate findings statistics."""

    summary = defaultdict(int)

    urls = set()
    endpoints = set()

    for f in findings:

        summary[f["type"]] += 1
        urls.add(f["url"])

        if f["type"] == "ENDPOINT":
            endpoints.add(f["value"])

    return {
        "type_counts": dict(summary),
        "unique_urls": len(urls),
        "unique_endpoints": len(endpoints),
        "total_findings": len(findings)
    }
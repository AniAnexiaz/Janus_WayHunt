import re
from typing import List, Dict

PATTERNS = [
    r"/api/[A-Za-z0-9_\-/]+",
    r"/internal/[A-Za-z0-9_\-/]+",
    r"/admin/[A-Za-z0-9_\-/]+"
]


def extract_endpoints(content: str, url: str, timestamp: str) -> List[Dict]:

    findings = []

    for pattern in PATTERNS:

        matches = re.findall(pattern, content)

        for m in matches:
            findings.append({
                "type": "ENDPOINT",
                "value": m,
                "url": url,
                "timestamp": timestamp,
                "context": m
            })

    return findings
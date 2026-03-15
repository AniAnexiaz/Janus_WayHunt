"""
Sensitive file discovery from findings and URLs.
"""

import json
import os
from typing import List, Dict

from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import SUBPATHS

SENSITIVE_PATTERNS = [
    ".env",
    ".env.production",
    "config.json",
    "settings.py",
    "database.sql",
    "backup.sql",
    "credentials.json",
    "secrets.yml",
    "docker-compose.yml"
]


def detect_sensitive_files(findings: List[Dict], run_dir: str) -> List[Dict]:

    results = []

    for f in findings:

        url = f.get("url", "")
        ts = f.get("first_seen")

        for pattern in SENSITIVE_PATTERNS:

            if pattern in url.lower():

                results.append({
                    "url": url,
                    "timestamp": ts,
                    "file_type": pattern
                })

    path = os.path.join(run_dir, SUBPATHS["sensitive_files"])
    ensure_directory(os.path.dirname(path))

    with open(path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)

    return results

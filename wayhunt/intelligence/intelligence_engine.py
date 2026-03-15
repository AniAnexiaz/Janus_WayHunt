"""
Generate enriched intelligence findings from raw scanner results.
"""

import json
import os
from typing import List, Dict

from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import SUBPATHS
from wayhunt.intelligence.dedupe_findings import collapse_duplicate_findings
from wayhunt.intelligence.risk_scoring import score_finding


def generate_intelligence(findings: List[Dict], run_dir: str) -> List[Dict]:

    collapsed = collapse_duplicate_findings(findings)

    enriched = []

    for f in collapsed:

        scored = score_finding(f)

        enriched.append(scored)

    path = os.path.join(run_dir, SUBPATHS["intelligence"])
    ensure_directory(os.path.dirname(path))

    with open(path, "w", encoding="utf-8") as f:
        json.dump(enriched, f, indent=2)

    return enriched

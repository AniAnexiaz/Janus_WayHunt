import re
import math
from collections import Counter
from typing import List, Dict

KEYWORDS = ["api", "token", "secret", "key", "auth", "password"]


def shannon_entropy(data: str) -> float:

    if not data:
        return 0

    counts = Counter(data)
    length = len(data)

    entropy = 0

    for c in counts:
        p = counts[c] / length
        entropy -= p * math.log2(p)

    return entropy


def detect_entropy(content: str, url: str, timestamp: str) -> List[Dict]:

    findings = []

    candidates = re.findall(r"[A-Za-z0-9_\-]{20,}", content)

    for c in candidates:

        if shannon_entropy(c) > 4.5:

            for k in KEYWORDS:

                if k in content.lower():

                    findings.append({
                        "type": "HIGH_ENTROPY_SECRET",
                        "value": c,
                        "url": url,
                        "timestamp": timestamp,
                        "context": c
                    })

                    break

    return findings
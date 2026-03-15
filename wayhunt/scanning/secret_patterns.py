import re
from typing import List, Dict

PATTERNS = {
    "AWS_KEY": r"AKIA[0-9A-Z]{16}",
    "GOOGLE_API_KEY": r"AIza[0-9A-Za-z\-_]{35}",
    "STRIPE_SECRET": r"sk_live_[0-9a-zA-Z]{24}",
    "JWT": r"eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
}

GENERIC_PATTERNS = [
    r"password\s*[:=]\s*['\"]?.+",
    r"api_key\s*[:=]\s*['\"]?.+",
    r"secret\s*[:=]\s*['\"]?.+",
    r"token\s*[:=]\s*['\"]?.+",
]


def detect_patterns(content: str, url: str, timestamp: str) -> List[Dict]:

    findings = []

    for name, pattern in PATTERNS.items():
        matches = re.findall(pattern, content)

        for m in matches:
            findings.append({
                "type": name,
                "value": m,
                "url": url,
                "timestamp": timestamp,
                "context": m
            })

    for pattern in GENERIC_PATTERNS:
        matches = re.findall(pattern, content)

        for m in matches:
            findings.append({
                "type": "GENERIC_SECRET",
                "value": m,
                "url": url,
                "timestamp": timestamp,
                "context": m
            })

    return findings
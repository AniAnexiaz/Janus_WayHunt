"""
Assign risk scores and severity classifications.
"""

from typing import Dict


SENSITIVE_TYPES = {
    "AWS_KEY",
    "GOOGLE_API_KEY",
    "STRIPE_SECRET"
}

EXPLOIT_PATTERNS = [
    "/admin",
    "/internal",
    "/debug",
    "/dev"
]


def score_finding(finding: Dict) -> Dict:

    score = 0

    if finding.get("type") in SENSITIVE_TYPES:
        score += 5

    if finding.get("type") == "HIGH_ENTROPY_SECRET":
        score += 3

    if finding.get("type") == "JS_ENDPOINT":
        score += 2

    if finding.get("value") and any(k in finding["value"].lower() for k in ["key", "token", "secret"]):
        score += 2

    exploitability = False

    value = finding.get("value", "")

    if any(p in value for p in EXPLOIT_PATTERNS):
        exploitability = True
        score += 2

    if score >= 8:
        risk = "HIGH"
    elif score >= 5:
        risk = "MEDIUM"
    else:
        risk = "LOW"

    finding["score"] = score
    finding["risk"] = risk
    finding["exploitability"] = exploitability

    return finding
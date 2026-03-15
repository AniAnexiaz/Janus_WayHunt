"""
ThreatCrowd domain intelligence source.
"""

import requests
from typing import Set


def fetch_threatcrowd(domain: str) -> Set[str]:

    url = f"https://www.threatcrowd.org/searchApi/v2/domain/report/?domain={domain}"

    subdomains = set()

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return subdomains

        data = r.json()

        for sub in data.get("subdomains", []):
            if sub.endswith(domain):
                subdomains.add(sub)

    except Exception:
        pass

    return subdomains
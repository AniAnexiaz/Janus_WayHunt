"""
AlienVault OTX passive DNS source.
"""

import requests
from typing import Set


def fetch_otx(domain: str) -> Set[str]:

    url = f"https://otx.alienvault.com/api/v1/indicators/domain/{domain}/passive_dns"

    subdomains = set()

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return subdomains

        data = r.json()

        for entry in data.get("passive_dns", []):
            host = entry.get("hostname")

            if host and host.endswith(domain):
                subdomains.add(host)

    except Exception:
        pass

    return subdomains
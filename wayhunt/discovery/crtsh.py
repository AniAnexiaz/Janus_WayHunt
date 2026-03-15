"""
crt.sh certificate transparency source.
"""

import requests
from typing import Set


def fetch_crtsh(domain: str) -> Set[str]:

    url = f"https://crt.sh/?q=%25.{domain}&output=json"

    subdomains = set()

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return subdomains

        data = r.json()

        for entry in data:
            names = entry.get("name_value", "").split("\n")

            for name in names:
                if name.endswith(domain):
                    subdomains.add(name.strip())

    except Exception:
        pass

    return subdomains
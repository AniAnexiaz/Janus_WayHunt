"""
Extract hostnames from Wayback archive URLs.
"""

import requests
from urllib.parse import urlparse
from typing import Set


def fetch_wayback_hosts(domain: str) -> Set[str]:

    url = f"http://web.archive.org/cdx/search/cdx?url=*.{domain}/*&output=json&fl=original&collapse=urlkey"

    subdomains = set()

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return subdomains

        data = r.json()

        for row in data[1:]:
            original = row[0]

            host = urlparse(original).hostname

            if host and host.endswith(domain):
                subdomains.add(host)

    except Exception:
        pass

    return subdomains
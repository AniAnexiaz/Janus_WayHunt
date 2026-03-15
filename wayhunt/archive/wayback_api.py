"""
Wayback CDX API integration.
"""

import requests
from datetime import datetime
from typing import List, Tuple

Snapshot = Tuple[str, str, str]


def query_wayback(domain: str, years: int) -> List[Snapshot]:
    """
    Query Wayback CDX API for archived URLs of a domain.

    Args:
        domain: target domain or subdomain
        years: number of years of history to include

    Returns:
        list of (timestamp, url, statuscode)
    """

    start_year = datetime.utcnow().year - years

    url = (
        "http://web.archive.org/cdx/search/cdx"
        f"?url=*.{domain}/*"
        "&output=json"
        "&fl=original,timestamp,statuscode"
        "&collapse=urlkey"
        f"&from={start_year}"
    )

    snapshots: List[Snapshot] = []

    try:
        r = requests.get(url, timeout=20)

        if r.status_code != 200:
            return snapshots

        data = r.json()

        for row in data[1:]:
            original = row[0]
            timestamp = row[1]
            status = row[2]

            snapshots.append((timestamp, original, status))

    except Exception:
        pass

    return snapshots
import json
import os
import threading
from typing import Dict

from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import SUBPATHS

# Lock prevents concurrent threads from corrupting the JSON file
_lock = threading.Lock()


def store_finding(finding: Dict, run_dir: str):

    path = os.path.join(run_dir, SUBPATHS["raw_findings"])

    with _lock:

        ensure_directory(os.path.dirname(path))

        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump([], f)

        with open(path, "r+", encoding="utf-8") as f:

            data = json.load(f)

            data.append(finding)

            f.seek(0)

            json.dump(data, f, indent=2)

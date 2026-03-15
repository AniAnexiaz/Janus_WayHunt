import json
import os

from wayhunt.core.utils import ensure_directory
from wayhunt.core.config import SUBPATHS


def generate_dashboard(findings, summary, run_dir: str):

    path = os.path.join(run_dir, SUBPATHS["dashboard"])
    ensure_directory(os.path.dirname(path))

    with open(
        "wayhunt/reporting/templates/dashboard_template.html",
        encoding="utf-8"
    ) as f:
        template = f.read()

    data = {
        "summary": summary,
        "findings": findings
    }

    html = template.replace(
        "__DATA__", json.dumps(data)
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

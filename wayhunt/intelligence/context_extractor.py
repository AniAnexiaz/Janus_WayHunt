"""
Extract contextual code snippets around detected secrets.
"""

from typing import Optional


CONTEXT_WINDOW = 80


def extract_context(content: str, match: str) -> Optional[str]:

    idx = content.find(match)

    if idx == -1:
        return None

    start = max(idx - CONTEXT_WINDOW, 0)
    end = min(idx + len(match) + CONTEXT_WINDOW, len(content))

    return content[start:end].strip()
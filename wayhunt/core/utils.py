"""
Utility helpers used across WayHunt modules.
"""

import os


def ensure_directory(path: str) -> None:
    """
    Ensure a directory exists.

    Args:
        path: directory path
    """

    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def safe_filename(name: str) -> str:
    """
    Convert string into filesystem-safe filename.

    Args:
        name: input filename

    Returns:
        sanitized filename
    """

    return "".join(c for c in name if c.isalnum() or c in ("-", "_", "."))
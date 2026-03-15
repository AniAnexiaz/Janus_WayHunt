"""
Content hashing for smart deduplication.
"""

import hashlib


def hash_content(content: bytes) -> str:
    """
    Compute SHA256 hash of content.

    Args:
        content: response body

    Returns:
        hash string
    """

    return hashlib.sha256(content).hexdigest()
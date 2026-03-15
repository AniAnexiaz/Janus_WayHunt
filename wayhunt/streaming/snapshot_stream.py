"""
Snapshot streaming processor.

Downloads Wayback snapshots, performs size checks,
deduplicates content via hashing, and streams valid
content to a scanner callback.
"""

import requests
import threading
from typing import List, Tuple, Callable
from concurrent.futures import ThreadPoolExecutor, as_completed

from tqdm import tqdm

from wayhunt.core.logger import get_logger, is_verbose
from .content_hash import hash_content

logger = get_logger()

Snapshot = Tuple[str, str, str]

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB


def build_archive_url(timestamp: str, url: str) -> str:
    """Construct Wayback snapshot URL."""
    return f"https://web.archive.org/web/{timestamp}/{url}"


def stream_snapshots(
    snapshots: List[Snapshot],
    threads: int,
    scanner_callback: Callable[[str, str, str], None] | None = None
):
    """
    Stream snapshots and process them immediately.

    Args:
        snapshots: snapshot metadata
        threads: worker threads
        scanner_callback: optional scanning function
    """

    logger.info(f"Streaming {len(snapshots)} archived snapshots...")

    seen_hashes = set()
    _lock = threading.Lock()

    processed = 0
    skipped_duplicates = 0
    skipped_large = 0
    failed = 0

    # In quiet mode use tqdm; in verbose mode just log normally
    progress = None if is_verbose() else tqdm(
        total=len(snapshots),
        desc="  Scanning",
        unit="snap",
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]"
    )

    def worker(snapshot: Snapshot):

        nonlocal processed, skipped_duplicates, skipped_large, failed

        timestamp, url, _ = snapshot
        archive_url = build_archive_url(timestamp, url)

        try:

            r = requests.get(archive_url, timeout=15)

            if r.status_code != 200:
                with _lock:
                    failed += 1
                return

            size = int(r.headers.get("Content-Length", 0))

            if size > MAX_FILE_SIZE:
                with _lock:
                    skipped_large += 1
                return

            content = r.content
            content_hash = hash_content(content)

            with _lock:
                if content_hash in seen_hashes:
                    skipped_duplicates += 1
                    return
                seen_hashes.add(content_hash)

            if scanner_callback:
                scanner_callback(timestamp, url, content)

            with _lock:
                processed += 1

        except Exception:
            with _lock:
                failed += 1

        finally:
            if progress:
                progress.update(1)

    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = [executor.submit(worker, s) for s in snapshots]
        for _ in as_completed(futures):
            pass

    if progress:
        progress.close()

    # Summary always shown
    print(f"  Processed: {processed}  |  Duplicates skipped: {skipped_duplicates}  |  Failed: {failed}")

    logger.info(f"Processed: {processed}")
    logger.info(f"Skipped duplicates: {skipped_duplicates}")
    logger.info(f"Skipped large files: {skipped_large}")
    logger.info(f"Failed downloads: {failed}")

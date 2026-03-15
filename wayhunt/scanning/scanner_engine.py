from wayhunt.scanning.secret_patterns import detect_patterns
from wayhunt.scanning.entropy_detector import detect_entropy
from wayhunt.scanning.endpoint_extractor import extract_endpoints
from wayhunt.scanning.findings_extractor import store_finding
from wayhunt.core.logger import get_logger

logger = get_logger()


def scan_snapshot(timestamp: str, url: str, content: bytes, run_dir: str):

    try:
        text = content.decode("utf-8", errors="ignore")
    except Exception:
        return

    findings = []

    findings.extend(detect_patterns(text, url, timestamp))
    findings.extend(detect_entropy(text, url, timestamp))
    findings.extend(extract_endpoints(text, url, timestamp))

    for f in findings:

        store_finding(f, run_dir)

        # Per-finding detail only in verbose mode
        logger.info(f"Secret detected: {f['type']} | {url}")

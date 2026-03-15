"""
WayHunt Configuration

Global configuration values and defaults.
"""

DEFAULT_YEARS = 5
DEFAULT_THREADS = 10

DEFAULT_OUTPUT_DIR = "output"

MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB limit for snapshot downloads

# Relative sub-paths within a run directory.
# Every module builds its output path as: os.path.join(run_dir, SUBPATHS["key"])
SUBPATHS = {
    "subdomains":         "data/subdomains.txt",
    "snapshots":          "data/snapshots.json",
    "raw_findings":       "results/raw_findings.json",
    "intelligence":       "results/intelligence_findings.json",
    "report_md":          "reports/security_report.md",
    "secret_timeline":    "reports/secret_timeline.json",
    "endpoint_timeline":  "reports/endpoint_timeline.json",
    "sensitive_files":    "reports/sensitive_files.json",
    "dashboard":          "reports/dashboard/index.html",
    "llm_analysis":       "reports/llm_analysis.md",
}

# WayHunt

**Wayback Archive Attack Surface Analysis Tool**  
Part of the Janus Security Tool Suite

WayHunt discovers subdomains, retrieves historical snapshots from the Wayback Machine, scans them for exposed secrets and endpoints, and generates structured security reports — all from passive sources with no active scanning.

---

## Features

- Passive subdomain discovery via crt.sh, OTX, ThreatCrowd, and Wayback hosts
- Historical snapshot retrieval via the Wayback CDX API
- Secret detection — AWS keys, Google API keys, Stripe secrets, JWTs, generic credentials
- High-entropy string detection for unlabelled secrets
- Endpoint discovery — `/api/`, `/admin/`, `/internal/` paths
- Risk scoring and deduplication of findings
- Markdown security report, optional HTML dashboard, optional LLM analysis
- Isolated output per run — no overwriting between domains or repeat scans
- Clean progress bar UI by default, full verbose logging with `-v`

---

## Installation

```bash
git clone https://github.com/youruser/janus-wayhunt.git
cd janus-wayhunt
pip install -r requirements.txt
```

**requirements.txt**
```
requests
tqdm
```

---

## Usage

```bash
python janus_wayhunt.py <domain> [options]
```

### Examples

```bash
# Basic scan
python janus_wayhunt.py example.com

# Scan last 10 years of archives
python janus_wayhunt.py example.com --last 10

# Use more threads for faster scanning
python janus_wayhunt.py example.com --threads 20

# Generate HTML dashboard
python janus_wayhunt.py example.com --dashboard

# Verbose output (shows per-host and per-finding detail)
python janus_wayhunt.py example.com -v

# LLM analysis via local Ollama
python janus_wayhunt.py example.com --llm-url http://localhost:11434

# LLM analysis via OpenAI
python janus_wayhunt.py example.com --llm-api sk-xxxx --llm-model gpt-4o
```

### All Options

| Option | Default | Description |
|--------|---------|-------------|
| `--last <years>` | 5 | Wayback archive window in years |
| `--threads <n>` | 10 | Worker threads for snapshot downloading |
| `--dashboard` | off | Generate HTML dashboard |
| `--llm-url <url>` | — | Local LLM endpoint for analysis report |
| `--llm-api <key>` | — | OpenAI-compatible API key |
| `--llm-model <name>` | gpt-4o-mini | Model name for API LLM |
| `-v, --verbose` | off | Full per-item log output |
| `--no-banner` | off | Suppress ASCII banner |

---

## Output Structure

Every run creates an isolated directory so results are never overwritten:

```
output/
└── example_com_20240315_143022/
    ├── data/
    │   ├── subdomains.txt          # Discovered subdomains
    │   └── snapshots.json          # Filtered snapshot metadata
    ├── results/
    │   ├── raw_findings.json       # All findings from scanner
    │   └── intelligence_findings.json  # Deduplicated + scored findings
    └── reports/
        ├── security_report.md      # Main markdown report
        ├── secret_timeline.json    # Secret exposure windows
        ├── endpoint_timeline.json  # Endpoint evolution over time
        ├── sensitive_files.json    # Sensitive file URLs detected
        ├── dashboard/
        │   └── index.html          # HTML dashboard (--dashboard only)
        └── llm_analysis.md         # LLM report (--llm-* only)
```

---

## Project Structure

```
Janus_WayHunt/
├── janus_wayhunt.py          # Entry point
└── wayhunt/
    ├── core/
    │   ├── config.py         # Global config and output paths
    │   ├── logger.py         # Logging (verbose/quiet mode)
    │   ├── pipeline.py       # Main pipeline orchestrator
    │   └── utils.py          # Shared helpers
    ├── discovery/
    │   ├── subdomains.py     # Subdomain aggregator
    │   ├── crtsh.py          # crt.sh source
    │   ├── otx.py            # AlienVault OTX source
    │   ├── threatcrowd.py    # ThreatCrowd source
    │   └── wayback_hosts.py  # Wayback host extraction
    ├── archive/
    │   ├── snapshot_collector.py  # Wayback CDX querying
    │   ├── snapshot_filter.py     # URL dedup and extension filtering
    │   └── wayback_api.py         # CDX API wrapper
    ├── streaming/
    │   ├── snapshot_stream.py     # Threaded snapshot downloader
    │   ├── snapshot_loader.py     # Load saved snapshots
    │   └── content_hash.py        # SHA256 dedup
    ├── scanning/
    │   ├── scanner_engine.py      # Per-snapshot scan coordinator
    │   ├── secret_patterns.py     # Regex pattern matching
    │   ├── entropy_detector.py    # Shannon entropy detection
    │   ├── endpoint_extractor.py  # API/admin path extraction
    │   └── findings_extractor.py  # Thread-safe finding storage
    ├── intelligence/
    │   ├── intelligence_engine.py # Dedup + scoring orchestrator
    │   ├── dedupe_findings.py     # Cross-snapshot deduplication
    │   ├── risk_scoring.py        # Risk scoring and classification
    │   └── context_extractor.py  # Code context snippets
    ├── analysis/
    │   ├── secret_timeline.py     # Secret exposure windows
    │   ├── endpoint_timeline.py   # Endpoint evolution
    │   └── sensitive_files.py     # Sensitive file detection
    └── reporting/
        ├── report_generator.py    # Finding aggregation
        ├── markdown_report.py     # Markdown report writer
        ├── dashboard_generator.py # HTML dashboard
        ├── llm_report.py          # LLM analysis report
        └── templates/
            └── dashboard_template.html
```

---

## Known Limitations

- **Speed** — scanning large sites (e.g. wikipedia.com) can take a long time due to the volume of Wayback snapshots. Use `--last 2` or `--threads 20` to reduce scan time. A snapshot cap and further parallelisation are planned.
- **False positives** — high-entropy detection and generic secret patterns produce false positives on minified JS. Manual triage of findings is recommended.
- **ThreatCrowd** — this source is often unreliable and may return 0 results. This is expected.
- **Wayback failures** — a high failed download count is normal; many archived URLs are no longer served by Wayback. Filtering by HTTP status code at the snapshot stage is a planned improvement.

---

## Disclaimer

WayHunt is intended for **authorised security testing and research only**. Only scan domains you own or have explicit permission to test. All data retrieved is sourced from public Wayback Machine archives.

---

*Janus Security Tool Suite — by Kels1er*

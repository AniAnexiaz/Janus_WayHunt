# WayHunt — To-Do

Tracked improvements and known issues. See `README.md` for current features and limitations.

---

## Performance

- [ ] Parallelise Wayback CDX queries across subdomains — currently sequential, major bottleneck on large sites
- [ ] Filter snapshots by recorded HTTP status before downloading — cuts failed downloads significantly
- [ ] Configurable snapshot cap (`MAX_SNAPSHOTS` in `config.py`) to limit run time on large sites
- [ ] Reduce default timeouts — `wayback_api.py` (20s → 10s), `snapshot_stream.py` (15s → 6s)
- [ ] Increase default threads from 10 to 20

## Features

- [ ] Wire up `context_extractor.py` to enrich finding context snippets in reports
- [ ] Add `--no-cap` flag to override snapshot cap for full deep scans
- [ ] Resume interrupted scans from saved `snapshots.json`
- [ ] Add `--output <dir>` flag to override the default output directory

## Code Quality

- [ ] Add `__init__.py` files to all packages if missing
- [ ] Add unit and integration test suite (see `WayHunt_Test_Plan.docx`)
- [ ] Replace hardcoded `→` arrow in markdown report with ASCII `->` for full Windows cp1252 compatibility (currently fixed with utf-8 encoding)

## Reporting

- [ ] Add severity breakdown chart to HTML dashboard
- [ ] Include subdomain list in markdown report summary
- [ ] Add JSON export of final intelligence findings for external tooling

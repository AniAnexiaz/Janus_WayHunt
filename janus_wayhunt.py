import argparse
import re
import sys

from wayhunt.core.logger import set_verbose
from wayhunt.core.pipeline import run_pipeline


FULL_BANNER = r"""
██     ██  █████  ██    ██ ██   ██ ██    ██ ███    ██ ████████
██     ██ ██   ██  ██  ██  ██   ██ ██    ██ ████   ██    ██
██  █  ██ ███████   ████   ███████ ██    ██ ██ ██  ██    ██
██ ███ ██ ██   ██    ██    ██   ██ ██    ██ ██  ██ ██    ██
 ███ ███  ██   ██    ██    ██   ██  ██████  ██   ████    ██

              WayHunt Wayback Archive Attack Surface Analysis Tool
              by Kels1er
"""

MIN_BANNER = "WayHunt — Janus Security Tool Suite"


MIN_HELP = """
Usage:
  janus wayhunt <domain> [options]

Run with --help for full help.
"""


FULL_HELP = """
WayHunt
Janus Security Tool Suite

Usage:
  janus wayhunt <domain> [options]

Core Options

  --last <years>       Wayback search window (default: 5)
  --threads <n>        Worker threads (default: 10)

Reporting

  --dashboard          Generate HTML dashboard

LLM Analysis

  --llm-url <url>      Local or custom LLM endpoint
  --llm-api <key>      API provider key
  --llm-model <name>   Optional model name

Display

  -v, --verbose        Show detailed per-item log output
  --no-banner          Disable banner output

Examples

  python janus_wayhunt.py example.com
  python janus_wayhunt.py example.com --last 10
  python janus_wayhunt.py example.com --dashboard
  python janus_wayhunt.py example.com -v
  python janus_wayhunt.py example.com --llm-url http://localhost:11434
  python janus_wayhunt.py example.com --llm-api sk-xxxxx
"""


DOMAIN_REGEX = r"^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def valid_domain(domain: str) -> bool:
    return re.match(DOMAIN_REGEX, domain) is not None


def build_parser():

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument("domain", nargs="?")

    parser.add_argument("--last", type=int, default=5)
    parser.add_argument("--threads", type=int, default=10)

    parser.add_argument("--dashboard", action="store_true")

    parser.add_argument("--llm-url")
    parser.add_argument("--llm-api")
    parser.add_argument("--llm-model")

    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--no-banner", action="store_true")

    parser.add_argument("-h", "--help", action="store_true")

    return parser


def main():

    parser = build_parser()
    args = parser.parse_args()

    # No arguments
    if len(sys.argv) == 1:
        print(FULL_BANNER)
        print(MIN_HELP)
        return

    # Help
    if args.help:
        if not args.no_banner:
            print(FULL_BANNER)
        print(FULL_HELP)
        return

    # Domain required
    if not args.domain:
        print(MIN_HELP)
        return

    # Domain validation
    if not valid_domain(args.domain):
        print("[WayHunt] Invalid domain format")
        return

    # Set verbose BEFORE any module imports logger
    set_verbose(args.verbose)

    # Banner
    if not args.no_banner:
        print(MIN_BANNER)

    print(f"Target: {args.domain}")
    print(f"Wayback window: last {args.last} years")
    print(f"Threads: {args.threads}")
    if args.verbose:
        print("Mode: verbose\n")

    # LLM config
    llm_config = {
        "url": args.llm_url,
        "api_key": args.llm_api,
        "model": args.llm_model
    }

    llm_enabled = any(llm_config.values())

    # Run pipeline
    run_pipeline(
        domain=args.domain,
        years=args.last,
        threads=args.threads,
        dashboard=args.dashboard,
        llm=llm_config if llm_enabled else None
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Job Search Agent - CLI entry point."""

import argparse
import sys

from job_search_agent.orchestrator import Orchestrator


def main():
    parser = argparse.ArgumentParser(
        description="Search jobs from target companies",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default configuration
  python search.py -c config/companies.yaml -t config/titles.yaml

  # Custom output directory
  python search.py -c config/companies.yaml -t config/titles.yaml -o my_results

  # Longer timeout for slow sites
  python search.py -c config/companies.yaml -t config/titles.yaml --timeout 60
        """,
    )

    parser.add_argument(
        "--companies", "-c",
        required=True,
        help="Path to companies YAML file",
    )
    parser.add_argument(
        "--titles", "-t",
        required=True,
        help="Path to job titles YAML file",
    )
    parser.add_argument(
        "--output", "-o",
        default="job_results",
        help="Output directory for results (default: job_results)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Request timeout in seconds (default: 30)",
    )

    args = parser.parse_args()

    try:
        orchestrator = Orchestrator(
            companies_file=args.companies,
            titles_file=args.titles,
            output_dir=args.output,
            timeout=args.timeout,
        )

        summary = orchestrator.run()
        print("\nDone!")

    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

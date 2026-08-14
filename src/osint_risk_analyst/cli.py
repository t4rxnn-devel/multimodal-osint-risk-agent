"""
Command-line interface for the OSINT Risk Analyst.

Usage:
    osint-analyze --target "TSMC Arizona" --focus water --focus geopolitical
"""

from __future__ import annotations

import argparse
import json
import sys

from osint_risk_analyst import RiskAnalyst


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Enterprise OSINT Supply Chain Risk Analyst",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Target entity, corporation, or trade corridor to analyze.",
    )
    parser.add_argument(
        "--focus",
        action="append",
        default=[],
        help="Risk domain to emphasize (can be used multiple times).",
    )
    parser.add_argument(
        "--format",
        choices=["markdown", "json"],
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--output",
        "-o",
        help="Write output to file instead of stdout.",
    )

    args = parser.parse_args()

    analyst = RiskAnalyst()
    result = analyst.analyze(
        target=args.target,
        focus_areas=args.focus,
        output_format=args.format,
    )

    output = result if args.format == "markdown" else json.dumps(result, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"Report written to {args.output}", file=sys.stderr)
    else:
        print(output)

    return 0


if __name__ == "__main__":
    sys.exit(main())

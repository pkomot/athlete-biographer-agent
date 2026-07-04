"""CLI entry point: python -m beyond_the_track "Athlete Name" """

import argparse
import os
import sys

from .agent import MODEL_ID, BeyondTheTrackBiographer


def main() -> int:
    parser = argparse.ArgumentParser(
        prog="beyond_the_track",
        description="Profile an athlete's life beyond their sport.",
    )
    parser.add_argument("athlete", help='Athlete name, e.g. "Faith Kipyegon"')
    parser.add_argument(
        "--model", default=MODEL_ID, help=f"Claude model id (default: {MODEL_ID})"
    )
    parser.add_argument(
        "--max-searches", type=int, default=15,
        help="Cap on web searches per profile (default: 15)",
    )
    args = parser.parse_args()

    if not os.environ.get("ANTHROPIC_API_KEY"):
        print(
            "ANTHROPIC_API_KEY is not set. Export it first:\n"
            "  export ANTHROPIC_API_KEY=sk-ant-...",
            file=sys.stderr,
        )
        return 1

    biographer = BeyondTheTrackBiographer(
        model=args.model, max_searches=args.max_searches
    )
    print(f'Researching "{args.athlete}" — this can take a couple of minutes...\n',
          file=sys.stderr)
    print(biographer.profile(args.athlete))
    return 0


if __name__ == "__main__":
    sys.exit(main())

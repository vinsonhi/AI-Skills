#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys

from real_chrome_helpers import extract_x_timeline_with_personal_chrome


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["for_you", "following"], required=True)
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--settle-seconds", type=int, default=8)
    parser.add_argument("--click-seconds", type=int, default=4)
    args = parser.parse_args()

    payload = extract_x_timeline_with_personal_chrome(
        args.mode,
        limit=args.limit,
        settle_seconds=args.settle_seconds,
        click_seconds=args.click_seconds,
    )
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if payload.get("items") else 1


if __name__ == "__main__":
    sys.exit(main())

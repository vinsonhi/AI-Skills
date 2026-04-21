#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo


SH_TZ = ZoneInfo("Asia/Shanghai")
SKILL_ROOT = Path(__file__).resolve().parents[1]


def normalize_title(title: str) -> str:
    title = title.lower()
    title = re.sub(r"^show hn:\s*", "", title)
    title = re.sub(r"[\W_]+", "", title)
    return title


def parse_time_label(value: str, now: datetime) -> datetime | None:
    text = (value or "").strip()
    lower = text.lower()
    if not text:
        return None
    if lower in {"real-time", "today", "updated recently"}:
        return now

    minute_match = re.match(r"^(\d+)\s*分钟前$", text)
    if minute_match:
        return now - timedelta(minutes=int(minute_match.group(1)))

    hour_match = re.match(r"^(\d+)\s*(hours?|小时前?)\s*ago?$", lower)
    if hour_match:
        return now - timedelta(hours=int(hour_match.group(1)))

    for fmt in (
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%d %H:%M",
        "%Y-%m-%dT%H:%M:%S%z",
        "%Y-%m-%dT%H:%M:%S",
        "%a, %d %b %Y %H:%M:%S %Z",
    ):
        try:
            dt = datetime.strptime(text, fmt)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=SH_TZ)
            return dt.astimezone(SH_TZ)
        except ValueError:
            continue
    return None


def load_recent_titles(sections_dir: Path, section_suffix: str, date_str: str, lookback_days: int) -> set[str]:
    current = datetime.strptime(date_str, "%Y-%m-%d").date()
    titles: set[str] = set()
    for offset in range(1, lookback_days + 1):
        day = current - timedelta(days=offset)
        path = sections_dir / f"{day.isoformat()}-{section_suffix}.md"
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("#### "):
                titles.add(normalize_title(line[5:].strip()))
    return titles


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-json", required=True)
    parser.add_argument("--section-suffix", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--sections-dir", default=str(SKILL_ROOT / "reports" / "sections"))
    parser.add_argument("--lookback-days", type=int, default=3)
    parser.add_argument("--hours", type=int, default=24)
    args = parser.parse_args()

    now = datetime.now(SH_TZ)
    recent_titles = load_recent_titles(
        Path(args.sections_dir),
        args.section_suffix,
        args.date,
        args.lookback_days,
    )
    payload = json.loads(Path(args.input_json).read_text())

    kept = []
    for item in payload:
        item_dt = parse_time_label(item.get("time", ""), now)
        if item_dt is None or now - item_dt > timedelta(hours=args.hours):
            continue
        if normalize_title(item.get("title", "")) in recent_titles:
            continue
        kept.append(item)

    print(json.dumps(kept, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

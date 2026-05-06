#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
LOCAL_SCRIPT = SKILL_ROOT / "scripts" / "extract_x_accounts_with_personal_chrome.py"
DEFAULT_FOLLOW_BUILDERS_FEED = (
    "https://raw.githubusercontent.com/zarazhangrui/follow-builders/main/feed-x.json"
)


def parse_time(value: str) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def filter_recent(items: list[dict], *, lookback_hours: int, now: datetime) -> list[dict]:
    cutoff = now - timedelta(hours=lookback_hours)
    recent = []
    for item in items:
        dt = parse_time(str(item.get("createdAt") or item.get("published_at") or ""))
        if dt is None or dt >= cutoff:
            recent.append(item)
    return recent


def run_local(per_account_limit: int, settle_seconds: int, lookback_hours: int) -> dict:
    proc = subprocess.run(
        [
            sys.executable,
            str(LOCAL_SCRIPT),
            "--per-account-limit",
            str(per_account_limit),
            "--settle-seconds",
            str(settle_seconds),
        ],
        text=True,
        capture_output=True,
        timeout=max(120, settle_seconds * 40),
    )
    if proc.returncode != 0:
        raise RuntimeError((proc.stderr or proc.stdout or "").strip() or f"local script exited {proc.returncode}")

    payload = json.loads(proc.stdout)
    now = datetime.now(timezone.utc)
    total_recent = 0
    accounts = []
    for account in payload.get("results", []):
        items = account.get("items") or []
        recent_items = filter_recent(items, lookback_hours=lookback_hours, now=now)
        if not recent_items:
            continue
        tweets = []
        for item in recent_items:
            status_url = item.get("status_url", "")
            tweet_id = status_url.rstrip("/").rsplit("/", 1)[-1] if status_url else ""
            tweets.append(
                {
                    "id": tweet_id,
                    "text": item.get("text", ""),
                    "createdAt": item.get("published_at", ""),
                    "url": status_url,
                    "metrics": item.get("metrics", []),
                }
            )
        accounts.append(
            {
                "source": "x",
                "name": account.get("identity") or account.get("handle", ""),
                "handle": str(account.get("handle", "")).lstrip("@"),
                "bio": account.get("identity", ""),
                "tweets": tweets,
            }
        )
        total_recent += len(tweets)

    if total_recent == 0:
        raise RuntimeError("local X session returned no recent fixed-account posts")

    return {
        "source": "X Fixed AI Builders",
        "fetch_mode": "local_chrome_login",
        "lookback_hours": lookback_hours,
        "x": accounts,
        "stats": {
            "xBuilders": len(accounts),
            "totalTweets": total_recent,
        },
        "failures": payload.get("failures", []),
        "profile": payload.get("profile"),
    }


def fetch_follow_builders(feed_url: str, lookback_hours: int) -> dict:
    req = urllib.request.Request(feed_url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as response:
        payload = json.loads(response.read().decode("utf-8"))

    now = datetime.now(timezone.utc)
    total_recent = 0
    accounts = []
    for account in payload.get("x", []):
        tweets = filter_recent(account.get("tweets") or [], lookback_hours=lookback_hours, now=now)
        if not tweets:
            continue
        normalized = dict(account)
        normalized["tweets"] = tweets
        accounts.append(normalized)
        total_recent += len(tweets)

    if total_recent == 0:
        raise RuntimeError("follow-builders feed contains no recent fixed-account posts")

    return {
        "source": "X Fixed AI Builders",
        "fetch_mode": "follow_builders_central_feed",
        "feed_url": feed_url,
        "generatedAt": payload.get("generatedAt"),
        "lookback_hours": lookback_hours,
        "x": accounts,
        "stats": {
            "xBuilders": len(accounts),
            "totalTweets": total_recent,
        },
        "errors": payload.get("errors"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["auto", "local", "follow-builders"], default="auto")
    parser.add_argument("--per-account-limit", type=int, default=3)
    parser.add_argument("--settle-seconds", type=int, default=7)
    parser.add_argument("--lookback-hours", type=int, default=24)
    parser.add_argument("--follow-builders-feed", default=DEFAULT_FOLLOW_BUILDERS_FEED)
    args = parser.parse_args()

    errors = []
    if args.mode in {"auto", "local"}:
        try:
            print(
                json.dumps(
                    run_local(args.per_account_limit, args.settle_seconds, args.lookback_hours),
                    ensure_ascii=False,
                    indent=2,
                )
            )
            return 0
        except Exception as exc:
            errors.append(f"local_chrome_login: {type(exc).__name__}: {exc}")
            if args.mode == "local":
                print(json.dumps({"ok": False, "errors": errors}, ensure_ascii=False, indent=2))
                return 1

    if args.mode in {"auto", "follow-builders"}:
        try:
            payload = fetch_follow_builders(args.follow_builders_feed, args.lookback_hours)
            if errors:
                payload["fallback_reason"] = errors
            print(json.dumps(payload, ensure_ascii=False, indent=2))
            return 0
        except Exception as exc:
            errors.append(f"follow_builders_central_feed: {type(exc).__name__}: {exc}")

    print(
        json.dumps(
            {
                "ok": False,
                "source": "X Fixed AI Builders",
                "fetch_mode": "missing",
                "errors": errors,
                "message": "X fixed-account source unavailable. Write an explicit X data gap; do not substitute anonymous search or recommendation feeds.",
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())

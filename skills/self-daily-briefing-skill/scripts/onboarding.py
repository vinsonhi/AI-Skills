#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
WATCHLIST_PATH = SKILL_ROOT / "instructions" / "us_stocks_watchlist_default.txt"
PREFERENCES_PATH = SKILL_ROOT / "instructions" / "local_user_preferences.md"
ONBOARDING_STATE_PATH = SKILL_ROOT / "instructions" / ".local_onboarding_state.json"
X_ACCOUNTS_PATH = SKILL_ROOT / "instructions" / "x_ai_accounts.txt"
PODCASTS_PATH = SKILL_ROOT / "instructions" / "ai_podcasts.txt"
BLOGS_PATH = SKILL_ROOT / "instructions" / "ai_official_blogs.txt"


def normalize_tickers(raw: str) -> list[str]:
    candidates = re.split(r"[\s,，;；/|]+", raw.strip())
    tickers: list[str] = []
    seen: set[str] = set()
    for item in candidates:
        ticker = item.strip().upper()
        if not ticker or ticker in {"无", "没有", "NO", "NONE", "NA", "N/A"}:
            continue
        if not re.fullmatch(r"[A-Z][A-Z0-9.-]{0,9}", ticker):
            raise ValueError(f"invalid ticker: {item}")
        if ticker not in seen:
            seen.add(ticker)
            tickers.append(ticker)
    return tickers


def write_watchlist(tickers: list[str]) -> None:
    WATCHLIST_PATH.parent.mkdir(parents=True, exist_ok=True)
    WATCHLIST_PATH.write_text("\n".join(tickers) + "\n", encoding="utf-8")


def count_data_lines(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.startswith("#"))


def first_column_values(path: Path) -> list[str]:
    if not path.exists():
        return []
    values = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if line and not line.startswith("#"):
            values.append(line.split("\t")[0])
    return values


def write_preferences(*, language: str | None, interests: str | None) -> None:
    if not language and not interests:
        return
    lines = ["# Local Daily Briefing Preferences", ""]
    if language:
        lines.append(f"- language: {language}")
    if interests:
        lines.append(f"- extra_interests: {interests}")
    lines.append("")
    PREFERENCES_PATH.write_text("\n".join(lines), encoding="utf-8")


def onboarding_complete() -> bool:
    if not ONBOARDING_STATE_PATH.exists():
        return False
    try:
        state = json.loads(ONBOARDING_STATE_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return False
    return bool(state.get("onboardingComplete"))


def mark_onboarding_complete() -> None:
    ONBOARDING_STATE_PATH.write_text(
        json.dumps({"onboardingComplete": True}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Onboard self-daily-briefing-skill and optionally save a local US stock watchlist."
    )
    parser.add_argument(
        "--language",
        choices=["zh", "en", "bilingual"],
        help="Preferred report language.",
    )
    parser.add_argument(
        "--watchlist",
        help="Comma or space separated tickers to save, for example: NVDA,AMD,MSFT",
    )
    parser.add_argument(
        "--interests",
        help="Extra topics, companies, people, or themes to pay attention to.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the onboarding prompt without writing files.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Show onboarding even if it has already been completed.",
    )
    args = parser.parse_args()

    if onboarding_complete() and not args.force:
        print("日报偏好已经设置过了。之后直接生成日报即可；如果你想调整股票、语言或关注主题，告诉我“重新设置日报偏好”。")
        return 0

    existing = WATCHLIST_PATH.read_text(encoding="utf-8").strip() if WATCHLIST_PATH.exists() else ""
    x_count = count_data_lines(X_ACCOUNTS_PATH)
    podcast_names = first_column_values(PODCASTS_PATH)
    blog_names = first_column_values(BLOGS_PATH)

    print("Step 1 — 自我介绍")
    print("我是你的个人日报助手。每天我会帮你把综合新闻、财经、科技、AI 深度和美股自选整理成一份能直接读的 Morning Brief。")
    print(f"AI 深度部分会重点跟踪 {x_count} 位 AI builder 的 X 动态、{len(podcast_names)} 档顶级 AI 播客，以及 AI 公司官方博客。")
    print("")
    print("Step 2 — 语言偏好")
    print("你希望日报用哪种语言？可以选：中文、英文、双语。")
    print("如果你没有特别偏好，我会默认用中文，并保留关键英文产品名、论文名和公司名。")
    print("")
    print("Step 3 — 股票跟踪偏好和额外关注")
    if existing:
        print("我看到你本地已经有一份美股观察名单；要更新的话，直接给我新的 ticker 列表就行。")
    else:
        print("你有想长期关注的美股股票吗？有的话直接发 ticker，例如：NVDA, AMD, MSFT。")
        print("还没想好也没关系，回复“没有”即可；以后想加的时候再告诉我。")
    print("除了股票，也可以告诉我你特别想关注的公司、产品、人物或主题，比如 Claude Code、机器人、AI 搜索、OpenAI、Anthropic、英伟达产业链。")
    print("")
    print("Step 4 — 信息源确认")
    print("我默认会看这些 AI 信息源：")
    print(f"- X builders：{', '.join(first_column_values(X_ACCOUNTS_PATH)[:8])} 等 {x_count} 个账号")
    print(f"- 播客：{', '.join(podcast_names)}")
    print(f"- 官方博客：{', '.join(blog_names)}")
    print("如果这些没问题，我可以现在就先跑一遍，让你看第一版日报效果。")

    if args.dry_run:
        return 0

    write_preferences(language=args.language, interests=args.interests)

    raw = args.watchlist
    if raw is None and not sys.stdin.isatty():
        raw = sys.stdin.read().strip()
    if raw:
        tickers = normalize_tickers(raw)
        if tickers:
            write_watchlist(tickers)
            print("已记下你的美股观察名单，之后美股早报会默认跟踪：")
            print(", ".join(tickers))
        else:
            print("未写入股票名单；之后可随时补充。")
    if args.language or args.interests:
        print("已记下你的日报偏好。")
    mark_onboarding_complete()
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from real_chrome_helpers import applescript_quote, resolve_profile_info, run_applescript


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ACCOUNTS = SKILL_ROOT / "instructions" / "x_ai_accounts.txt"


def load_accounts(path: Path) -> list[dict[str, str]]:
    accounts: list[dict[str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        handle, _, identity = line.partition("\t")
        handle = handle.strip()
        if not handle.startswith("@"):
            handle = f"@{handle}"
        accounts.append({"handle": handle, "identity": identity.strip()})
    return accounts


def _extract_js(limit: int) -> str:
    return rf"""
(() => {{
  const cleanStatusUrl = (href) => {{
    if (!href) return "";
    return href.replace(/\/photo\/\d+$/, "").replace(/\/analytics$/, "");
  }};
  const articles = [...document.querySelectorAll('article[data-testid="tweet"]')];
  const items = [];
  const seen = new Set();
  for (const article of articles) {{
    const status = [...article.querySelectorAll('a[href*="/status/"]')]
      .map((node) => cleanStatusUrl(node.href))
      .find((href) => href && !href.includes("/photo/") && !href.endsWith("/analytics"));
    const text = [...article.querySelectorAll('[data-testid="tweetText"]')]
      .map((node) => node.innerText.trim())
      .filter(Boolean)
      .join("\n") || article.innerText.trim();
    if (!status || !text || seen.has(status)) {{
      continue;
    }}
    seen.add(status);
    const timeNode = article.querySelector("time");
    const metrics = [...article.querySelectorAll('[role="group"] span')]
      .map((node) => node.innerText.trim())
      .filter(Boolean);
    items.push({{
      status_url: status,
      published_at: timeNode ? timeNode.getAttribute("datetime") : "",
      text,
      metrics,
    }});
    if (items.length >= {int(limit)}) break;
  }}
  return JSON.stringify({{
    url: location.href,
    title: document.title,
    body_hint: document.body ? document.body.innerText.slice(0, 400) : "",
    items,
  }});
}})();
""".strip()


def extract_account(handle: str, *, limit: int, settle_seconds: int) -> dict:
    screen_name = handle.lstrip("@")
    target_url = f"https://x.com/{screen_name}"
    script = f"""
set targetUrl to {applescript_quote(target_url)}
set extractSource to {applescript_quote(_extract_js(limit))}
tell application "Google Chrome"
  activate
  set probeWindow to make new window
  set URL of active tab of probeWindow to targetUrl
  delay {int(settle_seconds)}
  set extractResult to execute active tab of probeWindow javascript extractSource
  close probeWindow
  return extractResult
end tell
"""
    payload = json.loads(run_applescript(script))
    payload["handle"] = handle
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--accounts-file", default=str(DEFAULT_ACCOUNTS))
    parser.add_argument("--per-account-limit", type=int, default=3)
    parser.add_argument("--settle-seconds", type=int, default=7)
    args = parser.parse_args()

    accounts = load_accounts(Path(args.accounts_file))
    results = []
    failures = []
    for account in accounts:
        try:
            payload = extract_account(
                account["handle"],
                limit=args.per_account_limit,
                settle_seconds=args.settle_seconds,
            )
            payload["identity"] = account["identity"]
            results.append(payload)
        except Exception as exc:
            failures.append(
                {
                    "handle": account["handle"],
                    "identity": account["identity"],
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    output = {
        "source": "X Fixed AI Builders",
        "accounts_file": str(Path(args.accounts_file).resolve()),
        "profile": resolve_profile_info(),
        "results": results,
        "failures": failures,
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))
    return 0 if any(item.get("items") for item in results) else 1


if __name__ == "__main__":
    sys.exit(main())

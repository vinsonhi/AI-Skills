#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any


CHROME_APP = "/Applications/Google Chrome.app"
CHROME_BIN = f"{CHROME_APP}/Contents/MacOS/Google Chrome"
CHROME_USER_DATA_DIR = Path.home() / "Library/Application Support/Google/Chrome"
LOCAL_STATE_PATH = CHROME_USER_DATA_DIR / "Local State"


def applescript_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def run_applescript(source: str) -> str:
    proc = subprocess.run(
        ["osascript", "-"],
        input=source,
        text=True,
        capture_output=True,
        check=True,
    )
    return proc.stdout.strip()


def chrome_running() -> bool:
    try:
        out = run_applescript('tell application "Google Chrome" to return running')
    except subprocess.CalledProcessError:
        return False
    return out.strip().lower() == "true"


def resolve_profile_info() -> dict[str, Any]:
    profile_name = "Default"
    last_active_profiles: list[str] = []
    info_cache_keys: list[str] = []

    if LOCAL_STATE_PATH.exists():
        state = json.loads(LOCAL_STATE_PATH.read_text())
        profile = state.get("profile", {})
        profile_name = profile.get("last_used") or "Default"
        last_active_profiles = profile.get("last_active_profiles") or []
        info_cache_keys = sorted((profile.get("info_cache") or {}).keys())

    return {
        "chrome_bin": CHROME_BIN,
        "user_data_dir": str(CHROME_USER_DATA_DIR),
        "profile_directory": profile_name,
        "last_active_profiles": last_active_profiles,
        "info_cache_keys": info_cache_keys,
        "chrome_running": chrome_running(),
    }


def _x_probe_payload() -> str:
    return r"""
(() => {
  const body = document.body ? document.body.innerText.slice(0, 2000) : "";
  const tabs = [...document.querySelectorAll('[role="tab"]')]
    .map((el) => (el.innerText || "").trim())
    .filter(Boolean);
  return JSON.stringify({
    url: location.href,
    title: document.title,
    tabs,
    body,
  });
})();
""".strip()


def probe_x_home_with_personal_chrome(settle_seconds: int = 8, close_window: bool = True) -> dict[str, Any]:
    script = f"""
set targetUrl to {applescript_quote("https://x.com/home")}
set jsSource to {applescript_quote(_x_probe_payload())}
tell application "Google Chrome"
  activate
  set probeWindow to make new window
  set URL of active tab of probeWindow to targetUrl
  delay {int(settle_seconds)}
  set probeResult to execute active tab of probeWindow javascript jsSource
  {"close probeWindow" if close_window else ""}
  return probeResult
end tell
"""
    payload = json.loads(run_applescript(script))
    payload["profile"] = resolve_profile_info()
    payload["logged_in"] = (
        payload.get("url", "").startswith("https://x.com/home")
        and "For you" in payload.get("tabs", [])
        and "Following" in payload.get("tabs", [])
        and "/i/flow/login" not in payload.get("url", "")
        and "Sign in" not in payload.get("body", "")
    )
    return payload


def extract_x_timeline_with_personal_chrome(
    mode: str,
    *,
    limit: int = 5,
    settle_seconds: int = 8,
    click_seconds: int = 4,
) -> dict[str, Any]:
    if mode not in {"for_you", "following"}:
        raise ValueError(f"unsupported mode: {mode}")

    click_js = "null"
    if mode == "following":
        click_js = r"""
(() => {
  const tab = [...document.querySelectorAll('[role="tab"]')]
    .find((el) => (el.innerText || "").trim() === "Following");
  if (!tab) {
    return "missing";
  }
  tab.click();
  return "clicked";
})();
""".strip()
    else:
        click_js = r"""
(() => {
  const tab = [...document.querySelectorAll('[role="tab"]')]
    .find((el) => (el.innerText || "").trim() === "For you");
  if (!tab) {
    return "missing";
  }
  tab.click();
  return "clicked";
})();
""".strip()

    extract_js = r"""
(() => {
  const cleanStatusUrl = (href) => {
    if (!href) return "";
    return href.replace(/\/photo\/\d+$/, "").replace(/\/analytics$/, "");
  };
  const articles = [...document.querySelectorAll('article[data-testid="tweet"]')];
  const items = [];
  const seen = new Set();
  for (const article of articles) {
    const status = [...article.querySelectorAll('a[href*="/status/"]')]
      .map((node) => cleanStatusUrl(node.href))
      .find((href) => href && !href.includes("/photo/") && !href.endsWith("/analytics"));
    const text = [...article.querySelectorAll('[data-testid="tweetText"]')]
      .map((node) => node.innerText.trim())
      .filter(Boolean)
      .join("\n") || article.innerText.trim();
    if (!status || !text || seen.has(status)) {
      continue;
    }
    seen.add(status);
    const timeNode = article.querySelector("time");
    const metrics = [...article.querySelectorAll('[role="group"] span')]
      .map((node) => node.innerText.trim())
      .filter(Boolean);
    items.push({
      status_url: status,
      author: (article.innerText.split("\n")[0] || "").trim(),
      published_at: timeNode ? timeNode.getAttribute("datetime") : "",
      text,
      metrics,
    });
  }
  return JSON.stringify({
    url: location.href,
    title: document.title,
    tabs: [...document.querySelectorAll('[role="tab"]')].map((el) => ({
      text: (el.innerText || "").trim(),
      selected: el.getAttribute("aria-selected"),
    })),
    items,
  });
})();
""".strip()

    script = f"""
set targetUrl to {applescript_quote("https://x.com/home")}
set clickSource to {applescript_quote(click_js)}
set extractSource to {applescript_quote(extract_js)}
tell application "Google Chrome"
  activate
  set probeWindow to make new window
  set URL of active tab of probeWindow to targetUrl
  delay {int(settle_seconds)}
  set clickResult to execute active tab of probeWindow javascript clickSource
  delay {int(click_seconds)}
  set extractResult to execute active tab of probeWindow javascript extractSource
  close probeWindow
  return clickResult & linefeed & extractResult
end tell
"""
    raw = run_applescript(script)
    click_result, _, payload_raw = raw.partition("\n")
    payload = json.loads(payload_raw)
    payload["mode"] = mode
    payload["click_result"] = click_result.strip()
    payload["items"] = payload.get("items", [])[:limit]
    payload["profile"] = resolve_profile_info()
    return payload

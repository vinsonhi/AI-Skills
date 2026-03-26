#!/usr/bin/env python3
from __future__ import annotations

import json
import sys

import browser_cookie3

from real_chrome_helpers import probe_x_home_with_personal_chrome


EXPECTED = {"auth_token", "ct0"}


def auxiliary_cookie_probe() -> dict[str, str]:
    try:
        jar = browser_cookie3.chrome(domain_name="x.com")
        names = {cookie.name for cookie in jar}
        missing = sorted(EXPECTED - names)
        return {
            "cookie_probe": "ok",
            "cookie_count": str(len(jar)),
            "cookie_names": ",".join(sorted(names)),
            "missing_required": ",".join(missing),
        }
    except Exception as exc:  # pragma: no cover - machine specific failure path
        return {
            "cookie_probe": "error",
            "cookie_error": f"{type(exc).__name__}: {exc}",
        }


def main() -> int:
    aux = auxiliary_cookie_probe()
    state = probe_x_home_with_personal_chrome()
    profile = state["profile"]

    lines = {
        "chrome_bin": profile["chrome_bin"],
        "user_data_dir": profile["user_data_dir"],
        "profile_directory": profile["profile_directory"],
        "chrome_running": str(profile["chrome_running"]).lower(),
        "url": state.get("url", ""),
        "title": state.get("title", ""),
        "tabs": ",".join(state.get("tabs", [])),
        "logged_in": str(state.get("logged_in", False)).lower(),
        "body_hint": state.get("body", "")[:240].replace("\n", " "),
    }
    lines.update(aux)

    for key, value in lines.items():
        print(f"{key}={value}")
    print("probe_json=" + json.dumps(state, ensure_ascii=False))
    return 0 if state.get("logged_in") else 1


if __name__ == "__main__":
    sys.exit(main())

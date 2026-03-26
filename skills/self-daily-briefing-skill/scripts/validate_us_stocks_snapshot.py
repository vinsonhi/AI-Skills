#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def load_snapshot(path: Path) -> dict[str, dict]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, list):
        items = raw
    elif isinstance(raw, dict) and isinstance(raw.get("items"), list):
        items = raw["items"]
    elif isinstance(raw, dict):
        items = []
        for ticker, payload in raw.items():
            if isinstance(payload, dict):
                item = dict(payload)
                item.setdefault("ticker", ticker)
                items.append(item)
    else:
        raise ValueError("unsupported snapshot format")

    out: dict[str, dict] = {}
    for item in items:
        ticker = str(item.get("ticker", "")).upper().strip()
        if ticker:
            out[ticker] = item
    return out


def parse_expected(value: str) -> list[str]:
    return [part.strip().upper() for part in value.split(",") if part.strip()]


def as_float(value) -> float | None:
    try:
        return float(value)
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--snapshot-json", required=True)
    parser.add_argument("--expected-tickers", required=True)
    parser.add_argument("--secondary-json")
    parser.add_argument("--max-drift-pct", type=float, default=1.0)
    args = parser.parse_args()

    primary = load_snapshot(Path(args.snapshot_json))
    expected = parse_expected(args.expected_tickers)
    secondary = load_snapshot(Path(args.secondary_json)) if args.secondary_json else {}

    errors: list[str] = []
    warnings: list[str] = []

    missing = [ticker for ticker in expected if ticker not in primary]
    extra = [ticker for ticker in primary if ticker not in expected]
    if missing:
        errors.append(f"missing tickers: {', '.join(missing)}")
    if extra:
        warnings.append(f"unexpected tickers: {', '.join(extra)}")

    required_fields = ("price", "change", "change_percent", "latest_trade_time")
    trade_times: dict[str, str] = {}
    for ticker in expected:
        item = primary.get(ticker)
        if not item:
            continue
        for field in required_fields:
            if item.get(field) in (None, ""):
                errors.append(f"{ticker}: missing field {field}")
        price = as_float(item.get("price"))
        change = as_float(item.get("change"))
        change_pct = as_float(item.get("change_percent"))
        if price is None or price <= 0:
            errors.append(f"{ticker}: invalid price {item.get('price')}")
        if change is None:
            errors.append(f"{ticker}: invalid change {item.get('change')}")
        if change_pct is None:
            errors.append(f"{ticker}: invalid change_percent {item.get('change_percent')}")
        trade_times[ticker] = str(item.get("latest_trade_time", ""))

    for ticker in expected:
        if ticker not in secondary or ticker not in primary:
            continue
        primary_price = as_float(primary[ticker].get("price"))
        secondary_price = as_float(secondary[ticker].get("price"))
        if primary_price is None or secondary_price is None or primary_price == 0:
            continue
        drift_pct = abs(primary_price - secondary_price) / primary_price * 100
        if drift_pct > args.max_drift_pct:
            errors.append(
                f"{ticker}: secondary drift {drift_pct:.2f}% exceeds {args.max_drift_pct:.2f}%"
            )

    payload = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "expected_tickers": expected,
        "primary_tickers": sorted(primary.keys()),
        "trade_times": trade_times,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())

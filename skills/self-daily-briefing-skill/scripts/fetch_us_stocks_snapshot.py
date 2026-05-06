#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import json
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo


SKILL_ROOT = Path(__file__).resolve().parents[1]
WATCHLIST_PATH = SKILL_ROOT / "instructions" / "us_stocks_watchlist_default.txt"
VALIDATOR = SKILL_ROOT / "scripts" / "validate_us_stocks_snapshot.py"
DEFAULT_WATCHLIST = ["AAPL", "MSFT", "NVDA", "AMZN", "GOOGL", "META", "TSLA"]


def read_watchlist(path: Path) -> list[str]:
    if not path.exists():
        return DEFAULT_WATCHLIST
    tickers = []
    seen = set()
    for raw in path.read_text(encoding="utf-8").splitlines():
        ticker = raw.strip().upper()
        if not ticker or ticker.startswith("#"):
            continue
        if ticker not in seen:
            seen.add(ticker)
            tickers.append(ticker)
    return tickers or DEFAULT_WATCHLIST


def yahoo_symbol(ticker: str) -> str:
    # Yahoo uses hyphen for share classes such as BRK-B.
    return ticker.replace(".", "-")


def stooq_symbol(ticker: str) -> str:
    return ticker.replace("-", ".").lower() + ".us"


def fetch_yahoo(ticker: str) -> dict:
    symbol = yahoo_symbol(ticker)
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(symbol)}?range=7d&interval=1d&includePrePost=false"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        payload = json.loads(response.read().decode("utf-8"))
    result = payload["chart"]["result"][0]
    quote = result["indicators"]["quote"][0]
    rows = []
    for ts, open_, high, low, close, volume in zip(
        result["timestamp"],
        quote["open"],
        quote["high"],
        quote["low"],
        quote["close"],
        quote["volume"],
    ):
        if close is not None:
            rows.append((ts, open_, high, low, close, volume))
    if len(rows) < 2:
        raise RuntimeError(f"{ticker}: insufficient Yahoo chart rows")
    ts, open_, high, low, close, volume = rows[-1]
    prev_close = rows[-2][4]
    change = close - prev_close
    change_percent = change / prev_close * 100 if prev_close else 0.0
    trade_date = datetime.fromtimestamp(ts, timezone.utc).astimezone(ZoneInfo("America/New_York")).date()
    return {
        "ticker": ticker,
        "source": "Yahoo Chart",
        "price": round(close, 4),
        "previous_close": round(prev_close, 4),
        "change": round(change, 4),
        "change_percent": round(change_percent, 4),
        "latest_trade_time": f"{trade_date.isoformat()} 16:00:00 America/New_York",
        "open": round(open_, 4) if open_ is not None else None,
        "high": round(high, 4) if high is not None else None,
        "low": round(low, 4) if low is not None else None,
        "volume": volume,
    }


def fetch_stooq(ticker: str) -> dict:
    symbol = stooq_symbol(ticker)
    url = f"https://stooq.com/q/l/?s={urllib.parse.quote(symbol)}&f=sd2t2ohlcv&h&e=csv"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=15) as response:
        text = response.read().decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(text)))
    if not rows or rows[0].get("Close") in {"", "N/D", None}:
        raise RuntimeError(f"{ticker}: no Stooq quote")
    row = rows[0]
    return {
        "ticker": ticker,
        "source": "Stooq",
        "price": float(row["Close"]),
        "latest_trade_time": f"{row.get('Date', '')}T{row.get('Time', '')}",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--watchlist-file", default=str(WATCHLIST_PATH))
    parser.add_argument("--tickers", help="Comma separated override. If omitted, reads watchlist file.")
    parser.add_argument("--out", help="Optional path to write primary snapshot JSON.")
    parser.add_argument("--no-secondary", action="store_true", help="Skip Stooq drift check.")
    parser.add_argument("--max-drift-pct", type=float, default=1.0)
    args = parser.parse_args()

    tickers = (
        [part.strip().upper() for part in args.tickers.split(",") if part.strip()]
        if args.tickers
        else read_watchlist(Path(args.watchlist_file))
    )

    primary_items = []
    secondary_items = []
    errors = []
    for ticker in tickers:
        try:
            primary_items.append(fetch_yahoo(ticker))
        except Exception as exc:
            errors.append(f"{ticker}: Yahoo Chart failed: {type(exc).__name__}: {exc}")
        if not args.no_secondary:
            try:
                secondary_items.append(fetch_stooq(ticker))
            except Exception as exc:
                errors.append(f"{ticker}: Stooq drift check failed: {type(exc).__name__}: {exc}")

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "watchlist_file": str(Path(args.watchlist_file).resolve()),
        "tickers": tickers,
        "primary_source": "Yahoo Chart",
        "secondary_source": None if args.no_secondary else "Stooq",
        "items": primary_items,
        "errors": errors,
    }

    out_path = Path(args.out) if args.out else None
    if out_path:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    validation_payload = None
    if len(primary_items) == len(tickers):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            primary_path = Path(tmp) / "primary.json"
            secondary_path = Path(tmp) / "secondary.json"
            primary_path.write_text(json.dumps({"items": primary_items}), encoding="utf-8")
            secondary_path.write_text(json.dumps({"items": secondary_items}), encoding="utf-8")
            cmd = [
                sys.executable,
                str(VALIDATOR),
                "--snapshot-json",
                str(primary_path),
                "--expected-tickers",
                ",".join(tickers),
                "--max-drift-pct",
                str(args.max_drift_pct),
            ]
            if secondary_items and not args.no_secondary:
                cmd.extend(["--secondary-json", str(secondary_path)])
            proc = subprocess.run(cmd, text=True, capture_output=True)
            try:
                validation_payload = json.loads(proc.stdout)
            except Exception:
                validation_payload = {"ok": False, "errors": [proc.stderr or proc.stdout]}
    else:
        validation_payload = {
            "ok": False,
            "errors": ["primary snapshot did not return every watchlist ticker"],
        }

    payload["validation"] = validation_payload
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if validation_payload and validation_payload.get("ok") and not errors else 1


if __name__ == "__main__":
    sys.exit(main())

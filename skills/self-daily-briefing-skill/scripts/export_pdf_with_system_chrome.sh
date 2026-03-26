#!/usr/bin/env bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 <input_html> <output_pdf>" >&2
  exit 2
fi

CHROME_BIN="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
INPUT_HTML="$1"
OUTPUT_PDF="$2"

if [ ! -x "$CHROME_BIN" ]; then
  echo "Chrome not found at: $CHROME_BIN" >&2
  exit 1
fi

if [ ! -f "$INPUT_HTML" ]; then
  echo "Input HTML not found: $INPUT_HTML" >&2
  exit 1
fi

pick_port() {
  python3 - <<'PY'
import socket
s = socket.socket()
s.bind(("127.0.0.1", 0))
print(s.getsockname()[1])
s.close()
PY
}

PORT="$(pick_port)"
ROOT_DIR="$(dirname "$INPUT_HTML")"
INPUT_BASENAME="$(basename "$INPUT_HTML")"
OUTPUT_DIR="$(dirname "$OUTPUT_PDF")"
LOG_FILE="$(mktemp -t morning-brief-http.XXXXXX.log)"
TMP_PROFILE="$(mktemp -d -t morning-brief-chrome.XXXXXX)"
mkdir -p "$OUTPUT_DIR"
rm -f "$OUTPUT_PDF"

cleanup() {
  if [ -n "${CHROME_PID:-}" ]; then
    kill "$CHROME_PID" >/dev/null 2>&1 || true
    pkill -P "$CHROME_PID" >/dev/null 2>&1 || true
    wait "$CHROME_PID" 2>/dev/null || true
  fi
  if [ -n "${TMP_PROFILE:-}" ]; then
    pkill -f "$TMP_PROFILE" >/dev/null 2>&1 || true
  fi
  if [ -n "${SERVER_PID:-}" ]; then
    kill "$SERVER_PID" >/dev/null 2>&1 || true
    wait "$SERVER_PID" 2>/dev/null || true
  fi
  rm -rf "$TMP_PROFILE"
  rm -f "$LOG_FILE"
}
trap cleanup EXIT INT TERM HUP

(
  cd "$ROOT_DIR"
  python3 -m http.server "$PORT" --bind 127.0.0.1 >"$LOG_FILE" 2>&1
) &
SERVER_PID="$!"
sleep 1

PAGE_URL="http://127.0.0.1:${PORT}/${INPUT_BASENAME}"

python3 - "$PAGE_URL" <<'PY'
import sys
import time
import urllib.request

url = sys.argv[1]
last_error = None
for _ in range(30):
    try:
        with urllib.request.urlopen(url, timeout=2) as resp:
            body = resp.read(1024).decode("utf-8", "ignore")
            if resp.status == 200 and "<html" in body.lower():
                raise SystemExit(0)
    except Exception as exc:  # pragma: no cover - shell-side retry loop
        last_error = exc
    time.sleep(0.2)
raise SystemExit(f"HTTP server never became ready for {url}: {last_error}")
PY

"$CHROME_BIN" \
  --headless=new \
  --disable-gpu \
  --no-sandbox \
  --no-pdf-header-footer \
  --disable-dev-shm-usage \
  --user-data-dir="$TMP_PROFILE" \
  --print-to-pdf="$OUTPUT_PDF" \
  "$PAGE_URL" &
CHROME_PID="$!"
wait "$CHROME_PID"
CHROME_PID=""

if [ ! -f "$OUTPUT_PDF" ]; then
  echo "Chrome exited without creating PDF: $OUTPUT_PDF" >&2
  exit 1
fi

if command -v pdftotext >/dev/null 2>&1; then
  PDF_TEXT="$(pdftotext "$OUTPUT_PDF" - 2>/dev/null || true)"
  if printf '%s' "$PDF_TEXT" | rg -q "ERR_CONNECTION_REFUSED|无法访问此网站|404 File not found"; then
    echo "Printed PDF contains a browser error page instead of the HTML content." >&2
    exit 1
  fi
  if [ "$(printf '%s' "$PDF_TEXT" | wc -m | tr -d ' ')" -lt 300 ]; then
    echo "Printed PDF text is unexpectedly short; likely failed to render the HTML content." >&2
    exit 1
  fi
fi

echo "$OUTPUT_PDF"

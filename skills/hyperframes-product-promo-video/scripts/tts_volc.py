#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
import uuid
import urllib.error
import urllib.request
from pathlib import Path


ENDPOINT = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
DEFAULT_SPEAKER = "zh_female_vv_uranus_bigtts"
DEFAULT_RESOURCE_ID = "seed-tts-2.0"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate Mandarin narration with Volcengine Seed-TTS 2.0."
    )
    parser.add_argument("input", help="UTF-8 text file, or literal text with --literal")
    parser.add_argument("output", help="Output MP3 path")
    parser.add_argument("--literal", action="store_true", help="Treat input as literal text")
    parser.add_argument("--speech-rate", type=int, default=12)
    parser.add_argument("--speaker", default=DEFAULT_SPEAKER)
    parser.add_argument("--uid", default="hyperframes-product-promo-video")
    return parser.parse_args()


def load_text(value, literal):
    if literal:
        text = value
    else:
        text = Path(value).read_text(encoding="utf-8")
    text = text.strip()
    if not text:
        raise SystemExit("Input text is empty")
    return text


def synthesize(text, api_key, speaker, speech_rate, uid):
    payload = {
        "user": {"uid": uid},
        "req_params": {
            "text": text,
            "speaker": speaker,
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000,
                "speech_rate": speech_rate,
                "loudness_rate": 0,
            },
        },
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "X-Api-Key": api_key,
            "X-Api-Resource-Id": DEFAULT_RESOURCE_ID,
            "X-Api-Request-Id": str(uuid.uuid4()),
        },
        method="POST",
    )

    audio = bytearray()
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            for raw_line in response:
                line = raw_line.decode("utf-8").strip()
                if not line:
                    continue
                item = json.loads(line)
                code = item.get("code")
                if code == 0 and item.get("data"):
                    audio.extend(base64.b64decode(item["data"]))
                elif code == 20000000:
                    break
                elif code not in (0, 20000000):
                    message = item.get("message") or item.get("msg") or "unknown error"
                    raise RuntimeError(f"TTS failed with code {code}: {message}")
    except urllib.error.HTTPError as exc:
        raise SystemExit(f"TTS HTTP error: {exc.code} {exc.reason}") from None
    except urllib.error.URLError as exc:
        raise SystemExit(f"TTS network error: {exc.reason}") from None

    if not audio:
        raise SystemExit("TTS returned no audio")
    return audio


def main():
    args = parse_args()
    if not -50 <= args.speech_rate <= 100:
        raise SystemExit("--speech-rate must be between -50 and 100")

    api_key = os.environ.get("VOLC_API_KEY")
    if not api_key:
        raise SystemExit(
            "VOLC_API_KEY is required. Create a Volcengine API Key and set it in the environment."
        )

    text = load_text(args.input, args.literal)
    audio = synthesize(text, api_key, args.speaker, args.speech_rate, args.uid)
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(audio)
    print(f"Wrote {len(audio)} bytes to {output}")


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)

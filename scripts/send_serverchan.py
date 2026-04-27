#!/usr/bin/env python3
"""Send a WeChat push notification through ServerChan Turbo."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


API_TEMPLATE = "https://sctapi.ftqq.com/{sendkey}.send"
SECRET_FILE = Path.home() / ".codex" / "secrets" / "serverchan_sendkey.txt"


def load_sendkey() -> str:
    if os.environ.get("SCT_SENDKEY"):
        return os.environ["SCT_SENDKEY"]
    if SECRET_FILE.exists():
        return SECRET_FILE.read_text(encoding="utf-8").strip()
    return ""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--title", required=True, help="Notification title.")
    parser.add_argument("--message", "--desp", dest="message", default="", help="Notification body. Markdown is supported.")
    parser.add_argument("--short", default="", help="Optional card summary.")
    parser.add_argument("--sendkey", default=load_sendkey())
    parser.add_argument("--channel", default="", help="Optional ServerChan channel override, for example 66 or 9|66.")
    parser.add_argument("--openid", default="", help="Optional recipient override for supported channels.")
    parser.add_argument("--noip", action="store_true", help="Hide caller IP when ServerChan supports it.")
    parser.add_argument("--timeout", type=int, default=10)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def build_payload(args: argparse.Namespace) -> dict[str, str]:
    payload = {
        "title": args.title,
        "desp": args.message,
    }
    if args.short:
        payload["short"] = args.short
    if args.channel:
        payload["channel"] = args.channel
    if args.openid:
        payload["openid"] = args.openid
    if args.noip:
        payload["noip"] = "1"
    return payload


def send(sendkey: str, payload: dict[str, str], timeout: int) -> dict:
    data = urllib.parse.urlencode(payload).encode("utf-8")
    request = urllib.request.Request(
        API_TEMPLATE.format(sendkey=sendkey),
        data=data,
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        body = response.read().decode("utf-8", errors="replace")
    try:
        return json.loads(body)
    except json.JSONDecodeError:
        return {"code": -1, "message": "Non-JSON response", "raw": body}


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    payload = build_payload(args)

    if not args.sendkey:
        print(
            json.dumps(
                {
                    "code": -1,
                    "message": "Missing SendKey. Set SCT_SENDKEY, pass --sendkey, or create ~/.codex/secrets/serverchan_sendkey.txt.",
                },
                ensure_ascii=False,
            ),
            file=sys.stderr,
        )
        return 2

    if args.dry_run:
        print(json.dumps({"dry_run": True, "payload": payload}, ensure_ascii=False, indent=2))
        return 0

    try:
        result = send(args.sendkey, payload, args.timeout)
    except urllib.error.URLError as exc:
        print(json.dumps({"code": -1, "message": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False))
    return 0 if result.get("code") == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

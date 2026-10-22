#!/usr/bin/env python3
import argparse
import json
import os
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"


def run_score(payload):
    account = str(payload.get("account", "Unnamed account")).strip() or "Unnamed account"
    values = [payload.get(key) for key in ("fit", "intent", "timing", "confidence")]
    if any(isinstance(value, bool) or not isinstance(value, (int, float)) for value in values):
        raise ValueError("fit, intent, timing, and confidence must be numbers")
    result = subprocess.run(
        [str(BUILD / "signal_relay"), *[str(value) for value in values]],
        check=True, capture_output=True, text=True,
    )
    body = json.loads(result.stdout)
    body.update({"account": account, "mode": "simulated", "destination": "HubSpot note + Apollo review queue"})
    return body


def run_analysis(payload):
    deal = str(payload.get("deal", "Unnamed deal")).strip() or "Unnamed deal"
    transcript = str(payload.get("transcript", "")).strip()
    if not transcript:
        raise ValueError("transcript is required")
    path = None
    try:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
            handle.write(transcript)
            path = handle.name
        result = subprocess.run(
            [str(BUILD / "deal_ledger"), path], check=True, capture_output=True, text=True,
        )
    finally:
        if path:
            os.unlink(path)
    body = json.loads(result.stdout)
    body.update({"deal": deal, "mode": "simulated", "destination": "HubSpot approval queue"})
    return body


def parser():
    root = argparse.ArgumentParser(description="Headless GTM evidence engines")
    commands = root.add_subparsers(dest="command", required=True)
    score = commands.add_parser("score", help="score an account")
    score.add_argument("--account", required=True)
    for name in ("fit", "intent", "timing", "confidence"):
        score.add_argument("--" + name, type=float, required=True)
    analyze = commands.add_parser("analyze", help="analyze a discovery transcript")
    analyze.add_argument("--deal", required=True)
    analyze.add_argument("--transcript-file", type=Path, required=True)
    return root


if __name__ == "__main__":
    if not (BUILD / "signal_relay").exists() or not (BUILD / "deal_ledger").exists():
        raise SystemExit("Build the C++ engines first with: make")
    args = parser().parse_args()
    if args.command == "score":
        result = run_score(vars(args))
    else:
        result = run_analysis({"deal": args.deal, "transcript": args.transcript_file.read_text(encoding="utf-8")})
    print(json.dumps(result, indent=2))

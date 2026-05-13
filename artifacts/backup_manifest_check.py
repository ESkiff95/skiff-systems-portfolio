#!/usr/bin/env python3
"""Validate backup artifacts from a small JSON manifest.

The tool is intentionally generic and public-safe. It does not know about any
private hosts, credentials, or backup paths. Operators provide a manifest that
describes which files should exist and how fresh they should be.
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class CheckResult:
    name: str
    path: str
    ok: bool
    details: list[str]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def check_gzip(path: Path) -> None:
    with gzip.open(path, "rb") as handle:
        while handle.read(1024 * 1024):
            pass


def validate_entry(entry: dict[str, Any], now: float) -> CheckResult:
    name = str(entry.get("name") or entry.get("path") or "unnamed")
    path = Path(str(entry.get("path", ""))).expanduser()
    details: list[str] = []
    ok = True

    if not path.exists():
        return CheckResult(name=name, path=str(path), ok=False, details=["missing"])

    if not path.is_file():
        return CheckResult(name=name, path=str(path), ok=False, details=["not_a_file"])

    max_age_hours = entry.get("max_age_hours")
    if max_age_hours is not None:
        age_hours = (now - path.stat().st_mtime) / 3600
        if age_hours > float(max_age_hours):
            ok = False
            details.append(f"stale age_hours={age_hours:.2f}")
        else:
            details.append(f"fresh age_hours={age_hours:.2f}")

    expected_sha256 = entry.get("sha256")
    if expected_sha256:
        actual_sha256 = sha256_file(path)
        if actual_sha256 != expected_sha256:
            ok = False
            details.append("sha256_mismatch")
        else:
            details.append("sha256_ok")

    if entry.get("gzip"):
        try:
            check_gzip(path)
            details.append("gzip_ok")
        except OSError as exc:
            ok = False
            details.append(f"gzip_error={exc.__class__.__name__}")

    if not details:
        details.append("exists")

    return CheckResult(name=name, path=str(path), ok=ok, details=details)


def load_manifest(path: Path) -> list[dict[str, Any]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    backups = data.get("backups")
    if not isinstance(backups, list):
        raise ValueError("manifest must contain a 'backups' list")
    return backups


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate backup manifest files")
    parser.add_argument("manifest", type=Path, help="JSON manifest path")
    parser.add_argument("--pretty", action="store_true", help="pretty-print JSON output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        entries = load_manifest(args.manifest)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "error": str(exc)}), file=sys.stderr)
        return 2

    now = time.time()
    results = [validate_entry(entry, now) for entry in entries]
    payload = {
        "ok": all(result.ok for result in results),
        "checked": len(results),
        "results": [
            {
                "name": result.name,
                "path": result.path,
                "ok": result.ok,
                "details": result.details,
            }
            for result in results
        ],
    }

    print(json.dumps(payload, indent=2 if args.pretty else None, sort_keys=True))
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the kpatch rewrite benchmark layout and JSON metadata."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED_CASE_FILES = {"metadata.json", "original.patch", "rewritten.patch"}


def load_json(path: Path) -> dict:
    with path.open() as f:
        return json.load(f)


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    dataset_path = ROOT / "dataset.json"
    if not dataset_path.exists():
        fail("missing dataset.json")

    dataset = load_json(dataset_path)

    cases = dataset.get("cases")
    if not isinstance(cases, list):
        fail("dataset.json cases must be a list")
    if dataset.get("case_count") != len(cases):
        fail("dataset.json case_count does not match cases length")

    seen = set()
    for item in cases:
        cve = item.get("cve_id")
        rel = item.get("path")
        if not cve or not rel:
            fail("case entry missing cve_id or path")
        if cve in seen:
            fail(f"duplicate case {cve}")
        seen.add(cve)

        case_dir = ROOT / rel
        if not case_dir.is_dir():
            fail(f"{cve}: missing case directory {rel}")
        present = {p.name for p in case_dir.iterdir() if p.is_file()}
        missing = REQUIRED_CASE_FILES - present
        if missing:
            fail(f"{cve}: missing files {sorted(missing)}")

        metadata = load_json(case_dir / "metadata.json")
        if metadata.get("cve_id") != cve:
            fail(f"{cve}: metadata cve_id mismatch")
        files = metadata.get("files") or {}
        for key in ("original_patch", "rewritten_patch"):
            filename = files.get(key)
            if not filename or not (case_dir / filename).is_file():
                fail(f"{cve}: files.{key} does not point to an existing file")
        original_dir = files.get("original_patches_dir")
        if original_dir is not None and not (case_dir / original_dir).is_dir():
            fail(f"{cve}: files.original_patches_dir does not exist")
        kpatch = metadata.get("kpatch") or {}
        if not kpatch.get("triggers_limit"):
            fail(f"{cve}: kpatch.triggers_limit must be true")
        if not kpatch.get("bypassable_by_rewrite"):
            fail(f"{cve}: kpatch.bypassable_by_rewrite must be true")
        if not kpatch.get("limitations"):
            fail(f"{cve}: kpatch.limitations must not be empty")

    actual_dirs = {p.name for p in (ROOT / "cases").iterdir() if p.is_dir()}
    if actual_dirs != seen:
        fail(f"case directories differ from dataset index: {sorted(actual_dirs ^ seen)}")

    print(f"OK: {len(cases)} cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

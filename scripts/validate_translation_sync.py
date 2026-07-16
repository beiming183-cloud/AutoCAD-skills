#!/usr/bin/env python3
"""Fail when the English baseline changes without its Chinese mirror."""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MIRRORS = {
    "SKILL.md": (
        "SKILL.zh-CN.md",
        "7c474f56b6cf00265dacd922882cb1da1e9278daa8633b62f56717feaf648728",
    ),
    "references/gbt-drafting.md": (
        "references/zh-CN/gbt-drafting.md",
        "112760800c7f331ccb0e2e80d47145f1406bfe94ff4475203f4777cdec967b54",
    ),
    "references/autocad-mcp-workflow.md": (
        "references/zh-CN/autocad-mcp-workflow.md",
        "be3b3783cad0377c3ff7bc45f09700109de1ccacc2740489156d1fa2d75cb8e9",
    ),
    "references/complex-assembly-drafting.md": (
        "references/zh-CN/complex-assembly-drafting.md",
        "a58047d8c737564582314a5b0e21364ad847f1c1ca116aa5c3adbaba43a03e19",
    ),
    "references/drc-review.md": (
        "references/zh-CN/drc-review.md",
        "7394c706ca4f2d5b0bef24a20aa7a9779e553a96c0eed5f16a5db200d76ac6aa",
    ),
}

SEMANTIC_IDS = {
    "DANGLING_ENDPOINT",
    "NEAR_MISS_CONNECTION",
    "INTERIOR_CROSSING",
    "UNOWNED_LINE",
    "UNCLOSED_MATERIAL_BOUNDARY",
    "PROTRUDING_OR_OCCLUDED_GEOMETRY",
    "VIEW_SOURCE_CONSISTENCY",
    "VIEW_SEMANTICS_CONSISTENCY",
    "DELIVERABLE_SCOPE_IDENTITY",
    "PLOT_SCALE_CONSISTENCY",
    "FINAL_VISUAL_INTEGRITY",
}
STABLE_ID_RE = re.compile(r"\b(?:E|GBT)_[A-Z0-9_]+\b")
HEADING_RE = re.compile(r"^(#{1,6})\s+", re.MULTILINE)


def read_text(relative_path: str) -> str:
    return (ROOT / relative_path).read_text(encoding="utf-8")


def digest(relative_path: str) -> str:
    return hashlib.sha256((ROOT / relative_path).read_bytes()).hexdigest()


def stable_ids(text: str) -> set[str]:
    return set(STABLE_ID_RE.findall(text)) | {rule for rule in SEMANTIC_IDS if rule in text}


def heading_profile(text: str) -> list[int]:
    return [len(match.group(1)) for match in HEADING_RE.finditer(text)]


def main() -> int:
    errors: list[str] = []

    for source, (mirror, expected_hash) in MIRRORS.items():
        source_path = ROOT / source
        mirror_path = ROOT / mirror
        if not source_path.is_file() or not mirror_path.is_file():
            errors.append(f"missing mirror pair: {source} -> {mirror}")
            continue

        actual_hash = digest(source)
        if actual_hash != expected_hash:
            errors.append(
                f"English source changed: {source}\n"
                f"  expected sha256: {expected_hash}\n"
                f"  actual sha256:   {actual_hash}\n"
                "  synchronize the Chinese mirror, then update MIRRORS"
            )

        source_text = read_text(source)
        mirror_text = read_text(mirror)
        source_ids = stable_ids(source_text)
        mirror_ids = stable_ids(mirror_text)
        if source_ids != mirror_ids:
            errors.append(
                f"stable IDs differ: {source} -> {mirror}\n"
                f"  missing in Chinese: {sorted(source_ids - mirror_ids)}\n"
                f"  extra in Chinese:   {sorted(mirror_ids - source_ids)}"
            )

        source_headings = heading_profile(source_text)
        mirror_headings = heading_profile(mirror_text)
        if source_headings != mirror_headings:
            errors.append(
                f"heading levels differ: {source} -> {mirror}\n"
                f"  English: {source_headings}\n"
                f"  Chinese: {mirror_headings}"
            )

        if source_text.count("```") != mirror_text.count("```"):
            errors.append(
                f"fenced code-block marker count differs: {source} -> {mirror}"
            )

    if errors:
        print("Translation sync validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1

    print(f"Translation sync validation passed for {len(MIRRORS)} mirror pairs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

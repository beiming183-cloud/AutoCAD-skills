#!/usr/bin/env python3
"""Validate repository presentation, the bundled skill, and installation round trip."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "mechanical-drafting-gbt"
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
PRIVATE_RE = re.compile(
    r"(?:[A-Za-z]:\\Us" + r"ers\\[^\\\s]+|/Us" + r"ers/[^/\s]+|/ho" + r"me/[^/\s]+|"
    r"gh" + r"p_[A-Za-z0-9]+|github_" + r"pat_[A-Za-z0-9_]+|BEGIN (?:RSA|OPENSSH|EC) PRIVATE KEY)"
)
PLACEHOLDER_RE = re.compile(r"\b(?:TO" + "DO|FIX" + "ME)\b")


def normalized_sha256(path: Path) -> str:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def check_frontmatter(errors: list[str]) -> None:
    skill_file = SKILL / "SKILL.md"
    if not skill_file.is_file():
        errors.append("missing skills/mechanical-drafting-gbt/SKILL.md")
        return
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n") and not text.startswith("---\r\n"):
        errors.append("SKILL.md does not start with YAML frontmatter")
    header = text.replace("\r\n", "\n").split("---", 2)[1]
    if "name: mechanical-drafting-gbt" not in header:
        errors.append("SKILL.md frontmatter has the wrong name")
    description = next(
        (line.split(":", 1)[1].strip() for line in header.splitlines() if line.startswith("description:")),
        "",
    )
    if len(description) < 80:
        errors.append("SKILL.md description is missing or too weak for discovery")


def check_markdown_links(errors: list[str]) -> None:
    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text(encoding="utf-8")
        for raw_target in LINK_RE.findall(text):
            target = raw_target.strip().strip("<>").split("#", 1)[0]
            if not target or re.match(r"^(?:https?://|mailto:)", target):
                continue
            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                errors.append(f"broken Markdown link: {path.relative_to(ROOT)} -> {target}")


def check_text_safety(errors: list[str]) -> None:
    suffixes = {".md", ".py", ".yml", ".yaml", ".json", ".txt", ".svg", ".cff"}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts or path.suffix.lower() not in suffixes:
            continue
        text = path.read_text(encoding="utf-8")
        if PRIVATE_RE.search(text):
            errors.append(f"private path or credential-like content: {path.relative_to(ROOT)}")
        if PLACEHOLDER_RE.search(text):
            errors.append(f"placeholder token: {path.relative_to(ROOT)}")


def run(command: list[str], errors: list[str], label: str) -> None:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode:
        detail = (result.stdout + result.stderr).strip()
        errors.append(f"{label} failed: {detail}")


def check_examples_and_assets(errors: list[str]) -> None:
    try:
        with (ROOT / "examples" / "drc-report.sample.json").open(encoding="utf-8") as stream:
            report = json.load(stream)
        if report.get("verdict") != "BLOCKED":
            errors.append("sample DRC report must demonstrate a blocking finding")
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid sample DRC report: {exc}")
    for asset in ("hero.svg", "release-gates-en.svg", "release-gates-zh.svg"):
        try:
            ET.parse(ROOT / "assets" / asset)
        except (OSError, ET.ParseError) as exc:
            errors.append(f"invalid SVG {asset}: {exc}")
    for required in (
        "README.md",
        "README.zh-CN.md",
        "LICENSE",
        "CONTRIBUTING.md",
        ".github/workflows/validate.yml",
    ):
        if not (ROOT / required).is_file():
            errors.append(f"missing repository file: {required}")


def check_install_round_trip(errors: list[str]) -> None:
    with tempfile.TemporaryDirectory(prefix="autocad-skills-") as temporary:
        target = Path(temporary) / "mechanical-drafting-gbt"
        run(
            [sys.executable, "scripts/install_skill.py", "--dest", str(target)],
            errors,
            "temporary installation",
        )
        if not (target / "SKILL.md").is_file():
            errors.append("temporary installation did not create SKILL.md")
            return
        source_files = sorted(path.relative_to(SKILL) for path in SKILL.rglob("*") if path.is_file())
        target_files = sorted(path.relative_to(target) for path in target.rglob("*") if path.is_file())
        if source_files != target_files:
            errors.append("temporary installation file inventory differs from source")
            return
        for relative in source_files:
            if normalized_sha256(SKILL / relative) != normalized_sha256(target / relative):
                errors.append(f"temporary installation content differs: {relative}")


def main() -> int:
    errors: list[str] = []
    check_frontmatter(errors)
    check_markdown_links(errors)
    check_text_safety(errors)
    check_examples_and_assets(errors)
    run(
        [sys.executable, str(SKILL / "scripts" / "validate_translation_sync.py")],
        errors,
        "translation sync",
    )
    check_install_round_trip(errors)
    if errors:
        print("Repository validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Repository validation passed.")
    print("- Skill frontmatter and bilingual mirrors")
    print("- Markdown links, examples, assets, and text safety")
    print("- Installation inventory and content round trip")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

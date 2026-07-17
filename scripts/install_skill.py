#!/usr/bin/env python3
"""Install the bundled mechanical-drafting-gbt skill without overwriting files."""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "mechanical-drafting-gbt"
SOURCE = ROOT / "skills" / SKILL_NAME


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--target",
        choices=("codex", "claude-user", "claude-project"),
        help="Known installation target; omit only when --dest is provided",
    )
    parser.add_argument(
        "--project",
        type=Path,
        help="Project root required by --target claude-project",
    )
    parser.add_argument(
        "--dest",
        type=Path,
        help="Exact destination skill directory; overrides the target-derived path",
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if args.dest is None and args.target is None:
        parser.error("provide --target or --dest")
    if args.target == "claude-project" and args.project is None and args.dest is None:
        parser.error("--target claude-project requires --project")
    return args


def destination(args: argparse.Namespace) -> Path:
    if args.dest is not None:
        return args.dest.expanduser().resolve()
    if args.target == "codex":
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        return (codex_home / "skills" / SKILL_NAME).expanduser().resolve()
    if args.target == "claude-user":
        return (Path.home() / ".claude" / "skills" / SKILL_NAME).resolve()
    assert args.project is not None
    return (args.project.expanduser().resolve() / ".claude" / "skills" / SKILL_NAME)


def source_files() -> list[Path]:
    return sorted(
        path
        for path in SOURCE.rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )


def main() -> int:
    args = parse_args()
    target = destination(args)
    if not (SOURCE / "SKILL.md").is_file():
        raise SystemExit(f"bundled skill is incomplete: {SOURCE}")
    files = source_files()

    print(f"source:      {SOURCE}")
    print(f"destination: {target}")
    print(f"files:       {len(files)}")
    if target.exists():
        raise SystemExit(
            "destination already exists; preserve or move the existing skill before installing"
        )
    if args.dry_run:
        print("dry run: no files written")
        return 0

    target.parent.mkdir(parents=True, exist_ok=True)
    staging_root = Path(tempfile.mkdtemp(prefix=f".{SKILL_NAME}-", dir=target.parent))
    staged_skill = staging_root / SKILL_NAME
    try:
        shutil.copytree(SOURCE, staged_skill, copy_function=shutil.copy2)
        staged_skill.rename(target)
    finally:
        shutil.rmtree(staging_root)

    if not (target / "SKILL.md").is_file():
        raise SystemExit("installation postcondition failed: SKILL.md missing")
    print("installed successfully; start a new agent turn/session if it is not detected live")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print("installation cancelled", file=sys.stderr)
        raise SystemExit(130)

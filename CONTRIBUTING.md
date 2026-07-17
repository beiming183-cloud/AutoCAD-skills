# Contributing

Thank you for helping make AI-assisted mechanical CAD more trustworthy.

## Good contributions

- A real drawing or automation failure reduced to a nonconfidential fixture.
- A deterministic DRC rule with units, applicability, thresholds, evidence, and known limits.
- A correction to a named GB/T rule with the exact standard edition and authoritative source.
- A safer AutoCAD/MCP postcondition, rollback, or capability-discovery contract.
- A clearer consumer-product, 2D/3D, assembly, GPS, inspection, DFM, or release workflow.
- A portability improvement for Codex, Claude Code, or another Agent Skills runner.

Do not submit invented fits, tolerances, materials, safety values, or remembered standards without traceable applicability. Missing evidence must remain `TBD` or `NOT_EVALUATED`, never a pass.

## Development setup

The repository uses Python standard-library checks only.

```bash
git clone https://github.com/beiming183-cloud/AutoCAD-skills.git
cd AutoCAD-skills
python scripts/validate_repo.py
```

## Editing the Skill

The runtime package lives in `skills/mechanical-drafting-gbt/`.

1. Keep `SKILL.md` concise and put detailed rules in directly linked `references/` files.
2. Preserve stable rule IDs and machine-readable error codes.
3. Update the Chinese maintenance mirror whenever mirrored core behavior changes.
4. Run `skills/mechanical-drafting-gbt/scripts/validate_translation_sync.py`.
5. Update the pinned normalized source hash in that script only after reviewing the corresponding Chinese mirror.
6. Run `python scripts/validate_repo.py` before opening a pull request.

The runtime Skill directory intentionally contains no repository README, contribution guide, license, or marketing asset. Those belong at the repository level.

## Pull requests

Keep each pull request focused. Include:

- The problem and a minimal reproducible example.
- Why the existing workflow or rule misses it.
- The proposed behavior and evidence boundary.
- Tests or fixtures proving both pass and fail behavior where applicable.
- Any compatibility, standard-edition, runtime, or migration impact.

For a standards change, link to an authoritative public source when possible and avoid long copyrighted quotations.

## Reporting unsafe behavior

Do not post credentials, proprietary drawings, personal data, export-controlled data, or a weaponizable automation payload in a public issue. Follow [SECURITY.md](SECURITY.md) for security-sensitive reports.

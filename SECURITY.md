# Security Policy

## Scope

Security issues may include:

- Installer or validation behavior that writes outside the selected destination.
- Prompt or workflow instructions that can cause unintended destructive CAD/file operations.
- Credential exposure in examples, logs, manifests, or automation payloads.
- CI or dependency behavior that permits untrusted code execution.
- A safety-critical rule that incorrectly converts missing evidence or failed validation into a favorable release verdict.

## Reporting

Use GitHub's private vulnerability reporting for this repository when it is available:

https://github.com/beiming183-cloud/AutoCAD-skills/security/advisories/new

If private reporting is unavailable, open a minimal public issue stating that you have a security report, without including secrets, private drawings, exploit details, or sensitive logs. The maintainer can then establish an appropriate private channel.

Include the affected version, runner/OS, reproduction conditions, impact, and the smallest nonconfidential evidence needed to understand the problem.

## Safety boundary

This project provides agent instructions and validation helpers, not certification. Do not use a security report, issue closure, DRC result, or repository release as evidence that a mechanical or electrical product is safe, compliant, or approved for manufacturing.

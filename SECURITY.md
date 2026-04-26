# Security Policy

## Reporting a vulnerability

Please report security vulnerabilities through GitHub's [Private Vulnerability Reporting](https://github.com/chrisdpurcell/star-trek-retro-remake/security/advisories/new). This is the preferred channel because it gives you a private space to share details and reproduction steps without exposing them publicly.

## Scope

This is a single-user desktop game. The attack surface is intentionally tiny.

**In scope:**

- Save-file deserialization vulnerabilities (the project explicitly rejects `pickle` and `dill` for this reason — see `DESIGN.md` §9.5).
- Configuration-file parsing (TOML loaded via `tomllib`, validated through pydantic).
- AppImage build and distribution integrity.
- Dependency vulnerabilities in `pyproject.toml` runtime dependencies.

**Out of scope:**

- Telemetry, analytics, or data exfiltration vectors — none exist. The game does not collect, transmit, or store personal data, and makes no network calls beyond user-initiated actions (which are none in v1.0). All save data lives on the user's local machine.
- Self-DoS via malformed save files or absurd resource values is not treated as a vulnerability — single-user desktop game; the attacker would be the player.

## What to include in a report

- Affected version (commit SHA or release tag)
- Steps to reproduce
- Expected vs. actual behavior
- Whether you've already disclosed elsewhere (please don't until coordinated)

## Response expectations

The project is a solo personal effort. Acknowledgment within seven days; mitigation timeline depends on severity. Public credit (if you want it) appears in the relevant `CHANGELOG.md` entry.

## Privacy and data

Per `DESIGN.md` §12.2: this is a single-user desktop application. It does not collect, transmit, or store personal data. No telemetry, no analytics, no network calls. All save data is local.

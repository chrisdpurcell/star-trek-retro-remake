# ADR-0002 — Linux-only, no Windows or macOS support

**Status:** Accepted
**Date:** 2026-04-26

## Context

This is a solo project with finite developer time. Cross-platform support inflates testing surface, packaging work, and bug-triage cost roughly linearly per platform. The author develops, plays, and tests on Linux exclusively.

## Decision

Linux is the only supported platform. Code uses Linux paths (`~/.config/`, `~/.local/share/`) and Linux conventions. The AppImage release format is Linux-only by design. Windows and macOS support is not on the roadmap and is out of scope for issues and PRs.

## Consequences

- POSIX paths, case-sensitive filesystems, and Linux-style config dirs can be assumed everywhere — no platform abstraction layer in `persistence/` or `config/`.
- The CI matrix is `ubuntu-latest` only; no Windows or macOS runner cost.
- Distribution is via AppImage (single-file Linux binary) at v1.0, plus dev-mode `uv run python -m stmrr` from a clone. No app stores, no installers, no platform-store compliance.
- Rejected alternative: best-effort cross-platform via Qt's natural portability. Rejected because "best-effort" still requires a CI matrix, per-platform bug triage, and packaging work that displaces gameplay implementation.

See `docs/design/DESIGN.md` §1.3, §9.3.

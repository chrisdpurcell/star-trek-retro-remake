# Handoff

**Last updated:** 2026-04-26

## State at a glance

- Pre-scaffold. `DESIGN.md` (canonical, 105 KB) + `tech-stack-pyside6.md` committed.
- Handoff system landed 2026-04-26 per `/mnt/share/claude-handoff-system.md` §2.1. Decision 3 = PER-REPO; Decision 1 implicitly YES; Decision 2 deferred until `src/` exists.
- Public-facing repo prep landed 2026-04-26: `README.md` (expanded), `CONTRIBUTING.md`, `SECURITY.md`, `NOTICE.md`, `CHANGELOG.md`, `.github/ISSUE_TEMPLATE/{bug,feature,design-discussion,config}.yml`, `.github/PULL_REQUEST_TEMPLATE.md`. LICENSE normalized to "Chris Purcell". GitHub repo configured (description, 7 topics, wiki/projects off). Branch protection deferred until CI lands.
- Next milestone: scaffold step 1 of `tech-stack-pyside6.md` §11 — `pyproject.toml`, `uv` lockfile, `src/stmrr/` skeleton, then ADRs 0001–0012.

## Session Instructions

Before any work:
1. `git -C ~/projects/star-trek-retro-remake pull` — ensure repo is current
2. Read `DESIGN.md` for game design + locked architecture; `tech-stack-pyside6.md` for scaffold-phase operational steps. Where they disagree, `DESIGN.md` wins (per its own §0 note).
3. Check `docs/conventions.md` before introducing new patterns.
4. New patterns that will persist are added as numbered conventions before session end.

**Active incidents as of 2026-04-26:**
- 🟢 None. Pre-scaffold; no deployments, no live state to monitor.

## What Remains

- Scaffold step 1 of `tech-stack-pyside6.md` §11 — `pyproject.toml` + `uv` lockfile + `src/stmrr/` + `tests/` skeleton + `.importlinter` + `.pre-commit-config.yaml`.
- ADRs 0001–0012 capturing the locked decisions per `DESIGN.md` §10.7 (scaffold step 2).
- `.github/workflows/ci.yml` (deferred — needs `pyproject.toml` to test against).
- Branch protection on `main` (deferred — enable once CI workflow lands; per `tech-stack-pyside6.md` §13.5).
- Bundled-font license texts under `assets/fonts/<font>/LICENSE` once fonts are committed (`NOTICE.md` placeholder lists JetBrains Mono + VT323).
- `GITHUB_EMAIL` in `~/.bashrc` still references the old `L3DigitalNet` no-reply address — sweep when convenient.

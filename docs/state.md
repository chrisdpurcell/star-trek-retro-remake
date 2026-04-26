# Handoff

**Last updated:** 2026-04-26

## State at a glance

- Pre-scaffold. Repo holds `DESIGN.md` (canonical, 105 KB) and `tech-stack-pyside6.md` (scaffold-phase operational notes); both currently untracked.
- Handoff system landed 2026-04-26 — this file, the SessionStart hook, and the `docs/` layout per `/mnt/share/claude-handoff-system.md` §2.1.
- Decision 3 = PER-REPO (hook checked into `.claude/`). Decision 1 (Auto Memory) is implicitly active — the project memory dir already exists. Decision 2 (path-scoped `.claude/rules/`) deferred until `src/` exists.
- Next milestone: scaffold per `tech-stack-pyside6.md` §11 — `pyproject.toml`, `uv` lockfile, repo skeleton from §2.1, ADRs 0001–0012.

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
- Commit `DESIGN.md` + `tech-stack-pyside6.md` to track the design artifacts (currently untracked).
- ADRs 0001–0012 capturing the locked decisions per `DESIGN.md` §10.7.

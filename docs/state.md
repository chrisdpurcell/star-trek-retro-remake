# Handoff

**Last updated:** 2026-04-26

## State at a glance

- v0.1 scaffold landed. `pyproject.toml` + `uv.lock` (Python 3.14, PySide6 6.11, tcod 21.2), `src/stmrr/` package skeleton, smoke test (2 passed), `.importlinter` end-to-end verified, `.pre-commit-config.yaml`, three CI/CD workflows (`ci.yml`, `release.yml`, `dependency-review.yml`), Dependabot config, ADRs 0001–0012 + template, CONTRIBUTING/NOTICE/CHANGELOG updates.
- All five DoD checks green locally: `ruff format --check`, `ruff check`, `mypy src/stmrr`, `lint-imports`, `pytest`. `pre-commit run --all-files` clean.
- `docs/design/DESIGN.md` + `docs/design/tech-stack-pyside6.md` are the canonical design artifacts (moved from repo root this session).
- Public-facing repo at https://github.com/chrisdpurcell/star-trek-retro-remake. Branch protection on `main` still deferred — required CI checks don't exist on the remote until the first push runs the new workflow.
- Next milestone: model-layer first concrete code per `docs/design/tech-stack-pyside6.md` §11 step 3 — `model/world/grid_position.py` + `model/entities/game_object.py`, fully unit-tested.

## Session Instructions

Before any work:
1. `git -C ~/projects/star-trek-retro-remake pull` — ensure repo is current.
2. Read `docs/design/DESIGN.md` for game design + locked architecture; `docs/design/tech-stack-pyside6.md` for scaffold-phase operational steps. Where they disagree, `docs/design/DESIGN.md` wins.
3. Check `docs/conventions.md` before introducing new patterns.
4. New patterns that will persist are added as numbered conventions before session end.
5. Read the relevant ADR under `docs/adr/` before proposing any change that contradicts a settled decision; the path forward is a new ADR that supersedes the old one.

**Active incidents as of 2026-04-26:**
- 🟢 None. Scaffold landed clean; no live deployments to monitor.

## What Remains

### Manual GitHub-side configuration (Chris, after this session lands)

Cannot be automated from the repo because the required CI checks don't exist on the remote until the workflow runs once. Full checklist in `CHANGELOG.md` ### Post-Session Tasks; summary:

- **Settings → General → Pull Requests:** disable merge commits; enable squash + rebase; enable auto-update suggestions; auto-delete head branches.
- **Settings → Branches → Branch protection rule for `main`:** require status checks (`ruff format`, `ruff check`, `mypy`, `lint-imports`, `pytest`) once they appear; require linear history; disallow force pushes and deletions; apply to admins.
- **Settings → Actions → General:** workflow permissions = read+write (release workflow needs it); allow Actions to create + approve PRs (Dependabot).

### Code follow-ups

- Scaffold step 3 of `docs/design/tech-stack-pyside6.md` §11 — `model/world/grid_position.py` + `model/entities/game_object.py`, pure Python, fully unit-tested.
- Bundled-font license texts under `assets/fonts/<font>/LICENSE` once fonts are committed. `NOTICE.md` placeholder lists JetBrains Mono + VT323; the explicit `TODO: license text on first font commit` marker in NOTICE.md is the grep tag.
- `GITHUB_EMAIL` in `~/.bashrc` still references the old `L3DigitalNet` no-reply address — sweep when convenient (orthogonal to this repo, but mentioned in handoff for continuity).

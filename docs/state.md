# Handoff

**Last updated:** 2026-04-26

## State at a glance

- v0.1 scaffold landed and CI is green on `main`. `pyproject.toml` + `uv.lock` (Python 3.14.4, PySide6 6.11.0, tcod 21.2.0), `src/stmrr/` package skeleton, smoke test (2 passed), `.importlinter` end-to-end verified, `.pre-commit-config.yaml`, three CI/CD workflows (`ci.yml`, `release.yml`, `dependency-review.yml`), Dependabot, ADRs 0001–0013 + template, CONTRIBUTING/NOTICE/CHANGELOG updates.
- GitHub-side governance applied via `gh api` and live: merge methods (squash + rebase, no merge commits, auto-delete head branches, auto-update suggestions), Actions workflow perms (read+write, can approve PRs for Dependabot), repo topics (7), and **ruleset `main protection`** (ID `15570954`) with admin bypass — external contributors must PR with the `ruff + mypy + import-linter + pytest` job green; the maintainer commits direct.
- All five DoD checks green locally; `pre-commit run --all-files` clean. Latest CI run: `24964461035` `success` on `d46e264`.
- `docs/design/DESIGN.md` + `docs/design/tech-stack-pyside6.md` are the canonical design artifacts (under `docs/design/`, not at repo root).
- Next milestone: scaffold step 3 of `docs/design/tech-stack-pyside6.md` §11 — `src/stmrr/model/world/grid_position.py` + `src/stmrr/model/entities/game_object.py`, pure Python, fully unit-tested.

## Session Instructions

Before any work:
1. `git -C ~/projects/star-trek-retro-remake pull` — ensure repo is current.
2. Read `docs/design/DESIGN.md` for game design + locked architecture; `docs/design/tech-stack-pyside6.md` for scaffold-phase operational steps. Where they disagree, `docs/design/DESIGN.md` wins.
3. Check `docs/conventions.md` before introducing new patterns; new persistent patterns become numbered conventions before session end.
4. Read the relevant ADR under `docs/adr/` before proposing any change that contradicts a settled decision; the path forward is a new ADR that supersedes the old one.
5. **Do not run `uv run pre-commit install`** — global `core.hooksPath = /home/chris/.config/git/hooks` blocks it. Run `uv run pre-commit run --all-files` directly when you need the hook check (memory: `feedback_pre_commit_install.md`).
6. Direct pushes to `main` work for the maintainer (admin bypass on ruleset `main protection`); CI must still go green or follow-up commits will be needed.

**Active incidents as of 2026-04-26:**
- 🟢 None. Scaffold green; no live deployments to monitor.

## What Remains

### Code (next session pickup)

- **Scaffold step 3** (`docs/design/tech-stack-pyside6.md` §11): `src/stmrr/model/world/grid_position.py` + `src/stmrr/model/entities/game_object.py`. Pure Python, model-layer-strict mypy (`stmrr.model.*` is `strict = true`), fully unit-tested under `tests/unit/`. No Qt imports — `import-linter` will block them.
- **Scaffold step 4** (after step 3 lands): `src/stmrr/view/scene/projection.py` — isometric math, fully unit-tested. Build before any rendering per the vertical-slice rule.

### Documentation follow-ups (no rush)

- Bundled-font license texts under `assets/fonts/<font>/LICENSE` once fonts are committed. `NOTICE.md` carries the explicit `> **TODO:** license text on first font commit` grep tag.
- `GITHUB_EMAIL` in `~/.bashrc` still references the old `L3DigitalNet` no-reply address — sweep when convenient (orthogonal to this repo, mentioned for continuity).

### Closed this session

- ✅ v0.1 scaffold per `docs/design/tech-stack-pyside6.md` §11 step 1 (pyproject + uv.lock + repo skeleton + .importlinter + .pre-commit + ADRs).
- ✅ CI/CD workflows registered and green.
- ✅ GitHub-side configuration (PR settings, ruleset, Actions perms, topics) applied via `gh api`. Documented in `CHANGELOG.md` `### Repository Configuration` and ADR-0013.
- ✅ DESIGN.md §9.1 corrected to include `include_external_packages = True` in the canonical `.importlinter` example.

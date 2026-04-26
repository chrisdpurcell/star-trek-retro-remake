# Handoff

**Last updated:** 2026-04-26

## State at a glance

- v0.1 scaffold landed and CI is green on `main`. `pyproject.toml` + `uv.lock` (Python 3.14.4, PySide6 6.11.0, tcod 21.2.0), `src/stmrr/` package skeleton, smoke test (2 passed), `.importlinter` end-to-end verified, `.pre-commit-config.yaml`, three CI/CD workflows (`ci.yml`, `release.yml`, `dependency-review.yml`), Dependabot, ADRs 0001–0013 + template, CONTRIBUTING/NOTICE/CHANGELOG updates.
- GitHub-side governance applied via `gh api` and live: merge methods (squash + rebase, no merge commits, auto-delete head branches, auto-update suggestions), Actions workflow perms (read+write, can approve PRs for Dependabot), repo topics (7), and **ruleset `main protection`** (ID `15570954`) with admin bypass — external contributors must PR with the `ruff + mypy + import-linter + pytest` job green; the maintainer commits direct.
- All five DoD checks green locally; `pre-commit run --all-files` clean.
- `docs/design/DESIGN.md` + `docs/design/tech-stack-pyside6.md` are the canonical design artifacts (under `docs/design/`, not at repo root).
- **v0.1 model-layer specs cleared adversarial review.** `docs/specs/v0.1-step-3-grid-position-and-game-object.md` (1187 words) and `docs/specs/v0.1-model-layer.md` (2429 words). Four-pass Codex audit converged at zero findings. 10 commits with `docs(spec):` prefix from `c87855e` to `680b015`. Indexed in `docs/specs-plans.md` under `## Specs (docs/specs/)`.
- Next milestone: implement scaffold step 3 of `docs/design/tech-stack-pyside6.md` §11 against the cleared specs — `src/stmrr/model/world/grid_position.py` + `src/stmrr/model/entities/game_object.py`, pure Python, 100% line+branch tested.

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

- **Scaffold step 3 against cleared specs** (`docs/design/tech-stack-pyside6.md` §11): implement `src/stmrr/model/world/grid_position.py` + `src/stmrr/model/entities/game_object.py` per `docs/specs/v0.1-step-3-grid-position-and-game-object.md` (module-level) and `docs/specs/v0.1-model-layer.md` (cross-cutting). 100% line+branch coverage required on both modules; tests under `tests/unit/model/world/` and `tests/unit/model/entities/`. Note: `model/exceptions.py` is also part of v0.1 per Spec C §4 (`ModelError` root with `IllegalActionError` and `IllegalTransitionError` peers) — but only the action/transition exceptions actually used by step 3 (i.e., none yet) need bodies; the file lands when `Starship`/`GameStateManager` arrive in later steps.
- **Open questions in the cleared specs** that may surface during implementation: spec A §9.2 (Coordinate NewType, slots+pydantic friction, neighbors method-vs-free, ID reset hook for tests); spec C §8.2 (GameStateManager lifecycle, replay-log integration, typed event payloads). None block step 3 — they apply when their respective consumers arrive.
- **Scaffold step 4** (after step 3 lands): `src/stmrr/view/scene/projection.py` — isometric math, fully unit-tested. Build before any rendering per the vertical-slice rule.

### Documentation follow-ups (no rush)

- Bundled-font license texts under `assets/fonts/<font>/LICENSE` once fonts are committed. `NOTICE.md` carries the explicit `> **TODO:** license text on first font commit` grep tag.
- `GITHUB_EMAIL` in `~/.bashrc` still references the old `L3DigitalNet` no-reply address — sweep when convenient (orthogonal to this repo, mentioned for continuity).

### Closed this session

- ✅ v0.1 model-layer specs authored, taken through 4 rounds of adversarial Codex review, converged at zero findings. Two specs total: module-level (`v0.1-step-3-...`) and cross-cutting (`v0.1-model-layer`). Both within DoD word ceilings (1187/1200 and 2429/2500). Cleared for implementation.

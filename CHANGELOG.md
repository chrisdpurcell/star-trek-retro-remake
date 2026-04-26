# Changelog

All notable changes to *Star Trek Retro Remake* are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/) once the first release lands.

## [Unreleased] — v0.1.0 (in progress)

### Added

- Canonical Game Design Document (`docs/design/DESIGN.md`).
- Scaffold-phase operational notes (`docs/design/tech-stack-pyside6.md`).
- Per-repo handoff system (`.claude/`, `docs/`, `CLAUDE.md`) per the shared handoff spec.
- Public-facing repository documents: `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `NOTICE.md`, `CHANGELOG.md`.
- GitHub issue and pull request templates under `.github/`.
- `pyproject.toml` declaring the `stmrr` package, runtime + dev dependency floors per `docs/design/DESIGN.md` §9.2, and the per-module mypy strictness split from §10.6 (model/controller/config strict; view relaxed; tests under `disallow_incomplete_defs`).
- `uv.lock` for reproducible installs under Python 3.14.
- `src/stmrr/` package skeleton mirroring `docs/design/DESIGN.md` §9.1 — empty `__init__.py` markers under `model/`, `view/`, `controller/`, `config/`, `persistence/`, plus the `model/` and `view/` subpackages.
- `tests/` skeleton with `tests/unit/test_smoke.py` exercising the import path and `__version__` attribute.
- `.importlinter` with two contracts: `model-is-qt-free` and `view-does-not-import-model-events`. End-to-end verified by deliberately importing `PySide6` in a model file and watching `lint-imports` exit non-zero.
- `.pre-commit-config.yaml` wiring ruff, mypy, import-linter, and standard hygiene hooks, with versions tracking the dev-deps floor.
- `.github/workflows/ci.yml` — runs ruff, mypy, import-linter, and pytest on every push and PR; uploads coverage as a workflow artifact; concurrency-cancels in-progress runs on the same ref.
- `.github/workflows/release.yml` — builds sdist + wheel via `uv build` on `v*.*.*` tag pushes and publishes a GitHub Release with the matching `CHANGELOG.md` section. AppImage build steps deferred to v1.0.
- `.github/workflows/dependency-review.yml` — flags added/changed dependencies on every PR.
- `.github/dependabot.yml` — weekly Monday updates for the `pip` and `github-actions` ecosystems with minor/patch grouping.
- ADRs 0001–0012 in `docs/adr/` plus a `template.md`, anchoring the locked v0.1 decisions per `docs/design/DESIGN.md` §10.7.
- Local development section in `CONTRIBUTING.md` covering the `uv` bootstrap and the full check-suite invocation.
- Branch and commit rules section in `CONTRIBUTING.md` documenting the trunk-based, direct-to-`main` workflow.

### Changed

- Moved `DESIGN.md` and `tech-stack-pyside6.md` from the repo root into `docs/design/`. All cross-references in `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CLAUDE.md`, the LLM-internal `docs/` tree, and the GitHub issue templates updated to the new paths.

### Post-Session Tasks

These steps must be done manually on github.com after this changelog entry lands; they cannot be automated from the repo because the required CI checks don't exist until the workflow runs at least once.

1. **Settings → General → Pull Requests:**
   - Disable "Allow merge commits".
   - Enable "Allow squash merging" (default to "Pull request title and description").
   - Enable "Allow rebase merging".
   - Enable "Always suggest updating pull request branches".
   - Enable "Automatically delete head branches".
2. **Settings → Branches → Branch protection rule for `main`:**
   - Require status checks to pass before merging. Add the CI job names once they appear after the first push (`ruff format`, `ruff check`, `mypy`, `lint-imports`, `pytest` — actual names follow the `ci.yml` job IDs).
   - Require branches to be up to date before merging.
   - Require linear history.
   - Do **not** require a pull request before merging — direct pushes to `main` are intended for the solo workflow.
   - Disallow force pushes and deletions.
   - Apply rules to administrators (no bypass).
3. **Settings → Actions → General:**
   - Workflow permissions: Read and write (needed for the release workflow to create releases).
   - Enable "Allow GitHub Actions to create and approve pull requests" (for Dependabot).
4. **Repo topics:** `python`, `pyside6`, `qt`, `turn-based-strategy`, `star-trek`, `fan-game`, `linux`.

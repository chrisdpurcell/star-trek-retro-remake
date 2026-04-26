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
- `docs/specs/v0.1-step-3-grid-position-and-game-object.md` — module-level spec for the v0.1 step 3 foundation pair (`GridPosition`, `GameObject`); pending Codex adversarial review before implementation.
- `docs/specs/v0.1-model-layer.md` — cross-cutting spec for the v0.1 pure-Python model layer (events, ID lifecycle, state-machine contract, dependency graph, invariants); pending Codex adversarial review before implementation.

### Changed

- Moved `DESIGN.md` and `tech-stack-pyside6.md` from the repo root into `docs/design/`. All cross-references in `README.md`, `CONTRIBUTING.md`, `SECURITY.md`, `CLAUDE.md`, the LLM-internal `docs/` tree, and the GitHub issue templates updated to the new paths.

### Repository Configuration (applied via gh API after first CI run)

Applied 2026-04-26 once the first CI run on `main` produced a check name to require. The chicken-and-egg with required status checks is unavoidable on a fresh repo — the workflow has to run once before its job name can be referenced as a required check.

1. **Repo settings (via `PATCH /repos/{owner}/{repo}`):**
   - `allow_merge_commit: false`
   - `allow_squash_merge: true`, `squash_merge_commit_title: PR_TITLE`, `squash_merge_commit_message: PR_BODY` (default to "Pull request title and description")
   - `allow_rebase_merge: true`
   - `allow_update_branch: true` ("Always suggest updating pull request branches")
   - `delete_branch_on_merge: true`
2. **Branch protection on `main` via repository ruleset** (rulesets, not classic protection, because the desired model is "external contributors must PR; maintainer commits direct" — admin bypass is a first-class concept on rulesets only):
   - Target: `~DEFAULT_BRANCH`. Enforcement: `active`. Ruleset ID: `15570954`, name `main protection`.
   - Bypass actors: `RepositoryRole` actor_id=5 (admin), bypass_mode=`always` — lets the maintainer push direct to `main` while requiring a PR from anyone else.
   - Rules: `deletion` (no branch delete), `non_fast_forward` (no force-push), `required_linear_history`, `pull_request` (`required_approving_review_count=0`, dismiss stale reviews on push), `required_status_checks` with `strict=true` and the `"ruff + mypy + import-linter + pytest"` job context (the actual job name from `.github/workflows/ci.yml`, not the per-step labels).
3. **Actions permissions (via `PUT /repos/{owner}/{repo}/actions/permissions/workflow`):**
   - `default_workflow_permissions: write` (so `release.yml` can create releases)
   - `can_approve_pull_request_reviews: true` (for Dependabot's auto-approval flow)
4. **Repo topics (via `PUT /repos/{owner}/{repo}/topics`):** `python`, `pyside6`, `qt`, `turn-based-strategy`, `star-trek`, `fan-game`, `linux`.

The maintainer's bypass is verified by the push of this very commit landing directly on `main` without a PR. Future external contributors will be required to open a PR that passes the `ruff + mypy + import-linter + pytest` job before merge.

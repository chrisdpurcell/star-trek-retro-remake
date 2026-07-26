---
schema_version: '1.1'
id: 'runbook-4gwdkg-contributing'
title: 'Contributing'
description: 'Contribution policy, local development setup, quality gates, and repository workflow for Star Trek Retro Remake.'
doc_type: 'runbook'
status: 'active'
created: '2026-04-26'
updated: '2026-07-26'
reviewed: null
owner: 'project-maintainer'
consumer: 'user'
tags:
  - 'onboarding'
  - 'policy'
  - 'tooling'
aliases: []
related: []
source: []
confidence: 'unknown'
visibility: 'public'
license: null
---

# Contributing

Thanks for your interest in _Star Trek Retro Remake_. The project is a personal labor of love under active development. v0.1 steps 1–10 are complete; external code contributions are not yet open, but issues and design discussions are welcome.

## Project status

The canonical game design lives in [`docs/design/DESIGN.md`](docs/design/DESIGN.md); supplementary operational notes live in [`docs/design/tech-stack-pyside6.md`](docs/design/tech-stack-pyside6.md). The v0.1 foundation and runnable MVC shell (steps 1–10) have landed, Step 11 is next, and the standards below are in effect.

## Reporting issues

Use the issue templates in `.github/ISSUE_TEMPLATE/`:

- **Bug** — only meaningful once builds exist
- **Feature** — for ideas that fit within the scope of `docs/design/DESIGN.md`
- **Design discussion** — for questions about decisions captured in `docs/design/DESIGN.md` §10.7 (ADRs) or scope changes

Before opening a feature or design discussion issue, skim `docs/design/DESIGN.md` to see whether the topic is already covered.

## IP boundary (read this first)

This is a non-commercial fan project with explicit IP boundaries — see [`NOTICE.md`](NOTICE.md). Contributions that violate the boundaries will be rejected:

- No copied assets from official Star Trek media (sprites, audio, screenshots, lifted text).
- No AI-generated visual assets that reproduce canonical Trek designs. Prompts must describe styling and silhouette.
- No commercial monetization, donation links, or upsells.

## Local development

Python 3.14 is not packaged in Debian 13 / Ubuntu 24.04 default repositories. The project bootstraps its own interpreter via [`uv`](https://docs.astral.sh/uv/) (see `docs/design/DESIGN.md` §9.3).

```bash
# One-time per machine
curl -LsSf https://astral.sh/uv/install.sh | sh
uv python install 3.14

# Per repo clone
cd star-trek-retro-remake
uv sync --locked --all-groups
```

After that, run the project with:

```bash
uv run python -m stmrr
```

### Running the full check suite locally

The repository-owned gate is the authoritative local and CI check:

```bash
uv run python scripts/check.py
```

It runs Ruff formatting and linting, BasedPyright strict, the import-linter contracts, branch-aware coverage with an aggregate 85% floor, and pip-audit. CI (`.github/workflows/ci.yml`) runs the same script on every push and PR. A push to `main` should be green locally before it leaves your machine.

Run the targeted hygiene and layer hooks directly when reviewing all tracked files; do not install them into `.git/hooks`:

```bash
uv run pre-commit run --all-files
```

## Coding standards

Standards are taken from `docs/design/DESIGN.md` §10.6. Project Standards Python Tooling 1.8 defines the executable gate contract; consumer-owned `scripts/check.py` and `.github/workflows/ci.yml` implement it. Its reference-only [Python Coding 0.6 companion](https://github.com/L3DigitalNet/project-standards/blob/v5.8.0/standards/python-coding/versions/0.6/README.md) governs Python code shape. Python Coding is intentionally absent from `.standards/config.toml` because Catalog 5 marks it non-selectable.

### Formatting and linting (ruff)

- **Line length:** 100 characters
- **Quote style:** double quotes
- **Import sorting:** ruff's isort-compatible rules (`I` rule set enabled)
- **Rule sets:** the managed `[tool.ruff.lint]` table in `pyproject.toml` is authoritative.
- **Formatter:** `ruff format`. No black, no separate isort.

### Typing (BasedPyright)

- `src/`, `tests/`, and `scripts/` run under BasedPyright strict mode.
- Warnings fail the gate.
- Configuration lives in `pyproject.toml` under `[tool.basedpyright]`.
- Third-party dynamic boundaries use narrow casts or diagnostic-specific, justified `# pyright: ignore[...]` comments; broad ignores are not accepted.

### Type hints

- All public APIs (anything not prefixed with `_`) require complete type hints on parameters and return values.
- Internal helpers are typed wherever strict checking cannot infer a precise contract.
- On Python 3.14+, do not add `from __future__ import annotations` merely for ordinary forward references. Existing uses remain where their runtime annotation behavior is understood and tested.

### Docstrings

- Public model classes, public functions, and any non-obvious algorithm: Google-style docstrings.
- Private helpers: a single-line summary or no docstring at all.
- Don't write docstrings that just restate the function name.

### Module-level conventions

- One class per module is _not_ required. Group closely-related classes.
- `__all__` declared in modules with public APIs.
- Avoid circular imports by routing through `events.py` in the model and `model_bridge.py` in the controller — both are explicit decoupling seams.

### Naming

- Classes: `PascalCase`
- Functions, methods, variables: `snake_case`
- Module-level constants: `UPPER_SNAKE_CASE`
- Qt signals: `snake_case` past tense (`ship_moved`, `turn_advanced`)
- Model events (blinker): same convention as Qt signals

### Pre-commit hooks

After `uv sync --locked --all-groups`, run `uv run pre-commit run --all-files` directly. Do not install hooks. These supplementary hooks run:

- standard file-hygiene checks
- `import-linter`

The complete Python gate remains `uv run python scripts/check.py`.

## Architectural rules

The project enforces strict layer boundaries — the model layer must have **zero Qt imports**. This is mechanically enforced by `import-linter` in CI (contract config: `.importlinter` at repo root).

If you find yourself wanting to import `PySide6` in `src/stmrr/model/`, you've identified a missing seam in `controller/model_bridge.py` — don't bypass the rule, raise it as a design discussion issue. Full rationale in `docs/design/DESIGN.md` §9.1.

## Branch and commit rules

The project is single-developer and uses a trunk-based workflow. Direct commits to `main` are the default; feature branches are the exception.

- **Default to direct commits on `main`.** Pull latest before starting; push when each logical unit is complete and CI-green locally.
- **Use a feature branch only when** (a) the work spans multiple sessions and shouldn't land partially, (b) the change is risky enough to throw away cleanly if it doesn't work out, or (c) explicitly requested. When in doubt, commit to `main`.
- **Branch naming when needed:** `<type>/<phase>-<description>` (e.g. `feat/v0.1-combat-prototype`). Rebase on `main` before merging. Squash to a single commit on merge unless commits are independently meaningful. Delete the branch after merge.
- **Commit in logical units, not one mega-commit per session.** Each commit message stands alone. Use [Conventional Commits](https://www.conventionalcommits.org/) prefixes: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `style`, `perf`, `ci`. Subject line under 70 characters.
- **Run the full local check suite before every push to `main`** (see "Running the full check suite locally" above). Don't push red builds.
- **Never force-push `main`.** Force-push is acceptable on personal feature branches before merge.
- **If a push is rejected by branch protection, fix locally and re-push.** Don't weaken protection to land a broken commit.
- **At session end, update `CHANGELOG.md`** under `## [Unreleased]` capturing what landed, any deviations from spec, and follow-ups.

Maintainer commits are GPG-signed. External contributors do not need signed commits.

## Pull requests

PRs are welcome for documentation fixes, typos, and external contributions. PRs should:

- Reference an issue (one of the templates in `.github/ISSUE_TEMPLATE/`) when fixing a tracked problem.
- Pass the repository gate (`uv run python scripts/check.py`) and the standards/Markdown workflows.
- Stay focused — one PR per logical change.

## Architecture Decision Records

Locked architectural decisions live in [`docs/adr/`](docs/adr/) as one-page Markdown files (Context / Decision / Consequences / Status). Read the relevant ADR before proposing a change that contradicts a settled decision; the path forward in that case is a new ADR that supersedes the old one explicitly. See `docs/adr/template.md` for the format and `docs/design/DESIGN.md` §10.7 for the full rationale.

## License

By contributing to this repository, you agree that your contributions will be licensed under the [MIT License](LICENSE).

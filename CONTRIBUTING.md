# Contributing

Thanks for your interest in *Star Trek Retro Remake*. The project is a personal labor of love — currently pre-scaffold, not yet open for external code contributions, but issues and design discussions are welcome.

## Project status

The canonical game design lives in [`docs/design/DESIGN.md`](docs/design/DESIGN.md); the scaffold-phase operational notes live in [`docs/design/tech-stack-pyside6.md`](docs/design/tech-stack-pyside6.md). The v0.1 scaffold (`pyproject.toml`, `src/stmrr/` package skeleton, ADRs 0001–0012, CI/CD workflows) has landed; the standards below are in effect.

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
uv sync --all-extras
uv run pre-commit install   # arm the local hooks
```

After that, run the project with:

```bash
uv run python -m stmrr      # (post-scaffold; entry point lands with v0.1 view shell)
```

### Running the full check suite locally

Pre-commit hooks cover most of this, but the explicit run catches anything skipped:

```bash
uv run ruff format --check . \
  && uv run ruff check . \
  && uv run mypy src/stmrr \
  && uv run lint-imports \
  && uv run pytest
```

CI (`.github/workflows/ci.yml`) re-runs the same five steps on every push and PR. A push to `main` should be CI-green locally before it leaves your machine.

## Coding standards

Standards are taken from `docs/design/DESIGN.md` §10.6.

### Formatting and linting (ruff)

- **Line length:** 100 characters
- **Quote style:** double quotes
- **Import sorting:** ruff's isort-compatible rules (`I` rule set enabled)
- **Rule sets enabled:** `E`, `F`, `W`, `I`, `B`, `UP`, `SIM`, `RUF`. Add `D` (pydocstyle) only if docstring discipline becomes a problem.
- **Formatter:** `ruff format`. No black, no separate isort.

### Typing (mypy)

- **`model/`, `controller/`, `config/`** run under `strict = true`.
- **`view/`** runs under a relaxed profile (`disallow_untyped_defs = true` but not full strict) — Qt's stub coverage has rough edges.
- **`tests/`** runs unchecked except for `disallow_incomplete_defs = true`.
- Configuration lives in `pyproject.toml` under `[tool.mypy]`.

### Type hints

- All public APIs (anything not prefixed with `_`) require complete type hints on parameters and return values.
- Internal helpers may omit hints where mypy can infer cleanly.
- `from __future__ import annotations` at the top of every module.

### Docstrings

- Public model classes, public functions, and any non-obvious algorithm: Google-style docstrings.
- Private helpers: a single-line summary or no docstring at all.
- Don't write docstrings that just restate the function name.

### Module-level conventions

- One class per module is *not* required. Group closely-related classes.
- `__all__` declared in modules with public APIs.
- Avoid circular imports by routing through `events.py` in the model and `model_bridge.py` in the controller — both are explicit decoupling seams.

### Naming

- Classes: `PascalCase`
- Functions, methods, variables: `snake_case`
- Module-level constants: `UPPER_SNAKE_CASE`
- Qt signals: `snake_case` past tense (`ship_moved`, `turn_advanced`)
- Model events (blinker): same convention as Qt signals

### Pre-commit hooks

`pre-commit install` after `uv sync`. Hooks run:

- `ruff format`
- `ruff check --fix`
- `mypy` (cached)
- `import-linter`

CI re-runs all checks; pre-commit is a local convenience.

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
- Pass CI (`ruff`, `mypy`, `import-linter`, `pytest`).
- Stay focused — one PR per logical change.

## Architecture Decision Records

Locked architectural decisions live in [`docs/adr/`](docs/adr/) as one-page Markdown files (Context / Decision / Consequences / Status). Read the relevant ADR before proposing a change that contradicts a settled decision; the path forward in that case is a new ADR that supersedes the old one explicitly. See `docs/adr/template.md` for the format and `docs/design/DESIGN.md` §10.7 for the full rationale.

## License

By contributing to this repository, you agree that your contributions will be licensed under the [MIT License](LICENSE).

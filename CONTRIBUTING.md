# Contributing

Thanks for your interest in *Star Trek Retro Remake*. The project is a personal labor of love — currently pre-scaffold, not yet open for external code contributions, but issues and design discussions are welcome.

## Project status

The repository is currently pre-scaffold: the canonical game design lives in [`docs/design/DESIGN.md`](docs/design/DESIGN.md) and the technical scaffold plan in [`docs/design/tech-stack-pyside6.md`](docs/design/tech-stack-pyside6.md), but `src/` does not yet exist. The standards below take effect when the scaffold lands (`v0.1`).

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

## Commit messages

Conventional-commit style:

```
<type>(<scope>): <subject>

<optional body>
```

Types: `feat`, `fix`, `docs`, `chore`, `refactor`, `test`, `style`, `perf`, `ci`. Subject line under 70 characters.

Maintainer commits are GPG-signed. External contributors do not need signed commits.

## Pull requests

Once `v0.1` lands, PRs should:

- Reference an issue (one of the templates in `.github/ISSUE_TEMPLATE/`)
- Pass CI (ruff, mypy, import-linter, pytest)
- Stay focused — one PR per logical change

Until then, PRs are welcome for documentation fixes and typos in `docs/design/DESIGN.md` / `docs/design/tech-stack-pyside6.md` / this file.

## License

By contributing to this repository, you agree that your contributions will be licensed under the [MIT License](LICENSE).

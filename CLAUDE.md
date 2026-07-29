# CLAUDE.md

**Session startup:** state is injected by the repo-local Agent Handoff SessionStart hook; do not reread it when injected.

**Document layout (read on demand):**

- `docs/handoff/state.md` — live state + active incidents (auto-injected, do not read directly)
- `docs/handoff/deployed.md` — deployment truth (pre-scaffold: nothing built yet)
- `docs/handoff/architecture.md` — layered architecture + pointers into `docs/design/DESIGN.md` / `docs/design/tech-stack-pyside6.md`
- `docs/handoff/credentials.md` — Bao path index
- `docs/handoff/conventions.md` — pattern library (Quick Reference at top, six-field schema)
- `docs/handoff/sessions/` — monthly session logs (grep by date)
- `docs/handoff/bugs/` — per-file bug KB (grep by service or tag)
- `docs/handoff/specs-plans.md` — pointer into `docs/superpowers/{specs,plans}/` plus the canonical design artifacts under `docs/design/`

## Status

v0.1 steps 1–10 are complete and the MVC triad is runnable. Step 11—planning and implementing `MapView`/`GridScene`—is next. The canonical design remains `docs/design/DESIGN.md`.

Python code is governed by the immutable [Python Coding 0.6 companion](https://github.com/L3DigitalNet/project-standards/blob/v5.11.0/standards/python-coding/versions/0.6/README.md). It is reference-only and intentionally not enabled in `.standards/`.

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:agent-handoff -->
<!-- markdownlint-disable MD025 -->
# Agent Handoff

Use the repo-local `agent-handoff` skill at session startup and closeout. Do not reread state already injected by SessionStart. Keep project knowledge inside this repository and store credential references only, never values.
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:agent-handoff -->

<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:markdown-tooling -->
<!-- markdownlint-disable MD025 -->
# Markdown and structured-text tooling

Prettier owns physical formatting and markdownlint owns Markdown structure. Do not add overlapping tools.

Enabled checks: format, lint.
Markdown scope: `**/*.md`.
Structured-config scope: `**/*.json`, `**/*.jsonc`, `**/*.yml`, `**/*.yaml`.

Declared exclusions:
- `.pytest_cache/**` (both): Generated pytest cache content is not repository documentation.
- `.venv/**` (both): The uv-managed virtual environment contains third-party package documentation.
- `.agents/**` (both): Package-owned agent assets must retain their released bytes.
- `.claude/**` (both): Harness configuration is outside the documentation corpus.
- `.codex/**` (both): Harness configuration is outside the documentation corpus.
- `.standards/**` (both): Control-plane outputs must retain their reconciled bytes.
- `.github/PULL_REQUEST_TEMPLATE.md` (both): The GitHub interaction template is maintained separately.
- `.github/workflows/format.yml` (format): The exclusive managed caller is not Prettier-stable in 5.8.0; see upstream issue 48.
- `.github/workflows/lint-markdown.yml` (format): The exclusive managed caller is not Prettier-stable in 5.8.0; see upstream issue 48.
- `.import_linter_cache/**` (format): Generated Import Linter cache content is not repository source.
- `AGENTS.md` (both): Agent instructions contain package-managed envelopes.
- `CLAUDE.md` (both): Agent instructions contain package-managed envelopes.
- `docs/STATUS.md` (both): Agent Handoff owns the live status document.
- `docs/TODO.md` (both): Agent Handoff owns the live task document.
- `docs/adr/template.md` (both): The authoring template intentionally contains placeholders.
- `docs/handoff/**` (both): Agent Handoff governs this knowledge corpus.

Run the enabled checks before claiming completion.
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:markdown-tooling -->

<!-- prettier-ignore-end -->

<!-- prettier-ignore-start -->

<!-- BEGIN project-standards:python-tooling -->
<!-- markdownlint-disable MD025 -->
# Python tooling

Use uv for environments and dependency changes. Ruff owns formatting, linting, and imports.
Use basedpyright in strict mode for type checking. Do not add a competing Python gate.

Run before claiming completion:

```bash
uv run ruff format --check .
uv run ruff check .
uv run basedpyright
uv run coverage run -m pytest
uv run coverage report
uv run pip-audit
```

When the gate reports formatting or lint findings, run:

```bash
uv run ruff format .
uv run ruff check . --fix
```
<!-- markdownlint-enable MD025 -->
<!-- END project-standards:python-tooling -->

<!-- prettier-ignore-end -->

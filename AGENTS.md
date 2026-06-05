# AGENTS.md

**Session state:** read `docs/handoff/state.md`, then this file, then `docs/handoff/conventions.md`.

**Full conventions reference:** [`docs/handoff/conventions.md`](docs/handoff/conventions.md) - LLM-targeted pattern library. Check it before adding persistent patterns.

**Detailed review workflows:** not configured for this repo.

## Repo Notes

- Canonical design: `docs/design/DESIGN.md`; `docs/design/tech-stack-pyside6.md` is supplementary and operational.
- Before implementation work, read the relevant spec or plan from `docs/handoff/specs-plans.md` and any ADR that would be contradicted.
- The model layer stays Qt-free; see convention 1 and `.importlinter`.
- Do not run `uv run pre-commit install`; run `uv run pre-commit run --all-files` directly.

## Session End

- Update only changed handoff facts in `docs/`.
- Add a compact row to `docs/handoff/sessions/<YYYY-MM>.md` for durable work.
- If bug docs change, run `python3 docs/handoff/bugs/_regen_index.py && git diff --exit-code docs/handoff/bugs/INDEX.md`.

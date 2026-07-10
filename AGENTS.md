# AGENTS.md

**Session state:** Agent Handoff SessionStart injects `docs/handoff/state.md`; do not reread it when injected. Then use this file and `docs/handoff/conventions.md`.

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

<!-- BEGIN agent-handoff managed instructions -->
Use the repo-local `$agent-handoff` skill at startup and closeout.
Do not reread `docs/handoff/state.md` when SessionStart already injected it.
Keep current status and tasks in `docs/STATUS.md` and `docs/TODO.md`; route durable facts through `docs/handoff/`.
At closeout, update only changed facts, preserve user-authored work, store credential references only, and run relevant validation.
<!-- END agent-handoff managed instructions -->

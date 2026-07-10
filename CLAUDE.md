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

<!-- BEGIN agent-handoff managed instructions -->
Use the repo-local `$agent-handoff` skill at startup and closeout.
Do not reread `docs/handoff/state.md` when SessionStart already injected it.
Keep current status and tasks in `docs/STATUS.md` and `docs/TODO.md`; route durable facts through `docs/handoff/`.
At closeout, update only changed facts, preserve user-authored work, store credential references only, and run relevant validation.
<!-- END agent-handoff managed instructions -->

# CLAUDE.md

**Session startup:** state is injected by the SessionStart hook (see `.claude/hooks/session_start.py`).

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

v0.1 scaffold steps 1–6 complete at HEAD `8fe5f8b`. Active work resumes at step 7 (`entities/starship.py` + `combat/turn_manager.py`). Read `docs/handoff/state.md` for current milestone pointers and remaining work. Design is locked in `docs/design/DESIGN.md` (canonical); `docs/design/tech-stack-pyside6.md` is supplementary for scaffold phases.

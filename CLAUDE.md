# CLAUDE.md

**Session startup:** state is injected by the SessionStart hook (see `.claude/hooks/session_start.py`).

**Document layout (read on demand):**
- `docs/state.md` — live state + active incidents (auto-injected, do not read directly)
- `docs/deployed.md` — deployment truth (pre-scaffold: nothing built yet)
- `docs/architecture.md` — layered architecture + pointers into `docs/design/DESIGN.md` / `docs/design/tech-stack-pyside6.md`
- `docs/credentials.md` — Bao path index
- `docs/conventions.md` — pattern library (Quick Reference at top, six-field schema)
- `docs/sessions/` — monthly session logs (grep by date)
- `docs/bugs/` — per-file bug KB (grep by service or tag)
- `docs/specs-plans.md` — pointer into `docs/superpowers/{specs,plans}/` plus the canonical design artifacts under `docs/design/`

## Status

Pre-scaffold. `docs/design/DESIGN.md` (canonical) and `docs/design/tech-stack-pyside6.md` (operational scaffold notes) are the design artifacts. First scaffold step is `docs/design/tech-stack-pyside6.md` §11 — `pyproject.toml` + `uv` lockfile + repo skeleton.

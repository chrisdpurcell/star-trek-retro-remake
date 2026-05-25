# State

**Last updated:** 2026-05-25 (post step-7 design + plan; awaiting execution in next session)

## State at a glance

- v0.1 scaffold on `main`; CI running on push at HEAD `8fe5f8b` (step-6 implementation last green). Step 3 (`GridPosition` + `GameObject`) at `1d657bc`; step 4 (`view/scene/projection.py`) at `bcd07b4`; step 5 (`states.py` + `exceptions.py` + `events.py`) at `5420568`; step 6 (`sector_map.py` + `station.py`) at `8fe5f8b`.
- **Step 7 design + plan complete at HEAD `3eb89f7`, awaiting execution** (this session, 7 commits ahead of `origin/main` once pushed): spec at `docs/specs/v0.1-step-7-starship-and-turn-manager.md` (revision 3, cleared 3 adversarial Codex rounds — verdict "audit/fix loop can stop") + plan at `docs/superpowers/plans/2026-05-25-v0.1-step-7-implementation.md` (revision 4, cleared 4 review rounds: qdev-quality-reviewer rounds 1-2 then external Codex rounds 1-2; final verdict "audit/fix loop can stop"). Spec covers `entities/starship.py` (full Starship surface — kwarg-only constructor with tight defensive scalar validation, validate-before-super EntityId preservation, atomic check-then-debit `_debit_ap(cost)` with non-bool-int-≥1 cost-domain validation, `move_to`/`dock_at`/`restore_ap` action methods per umbrella §5.6.1/5.6.2/5.6.3) + `combat/turn_manager.py` (`TurnManager(player_id, *, current_turn=1)` with both-fields-validated init; SA-001 lock: inactive player Starships SUCCEED at End Turn per umbrella §5.6.3 "always available"). Two new runtime DAG edges (turn_manager→starship, starship→station; no back-edges). Five coordinated umbrella amendments queued in spec §10. Two paired research files (`docs/research/2026-05-25-v0.1-step-7-{spec-assumptions,open-questions}.md`) with supersedence headers documenting any divergence from spec-locked decisions. Plan is a 5-task TDD execution (~75 embedded tests across the two test files; full validation gate including `--cov-reset --cov=stmrr.model --cov-fail-under=100`; final-task neutralizer prepend per `docs/conventions.md` §8).
- **Next milestone:** **execute** the cleared step-7 plan via `superpowers:subagent-driven-development` (recommended per writing-plans skill) or `superpowers:executing-plans`. Estimated 1-2 hours of subagent dispatches. No code has been written yet — only design + plan artifacts. Source modules at `src/stmrr/model/entities/starship.py` and `src/stmrr/model/combat/turn_manager.py` do NOT exist (verified by Task 1 Step 2 preflight assertions in the plan).
- Canonical design: `docs/design/DESIGN.md` (wins over `tech-stack-pyside6.md` on conflicts).

## Session Instructions

Before any work:
1. `git -C ~/projects/star-trek-retro-remake pull`.
2. Read `docs/design/DESIGN.md` and `docs/design/tech-stack-pyside6.md`.
3. Check `docs/conventions.md` before new patterns; numbered conventions before session end.
4. Read relevant `docs/adr/` before contradicting a settled decision; path forward = new superseding ADR.
5. **Do not run `uv run pre-commit install`** — global `core.hooksPath` blocks it. Run `uv run pre-commit run --all-files` directly. (memory: `feedback_pre_commit_install.md`)
6. Direct pushes to `main` work (admin bypass); CI must still go green.

## Active incidents

- 🟢 None.

## What Remains

- Step 7+: remaining model modules per `docs/specs/v0.1-model-layer.md` §4 — `entities/starship.py`, `combat/turn_manager.py`, `state/game_state_manager.py`, `state/states.py` concrete subclasses (`MainMenuState`, `SectorMapState`). Each lands as its own per-step spec.
- Font license texts due when fonts are committed; `NOTICE.md` has the grep tag.

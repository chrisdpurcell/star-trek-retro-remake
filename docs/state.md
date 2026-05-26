# State

**Last updated:** 2026-05-26 (step-8 spec ✅ cleared 2 Codex rounds; ready for plan authoring)

## State at a glance

- v0.1 scaffold on `main` at HEAD `14bc848`; CI on push at HEAD `14bc848` (step-7 implementation last green). Step 3 (`GridPosition` + `GameObject`) at `1d657bc`; step 4 (`view/scene/projection.py`) at `bcd07b4`; step 5 (`states.py` placeholder + `exceptions.py` + `events.py`) at `5420568`; step 6 (`sector_map.py` + `station.py`) at `8fe5f8b`; step 7 (`starship.py` + `turn_manager.py`) at `9898551` (with two review-driven test follow-ups at `b89a349`, `4edf9e7` and a docs closeout at `68e73fa`, `14bc848`).
- **Step 8 SPEC ✅ CLEARED 2 Codex rounds (uncommitted; ready for plan authoring).** Working-tree artifacts: `docs/research/2026-05-26-v0.1-step-8-open-questions.md` (8 Q-locks) + `docs/research/2026-05-26-v0.1-step-8-pre-review-research.md` (pre-Codex empirical verification) + `docs/specs/v0.1-step-8-game-state-manager.md` (round-1: 1 blocking + 6 non-blocking, all 7 resolved — SA-001 ruff noqa removed; SA-002 `GameState` to `TYPE_CHECKING` + new umbrella §6 amendment; SA-003 `__all__` lock + export tests; SA-004 transition count fix; SA-005 `__str__` row dropped; SA-006 new §6.5 lifecycle hook exception policy + invariant 13 + two test rows; SA-007 §7.3 mypy gate rewrite; round-2: 0 blocking, 0 regressions, 1 optional Low-severity wording polish SA-NEW-001 applied — TOML writer attributed to `tomli_w` per ADR-0004, not `tomllib` which is parse-only; round-2 verdict "audit/fix loop can stop") + `docs/specs-plans.md` index row + this state row. **Umbrella sync `rg` gate** has three patterns, all three verified to hit exactly one line each in `docs/specs/v0.1-model-layer.md` at HEAD `14bc848`. No code changes yet; implementation gated on the next phase.
- **Next move:** author the step-8 implementation plan at `docs/superpowers/plans/2026-05-26-v0.1-step-8-implementation.md` (mirror step-7's 5-task structure: preflight + scaffold verification; `game_state_manager.py` + tests; `states.py` extensions + tests; umbrella amendments — three rows per §10; index + plan tracking + final validation gate). Plan should target the §7.3 validation gate categories from the spec. Then Codex plan-review pass; then execute via `superpowers:subagent-driven-development` TDD. Per umbrella `docs/specs/v0.1-model-layer.md` §4, step 8 closes the controller-pivot surface for v0.1.
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
- 🟡 **Full-suite pytest collection count (11129) is suspiciously large** vs. the model-only subset (414) and the additional non-model files in `tests/` (~4 files). Likely a runaway parametrize cartesian product in `tests/unit/test_smoke.py` or `tests/unit/view/scene/test_projection.py`. Not a regression introduced by step 7 — predates it (step-6 close-out noted 11,023 cases). Worth diagnosing during the next session that touches view-layer tests; until then it's a benign efficiency concern (~4 s runtime), not a correctness one.

## What Remains

- Step 8: `state/game_state_manager.py` + concrete `MainMenuState`/`SectorMapState`. Closes the v0.1 controller surface.
- v0.2 deferrals carried forward from step-7 spec §9.2: local `_send_robust` utility (trigger: second non-bridge subscriber lands); `kind: ClassVar[str] → Final[str]` migration; `MissingEntityError(IllegalActionError)` split from `InactiveEntityError`; multi-cell pathing + Pythagorean-diagonal AP cost (`_debit_ap(cost)` is the extension point); faction/reputation gating on `accepts_dock` (step-6 `_Dockable: Protocol` is the extension point); `NotDockableError` split; TOML save/load (v0.2 persistence spec).
- Font license texts due when fonts are committed; `NOTICE.md` has the grep tag.

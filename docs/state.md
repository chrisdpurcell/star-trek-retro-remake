# State

**Last updated:** 2026-05-25 (post step-7 execution complete)

## State at a glance

- v0.1 scaffold on `main` at HEAD `14bc848`; CI on push at HEAD `14bc848` (step-7 implementation last green). Step 3 (`GridPosition` + `GameObject`) at `1d657bc`; step 4 (`view/scene/projection.py`) at `bcd07b4`; step 5 (`states.py` placeholder + `exceptions.py` + `events.py`) at `5420568`; step 6 (`sector_map.py` + `station.py`) at `8fe5f8b`; **step 7 (`starship.py` + `turn_manager.py`) at `9898551`** (with two review-driven test follow-ups at `b89a349`, `4edf9e7` and a docs closeout at `68e73fa`, `14bc848`).
- **Step 7 IMPLEMENTED.** Five-task TDD execution via `superpowers:subagent-driven-development` against the cleared plan at `docs/superpowers/plans/2026-05-25-v0.1-step-7-implementation.md` (now neutralized). Eight commits on `main`: `854c7fb` Starship + 75 tests → `b89a349` Starship review fixes (dual-violation precondition-order witnesses + no-mutation-assert tightening, +2 tests = 77) → `a686de2` TurnManager + 24 tests → `4edf9e7` TurnManager review fixes (DAG test tightening + parametrize symmetry + naming convention, +1 test = 25) → `6f1ace2` 5 umbrella amendments to `v0.1-model-layer.md` (§4 Starship + TurnManager rows, §6 DAG two rows, §9 new blinker-synchronous-emit risk bullet) → `9898551` docs/specs-plans index + full validation gate → `68e73fa` hash placeholder fill → `14bc848` completed-plan neutralizer prepend. **414 model tests at 100% line+branch coverage** on `stmrr.model`; full project suite green. mypy `--strict` clean across 29 source files; 4 import-linter contracts kept, 0 broken. Two new runtime DAG edges in place (`combat.turn_manager → entities.starship` for `isinstance`; `entities.starship → entities.station` for `isinstance`); no back-edges. SA-001 lock doubly-enforced (production `advance_turn` does NOT check `player.active`; `test_advance_turn_inactive_player_starship_succeeds` named defensive test pins the behavior).
- **Next milestone:** **step 8** — `model/state/game_state_manager.py` + concrete `MainMenuState`/`SectorMapState` subclasses of `state/states.State` (the abstract base landed in step 5). Per umbrella `docs/specs/v0.1-model-layer.md` §4, this closes the controller-pivot surface for v0.1. Pre-execution: author a step-8 spec + plan following the same multi-round review discipline that worked for steps 6 and 7 (3-4 rounds typically converges).
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

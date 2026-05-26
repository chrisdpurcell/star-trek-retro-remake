# State

**Last updated:** 2026-05-26 (session closeout — step-8 spec ✅ + plan ✅ both cleared 2 Codex rounds each; execution pickup in new session)

## State at a glance

- v0.1 scaffold on `main` at HEAD `3ea4d1c` (CI on push last green at `14bc848` per step-7 implementation; HEADs `1390dee` and `3ea4d1c` are docs-only and do not affect CI status). Step 3 (`GridPosition` + `GameObject`) at `1d657bc`; step 4 (`view/scene/projection.py`) at `bcd07b4`; step 5 (`states.py` placeholder + `exceptions.py` + `events.py`) at `5420568`; step 6 (`sector_map.py` + `station.py`) at `8fe5f8b`; step 7 (`starship.py` + `turn_manager.py`) at `9898551`.
- **Step 8 SPEC ✅ + PLAN ✅ both CLEARED 2 Codex rounds each — awaiting execution in new session.** Committed artifacts: `docs/specs/v0.1-step-8-game-state-manager.md` (cleared at HEAD `1390dee`; 7/7 round-1 + 1/1 round-2 polish resolved); `docs/research/2026-05-26-v0.1-step-8-open-questions.md` (8 Q-locks, at `1390dee`); `docs/research/2026-05-26-v0.1-step-8-pre-review-research.md` (pre-Codex empirical verification — mypy 1.20.2 `--strict` confirmed clean on the post-class patch + SA-002 TYPE_CHECKING-import structure, at `1390dee`); `docs/superpowers/plans/2026-05-26-v0.1-step-8-implementation.md` (cleared at HEAD `3ea4d1c`; round-1: 2 blocking + 1 medium + 1 low — CR-001 Plan-tracking prerequisite added, CR-002 five piped pytest gates unpiped, CR-003 test_states.py count corrected 7→8/20→21, CR-004 Task 3 collection-error sequencing restructured; round-2: 0 findings, 0 regressions, verdict "audit/fix loop can stop"). **Umbrella sync `rg` gate** has three patterns, all three verified to hit exactly one line each in `docs/specs/v0.1-model-layer.md` at HEAD `1390dee`. **No code changes yet**; execution gated on the next session.
- **Pickup in new session:** open a new session; the SessionStart hook will inject this state file. Invoke `superpowers:subagent-driven-development`, point at `docs/superpowers/plans/2026-05-26-v0.1-step-8-implementation.md`, start with Task 1 (preflight + 21 OK-* scaffold checks + `git pull` per session ritual, no commits). Then T2-T5 produce ~5 commits total: T2 one commit for `states.py` extensions + 13 test rows; T3 one commit for `game_state_manager.py` + ~22 new tests + `state/__init__.py` re-exports landing atomically; T4 one commit for three umbrella amendments to `v0.1-model-layer.md` per spec §10; T5 three commits for index update + hash-fill dance + completed-plan neutralizer. Full validation gate at end of T5: `ruff format --check`, `ruff check`, `mypy --strict src/stmrr`, `lint-imports`, model-layer pytest with `--cov-reset --cov=stmrr.model --cov-fail-under=100`, full project pytest, three-pattern umbrella sync `rg` (3 hits pre / 0 hits post), no-Qt guard, invariant-10 guard. Estimated ~3 hours of focused subagent dispatch (vs step 7's ~4-6h). Per umbrella `docs/specs/v0.1-model-layer.md` §4, step 8 closes the controller-pivot surface for v0.1.
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

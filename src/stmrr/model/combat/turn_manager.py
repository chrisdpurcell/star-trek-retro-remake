"""TurnManager: turn-counter + orchestrator for the v0.1 End-Turn pipeline.

Per umbrella §5.4, AP lives on the entity (Starship.ap_remaining), NOT
here. TurnManager.advance_turn calls player.restore_ap(); it does NOT
debit AP, track NPC turn order, or own initiative. Those land at v0.2
when combat ships.

Runtime imports entities.starship for isinstance(player, Starship) in
advance_turn (umbrella §6 amended in step-7 §10); no back-edge —
Starship does not import turn_manager.

SA-001 lock (step-7 spec §5.3 + invariant 8): advance_turn is
type-and-presence verification only. Inactive (destroyed) player ships
SUCCEED at End Turn — AP restored, counter incremented, event emitted.
Umbrella §5.6.3 locks "Preconditions: none — End Turn is always
available." Game-over detection is the controller's job via state
transitions, not advance_turn refusing.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from stmrr.model.entities.starship import Starship
from stmrr.model.events import TurnAdvancedPayload, turn_advanced
from stmrr.model.exceptions import InactiveEntityError

if TYPE_CHECKING:
    from stmrr.model.entities.game_object import EntityId
    from stmrr.model.world.sector_map import SectorMap


class TurnManager:
    """Owns the turn counter; orchestrates per-turn restoration via the
    player Starship.

    Single-player v0.1: TurnManager carries one player_id. v0.2
    generalizes when NPC ships join the turn loop.

    Not a GameObject subclass — object.__init__ is side-effect-free,
    so no validate-before-super requirement (research [spec-assumptions
    §E]).
    """

    def __init__(self, player_id: EntityId, *, current_turn: int = 1) -> None:
        if not isinstance(player_id, int) or isinstance(player_id, bool):
            raise TypeError(f"player_id must be int, got {type(player_id).__name__}")
        if player_id < 1:
            raise ValueError(f"player_id must be >= 1, got {player_id}")

        if not isinstance(current_turn, int) or isinstance(current_turn, bool):
            raise TypeError(f"current_turn must be int, got {type(current_turn).__name__}")
        if current_turn < 1:
            raise ValueError(f"current_turn must be >= 1, got {current_turn}")

        self.player_id: EntityId = player_id
        self.current_turn: int = current_turn

    def advance_turn(self, sector_map: SectorMap) -> None:
        """End the current turn. Implements umbrella §5.6.3.

        Preconditions: none — End Turn is always available, including
        when the player ship is inactive (game-over state). SA-001 lock.

        Effects (umbrella invariant 9 — mutate → emit):
          1. Resolve player from sector_map.
          2. Type-and-presence check: None or non-Starship → raise
             InactiveEntityError. Does NOT check player.active.
          3. player.restore_ap() — runs even if player.active is False.
          4. self.current_turn += 1.
          5. Emit turn_advanced with payload.turn_number = NEW turn.

        Subscribers reading manager.current_turn or player.ap_remaining
        inside the handler see the new values.
        """
        player = sector_map.get(self.player_id)
        if player is None or not isinstance(player, Starship):
            raise InactiveEntityError(entity_id=self.player_id)

        player.restore_ap()
        self.current_turn += 1
        turn_advanced.send(
            self,
            payload=TurnAdvancedPayload(turn_number=self.current_turn),
        )


__all__ = ["TurnManager"]

from __future__ import annotations

from typing import TYPE_CHECKING

# see https://docs.python.org/3/library/typing.html#typing.TYPE_CHECKING
if TYPE_CHECKING:
    from engine import Engine
    from entity import Entity


class Action:
    def perform(self, scope_engine: Engine, doer_entity: Entity) -> None:
        """
        the Engine passed gives information about the scope that the action
        is being performed in. The Entity passed is the entity which performs
        the action.
        This method must be overridden by Action subclasses.
        """
        raise NotImplementedError()

class EscapeAction(Action):
    def perform(self, scope_engine: Engine, doer_entity: Entity) -> None:
        raise SystemExit()

class MovementAction(Action):
    def __init__(self, dx: int, dy: int):
        super().__init__()

        self.dx = dx
        self.dy = dy

    def perform(self, scope_engine: Engine, doer_entity: Entity) -> None:
        new_x = doer_entity.x + self.dx
        new_y = doer_entity.y + self.dy
        # the in-bounds check must come first before the tile array access
        if not scope_engine.game_map.in_bounds(new_x, new_y):
            return
        if not scope_engine.game_map.tiles["walkable"][new_x, new_y]:
            return
        # assuming the above checks were passed, we can now have the entity move
        doer_entity.move(dx=self.dx, dy=self.dy)

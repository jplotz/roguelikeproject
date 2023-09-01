from __future__ import annotations

from copy import deepcopy
from typing import Tuple, TypeVar, TYPE_CHECKING

if TYPE_CHECKING:
    from game_map import GameMap

T = TypeVar("T", bound="Entity")

class Entity:
    # players, monsters, items, etc.

    def __init__(self,
            x: int = 0,
            y: int = 0,
            char: str = " ",
            color: Tuple[int, int, int] = (255, 255, 255),
            name: str = "<Unnamed>",
            blocks_movement: bool = False,
            ):
        self.x = x
        self.y = y
        self.char = char
        self.color = color
        self.name = name
        self.blocks_movement = blocks_movement

    def spawn(self: T, game_map: GameMap, x: int, y: int) -> T:
        """Spawn a copy of this instance at the given location"""
        new_entity = deepcopy(self)
        new_entity.x, new_entity.y = (x, y)
        game_map.entities.add(new_entity)
        return new_entity

    def move(self, dx: int, dy: int) -> None:
        self.x += dx
        self.y += dy

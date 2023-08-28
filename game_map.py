from __future__ import annotations
from typing import Iterable, TYPE_CHECKING

import numpy as np
from tcod.console import Console

import tile_types

if TYPE_CHECKING:
    from entity import Entity

class GameMap:
    def __init__(self, width: int, height: int, entities: Iterable[Entity] = {}):
        self.width = width
        self.height = height

        self.entities = set(entities)

        self.tiles = np.full((width, height),
                fill_value=tile_types.wall,
                order="F")

        # currently in FOV (being seen)
        self.visible = np.full((width, height),
                fill_value=False,
                order="F")

        # not currently in FOV, but seen before
        # and remembered by player
        self.explored = np.full((width, height),
                fill_value=False,
                order="F")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def render(self, console: Console) -> None:
        """
        If a tile is visible, use the light colors.
        Else if a tile is not visible, but it has been explored (seen), use the dark colors.
        Otherwise, use the SHROUD, which is completely dark.
        """
        console.rgb[0:self.width, 0:self.height] = np.select(
                condlist=[self.visible, self.explored],
                choicelist=[self.tiles["light"], self.tiles["dark"]],
                default=tile_types.SHROUD
        )

        for entity in self.entities:
            if self.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)


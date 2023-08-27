import numpy as np
from tcod.console import Console

import tile_types

class GameMap:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

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

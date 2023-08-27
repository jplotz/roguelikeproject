from typing import Tuple

import numpy as np

graphic_dt = np.dtype(
        [
            ("ch", np.int32), # Unicode codepoint
            ("fg", "3B"),     # 3 unsigned bytes, for RGB color
            ("bg", "3B"),
        ]
)

tile_dt = np.dtype(
        [
            ("walkable", bool),
            ("transparent", bool),
            ("dark", graphic_dt),  # graphics for when tile not in FOV
            ("light", graphic_dt), # graphics for when tile IS in FOV
        ]
)

def new_tile(
        *, # force keyword arguments
        walkable: bool,
        transparent: bool,
        dark: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        light: Tuple[int, Tuple[int, int, int], Tuple[int, int, int]],
        ) -> np.ndarray:
    """
    Helper function for defining individual tile types
    """
    return np.array((walkable, transparent, dark, light), dtype=tile_dt)

SHROUD = np.array((ord(" "), (0, 0, 0), (0, 0, 0)), dtype=graphic_dt)

floor = new_tile(walkable=True,
        transparent=True,
        dark=(ord("."), (165, 201, 202), (0, 0, 0)),
        light=(ord("."), (231, 246, 242), (57, 91, 100))
        )

wall = new_tile(walkable=False,
        transparent=False,
        dark=(ord(" "), (0, 0, 0), (14, 21, 21)),
        light=(ord(" "), (0, 0, 0), (54, 61, 41))
        )

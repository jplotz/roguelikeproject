from __future__ import annotations

import random

from typing import Iterator, Tuple
from collections import namedtuple

import tcod

from game_map import GameMap
import tile_types


Point = namedtuple("Point", "x y")
PointRange = namedtuple("PointRange", "xslice yslice")

def average(a: int, b: int) -> int:
    return int(a/2 + b/2)


class RectangularRoom:
    def __init__(self, p: Point, width: int, height: int):
        self.p1 = p
        self.p2 = Point(x=p.x+width, y=p.y+height)

    @property
    def center(self) -> Point:
        center_x = average(self.p1.x, self.p2.x)
        center_y = average(self.p1.y, self.p2.y)

        return Point(x=center_x, y=center_y)

    @property
    def inner(self) -> PointRange:
        """
        Return inner area of this room as a 2d array index.
        """
        return PointRange(xslice=slice(self.p1.x+1, self.p2.x),
                yslice=slice(self.p1.y+1, self.p2.y))

    def intersects(self, other: RectangularRoom) -> bool:
        """
        Does this RectangularRoom overlap with another RectangularRoom?
        """
        return (self.p1.x <= other.p2.x and
               self.p2.x >= other.p1.x and
               self.p1.y <= other.p2.y and
               self.p2.y >= other.p1.y)
                


def tunnel_between(start: Point, end: Point) -> Iterator[Point]:
    if random.random() < 0.5: # 50% chance
        # Move horizontally, then vertically
        corner = Point(end.x, start.y)
    else:
        # Move vertically, then horizontally
        corner = Point(start.x, end.y)

    # Generate the coordinates for this tunnel
    for (x, y) in tcod.los.bresenham(start, corner).tolist():
        yield Point(x=x, y=y)
    for (x, y) in tcod.los.bresenham(corner, end).tolist():
        yield Point(x=x, y=y)

def generate_dungeon(
        max_rooms: int,
        room_min_size: int,
        room_max_size: int,
        map_width: int,
        map_height: int,
        player: Entity) -> GameMap:
    dungeon = GameMap(map_width, map_height)

    rooms: List[RectangularRoom] = []

    for r in range(max_rooms):
        room_width = random.randint(room_min_size, room_max_size)
        room_height = random.randint(room_min_size, room_max_size)

        p = Point(x=random.randint(0, dungeon.width - room_width - 1),
                  y=random.randint(0, dungeon.height - room_height - 1))

        new_room = RectangularRoom(p, room_width, room_height)

        if any(new_room.intersects(other_room) for other_room in rooms):
            continue

        dungeon.tiles[new_room.inner] = tile_types.floor

        if len(rooms) == 0:
            # if this is the first room that has been created, start the player
            # in that room
            player.x, player.y = new_room.center
        else:
            for (x, y) in tunnel_between(rooms[-1].center, new_room.center):
                dungeon.tiles[x, y] = tile_types.floor

        rooms.append(new_room)

    return dungeon

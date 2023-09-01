#!/usr/bin/env python3
import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler
from procgen import generate_dungeon


from entity import Entity
from game_map import GameMap
from engine import Engine

from copy import deepcopy
import entity_factories


def main() -> None:
    screen_width = 80
    screen_height = 24

    map_width = screen_width
    map_height = screen_height - 5

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    max_monsters_per_room = 2

    tilesheet_filename = "dejavu10x10_gs_tc.png"

    player = deepcopy(entity_factories.player)

    tileset = tcod.tileset.load_tilesheet(
            tilesheet_filename, 32, 8, tcod.tileset.CHARMAP_TCOD)

    event_handler = EventHandler()

    game_map = generate_dungeon(max_rooms,
            room_min_size,
            room_max_size,
            map_width,
            map_height,
            max_monsters_per_room,
            player)

    engine = Engine(
            event_handler=event_handler,
            game_map=game_map,
            player=player)

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="Game",
            vsync=True) as context:
        root_console = tcod.console.Console(screen_width,
                screen_height,
                order="F")

        while True:
            engine.handle_events(tcod.event.wait())
            engine.render(console=root_console, context=context)


if __name__ == "__main__":
    main()

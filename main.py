#!/usr/bin/env python3
import tcod

from actions import EscapeAction, MovementAction
from input_handlers import EventHandler

from entity import Entity
from game_map import GameMap
from engine import Engine


def main() -> None:
    screen_width = 80
    screen_height = 50

    map_width = 80
    map_height = 45

    tilesheet_filename = "dejavu10x10_gs_tc.png"

    player_x = int(screen_width / 2)
    player_y = int(screen_height / 2)

    player = Entity(player_x, player_y, char="@", color=(255, 255, 255))
    npc = Entity(player_x - 5, player_y, char="@", color=(255, 255, 0))

    entities = {npc, player}

    tileset = tcod.tileset.load_tilesheet(
            tilesheet_filename, 32, 8, tcod.tileset.CHARMAP_TCOD)

    event_handler = EventHandler()

    game_map = GameMap(map_width, map_height)

    engine = Engine(entities=entities, event_handler=event_handler, game_map=game_map, player=player)

    with tcod.context.new_terminal(
            screen_width,
            screen_height,
            tileset=tileset,
            title="LoserQuest",
            vsync=True) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")


        while True:
            engine.handle_events(tcod.event.wait())

            engine.render(console=root_console, context=context)

if __name__ == "__main__":
    main()

from typing import Set, Iterable, Any

from tcod.context import Context
from tcod.console import Console
from tcod.map import compute_fov

from entity import Entity
from input_handlers import EventHandler

from game_map import GameMap

# the Engine "handles" the events, which means that it makes use of an
# EventHandler to figure out the correct Action object, then calls the
# perform method of that object, with the current engine and player passed in.

# the Engine is also responsible for rendering all game elements (dungeon,
# terrain, player, monsters, npcs, etc. to the screen. The Engine does NOT
# render menus or status lines.

class Engine:
    def __init__(self, entities: Set[Entity],
            event_handler: EventHandler,
            game_map: GameMap,
            player: Entity):
        self.entities = entities
        self.event_handler = event_handler
        self.game_map = game_map
        self.player = player
        self.update_fov()

    def handle_events(self, events: Iterable[Any]) -> None:
        for event in events:
            action = self.event_handler.dispatch(event)

            if action is None:
                continue
            else:
                action.perform(scope_engine=self, doer_entity=self.player)
                self.update_fov()

    def update_fov(self) -> None:
        self.game_map.visible[:] = compute_fov(
                self.game_map.tiles["transparent"],
                (self.player.x, self.player.y),
                radius=8)

        # if the player can see a tile then they have explored it
        # "visible" tiles should be added to "explored"
        self.game_map.explored |= self.game_map.visible

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)

        for entity in self.entities:
            if self.game_map.visible[entity.x, entity.y]:
                console.print(entity.x, entity.y, entity.char, fg=entity.color)

        context.present(console)
        console.clear()

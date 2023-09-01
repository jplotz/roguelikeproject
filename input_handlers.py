from __future__ import annotations
import tcod.event

from actions import Action, EscapeAction, BumpAction

# Q: Why does it say tcod.event.EventDispatch[Action]? Why is the [Action]
# there?
# A: see https://python-tcod.readthedocs.io/en/latest/_modules/tcod/event.html#EventDispatch
# "The type hints at the return value of :any:`dispatch` and the `ev_*` methods"

class EventHandler(tcod.event.EventDispatch[Action]):
    """
    Inherits from EventDispatch class. This is how to use it:
    e = EventHandler()
    action = e.dispatch(event)
    if action is not None:
        action.perform(...)
    """
    def ev_quit(self, event: tcod.event.Quit) -> Action | None:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Action | None:
        action: Action | None = None

        key = event.sym

        if key == tcod.event.KeySym.UP:
            action = BumpAction(dx=0, dy=-1)
        elif key == tcod.event.KeySym.DOWN:
            action = BumpAction(dx=0, dy=1)
        elif key == tcod.event.KeySym.LEFT:
            action = BumpAction(dx=-1, dy=0)
        elif key == tcod.event.KeySym.RIGHT:
            action = BumpAction(dx=1, dy=0)

        elif key == tcod.event.KeySym.ESCAPE:
            action = EscapeAction()

        return action

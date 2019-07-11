import tcod.event
import tcod.event_constants as keys
from components.action import *


class InputStrategy:
    def __init__(self):
        pass

    def act(self, entity, world):
        return handle_input()


def handle_input():
    result = None

    while result is None:
        for event in tcod.event.wait():
            if event.type == 'QUIT':
                result = QuitAction()
            elif event.type == 'KEYDOWN':
                result = handle_keys(event)

    return result


def handle_keys(event):
    if event.sym == keys.K_UP:
        return move(0, -1)
    elif event.sym == keys.K_DOWN:
        return move(0, 1)
    elif event.sym == keys.K_LEFT:
        return move(-1, 0)
    elif event.sym == keys.K_RIGHT:
        return move(1, 0)
    elif event.sym == keys.K_RETURN and event.mod & tcod.event.KMOD_ALT:
        return FullscreenAction()
    elif event.sym == keys.K_ESCAPE:
        return QuitAction()

    return {}


def move(x, y):
    return MoveAction((x, y))

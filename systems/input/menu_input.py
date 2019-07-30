import logging

import esper
import tcod.event
import tcod.event_constants as keys

from states import State


class MenuInputSystem(esper.Processor):
    def __init__(self, game_state):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state

    def process(self):
        action = self.handle_input()

        if action["select"] != 0:
            selected = self.game.menu_selected + action["select"]
            if 0 <= selected < len(self.game.menus):
                self.game.menu_selected = selected
        elif action["activate"]:
            selected = self.game.menus[self.game.menu_selected]
            self.game.new_state = selected["state"]

    def handle_input(self):
        result = None

        while result is None:
            for event in tcod.event.wait():
                if event.type == "KEYDOWN":
                    result = self.handle_keys(event)
                elif event.type == "QUIT":
                    self.game.new_state = State.QUIT
                    result = response()

        return result

    def handle_keys(self, event):
        if event.sym == keys.K_UP:
            return response(select=-1)
        elif event.sym == keys.K_DOWN:
            return response(select=1)
        elif event.sym == keys.K_RETURN:
            return response(activate=True)

        return response()


def response(select=0, activate=False):
    return {"select": select, "activate": activate}

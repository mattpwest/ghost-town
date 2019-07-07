import esper
import tcod as libtcod

from components import Actor
from components.action import FullscreenAction, QuitAction, NoAction


class FreeActionsSystem(esper.Processor):
    def __init__(self, game_state):
        self.game_state = game_state

    def process(self):
        for entity, action in self.world.get_component(QuitAction):
            self.game_state['running'] = False

            self.world.remove_component(entity, QuitAction)

        for entity, action in self.world.get_component(FullscreenAction):
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            self.world.remove_component(entity, FullscreenAction)

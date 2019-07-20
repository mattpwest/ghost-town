import esper
import tcod as libtcod

from components import Actor
from components.action import FullscreenAction, QuitAction, NoAction


class FreeActionsSystem(esper.Processor):
    def __init__(self, game):
        self.game = game

    def process(self):
        for entity, action in self.world.get_component(QuitAction):
            self.game.running = False

            self.world.remove_component(entity, QuitAction)

        for entity, action in self.world.get_component(FullscreenAction):
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            self.world.remove_component(entity, FullscreenAction)

        for entity, (actor, action) in self.world.get_components(Actor, NoAction):
            actor.energy -= action.cost

            self.world.remove_component(entity, NoAction)

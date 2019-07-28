import logging

import esper
import tcod as libtcod

from components import Actor, LookAction, Player, Position, OpenInventoryAction
from components.action import FullscreenAction, QuitAction, NoAction
from states import State


class FreeActionsSystem(esper.Processor):
    def __init__(self, game_state, entity_factory):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.entity_factory = entity_factory

    def process(self):
        for entity, action in self.world.get_component(QuitAction):
            self.game.running = False

            self.world.remove_component(entity, QuitAction)

        for entity, action in self.world.get_component(FullscreenAction):
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

            self.world.remove_component(entity, FullscreenAction)

        for entity, (actor, action) in self.world.get_components(Actor, NoAction):
            self.log.debug("NoAction reduces %s's %s energy by %s", entity, actor.energy, action.cost)
            actor.energy -= action.cost

            self.world.remove_component(entity, NoAction)

        for entity, (actor, action) in self.world.get_components(Actor, LookAction):
            for player_entity, (position, player) in self.world.get_components(Position, Player):
                self.entity_factory.target(position.x, position.y)

            self.game.new_state = State.LOOK

            self.world.remove_component(entity, LookAction)

        for entity, action in self.world.get_component(OpenInventoryAction):
            self.game.new_state = State.INVENTORY

            self.world.remove_component(entity, OpenInventoryAction)

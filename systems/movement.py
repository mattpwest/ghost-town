import logging
import sys

import esper

from components import Tangible
from components.actor import Actor
from components.position import Position
from components.action import MoveAction


class MovementSystem(esper.Processor):
    def __init__(self, map):
        self.log = logging.getLogger("MovementSystem")
        self.log.setLevel(logging.INFO)

        self.map = map

    def process(self):
        for entity, (actor, position, action) in self.world.get_components(Actor, Position, MoveAction):
            target_x = position.x + action.delta[0]
            target_y = position.y + action.delta[1]

            self.log.debug("Moving (entity=" + str(entity) + ", x=" + str(target_x) + ", y=" + str(target_y) + ")")

            tile = self.map.tiles[target_x][target_y]
            tile_tangible = self.world.component_for_entity(tile, Tangible)

            if tile_tangible.blocks_physical:
                self.log.info("The rough wall is solid and unyielding.")
                return

            target = self.map.entities[target_x][target_y]
            if target is not None and self.world.component_for_entity(target, Tangible).blocks_physical:
                self.log.info("You kick the monster!")
            else:
                position.x = target_x
                position.y = target_y

            actor.energy -= action.cost
            self.world.remove_component(entity, MoveAction)

import logging

import esper

from components import Tangible, Fighter, Attack, Player, Possessor, Essence, Possession
from components.action import MoveAction
from components.actor import Actor
from components.position import Position


class MovementSystem(esper.Processor):
    def __init__(self, game_map, message_log):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.WARN)

        self.map = game_map
        self.messages = message_log

    def process(self):
        for entity, (actor, position, action, tangible) \
                in self.world.get_components(Actor, Position, MoveAction, Tangible):
            target_x = position.x + action.delta[0]
            target_y = position.y + action.delta[1]

            self.log.debug("Moving (entity=" + str(entity) + ", x=" + str(target_x) + ", y=" + str(target_y) + ")")

            tile = self.map.tiles[target_x][target_y]
            tile_tangible = self.world.component_for_entity(tile, Tangible)

            if tile_tangible.blocks_physical and tangible.blocks_physical:
                if self.world.has_component(entity, Player):
                    message = "The rough wall is solid and unyielding."
                    self.log.info(message)
                    self.messages.add(message)
                continue

            target = self.map.entities[target_x][target_y]
            if target is not None and self.world.component_for_entity(target, Tangible).blocks_physical:
                self.generate_attack(entity, target)
            else:
                self.map.entities[position.x][position.y] = None
                position.x = target_x
                position.y = target_y
                self.map.entities[position.x][position.y] = entity

            actor.energy -= action.cost
            self.world.remove_component(entity, MoveAction)

    def generate_attack(self, from_entity, to_entity):
        if self.world.has_component(from_entity, Fighter) and self.world.has_component(to_entity, Fighter):
            self.world.add_component(to_entity, Attack(from_entity))
        elif self.world.has_component(from_entity, Possessor) and self.world.has_component(to_entity, Essence):
            self.world.add_component(to_entity, Possession(from_entity))

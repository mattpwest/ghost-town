import logging

import esper

from components import NoAction, Optics, Position, Player, MoveAction, Creature, Actor


class BasicAiSystem(esper.Processor):
    def __init__(self, game_map):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

        self.game_map = game_map

    def process(self):
        target = None
        for player_entity, (position, player) in self.world.get_components(Position, Player):
            target = position

        for entity, (actor, optics, creature) in self.world.get_components(Actor, Optics, Creature):
            if actor.energy < actor.cost:
                continue

            self.log.debug("AI entity " + str(entity) + ":")

            if not optics.lit:
                self.log.debug("\tNot lit - do nothing.")
                self.world.add_component(entity, NoAction())
                continue

            if target is None:
                self.log.debug("\tNo target - do nothing.")
                self.world.add_component(entity, NoAction())
                continue

            action = self.basic_move(entity, target)
            self.world.add_component(entity, action)
            self.log.debug("\tAction: " + type(action).__name__)

    def basic_move(self, entity, target):
        position = self.world.component_for_entity(entity, Position)
        x_distance = target.x - position.x
        y_distance = target.y - position.y

        manhattan_distance = abs(x_distance) + abs(y_distance)
        if manhattan_distance == 1:
            return MoveAction((x_distance, y_distance))

        if abs(x_distance) > 0:
            dx = int(round(x_distance / abs(x_distance)))
            dy = 0
            if not self.game_map.is_blocked(position.x + dx, position.y + dy):
                return MoveAction((dx, dy))

        if abs(y_distance) > 0:
            dx = 0
            dy = int(round(y_distance / abs(y_distance)))
            if not self.game_map.is_blocked(position.x + dx, position.y + dy):
                return MoveAction((dx, dy))

        return NoAction()

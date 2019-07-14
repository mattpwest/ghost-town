import logging
import math

from components import NoAction, Optics, Position, Player, MoveAction


class AIStrategy:
    def __init__(self):
        self.log = logging.getLogger("AIStrategy")
        self.log.setLevel(logging.INFO)

    def act(self, entity, world, game_map):
        viewable = world.component_for_entity(entity, Optics)

        action = NoAction()
        if not viewable.lit:
            return action

        target = None
        for player_entity, (position, player) in world.get_components(Position, Player):
            target = position

        if target is None:
            return action

        action = self.basic_move(entity, world, game_map, target)

        return action

    def basic_move(self, entity, world, game_map, target):
        position = world.component_for_entity(entity, Position)
        x_distance = target.x - position.x
        y_distance = target.y - position.y

        manhattan_distance = abs(x_distance) + abs(y_distance)
        if manhattan_distance == 1:
            return MoveAction((x_distance, y_distance))

        if abs(x_distance) > 0:
            dx = int(round(x_distance / abs(x_distance)))
            dy = 0
            if not game_map.is_blocked(position.x + dx, position.y + dy):
                return MoveAction((dx, dy))

        if abs(y_distance) > 0:
            dx = 0
            dy = int(round(y_distance / abs(y_distance)))
            if not game_map.is_blocked(position.x + dx, position.y + dy):
                return MoveAction((dx, dy))

        return NoAction()

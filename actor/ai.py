import logging
import math

from components import NoAction, Viewable, Position, Player, MoveAction


class AIStrategy:
    def __init__(self):
        self.log = logging.getLogger("AIStrategy")
        self.log.setLevel(logging.INFO)

    def act(self, entity, world, game_map):
        viewable = world.component_for_entity(entity, Viewable)

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
        dx = target.x - position.x
        dy = target.y - position.y

        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance == 1:
            return MoveAction((dx, dy))

        dx = int(round(dx / distance))
        dy = 0 if dx > 0 else int(round(dy / distance))
        if not game_map.is_blocked(position.x + dx, position.y + dy):
            return MoveAction((dx, dy))

        dx = 0
        dy = int(round(dy / distance))
        if not game_map.is_blocked(position.x + dx, position.y + dy):
            return MoveAction((dx, dy))

        return NoAction()

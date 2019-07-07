import logging
import tcod as libtcod

import components as components
from actor import InputStrategy, AIStrategy


class EntityFactory:
    def __init__(self, world):
        self.world = world
    
    def player(self, x, y):
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('@', libtcod.turquoise),
            components.Tangible(True),
            components.Viewable(False),
            components.Actor(InputStrategy())
        )

    def orc(self, x, y):
        logging.debug("Adding orc at (" + str(x) + ", " + str(y) + ")")
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('o', libtcod.desaturated_green),
            components.Tangible(True),
            components.Viewable(False),
            components.Actor(AIStrategy())
        )

    def troll(self, x, y):
        logging.debug("Adding troll at (" + str(x) + ", " + str(y) + ")")
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('T', libtcod.darker_green),
            components.Tangible(True),
            components.Viewable(False),
            components.Actor(AIStrategy())
        )

    def wall(self, x, y):
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('#', libtcod.dark_gray),
            components.Tangible(True),
            components.Viewable(True)
        )
    
    def floor(self, x, y):
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('.', libtcod.dark_gray),
            components.Tangible(False),
            components.Viewable(False)
        )
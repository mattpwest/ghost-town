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
            components.Optics(transparent=True),
            components.Actor(InputStrategy()),
            components.Player(),
            components.Text('Matt', 'ghost', 'A creepy old ghost...'),
            components.Health(30),
            components.Fighter(5, 2),
            components.Inventory(5)
        )

    def orc(self, x, y):
        logging.debug("Adding orc at (" + str(x) + ", " + str(y) + ")")
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('o', libtcod.desaturated_green),
            components.Tangible(True),
            components.Optics(transparent=True),
            components.Actor(AIStrategy()),
            components.Creature(),
            components.Text('orc', description='A massive snarling orc'),
            components.Health(10),
            components.Fighter(3, 0)
        )

    def troll(self, x, y):
        logging.debug("Adding troll at (" + str(x) + ", " + str(y) + ")")
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('T', libtcod.darker_green),
            components.Tangible(True),
            components.Optics(transparent=True),
            components.Actor(AIStrategy()),
            components.Creature(),
            components.Text('troll', description='A slimy green troll'),
            components.Health(20),
            components.Fighter(5, 1)
        )

    def corpse(self, x, y, creature_type):
        logging.debug("Adding corpse at (" + str(x) + ", " + str(y) + ")")
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('%', libtcod.darker_red),
            components.Optics(transparent=True, lit=True),
            components.Item(),
            components.Text('corpse', description='A mutilated ' + creature_type + ' corpse.')
        )

    def wall(self, x, y):
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('#', libtcod.dark_gray),
            components.Tangible(True),
            components.Optics(transparent=False),
            components.Terrain()
        )
    
    def floor(self, x, y):
        return self.world.create_entity(
            components.Position(x, y),
            components.Render('.', libtcod.dark_gray),
            components.Tangible(False),
            components.Optics(transparent=True),
            components.Terrain()
        )
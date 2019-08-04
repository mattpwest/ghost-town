import logging
import tcod as libtcod

import components as components


class EntityFactory:
    def __init__(self, world):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.world = world
    
    def player(self, x, y):
        player = self.world.create_entity(
            components.Actor(initial=0),
            components.Position(x, y),
            components.Render("@", libtcod.turquoise),
            components.Tangible(False),
            components.Optics(transparent=True),
            components.Player(),
            components.Text("ghost", "a", "A creepy old ghost..."),
            components.Possessor(2.0),
            components.Essence(100),
            components.EssenceAbsorber(1, 10),
            components.EssenceDrain(0.1, 1000),
            components.Time()
        )

        return player

    def orc(self, x, y):
        self.log.debug("Adding orc at (" + str(x) + ", " + str(y) + ")")
        return self.world.create_entity(
            components.Actor(),
            components.Position(x, y),
            components.Render("o", libtcod.desaturated_green),
            components.Tangible(True),
            components.Optics(transparent=True),
            components.Creature(),
            components.Text("orc", description="A massive snarling orc"),
            components.Health(10),
            components.Fighter(3, 0),
            components.Essence(20),
            components.Time(),
            components.Inventory()
        )

    def troll(self, x, y):
        self.log.debug("Adding troll at (" + str(x) + ", " + str(y) + ")")
        return self.world.create_entity(
            components.Actor(),
            components.Position(x, y),
            components.Render("T", libtcod.darker_green),
            components.Tangible(True),
            components.Optics(transparent=True),
            components.Creature(),
            components.Text("troll", description="A slimy green troll"),
            components.Health(20),
            components.Fighter(5, 1),
            components.Essence(40),
            components.Time(),
            components.Inventory()
        )

    def corpse(self, x, y, creature_type):
        self.log.debug("Adding corpse at (" + str(x) + ", " + str(y) + ")")

        item = self.world.create_entity(
            components.Position(x, y),
            components.Render("%", libtcod.darker_red),
            components.Optics(transparent=True, lit=True),
            components.Item(),
            components.Text(
                noun=creature_type.lower() + " corpse",
                pronoun=pronoun_from_name(creature_type), 
                description="A mutilated " + creature_type + " corpse."
            )
        )

        drop_action = components.DropAction(item)
        self.world.add_component(item, drop_action)

        return item

    def potion_healing(self, x, y):
        self.log.debug("Adding healing potion at (" + str(x) + ", " + str(y) + ")")

        item = self.world.create_entity(
            components.Position(x, y),
            components.Render("!", libtcod.light_red),
            components.Optics(transparent=True, lit=True),
            components.Item(),
            components.Text(
                noun="healing potion",
                pronoun=pronoun_from_name("healing potion"),
                description="A bubbling red potion with miraculous healing powers."
            ),
            components.HealingEffect(hit_points=5, duration=3000, interval=1000)
        )

        drop_action = components.DropAction(item)
        self.world.add_component(item, drop_action)

        drink_action = components.DrinkAction(item)
        self.world.add_component(item, drink_action)

        throw_action = components.ThrowAction(item, distance=4)
        self.world.add_component(item, throw_action)

        return item

    def wall(self, x, y):
        return self.world.create_entity(
            components.Position(x, y),
            components.Render("#", libtcod.dark_gray),
            components.Tangible(True),
            components.Optics(transparent=False),
            components.Terrain(),
            components.Text("wall", "a", description="A smooth stone wall."),
            components.Essence(0),
        )
    
    def floor(self, x, y):
        return self.world.create_entity(
            components.Position(x, y),
            components.Render(".", libtcod.dark_gray),
            components.Tangible(False),
            components.Optics(transparent=True),
            components.Terrain(),
            components.Text("floor", "a", description="A smooth stone floor."),
            components.Essence(0),
        )

    def target(self, x, y):
        return self.world.create_entity(
            components.Position(x, y),
            components.Render("", color=libtcod.yellow),
            components.Target()
        )


vowels = ["a", "e", "i", "o", "u"]


def pronoun_from_name(creature_type):
    if creature_type is None or len(creature_type) == 0:
        return "a"

    first_char = creature_type.lower()[0]
    if first_char in vowels:
        return "an"
    else:
        return "a"

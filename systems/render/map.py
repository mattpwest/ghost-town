import logging

import esper
import tcod as libtcod

from components import Position, Render, Optics, Terrain, Creature, Player, Item
from systems.render.consoles import ConsoleLayer, ConsoleRect, ConsolePoint


class RenderMapSystem(esper.Processor):
    def __init__(self, config, consoles):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)
        self.log_draw = False

        self.config = config
        self.consoles = consoles

        self.consoles_map = ConsoleLayer(
            libtcod.console.Console(
                self.config.display.width,
                self.config.display.height - self.config.ui.height
            ),
            priority=1,
            name="map",
            from_rect=ConsoleRect(0, 0, self.config.display.width, self.config.display.height - self.config.ui.height),
            to_point=ConsolePoint(0, 0)
        )
        self.consoles.add_layer(self.consoles_map)

        self.log.debug("Initialized!")

    def process(self):
        self.clear_buffer()

        self.render_type_to_buffer(Terrain)
        self.render_type_to_buffer(Item)
        self.render_type_to_buffer(Creature)
        self.render_type_to_buffer(Player)

        if self.config.map.debug_position:
            self.render_debug()

    def render_type_to_buffer(self, entity_type):
        type_name = str(entity_type.__name__)
        self.log.debug("===== RENDERING MAP " + type_name + " =====")

        count = 0
        drew = 0
        for entity, (position, render, optics, unused_type) \
                in self.world.get_components(Position, Render, Optics, entity_type):
            drew += self.draw_entity(entity, position, render, optics)
            count += 1

        self.log.debug("Checked " + str(count) + " " + type_name + " - drew " + str(drew))

    def clear_buffer(self):
        self.consoles_map.console.clear()

    def draw_entity(self, entity, position, render, optics):
        if self.log_draw:
            self.log.debug("Drawing entity: " + str(entity) + " (x=" + str(position.x) + ", y=" + str(position.y) +
                           ", char=" + render.char + ", color=" + str(render.color) + ")")
        if optics.lit:
            self.draw(position, render.char, render.color)
            return 1
        elif optics.explored:
            self.draw(position, render.char, render.color * libtcod.Color(50, 50, 50))
            return 1

        return 0

    def draw(self, position, char, color):
        libtcod.console_set_default_foreground(self.consoles_map.console, color)
        libtcod.console_put_char(self.consoles_map.console, position.x, position.y, char, libtcod.BKGND_NONE)

    def clear(self, x, y):
        libtcod.console_put_char(self.consoles_map.console, x, y, ' ', libtcod.BKGND_NONE)

    def render_debug(self):
        top_left = Position(0, 0)
        top_right = Position(self.config.map.width - 1, 0)
        bottom_left = Position(0, self.config.map.height - 1)
        bottom_right = Position(self.config.map.width - 1, self.config.map.height - 1)

        self.draw(top_left, 'M', libtcod.red)
        self.draw(top_right, 'M', libtcod.red)
        self.draw(bottom_left, 'M', libtcod.red)
        self.draw(bottom_right, 'M', libtcod.red)

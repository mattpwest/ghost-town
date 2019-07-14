import logging

import esper
import tcod as libtcod

from components import Position, Render, Optics, Terrain, Creature, Player, Text, Health


class RenderMapSystem(esper.Processor):
    def __init__(self, config, state, world):
        self.log = logging.getLogger("RenderMapSystem")
        self.log.setLevel(logging.INFO)

        self.config = config
        self.state = state
        self.world = world

        self.state.consoles.map = libtcod.console.Console(
            self.config.display.width,
            self.config.display.height - self.config.ui.height
        )

        self.log.debug("RenderMapSystem initialized!")

    def process(self):
        self.clear_buffer()

        self.render_type_to_buffer(Terrain)
        self.render_type_to_buffer(Creature)
        self.render_type_to_buffer(Player)

        if self.config.map.debug_position:
            self.render_debug()

    def render_type_to_buffer(self, entity_type):
        for entity, (position, render, optics, type) \
                in self.world.get_components(Position, Render, Optics, entity_type):
            self.draw_entity(entity, position, render, optics)

    def clear_buffer(self):
        for y in range(0, self.state.consoles.map.height):
            for x in range(0, self.state.consoles.map.width):
                self.clear(x, y)

    def draw_entity(self, entity, position, render, optics):
        self.log.debug("Drawing entity: " + str(entity) + " (x=" + str(position.x) + ", y=" + str(position.y) +
                       ", char=" + render.char + ", color=" + str(render.color) + ")")
        if optics.lit:
            self.draw(position, render.char, render.color)
        elif optics.explored:
            self.draw(position, render.char, render.color * libtcod.Color(50, 50, 50))

    def draw(self, position, char, color):
        libtcod.console_set_default_foreground(self.state.consoles.map, color)
        libtcod.console_put_char(self.state.consoles.map, position.x, position.y, char, libtcod.BKGND_NONE)

    def clear(self, x, y):
        libtcod.console_put_char(self.state.consoles.map, x, y, ' ', libtcod.BKGND_NONE)

    def render_debug(self):
        top_left = Position(0, 0)
        top_right = Position(self.config.map.width - 1, 0)
        bottom_left = Position(0, self.config.map.height - 1)
        bottom_right = Position(self.config.map.width - 1, self.config.map.height - 1)

        self.draw(top_left, 'M', libtcod.red)
        self.draw(top_right, 'M', libtcod.red)
        self.draw(bottom_left, 'M', libtcod.red)
        self.draw(bottom_right, 'M', libtcod.red)

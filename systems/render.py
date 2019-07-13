import logging

import esper
import tcod as libtcod

from components import Position, Render, Viewable, Terrain, Creature, Player, Text, Health


class RenderSystem(esper.Processor):
    def __init__(self, world, screen_width, screen_height, renderer):
        self.world = world
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.log = logging.getLogger("RenderSystem")
        self.log.setLevel(logging.INFO)

        libtcod.console_set_custom_font('data/arial10x10.png', libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
        self.root = libtcod.console_init_root(screen_width, screen_height, 'Ghost Town', False, renderer, vsync=True)
        self.con = libtcod.console.Console(screen_width, screen_height)
        self.log.debug("RenderSystem initialized!")

    def process(self):
        self.render_type_to_buffer(Terrain)
        self.render_type_to_buffer(Creature)
        self.render_type_to_buffer(Player)

        self.render_ui()

        self.render_buffer_to_screen()

        self.clear_buffer()

    def render_type_to_buffer(self, entity_type):
        for entity, (position, render, viewable, type) \
                in self.world.get_components(Position, Render, Viewable, entity_type):
            self.draw_entity(entity, position, render, viewable)

    def render_ui(self):
        libtcod.console_set_default_foreground(self.con, libtcod.white)

        x = 1
        y = self.screen_height - 2
        align = libtcod.LEFT
        for entity, (text, health, player) in self.world.get_components(Text, Health, Player):
            self.draw_text('HP: {0:02}/{1:02}'.format(health.points, health.maximum), x, y, align)

    def render_buffer_to_screen(self):
        libtcod.console_blit(self.con, 0, 0, self.screen_width, self.screen_height, self.root, 0, 0)
        libtcod.console_flush()

    def clear_buffer(self):
        for entity, (position, render, viewable) in self.world.get_components(Position, Render, Viewable):
            if viewable.visible or viewable.explored:
                self.clear(position)

    def draw_entity(self, entity, position, render, viewable):
        self.log.debug("Drawing entity: " + str(entity) + " (x=" + str(position.x) + ", y=" + str(position.y) +
                       ", char=" + render.char + ", color=" + str(render.color) + ")")
        if viewable.lit:
            self.draw(position, render.char, render.color)

            viewable.explored = True
        elif viewable.explored:
            self.draw(position, render.char, render.color * libtcod.Color(50, 50, 50))

    def draw(self, position, char, color):
        libtcod.console_set_default_foreground(self.con, color)
        libtcod.console_put_char(self.con, position.x, position.y, char, libtcod.BKGND_NONE)

    def clear(self, position):
        libtcod.console_put_char(self.con, position.x, position.y, ' ', libtcod.BKGND_NONE)

    def draw_text(self, text, x, y, align):
        libtcod.console_print_ex(self.con, x, y, libtcod.BKGND_NONE, align, text)

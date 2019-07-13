import logging

import esper
import tcod as libtcod

from components import Player, Text, Health


class RenderUISystem(esper.Processor):
    def __init__(self, config, state, world):
        self.log = logging.getLogger("RenderUISystem")
        self.log.setLevel(logging.INFO)

        self.config = config
        self.state = state
        self.world = world

        self.state.consoles.ui = libtcod.console.Console(self.config.ui.width, self.config.ui.height)
        self.log.debug("RenderUISystem initialized!")

    def process(self):
        self.clear_buffer()
        self.render_ui()

        if self.config.ui.debug_position:
            self.render_debug()

    def render_ui(self):
        libtcod.console_set_default_foreground(self.state.consoles.ui, libtcod.white)

        x = 1
        y = self.config.ui.height - 2
        align = libtcod.LEFT
        for entity, (text, health, player) in self.world.get_components(Text, Health, Player):
            self.draw_text('HP: {0:02}/{1:02}'.format(health.points, health.maximum), x, y, align)

    def clear_buffer(self):
        for y in range(self.config.ui.height):
            for x in range(self.config.ui.width):
                libtcod.console_put_char(self.state.consoles.ui, x, y, ' ', libtcod.BKGND_NONE)

    def draw(self, x, y, char, color):
        libtcod.console_set_default_foreground(self.state.consoles.ui, color)
        libtcod.console_put_char(self.state.consoles.ui, x, y, char, libtcod.BKGND_NONE)

    def draw_text(self, text, x, y, align):
        libtcod.console_print_ex(self.state.consoles.ui, x, y, libtcod.BKGND_NONE, align, text)

    def render_debug(self):
        self.draw(0, 0, 'U', libtcod.red)
        self.draw(self.config.ui.width - 1, 0, 'U', libtcod.red)
        self.draw(0, self.config.ui.height - 1, 'U', libtcod.red)
        self.draw(self.config.ui.width - 1, self.config.ui.height - 1, 'U', libtcod.red)

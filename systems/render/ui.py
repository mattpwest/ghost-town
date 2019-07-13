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
        for entity, (text, health, player) in self.world.get_components(Text, Health, Player):
            self.draw_bar(x, y, 'HP', health.points, health.maximum, libtcod.light_red, libtcod.darker_red)

    def clear_buffer(self):
        libtcod.console_set_default_background(self.state.consoles.ui, libtcod.black)
        libtcod.console_clear(self.state.consoles.ui)

    def draw(self, x, y, char, color):
        libtcod.console_set_default_foreground(self.state.consoles.ui, color)
        libtcod.console_put_char(self.state.consoles.ui, x, y, char, libtcod.BKGND_NONE)

    def draw_text(self, text, x, y, align):
        libtcod.console_print_ex(self.state.consoles.ui, x, y, libtcod.BKGND_NONE, align, text)

    def draw_bar(self, x, y, name, value, maximum, bar_color, back_color):
        console = self.state.consoles.ui
        total_width = self.config.ui.bar_width

        bar_width = int(float(value) / maximum * total_width)

        libtcod.console_set_default_background(console, back_color)
        libtcod.console_rect(console, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

        libtcod.console_set_default_background(console, bar_color)
        if bar_width > 0:
            libtcod.console_rect(console, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

        libtcod.console_set_default_foreground(console, libtcod.white)
        libtcod.console_print_ex(console, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                                 '{0}: {1}/{2}'.format(name, value, maximum))

    def render_debug(self):
        self.draw(0, 0, 'U', libtcod.red)
        self.draw(self.config.ui.width - 1, 0, 'U', libtcod.red)
        self.draw(0, self.config.ui.height - 1, 'U', libtcod.red)
        self.draw(self.config.ui.width - 1, self.config.ui.height - 1, 'U', libtcod.red)

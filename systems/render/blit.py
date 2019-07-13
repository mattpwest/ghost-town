import logging

import esper
import tcod as libtcod


class RenderBlitSystem(esper.Processor):
    def __init__(self, config, render_state):
        self.log = logging.getLogger("RenderBlitSystem")
        self.log.setLevel(logging.INFO)

        self.config = config
        self.state = render_state

        font = 'data/' + config.display.font
        fullscreen = False

        libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_TCOD)
        self.state.consoles.root = libtcod.console_init_root(
            config.display.width,
            config.display.height,
            'Ghost Town',
            fullscreen,
            config.display.renderer,
            vsync=True
        )
        self.log.debug("Initialized TCOD graphics!")

    def process(self):
        self.render_buffers_to_screen()

    def render_buffers_to_screen(self):
        libtcod.console_blit(
            self.state.consoles.map,
            0,
            0,
            self.config.display.width,
            self.config.display.height - self.config.ui.height,
            self.state.consoles.root,
            0,
            0
        )

        libtcod.console_blit(
            self.state.consoles.ui,
            0,
            0,
            self.config.ui.width,
            self.config.ui.height,
            self.state.consoles.root,
            0,
            self.config.display.height - self.config.ui.height,
        )

        libtcod.console_flush()

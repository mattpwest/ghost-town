import logging

import esper
import tcod as libtcod


class RenderBlitSystem(esper.Processor):
    def __init__(self, config, consoles):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.config = config
        self.consoles = consoles

        font = 'data/' + self.config.display.font
        fullscreen = False

        libtcod.console_set_custom_font(font, libtcod.FONT_TYPE_GRAYSCALE | libtcod.FONT_LAYOUT_ASCII_INROW)
        self.consoles.root = libtcod.console_init_root(
            self.config.display.width,
            self.config.display.height,
            'Ghost Town',
            fullscreen,
            self.config.display.renderer,
            vsync=True
        )
        self.log.debug("Initialized TCOD graphics!")

    def process(self):
        self.render_buffers_to_screen()

    def render_buffers_to_screen(self):
        libtcod.console_blit(
            self.consoles.map,
            0,
            0,
            self.config.display.width,
            self.config.display.height - self.config.ui.height,
            self.consoles.root,
            0,
            0
        )

        libtcod.console_blit(
            self.consoles.ui,
            0,
            0,
            self.config.ui.width,
            self.config.ui.height,
            self.consoles.root,
            0,
            self.config.display.height - self.config.ui.height,
        )

        libtcod.console_blit(
            self.consoles.inventory,
            0,
            0,
            self.config.display.width,
            self.config.display.height,
            self.consoles.root,
            0,
            0,
        )

        libtcod.console_flush()

        self.log.debug("BLITTED consoles to screen.")

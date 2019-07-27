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
        for layer in self.consoles.layers_active:
            libtcod.console_blit(
                layer.console,
                layer.from_rect.x,
                layer.from_rect.y,
                layer.from_rect.width,
                layer.from_rect.height,
                self.consoles.root,
                layer.to_point.x,
                layer.to_point.y
            )

        libtcod.console_flush()

        self.log.debug("BLITTED consoles to screen.")

import logging
import time

import esper
import tcod as libtcod


class RenderFpsCounterSystem(esper.Processor):
    def __init__(self, consoles):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.average_fps = 60.0
        self.time_ms = time.time() * 1000
        self.consoles_ui = self.consoles_ui = consoles.layers["ui"]

        self.log.debug("Initialized!")

    def process(self):
        now = time.time() * 1000
        delta = now - self.time_ms
        self.time_ms = now

        fps = 1000 / float(delta)
        self.average_fps = (fps + self.average_fps) / 2.0

        fps_text = "FPS: {:.1f}".format(self.average_fps)
        self.draw_text(fps_text, 0, 0)

    def draw_text(self, text, x, y, align=libtcod.LEFT):
        libtcod.console_print_ex(self.consoles_ui.console, x, y, libtcod.BKGND_NONE, align, text)

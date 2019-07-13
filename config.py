import configparser
import tcod as libtcod


class Config:
    def __init__(self, filename):
        self.config = configparser.ConfigParser()
        self.config.read(filename)

        self.display = DisplayConfig(self.config['display'])
        self.ui = UIConfig(self.config['ui'])
        self.map = MapConfig(self.config['map'])
        self.vision = VisionConfig(self.config['vision'])


class DimensionConfig:
    def __init__(self, config):
        self.width = config.getint('width')
        self.height = config.getint('height')


class DisplayConfig(DimensionConfig):
    def __init__(self, config):
        DimensionConfig.__init__(self, config)

        self.font = config['font']

        self.renderer = libtcod.RENDERER_SDL2
        if config['renderer'] == 'GLSL':
            self.renderer = libtcod.RENDERER_GLSL
        elif config['renderer'] == 'OPENGL':
            self.renderer = libtcod.RENDERER_OPENGL
        elif config['renderer'] == 'OPENGL2':
            self.renderer = libtcod.RENDERER_OPENGL2
        elif config['renderer'] == 'SDL':
            self.renderer = libtcod.RENDERER_SDL
        elif config['renderer'] == 'SDL2':
            self.renderer = libtcod.RENDERER_SDL2


class UIConfig(DimensionConfig):
    def __init__(self, config):
        DimensionConfig.__init__(self, config)

        self.bar_width = config.getint('bar_width')
        self.debug_position = config.getboolean('debug_position')


class MapConfig(DimensionConfig):
    def __init__(self, config):
        DimensionConfig.__init__(self, config)

        self.max_rooms = config.getint('max_rooms')
        self.room_max_size = config.getint('room_max_size')
        self.room_min_size = config.getint('room_min_size')
        self.room_max_monsters = config.getint('room_max_monsters')
        self.debug_position = config.getboolean('debug_position')


class VisionConfig:
    def __init__(self, config):
        self.radius = config.getint('radius')
        self.light_walls = config.getboolean('light_walls')
        self.algorithm = config.getint('algorithm')

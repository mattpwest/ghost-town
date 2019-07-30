import logging
from enum import Enum, auto


class State(Enum):
    MENU = auto()
    GENERATE = auto()
    MAP = auto()
    DEAD = auto()
    LOOK = auto()
    INVENTORY = auto()
    QUIT = auto()
    NONE = auto()


class BaseState:
    def __init__(self, world, systems):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.DEBUG)

        self.world = world
        self.systems = systems

    @staticmethod
    def for_state():
        return State.NONE

    def on_enter(self, from_state):
        self.log.info("Entering " + type(self).__name__ + ":")

        len_systems = len(self.systems)
        for index in range(0, len_systems):
            priority = len_systems - index
            processor = self.systems[index]
            self.world.add_processor(processor, priority)
            self.log.debug("Added processor " + type(processor).__name__ + " at priority " + str(priority))

    def on_leave(self, to_state):
        for system in self.systems:
            self.world.remove_processor(type(system))

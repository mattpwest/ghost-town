import esper
import pinject

from config import Config
from entities import EntityFactory
from game_map import GameMap
from game_state import GameState
from messages import MessageLog


class RootModuleSpec(pinject.BindingSpec):
    def configure(self, bind):
        bind("game_map", to_class=GameMap)
        bind("game_state", to_class=GameState)
        bind("entity_factory", to_class=EntityFactory)
        bind("message_log", to_class=MessageLog)

    def provide_world(self):
        return esper.World()

    def provide_config(self):
        return Config('data/config.ini')

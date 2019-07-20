import logging

import esper

import systems as systems
from config import Config
from entities import EntityFactory
from game import Game
from game_map import GameMap
from messages import MessageLog
from states import MapState
from states.dead_state import DeadState


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
    logging.root.setLevel(logging.INFO)

    config = Config('data/config.ini')
    world = esper.World()
    factory = EntityFactory(world)
    messages = MessageLog()
    game_map = GameMap(config, world, factory)
    consoles = systems.Consoles()
    game = Game(config, factory, messages, game_map, consoles)

    game.map.generate_map()
    add_player(game.factory, game.map)

    # TODO: DI would be better for this
    render_map_system = systems.RenderMapSystem(game)
    render_ui_system = systems.RenderUISystem(game)
    render_blit_system = systems.RenderBlitSystem(game)
    vision_system = systems.VisionSystem(game)

    map_state = MapState(game, world, render_map_system, render_ui_system, render_blit_system, vision_system)
    dead_state = DeadState(game, world, render_map_system, render_ui_system, render_blit_system, vision_system)
    states = {
        map_state.for_state(): map_state,
        dead_state.for_state(): dead_state
    }

    while game.running:
        if game.new_state is not None and game.new_state != game.state:
            if game.state in states:
                states[game.state].on_leave()

            game.state = game.new_state
            game.new_state = None

            if game.state in states:
                states[game.state].on_enter()

        world.process()


def add_player(factory, game_map):
    x = game_map.rooms[0].center().x
    y = game_map.rooms[0].center().y
    player_entity = factory.player(x, y)
    game_map.entities[x][y] = player_entity


if __name__ == '__main__':
    main()

import logging

import esper

import systems as systems
from config import Config
from entities import EntityFactory
from game_map import GameMap
from messages import MessageLog


def main():
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
    logging.root.setLevel(logging.INFO)

    config = Config('data/config.ini')
    game_state = {'running': True}
    world = esper.World()
    factory = EntityFactory(world)
    messages = MessageLog()

    game_map = GameMap(config, world, factory)
    game_map.generate_map()
    game_state['map'] = game_map

    world.add_processor(systems.MovementSystem(game_map, messages), 10)
    world.add_processor(systems.FreeActionsSystem(game_state), 10)
    world.add_processor(systems.CombatSystem(messages), 9)
    world.add_processor(systems.DamageSystem(game_map, messages, factory), 8)
    world.add_processor(systems.VisionSystem(config), 6)

    render_state = systems.RenderState()
    world.add_processor(systems.RenderMapSystem(config, render_state, world), 5)
    world.add_processor(systems.RenderUISystem(config, render_state, world, messages), 4)
    world.add_processor(systems.RenderBlitSystem(config, render_state), 3)

    world.add_processor(systems.ActionSystem(game_state), 1)

    add_player(factory, game_map)

    while game_state['running']:
        world.process()


def add_player(factory, game_map):
    x = game_map.rooms[0].center().x
    y = game_map.rooms[0].center().y
    player_entity = factory.player(x, y)
    game_map.entities[x][y] = player_entity


if __name__ == '__main__':
    main()

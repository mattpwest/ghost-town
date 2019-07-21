import logging

import pinject

import systems
import states


from binding_specs import RootModuleSpec


class MainGame:
    def __init__(self, game_state, world, game_map, entity_factory,
                 map_state, dead_state, look_state):
        game_map.generate_map()
        self.add_player(entity_factory, game_map)

        game_states = {
            dead_state.for_state(): dead_state,
            look_state.for_state(): look_state,
            map_state.for_state(): map_state,
        }

        game = game_state
        while game.running:
            if game.new_state is not None and game.new_state != game.state:
                if game.state in game_states:
                    game_states[game.state].on_leave()

                game.state = game.new_state
                game.new_state = None

                if game.state in game_states:
                    game_states[game.state].on_enter()

            world.process()

    def add_player(self, factory, game_map):
        x = game_map.rooms[0].center().x
        y = game_map.rooms[0].center().y
        player_entity = factory.player(x, y)
        game_map.entities[x][y] = player_entity


def main():
    logging.basicConfig(format='%(asctime)s [ %(name)20s ]\t%(levelname)7s\t%(message)s')
    logging.root.setLevel(logging.INFO)

    obj_graph = pinject.new_object_graph(
        binding_specs=[RootModuleSpec()],
        modules=[systems, states]
    )

    obj_graph.provide(MainGame)


if __name__ == '__main__':
    main()

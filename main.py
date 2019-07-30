import logging

import pinject

import systems
import states

from binding_specs import RootModuleSpec


class MainGame:
    def __init__(
        self,
        game_state,
        world,
        menu_state,
        map_state,
        dead_state,
        look_state,
        inventory_state,
        quit_state,
        generate_state
    ):
        game_states = {
            menu_state.for_state(): menu_state,
            quit_state.for_state(): quit_state,
            generate_state.for_state(): generate_state,
            dead_state.for_state(): dead_state,
            look_state.for_state(): look_state,
            map_state.for_state(): map_state,
            inventory_state.for_state(): inventory_state,
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

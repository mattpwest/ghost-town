from states import BaseState, State


class DeadState(BaseState):
    def __init__(self, world, render_map_system, render_ui_system, render_blit_system, vision_system,
                 dead_input_system, free_actions_system, game_state, game_map):
        systems = [
            render_map_system,
            render_ui_system,
            render_blit_system,
            vision_system,
            dead_input_system,
            free_actions_system
        ]

        BaseState.__init__(self, world, systems)

        self.game = game_state
        self.map = game_map

    @staticmethod
    def for_state():
        return State.DEAD

    def on_enter(self, from_state):
        super().on_enter(from_state)

        self.game.new_game()

    def on_leave(self, to_state):
        super().on_leave(to_state)

        # TODO: Save a morgue file?

        self.map.clear()

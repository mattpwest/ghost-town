from states import BaseState, State


class DeadState(BaseState):
    def __init__(self, world, render_map_system, render_ui_system, render_blit_system, vision_system,
                 dead_input_system, free_actions_system):
        systems = [
            render_map_system,
            render_ui_system,
            render_blit_system,
            vision_system,
            dead_input_system,
            free_actions_system
        ]

        BaseState.__init__(self, world, systems)

    @staticmethod
    def for_state():
        return State.DEAD

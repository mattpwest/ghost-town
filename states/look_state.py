from states import BaseState, State


class LookState(BaseState):
    def __init__(self, world, render_map_system, render_ui_system, render_look_system, render_blit_system,
                 vision_system, target_input_system):
        systems = [
            render_map_system,
            render_ui_system,
            render_look_system,
            render_blit_system,
            vision_system,
            target_input_system
        ]

        BaseState.__init__(self, world, systems)

    @staticmethod
    def for_state():
        return State.LOOK

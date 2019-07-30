from states import BaseState, State


class GenerateState(BaseState):
    def __init__(self, world, render_blit_system, generate_map_system):
        systems = [
            render_blit_system,
            generate_map_system
        ]

        BaseState.__init__(self, world, systems)

    @staticmethod
    def for_state():
        return State.GENERATE

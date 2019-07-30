from states import BaseState, State


class LoadState(BaseState):
    def __init__(self, world, render_blit_system, load_system):
        systems = [
            render_blit_system,
            load_system
        ]

        BaseState.__init__(self, world, systems)

    @staticmethod
    def for_state():
        return State.LOAD

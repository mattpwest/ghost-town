from states import BaseState, State


class SaveState(BaseState):
    def __init__(self, world, render_blit_system, save_system):
        systems = [
            render_blit_system,
            save_system
        ]

        BaseState.__init__(self, world, systems)

    @staticmethod
    def for_state():
        return State.SAVE

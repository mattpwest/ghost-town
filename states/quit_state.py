from states import BaseState, State


class QuitState(BaseState):
    def __init__(self, world, render_blit_system, game_state):
        systems = [
            render_blit_system
        ]

        BaseState.__init__(self, world, systems)

        self.game = game_state

    @staticmethod
    def for_state():
        return State.QUIT

    def on_enter(self, from_state):
        super().on_enter(from_state)

        # TODO: Force-save game

        self.game.running = False

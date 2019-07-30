from states import BaseState, State


class MenuState(BaseState):
    def __init__(self, world, render_menu_system, render_blit_system, menu_input_system, consoles, game_state):
        systems = [
            render_menu_system,
            render_blit_system,
            menu_input_system
        ]

        BaseState.__init__(self, world, systems)

        self.consoles = consoles
        self.consoles_menu = consoles.layers["menu"]
        self.game = game_state

    @staticmethod
    def for_state():
        return State.MENU

    def on_enter(self, from_state):
        super().on_enter(from_state)

        self.consoles.enable_layer(self.consoles_menu)

    def on_leave(self, to_state):
        super().on_leave(to_state)

        self.consoles.disable_layer(self.consoles_menu)

        if to_state == State.GENERATE:
            self.game.resume_game()

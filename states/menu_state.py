from states import BaseState, State


class MenuState(BaseState):
    def __init__(self, world, render_menu_system, render_blit_system, menu_input_system, consoles):
        systems = [
            render_menu_system,
            render_blit_system,
            menu_input_system
        ]

        BaseState.__init__(self, world, systems)

        self.consoles = consoles
        self.consoles_menu = consoles.layers["menu"]

    @staticmethod
    def for_state():
        return State.MENU

    def on_enter(self):
        super().on_enter()

        self.consoles.enable_layer(self.consoles_menu)

    def on_leave(self):
        super().on_leave()

        self.consoles.disable_layer(self.consoles_menu)

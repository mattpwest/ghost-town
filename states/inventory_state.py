from states import BaseState, State


class InventoryState(BaseState):
    def __init__(self, world, render_map_system, render_ui_system, render_inventory_system, render_blit_system,
                 inventory_input_system, consoles):
        systems = [
            render_map_system,
            render_ui_system,
            render_inventory_system,
            render_blit_system,
            inventory_input_system
        ]

        BaseState.__init__(self, world, systems)
        self.consoles = consoles
        self.consoles_inventory = consoles.layers["inventory"]

    def on_enter(self):
        super().on_enter()

        self.consoles.enable_layer(self.consoles_inventory)

    def on_leave(self):
        super().on_leave()

        self.consoles.disable_layer(self.consoles_inventory)

    @staticmethod
    def for_state():
        return State.INVENTORY

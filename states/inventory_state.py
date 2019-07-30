from components import Inventory
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

    def on_enter(self, from_state):
        super().on_enter(from_state)

        self.consoles.enable_layer(self.consoles_inventory)

        for entity, inventory in self.world.get_component(Inventory):
            if len(inventory.items) > 0:
                inventory.selected = 0
            else:
                inventory.selected = 1

    def on_leave(self, to_state):
        super().on_leave(to_state)

        self.consoles.disable_layer(self.consoles_inventory)

    @staticmethod
    def for_state():
        return State.INVENTORY

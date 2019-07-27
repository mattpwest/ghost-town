from states import BaseState, State


class InventoryState(BaseState):
    def __init__(self, world, render_map_system, render_ui_system, render_inventory_system, render_blit_system,
                 inventory_input_system):
        systems = [
            render_map_system,
            render_ui_system,
            render_inventory_system,
            render_blit_system,
            inventory_input_system
        ]

        BaseState.__init__(self, world, systems)

    @staticmethod
    def for_state():
        return State.INVENTORY

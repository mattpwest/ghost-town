from states import State, BaseState


class MapState(BaseState):
    def __init__(self, world, action_system, movement_system, free_actions_system, inventory_system, vision_system,
                 combat_system, damage_system, render_map_system, render_ui_system, render_blit_system):
        systems = [
            action_system,
            movement_system,
            free_actions_system,
            inventory_system,
            vision_system,
            combat_system,
            damage_system,
            render_map_system,
            render_ui_system,
            render_blit_system
        ]

        BaseState.__init__(self, world, systems)

    @staticmethod
    def for_state():
        return State.MAP

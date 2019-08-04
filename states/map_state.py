from states import State, BaseState


class MapState(BaseState):
    def __init__(self, world, action_system, movement_system, free_actions_system, inventory_actions_system,
                 inventory_pickup_system, vision_system, combat_system, damage_system, render_map_system,
                 render_ui_system, render_blit_system, basic_ai_system, map_input_system, effects_system,
                 essence_absorption_system, essence_drain_system, possession_system):
        systems = [
            inventory_actions_system,  # Execute inventory actions immediately on re-entry into this state
            essence_drain_system,
            effects_system,
            render_map_system,
            render_ui_system,
            render_blit_system,
            action_system,
            map_input_system,
            basic_ai_system,
            movement_system,
            free_actions_system,
            inventory_pickup_system,
            essence_absorption_system,
            vision_system,
            combat_system,
            possession_system,
            damage_system
        ]

        BaseState.__init__(self, world, systems)

    @staticmethod
    def for_state():
        return State.MAP

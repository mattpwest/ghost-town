import systems
from states import State, BaseState


class MapState(BaseState):
    def __init__(self, game, world, render_map_system, render_ui_system, render_blit_system, vision_system):
        self.render_map_system = render_map_system
        self.render_ui_system = render_ui_system
        self.render_blit_system = render_blit_system
        self.vision_system = vision_system

        BaseState.__init__(self, game, world)

    def define_systems(self):
        return [
            systems.ActionSystem(self.game),
            systems.MovementSystem(self.game),
            systems.FreeActionsSystem(self.game),
            systems.InventorySystem(self.game),
            self.vision_system,
            systems.CombatSystem(self.game),
            systems.DamageSystem(self.game),
            self.render_map_system,
            self.render_ui_system,
            self.render_blit_system,
        ]

    @staticmethod
    def for_state():
        return State.MAP

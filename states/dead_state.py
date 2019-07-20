from states import BaseState, State


class DeadState(BaseState):
    def __init__(self, game, world, render_map_system, render_ui_system, render_blit_system, vision_system):
        self.render_map_system = render_map_system
        self.render_ui_system = render_ui_system
        self.render_blit_system = render_blit_system
        self.vision_system = vision_system

        BaseState.__init__(self, game, world)

    def define_systems(self):
        return [
            self.render_map_system,
            self.render_ui_system,
            self.render_blit_system,
            self.vision_system
            #systems.ActionSystem(self.game)
        ]

    @staticmethod
    def for_state():
        return State.DEAD

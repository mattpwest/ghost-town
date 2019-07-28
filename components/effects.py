class Effect:
    def __init__(self, duration=1):
        self.duration = duration


class HealingEffect(Effect):
    def __init__(self, hit_points, duration=1):
        Effect.__init__(self, duration)

        self.hit_points = hit_points

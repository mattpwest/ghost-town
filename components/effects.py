class Effect:
    def __init__(self, duration, interval=1000):
        self.time = 0
        self.duration = duration
        self.interval = interval


class HealingEffect(Effect):
    def __init__(self, hit_points, duration=1000, interval=1000):
        Effect.__init__(self, duration)

        self.hit_points = hit_points

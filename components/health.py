class Health:
    def __init__(self, points, maximum=None):
        self.points = points

        if maximum is not None and maximum >= points:
            self.maximum = maximum
        else:
            self.maximum = points

        # TODO: Consider splitting into HealthStats and CurrentHealth component - don't need to process healing
        #  systems on entities that are at max health

import logging

import esper

from components import Essence, Time, EssenceDrain


class EssenceDrainSystem(esper.Processor):
    def __init__(self, game_state, game_map):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.map = game_map

    def process(self):
        for entity, (essence, essence_drain, time) \
                in self.world.get_components(Essence, EssenceDrain, Time):

            if time.delta_time > 0:
                essence_drain.time_passed += time.delta_time

            if essence_drain.time_passed < essence_drain.frequency:
                continue

            essence_drain.time_passed -= essence_drain.frequency
            essence.value = max(0, essence.value - essence_drain.value)

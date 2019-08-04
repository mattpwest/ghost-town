import logging

import esper

from components import Essence, Time, EssenceDrain, Player
from states import State


class EssenceDrainSystem(esper.Processor):
    def __init__(self, game_state, message_log, config):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.messages = message_log
        self.config = config

    def process(self):
        for entity, (essence, essence_drain, time) \
                in self.world.get_components(Essence, EssenceDrain, Time):

            if time.delta_time > 0:
                essence_drain.time_passed += time.delta_time

            if essence_drain.time_passed < essence_drain.frequency:
                continue

            essence_drain.time_passed -= essence_drain.frequency
            essence.value = max(0, essence.value - essence_drain.value)

            if essence.value == 0 and self.world.has_component(entity, Player):
                self.messages.add("As the last of your essence drains away...", self.config.colors.message_critical)
                self.messages.add("Everything goes dark.", self.config.colors.message_critical)
                self.game.new_state = State.DEAD

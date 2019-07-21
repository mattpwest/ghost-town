import logging
import random

import esper

from components import Attack, Fighter, Damage, Text, Player


class CombatSystem(esper.Processor):
    def __init__(self, message_log):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.WARN)

        self.messages = message_log
        self.rng = random.Random()

    def process(self):
        for entity, (attack, fighter) in self.world.get_components(Attack, Fighter):
            attacker = self.world.component_for_entity(attack.from_entity, Fighter)
            defender = fighter

            max_damage = max(attacker.attack - defender.defence, 0)
            damage = self.rng.randint(0, max_damage)

            self.describe_attack(attack.from_entity, entity, damage, max_damage)

            self.world.add_component(entity, Damage(damage))
            self.world.remove_component(entity, Attack)

    def describe_attack(self, attacker, defender, damage, max_damage):
        text_attacker = self.world.component_for_entity(attacker, Text)
        text_defender = self.world.component_for_entity(defender, Text)

        if self.world.has_component(attacker, Player):
            subject = "You"
            verb = "kick"
            thing = "the " + text_defender.noun
        else:
            subject = "The " + text_attacker.noun
            verb = "kicks"
            thing = "the " + text_defender.noun

            if self.world.has_component(defender, Player):
                thing = "you"

        message = subject + " " + verb + " " + thing + " for " + str(damage) + " damage!"
        self.log.info(message)
        self.messages.add(message)

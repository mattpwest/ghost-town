import logging

import esper

from components import Position, Essence, EssenceAbsorber, Time


class EssenceAbsorptionSystem(esper.Processor):
    def __init__(self, game_state, game_map):
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.setLevel(logging.INFO)

        self.game = game_state
        self.map = game_map

    def process(self):
        for entity, (essence, essence_absorber, position, time) \
                in self.world.get_components(Essence, EssenceAbsorber, Position, Time):

            if time.delta_time > 0:
                essence_absorber.time_passed += time.delta_time

            if essence_absorber.time_passed >= essence_absorber.frequency:
                essence_absorber.time_passed -= essence_absorber.frequency
            else:
                continue

            for x in range(position.x - essence_absorber.range, position.x + essence_absorber.range + 1):
                for y in range(position.y - essence_absorber.range, position.y + essence_absorber.range + 1):
                    tile = self.map.tiles[x][y]
                    tile_essence = self.world.component_for_entity(tile, Essence)

                    amount = min(tile_essence.value, essence_absorber.strength)
                    tile_essence.value = max(0, tile_essence.value - amount)

                    while essence.value + amount > essence.maximum:
                        essence.maximum = essence.maximum * 2

                    essence.value += amount

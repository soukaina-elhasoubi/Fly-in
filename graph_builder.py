from zone_type import ZoneType
from zone_model import Zone
from connection import Connection
from typing import Dict, List


class GraphBuilder:

    def __init__(
        self,
        zones: List[Zone],
        connections: List[Connection],
    ) -> None:
        self.zones: List[Zone] = zones
        self.connections: List[Connection] = connections
        self.graph: Dict[str, List[tuple[str, int]]] = {}

    def build_graph(self) -> Dict[str, List[tuple[str, int]]]:
        for zone in self.zones:
            if zone.zone_type == ZoneType.BLOCKED:
                continue

            self.graph[zone.name] = []

            for conn in self.connections:
                if conn.zone1 == zone.name:
                    neighbor_zones = [
                        z for z in self.zones if z.name == conn.zone2
                    ]
                    travel_cost = self.get_zone_cost(neighbor_zones[0])

                    if travel_cost < 0:
                        continue
                    self.graph[zone.name].append((conn.zone2, travel_cost))

                elif conn.zone2 == zone.name:
                    neighbor_zones = [
                        z for z in self.zones if z.name == conn.zone1
                    ]
                    travel_cost = self.get_zone_cost(neighbor_zones[0])

                    if travel_cost < 0:
                        continue
                    self.graph[zone.name].append((conn.zone1, travel_cost))
        return self.graph

    @staticmethod
    def get_zone_cost(zone: Zone) -> int:
        if zone.zone_type == ZoneType.RESTRICTED:
            return 2
        elif zone.zone_type == ZoneType.BLOCKED:
            return -1
        else:
            return 1

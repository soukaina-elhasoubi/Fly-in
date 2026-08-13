from __future__ import annotations

from dataclasses import dataclass

from connection import Connection
from zone_model import Zone
from zone_type import ZoneType


@dataclass
class Path:
    zones: list[Zone]
    connections: list[Connection]
    total_cost: int

    @property
    def length(self) -> int:
        return len(self.zones) - 1

    @property
    def restricted_zone_count(self) -> int:
        return sum(
            zone.zone_type == ZoneType.RESTRICTED
            for zone in self.zones
        )

    @property
    def bottleneck(self) -> int:
        if not self.connections:
            return 0

        zone_capacity = min(
            zone.max_drones for zone in self.zones
        )
        link_capacity = min(
            connection.max_link_capacity
            for connection in self.connections
        )

        return min(zone_capacity, link_capacity)

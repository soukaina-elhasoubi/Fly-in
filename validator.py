from typing import Any, Dict, List, Tuple
from zone_model import Zone
from connection import Connection
from zone_type import ZoneRole, ZoneType


class Validator:
    def __init__(
        self,
        zones: List[Dict[str, Any]],
        connections: List[Dict[str, Any]],
        nb_drones: int
    ) -> None:
        self.zones: List[Dict[str, Any]] = zones
        self.conns: List[Dict[str, Any]] = connections
        self.nb_drones = nb_drones

        self.graph: Dict[str, List[Tuple[str, int]]] = {}
        self.start: Zone | None = None
        self.end: Zone | None = None

    def zones_obj(self) -> List[Zone]:
        zones = []
        for zone_data in self.zones:
            metadata = zone_data.get("meta_data", {})
            zone = Zone(
                name=zone_data["name"],
                x=zone_data["x"],
                y=zone_data["y"],
                color=metadata.get("color"),
                max_drones=int(metadata.get("max_drones", 1)),
                zone_type=(
                    ZoneType(metadata["zone"])
                    if metadata.get("zone") in ZoneType._value2member_map_
                    else ZoneType.NORMAL
                ),
                zone_role=(
                    ZoneRole(metadata["zone_role"])
                    if metadata.get("zone_role") in ZoneRole._value2member_map_
                    else ZoneRole.REGULAR
                ),
            )
            if zone_data["kind"] == "start_hub":
                self.start = zone
                zone.zone_role = ZoneRole.START
                zone.max_drones = self.nb_drones
            elif zone_data["kind"] == "end_hub":
                self.end = zone
                zone.zone_role = ZoneRole.END
                zone.max_drones = self.nb_drones

            zones.append(zone)
        return zones

    def connection_obj(self) -> List[Connection]:
        connections = []

        for connection_data in self.conns:
            metadata = connection_data.get("meta_data", {})
            zone1 = connection_data["zone1"]
            zone2 = connection_data["zone2"]
            connection = Connection(
                zone1=zone1,
                zone2=zone2,
                name=f"{zone1}-{zone2}",
                current_drones=[],
                max_link_capacity=int(metadata.get("max_link_capacity", 1))
            )
            connections.append(connection)
        return connections

from graph_builder import GraphBuilder
from typing import Dict, List, Optional, Tuple
from connection import Connection
from algo import Algo
from path import Path
from zone_model import Zone


class PathFinder:
    def __init__(
        self,
        zones: List[Zone],
        conns: List[Connection],
        start: Zone,
        end: Zone,
    ) -> None:
        self.zones: List[Zone] = zones
        self.conns: List[Connection] = conns
        self.start: Zone = start
        self.end: Zone = end
        self.graph: Dict[str, List[Tuple[str, int]]] = {}
        self.paths: List[List[Zone]] = []

    def load(self) -> None:
        gbuild = GraphBuilder(self.zones, self.conns)
        self.graph = gbuild.build_graph()

    def get_multiple_paths(self) -> List[List[Zone]]:
        self.load()

        algorithm = Algo(
            self.zones,
            self.graph,
        )

        all_paths: List[List[Tuple[str, int]]] = []

        algorithm.dfs(
            self.start.name,
            self.end.name,
            [(self.start.name, 0)],
            set(),
            all_paths
        )
        return self.sort_by_cost(all_paths)

    def get_zone_by_name(self, zone_name: str) -> Optional[Zone]:
        for zone in self.zones:
            if zone.name == zone_name:
                return zone
        return None

    def find_connection(
        self,
        zone_a: Zone,
        zone_b: Zone,
    ) -> Optional[Connection]:
        for connection in self.conns:
            left_matches = (
                connection.zone1 == zone_a.name
                and connection.zone2 == zone_b.name
            )
            right_matches = (
                connection.zone2 == zone_a.name
                and connection.zone1 == zone_b.name
            )
            if left_matches or right_matches:
                return connection
        return None

    def build_path_objects(
        self,
        path_cost_pairs: List[Tuple[List[Tuple[str, int]], int]],
    ) -> List[Path]:
        path_objects: List[Path] = []

        for path_list, total_cost in path_cost_pairs:
            zone_names = [name for name, _cost in path_list]
            zone_list: List[Zone] = []
            for zone_name in zone_names:
                zone = self.get_zone_by_name(zone_name)
                if zone is None:
                    raise ValueError(f"Unknown zone '{zone_name}' in path")
                zone_list.append(zone)

            connections: List[Connection] = []
            for current_zone, next_zone in zip(zone_list, zone_list[1:]):
                connection = self.find_connection(current_zone, next_zone)
                if connection is not None:
                    connections.append(connection)

            path_objects.append(
                Path(
                    zones=zone_list,
                    connections=connections,
                    total_cost=total_cost,
                )
            )

        return path_objects

    def sort_by_cost(
        self,
        all_paths: List[List[Tuple[str, int]]],
    ) -> List[List[Zone]]:
        path_cost_pairs: List[Tuple[List[Tuple[str, int]], int]] = []
        for path_list in all_paths:
            cost = 0
            for path_entry in path_list:
                cost += path_entry[1]
            path_cost_pairs.append((path_list, cost))

        sorted_pairs: List[Tuple[List[Tuple[str, int]], int]] = sorted(
            path_cost_pairs,
            key=lambda item: item[1]
        )

        path_objects = self.build_path_objects(sorted_pairs)
        zone_paths: List[List[Zone]] = []
        for path_object in path_objects:
            zone_paths.append(path_object.zones)
            if len(zone_paths) > 1:
                return [zone_paths[0], zone_paths[1]]
        return zone_paths

    def extract_path(
        self,
        old_path: List[List[Tuple[str, int]]],
    ) -> List[List[str]]:
        new_paths: List[List[str]] = []
        for path in old_path:
            lst: List[str] = []
            for item in path:
                lst.append(item[0])
            new_paths.append(lst)
        return new_paths

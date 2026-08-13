import pygame
from color import get_color
from connection import Connection
from zone_model import Zone
from typing import Dict, List, Union
import sys


class Visualizer:

    WINDOW_WIDTH = 1800
    WINDOW_HEIGHT = 900
    BACKGROUND_TOP = (18, 24, 38)
    BACKGROUND_BOTTOM = (43, 58, 90)
    ZONE_RADIUS = 30
    CONNECTION_WIDTH = 4
    LABEL_OFFSET = 52
    MARGIN = 90
    FRAME_TIME = 1000

    def __init__(
        self,
        zones: List[Zone],
        conns: List[Connection],
        frames: List[Dict[str, Union[Zone, Connection]]],
    ) -> None:
        pygame.init()
        pygame.display.set_caption("Fly-in Simulation")

        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        )

        self.zones: List[Zone] = zones
        self.conns = conns
        self.frames = frames
        self.zone_coords: Dict[str, tuple[int, int]] = {}
        self.compute_camera()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 18)
        self.info_font = pygame.font.SysFont(None, 22)
        self.title_font = pygame.font.SysFont(None, 26)
        self.current_frame = 0

    def get_zone_by_name(self, zone_name: str) -> Union[Zone, None]:
        for zone in self.zones:
            if zone.name == zone_name:
                return zone
        return None

    def compute_camera(self) -> None:
        self.min_x = min(z.x for z in self.zones)
        self.max_x = max(z.x for z in self.zones)
        self.min_y = min(z.y for z in self.zones)
        self.max_y = max(z.y for z in self.zones)

        usable_width = self.WINDOW_WIDTH - 2 * self.MARGIN
        usable_height = self.WINDOW_HEIGHT - 2 * self.MARGIN
        scale_x = usable_width / max(1, self.max_x - self.min_x)
        scale_y = usable_height / max(1, self.max_y - self.min_y)

        self.scale = min(scale_x, scale_y)

        map_width = (self.max_x - self.min_x) * self.scale
        map_height = (self.max_y - self.min_y) * self.scale

        self.offset_x = (self.WINDOW_WIDTH - map_width) / 2
        self.offset_y = (self.WINDOW_HEIGHT - map_height) / 2

    def world_to_screen(self, x: int, y: int) -> tuple[int, int]:
        screen_x = int((x - self.min_x) * self.scale + self.offset_x)
        screen_y = int((y - self.min_y) * self.scale + self.offset_y)
        return screen_x, screen_y

    def draw_background(self) -> None:
        for y in range(self.WINDOW_HEIGHT):
            ratio = y / max(1, self.WINDOW_HEIGHT)
            red = int(
                self.BACKGROUND_TOP[0]
                + (self.BACKGROUND_BOTTOM[0] - self.BACKGROUND_TOP[0]) * ratio
            )
            green = int(
                self.BACKGROUND_TOP[1]
                + (self.BACKGROUND_BOTTOM[1] - self.BACKGROUND_TOP[1]) * ratio
            )
            blue = int(
                self.BACKGROUND_TOP[2]
                + (self.BACKGROUND_BOTTOM[2] - self.BACKGROUND_TOP[2]) * ratio
            )
            pygame.draw.line(
                self.screen,
                (red, green, blue),
                (0, y),
                (self.WINDOW_WIDTH, y),
            )

    def draw_connections(self) -> None:
        for conn in self.conns:
            zone1 = self.get_zone_by_name(conn.zone1)
            zone2 = self.get_zone_by_name(conn.zone2)

            if zone1 is None or zone2 is None:
                continue

            x1, y1 = self.world_to_screen(zone1.x, zone1.y)
            x2, y2 = self.world_to_screen(zone2.x, zone2.y)

            pygame.draw.line(
                self.screen,
                (60, 74, 102),
                (x1 + 5, y1 + 6),
                (x2 + 5, y2 + 6),
                self.CONNECTION_WIDTH + 2,
            )
            pygame.draw.line(
                self.screen,
                (201, 214, 255),
                (x1, y1),
                (x2, y2),
                self.CONNECTION_WIDTH,
            )

    def draw_zones(self) -> None:
        for zone in self.zones:
            x, y = self.world_to_screen(zone.x, zone.y)
            self.zone_coords[zone.name] = (x, y)

            pygame.draw.circle(
                self.screen,
                (24, 30, 46),
                (x + 6, y + 8),
                self.ZONE_RADIUS + 4,
            )
            pygame.draw.circle(
                self.screen,
                get_color(zone.color),
                (x, y),
                self.ZONE_RADIUS,
            )
            pygame.draw.circle(
                self.screen,
                (247, 223, 255),
                (x, y),
                self.ZONE_RADIUS,
                2,
            )

            label = self.font.render(zone.name, True, (250, 250, 255))
            label_rect = label.get_rect(
                center=(x, y + self.ZONE_RADIUS + self.LABEL_OFFSET)
            )
            self.screen.blit(label, label_rect)

    def draw_drone(
        self,
        frame: Dict[str, Union[Zone, Connection]],
    ) -> None:
        for drone_id, location in frame.items():
            if isinstance(location, Zone):
                x, y = self.zone_coords[location.name]
            else:
                x1, y1 = self.zone_coords[location.zone1]
                x2, y2 = self.zone_coords[location.zone2]

                x = (x1 + x2) // 2
                y = (y1 + y2) // 2

            body_color = (255, 214, 102)
            wing_color = (170, 190, 255)
            shadow_color = (20, 24, 36)

            pygame.draw.ellipse(
                self.screen,
                shadow_color,
                (x - 12, y + 8, 24, 12),
            )

            pygame.draw.polygon(
                self.screen,
                wing_color,
                [
                    (x - 9, y - 2),
                    (x - 17, y + 5),
                    (x - 9, y + 10),
                ],
            )
            pygame.draw.polygon(
                self.screen,
                wing_color,
                [
                    (x + 9, y - 2),
                    (x + 17, y + 5),
                    (x + 9, y + 10),
                ],
            )

            pygame.draw.polygon(
                self.screen,
                body_color,
                [
                    (x - 8, y - 5),
                    (x, y - 12),
                    (x + 8, y - 5),
                    (x + 6, y + 8),
                    (x - 6, y + 8),
                ],
            )

            pygame.draw.circle(
                self.screen,
                (20, 20, 20),
                (x, y - 1),
                4,
            )
            pygame.draw.line(
                self.screen,
                (255, 255, 255),
                (x - 4, y + 1),
                (x + 4, y + 1),
                2,
            )

            drone_label = self.font.render(drone_id, True, (31, 24, 40))
            self.screen.blit(drone_label, (x + 12, y - 12))

    def draw_footer(self, frame_index: int) -> None:
        panel_height = 120
        panel_rect = pygame.Rect(
            0,
            self.WINDOW_HEIGHT - panel_height,
            self.WINDOW_WIDTH,
            panel_height,
        )
        pygame.draw.rect(self.screen, (18, 25, 40), panel_rect)
        pygame.draw.rect(self.screen, (121, 152, 255), panel_rect, 2)

        total_turns = max(1, len(self.frames))
        current_turn = min(frame_index + 1, total_turns)
        active_drones = len(self.frames[frame_index]) if self.frames else 0

        title = self.title_font.render(
            f"Turn {current_turn}/{total_turns}",
            True,
            (255, 255, 255),
        )
        self.screen.blit(title, (40, self.WINDOW_HEIGHT - 90))

        info_line = self.info_font.render(
            (
                f"Active drones: {active_drones} • Zones: {len(self.zones)} "
                f"• Connections: {len(self.conns)}"
            ),
            True,
            (223, 232, 255),
        )
        self.screen.blit(info_line, (40, self.WINDOW_HEIGHT - 55))

    def run(self) -> None:
        try:
            frame_index = 0
            last_update = pygame.time.get_ticks()
            running = True

            while running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                now = pygame.time.get_ticks()

                if (
                    now - last_update >= self.FRAME_TIME
                    and frame_index < len(self.frames) - 1
                ):
                    frame_index += 1
                    last_update = now

                self.draw_background()
                self.draw_connections()
                self.draw_zones()

                if self.frames:
                    self.draw_drone(self.frames[frame_index])
                    self.draw_footer(frame_index)

                pygame.display.flip()
                self.clock.tick(60)

            pygame.quit()
        except KeyboardInterrupt:
            sys.exit

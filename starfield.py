import math
import random

import pygame
from constants import SCREEN_HEIGHT, SCREEN_WIDTH, STAR_COUNT


class Starfield(pygame.sprite.Sprite):
    containers: pygame.sprite.Group

    def __init__(self, num_stars: int = STAR_COUNT) -> None:
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.time = 0.0
        self.stars = [
            {
                "pos": pygame.Vector2(
                    random.uniform(0, SCREEN_WIDTH), random.uniform(0, SCREEN_HEIGHT)
                ),
                "radius": random.choice([1, 1, 1, 2]),
                "brightness": random.uniform(110, 255),
                "twinkle_speed": random.uniform(1.0, 3.0),
                "twinkle_phase": random.uniform(0, math.tau),
            }
            for _ in range(num_stars)
        ]

    def update(self, dt: float) -> None:
        self.time += dt

    def draw(self, screen: pygame.Surface) -> None:
        for star in self.stars:
            twinkle = 0.5 + 0.5 * math.sin(
                self.time * star["twinkle_speed"] + star["twinkle_phase"]
            )
            level = int(star["brightness"] * (0.6 + 0.4 * twinkle))
            color = (level, level, level)
            pygame.draw.circle(screen, color, star["pos"], star["radius"])

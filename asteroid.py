import pygame
import random
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_COLOR, ASTEROID_OUTLINE_COLOR
from constants import ASTEROID_MIN_RADIUS
from logger import log_event


class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = random.uniform(0, 360)
        self.spin_speed = random.uniform(-40, 40)
        num_points = random.randint(8, 12)
        self.shape = [
            (
                (360 / num_points) * i + random.uniform(-10, 10),
                random.uniform(0.75, 1.0),
            )
            for i in range(num_points)
        ]

    def _polygon_points(self) -> list[pygame.Vector2]:
        points = []
        for angle_offset, radius_mult in self.shape:
            offset = pygame.Vector2(0, radius_mult * self.radius).rotate(
                angle_offset + self.rotation
            )
            points.append(self.position + offset)
        return points

    def draw(self, screen):
        points = self._polygon_points()
        pygame.draw.polygon(screen, ASTEROID_COLOR, points)
        pygame.draw.polygon(screen, ASTEROID_OUTLINE_COLOR, points, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rotation += self.spin_speed * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return

        random_angle = random.uniform(20, 50)
        log_event("asteroid_split")
        vel1 = self.velocity.rotate(random_angle) * 1.44
        vel2 = self.velocity.rotate(-random_angle) * 1.44
        new_radius = self.radius - ASTEROID_MIN_RADIUS

        a1 = Asteroid(self.position.x, self.position.y, new_radius)
        a2 = Asteroid(self.position.x, self.position.y, new_radius)
        a1.velocity = vel1
        a2.velocity = vel2

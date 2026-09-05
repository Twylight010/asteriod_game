import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS, SHOT_COLOR, SHOT_CORE_COLOR

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, SHOT_COLOR, self.position, self.radius)
        pygame.draw.circle(screen, SHOT_CORE_COLOR, self.position, self.radius / 2)

    def update(self, dt):
        self.position += self.velocity * dt

import pygame
from constants import PLAYER_RADIUS

# Base class for game objects
class CircleShape(pygame.sprite.Sprite):
    containers: tuple[pygame.sprite.Group, ...]

    def __init__(self, x: float, y: float, radius: float) -> None:
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(*self.containers)
        else:
            super().__init__()

        self.position: pygame.Vector2 = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.polygon(screen, "white", self.triangle())


    def update(self, dt: float) -> None:
        # must override
        pass

    def collides_with(self, other):
        radii_sum = self.radius + other.radius
        return self.position.distance_squared_to(other.position) <= radii_sum * radii_sum

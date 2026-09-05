import random

import pygame
from constants import PLAYER_RADIUS, PLAYER_TURN_SPEED, PLAYER_SPEED
from circleshape import CircleShape
from constants import PLAYER_SHOOT_COOLDOWN, PLAYER_SHOOT_SPEED
from constants import PLAYER_COLOR, PLAYER_OUTLINE_COLOR, FLAME_COLOR, FLAME_CORE_COLOR
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.timer = 0
        self.thrusting = False

    def triangle(self) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def flame(self, length_scale: float = 1.0) -> list[pygame.Vector2]:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        back_center = self.position - forward * self.radius
        flicker = self.radius * random.uniform(0.6, 1.2) * length_scale
        tip = back_center - forward * flicker
        return [
            back_center - right * 0.5 * length_scale,
            tip,
            back_center + right * 0.5 * length_scale,
        ]

    def rotate(self, dt: float) -> None:
            self.rotation += PLAYER_TURN_SPEED * dt

    def draw(self, screen: pygame.Surface) -> None:
        if self.thrusting:
            pygame.draw.polygon(screen, FLAME_COLOR, self.flame())
            pygame.draw.polygon(screen, FLAME_CORE_COLOR, self.flame(0.5))
        pygame.draw.polygon(screen, PLAYER_COLOR, self.triangle())
        pygame.draw.polygon(screen, PLAYER_OUTLINE_COLOR, self.triangle(), 2)

    def update(self, dt: float) -> None:
        keys = pygame.key.get_pressed()
        self.timer -= dt
        self.thrusting = False
        if keys[pygame.K_SPACE]:
            self.shoot()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_w]:
            self.move(dt)
            self.thrusting = True
        if keys[pygame.K_s]:
            self.move(-dt)

    def move(self, dt: float) -> None:
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt
        self.velocity = forward * PLAYER_SPEED

    def shoot(self) -> None:
        if self.timer <= 0:
            self.timer = PLAYER_SHOOT_COOLDOWN
            shot = Shot(self.position.x, self.position.y)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

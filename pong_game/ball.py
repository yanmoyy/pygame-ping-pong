from enum import Enum

import pygame

from constants import Game
from sprites import Circle


class BounceType(Enum):
    PADDLE = "paddle"
    WALL = "wall"


class Ball(Circle):
    def __init__(
        self,
        center: pygame.Vector2,
        velocity: pygame.Vector2,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(center, Game.BALL_RADIUS, *groups)
        self.velocity = velocity

    def update(self, dt: float):
        self.center += self.velocity * dt

    def bounce(self, normal: pygame.Vector2):
        self.velocity = self.velocity.reflect(normal)

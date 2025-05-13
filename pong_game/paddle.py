from enum import Enum
from typing import Tuple

import pygame

from constants import Game
from sprites import Rectangle


class Direction:
    LEFT = pygame.Vector2(-1, 0)
    RIGHT = pygame.Vector2(1, 0)
    UP = pygame.Vector2(0, -1)
    DOWN = pygame.Vector2(0, 1)


class Paddle(Rectangle):
    def __init__(
        self,
        center: Tuple[int, int],
        *groups: pygame.sprite.Group,
        is_player: bool,
    ) -> None:
        super().__init__(center, Game.PADDLE_WIDTH, Game.PADDLE_HEIGHT, *groups)
        self.is_player = is_player
        self.velocity = pygame.Vector2(0, 0)
        self.bouncing_ball = False

    def update(self, dt):
        self.make_velocity()
        self.center += self.velocity * dt

    def make_velocity(self):
        self.velocity = pygame.Vector2(0, 0)
        if self.is_player:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.move(Direction.UP)
            if keys[pygame.K_a]:
                self.move(Direction.LEFT)
            if keys[pygame.K_s]:
                self.move(Direction.DOWN)
            if keys[pygame.K_d]:
                self.move(Direction.RIGHT)
        if self.velocity != (0, 0):
            self.velocity.normalize()
        self.velocity *= Game.PADDLE_SPEED

    def move(self, direction: pygame.Vector2):
        match (direction):
            case Direction.LEFT:
                self.velocity += Direction.LEFT
            case Direction.RIGHT:
                self.velocity += Direction.RIGHT
            case Direction.UP:
                self.velocity += Direction.UP
            case Direction.DOWN:
                self.velocity += Direction.DOWN

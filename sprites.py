import math
from typing import Tuple

import pygame

from constants import Color


class Rectangle(pygame.sprite.Sprite):
    def __init__(
        self,
        center: Tuple[float, float],
        width: float,
        height: float,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.center = center
        self.width = width
        self.height = height
        self._rect = pygame.Rect(0, 0, width, height)
        self.color = Color.WHITE

    def draw(self, screen: pygame.Surface):
        self._rect.center = (int(self.center[0]), int(self.center[1]))
        pygame.draw.rect(screen, self.color, self._rect)

    @property
    def left(self):
        return self.center[0] - self.width / 2

    @property
    def right(self):
        return self.center[0] + self.width / 2

    @property
    def top(self):
        return self.center[1] - self.height / 2

    @property
    def bottom(self):
        return self.center[1] + self.height / 2

    def get_distance(self, x: float, y: float):
        closest_x = max(self.left, min(x, self.right))
        closest_y = max(self.top, min(y, self.bottom))
        return math.sqrt((x - closest_x) ** 2 + (y - closest_y) ** 2)

    def is_inside(self, x: float, y: float):
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def update(self, dt: float):
        pass


class Circle(pygame.sprite.Sprite):
    def __init__(
        self,
        center: pygame.Vector2,
        radius: float,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.center = center
        self.radius = radius
        self.color = Color.WHITE

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.color, self.center, self.radius)

    def update(self, dt: float):
        pass

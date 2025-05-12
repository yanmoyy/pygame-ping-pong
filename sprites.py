from typing import Tuple

import pygame

from constants import Color


class Rectangle(pygame.sprite.Sprite):
    def __init__(
        self,
        center: Tuple[int, int],
        width: float,
        height: float,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = center
        self.color = Color.WHITE

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)


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

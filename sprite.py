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

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, Color.WHITE, self.rect)


class Circle(pygame.sprite.Sprite):
    def __init__(
        self,
        center: Tuple[float, float],
        radius: float,
        *groups: pygame.sprite.Group,
    ) -> None:
        super().__init__(*groups)
        self.center = center
        self.radius = radius

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, Color.WHITE, self.center, self.radius)

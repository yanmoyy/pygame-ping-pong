import pygame
from pygame.sprite import Group

from constants import Color, Game, Screen
from pong_game.ball import Ball
from sprites import Rectangle


class Normal:
    LEFT_WALL = pygame.Vector2(1, 0)
    RIGHT_WALL = pygame.Vector2(-1, 0)
    TOP_WALL = pygame.Vector2(0, -1)
    BOTTOM_WALL = pygame.Vector2(0, 1)


class PongGame:
    def __init__(
        self,
        drawable: Group,
        updatable: Group,
        collidable: Group,
        width: float = Screen.WIDTH,
        height: float = Screen.HEIGHT,
    ) -> None:
        self.drawable = drawable
        self.updatable = updatable
        self.collidable = collidable

        self.width = width
        self.height = height

        self._init_objects()

    def update(self):
        self._ball_update()

    def _ball_update(self):
        x, y = self._ball.center
        radius = self._ball.radius
        if x - radius <= 0:
            self._ball.bounce(Normal.LEFT_WALL)
        if x + radius >= self.width:
            self._ball.bounce(Normal.RIGHT_WALL)
        if y + radius >= self.height:
            self._ball.bounce(Normal.TOP_WALL)
        if y - radius <= 0:
            self._ball.bounce(Normal.BOTTOM_WALL)

    def _get_collidable_groups(self):
        return (
            self.drawable,
            self.updatable,
            self.collidable,
        )

    def _init_objects(self):
        center_y = int(self.height // 2)
        center_x = int(self.width // 2)
        self._paddle1 = self._build_paddle(
            center_x=Game.PADDING,
            center_y=center_y,
        )
        self._paddle2 = self._build_paddle(
            center_x=int(self.width) - Game.PADDING,
            center_y=center_y,
        )
        self._ball = self._build_ball(center_x, center_y)
        self._set_players_color()

    def _build_paddle(self, center_x: int, center_y: int) -> Rectangle:
        return Rectangle(
            (center_x, center_y),
            Game.PADDLE_WIDTH,
            Game.PADDLE_HEIGHT,
            *self._get_collidable_groups(),
        )

    def _build_ball(self, center_x: float, center_y: float) -> Ball:
        return Ball(
            pygame.Vector2(center_x, center_y),
            pygame.Vector2(-Game.BALL_MIN_SPEED, 0),
            *self._get_collidable_groups(),
        )

    def _set_players_color(self):
        self._paddle1.color = Color.PLAYER_1_RED
        self._paddle2.color = Color.PLAYER_2_BLUE

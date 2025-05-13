import pygame
from pygame.sprite import Group

from constants import Color, Game, Screen
from pong_game.ball import Ball
from pong_game.paddle import Paddle
from sprites import Rectangle


class Normal:
    LEFT = pygame.Vector2(-1, 0)
    RIGHT = pygame.Vector2(1, 0)
    UP = pygame.Vector2(0, -1)
    DOWN = pygame.Vector2(0, 1)


class PongGame:
    def __init__(
        self,
        drawable: Group,
        updatable: Group,
        width: float = Screen.WIDTH,
        height: float = Screen.HEIGHT,
    ) -> None:
        self.drawable = drawable
        self.updatable = updatable

        self.width = width
        self.height = height

        self._init_objects()

    def update(self):
        self._ball_update()

    def _ball_update(self):
        self._ball_check_wall_collision()
        self._ball_check_paddle_collision(self._paddle1)
        # self._ball_check_rect_collision(self._paddle2)

    def _ball_check_wall_collision(self):
        x, y = self._ball.center
        velocity = self._ball.velocity
        radius = self._ball.radius
        if x - radius <= 0 and velocity.x < 0:
            self._ball.bounce(Normal.RIGHT)
        if x + radius >= self.width and velocity.x > 0:
            self._ball.bounce(Normal.LEFT)
        if y + radius >= self.height and velocity.y > 0:
            self._ball.bounce(Normal.UP)
        if y - radius <= 0 and velocity.y < 0:
            self._ball.bounce(Normal.DOWN)

    def _ball_check_paddle_collision(self, paddle: Paddle):
        """
        Collision Detection And Bounce the ball
        1. Check the distance
        2. if distance < radius : bounce!
        3. if ball center is inside the rect, throw to the opposite side!
        """
        x, y = self._ball.center
        radius = self._ball.radius
        distance = paddle.get_distance(x, y)
        if paddle.is_inside(x, y):
            distance = 0

        collision_detected = distance <= radius
        if collision_detected:  # collision detected
            if self._ball.is_bouncing:
                return
            self._ball.is_bouncing = True
            if distance == 0:
                self._ball.velocity *= -1
                return
            normal = pygame.Vector2(0, 0)
            if abs(x - paddle.left) <= radius:
                normal += Normal.LEFT
            if abs(x - paddle.right) <= radius:
                normal += Normal.RIGHT
            if abs(y - paddle.top) <= radius:
                normal += Normal.UP
            if abs(y - paddle.bottom) <= radius:
                normal += Normal.DOWN
            if normal != (0, 0):
                normal.normalize()
                self._ball.bounce(normal)
        else:
            if self._ball.is_bouncing:
                self._ball.is_bouncing = False

    def _get_updatable_group(self):
        return (
            self.drawable,
            self.updatable,
        )

    def _init_objects(self):
        center_y = int(self.height // 2)
        center_x = int(self.width // 2)
        self._paddle1 = self._build_paddle(
            center_x=Game.PADDING,
            center_y=center_y,
            is_player=True,
        )
        self._paddle2 = self._build_paddle(
            center_x=int(self.width) - Game.PADDING,
            center_y=center_y,
            is_player=False,
        )
        self._set_players_color()
        self._ball = self._build_ball(center_x, center_y)

    def _build_paddle(self, center_x: int, center_y: int, is_player: bool) -> Paddle:
        return Paddle(
            (center_x, center_y),
            *self._get_updatable_group(),
            is_player=is_player,
        )

    def _build_ball(self, center_x: float, center_y: float) -> Ball:
        return Ball(
            pygame.Vector2(center_x, center_y),
            pygame.Vector2(-Game.BALL_MIN_SPEED, Game.BALL_MIN_SPEED),
            *self._get_updatable_group(),
        )

    def _set_players_color(self):
        self._paddle1.color = Color.PLAYER_1_RED
        self._paddle2.color = Color.PLAYER_2_BLUE

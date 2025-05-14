import math

import pygame
from pygame.sprite import Group

from constants import Color, Game, Screen
from pong_game.ball import Ball
from pong_game.paddle import Paddle


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
        self.player1_score = 0
        self.player2_score = 0
        self.font = pygame.font.Font(None, 74)
        self.game_over = False
        self.winner = None
        self._ball_speed = Game.BALL_MIN_SPEED
        self._init_objects()

    def update(self):
        if not self.game_over:
            self._ball_update()
            self._check_score()
        else:
            self.handle_input()

    def draw(self, surface: pygame.Surface):
        # Draw court center line
        for y in range(0, int(self.height), 20):
            pygame.draw.rect(surface, Color.WHITE, (self.width / 2 - 2, y, 4, 10))

        # Draw scores
        score1_text = self.font.render(
            str(self.player1_score), True, Color.PLAYER_1_RED
        )
        score2_text = self.font.render(
            str(self.player2_score), True, Color.PLAYER_2_BLUE
        )
        surface.blit(score1_text, (self.width / 4, 50))
        surface.blit(score2_text, (3 * self.width / 4, 50))

        # Draw game over message if game is over
        if self.game_over:
            self._show_game_over_message(surface)

    def handle_input(self):
        """Handle input for resetting the game when game is over."""
        if self.game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self._reset_game()
                self.game_over = False
                self.winner = None

    def _ball_update(self):
        self._ball_check_wall_collision()
        self._ball_check_paddle_collision(self._paddle1)
        self._ball_check_paddle_collision(self._paddle2)

    def _ball_check_wall_collision(self):
        x, y = self._ball.center
        velocity = self._ball.velocity
        radius = self._ball.radius
        if x - radius <= 0 and velocity.x < 0:
            self.player2_score += 1
            self._reset_ball()
            self._reset_paddles()
        if x + radius >= self.width and velocity.x > 0:
            self.player1_score += 1
            self._reset_ball()
            self._reset_paddles()
        if y + radius >= self.height and velocity.y > 0:
            self._ball.bounce(Normal.UP)
        if y - radius <= 0 and velocity.y < 0:
            self._ball.bounce(Normal.DOWN)

    def _check_score(self):
        if self.player1_score >= Game.MAX_SCORE:
            self.game_over = True
            self.winner = "Player 1"
        elif self.player2_score >= Game.MAX_SCORE:
            self.game_over = True
            self.winner = "Player 2"
        if self.game_over:
            self._stop_ball()

    def _ball_check_paddle_collision(self, paddle: Paddle):
        """
        Collision Detection And Bounce the ball
        1. Check the distance
        2. if distance < radius : bounce!
        3. if ball center is inside the rect, throw to the opposite side!
        4. use bouncing_ball flag at paddle
        """
        x, y = self._ball.center
        radius = self._ball.radius
        distance = paddle.get_distance(x, y)
        if paddle.is_inside(x, y):
            distance = 0
        collision_detected = distance <= radius
        if collision_detected:  # collision detected
            if paddle.bouncing_ball:
                return
            paddle.bouncing_ball = True
            self._ball_increase_speed()
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
                if normal.x == 1 or normal.x == -1:
                    self._ball_modify_angle_by_position(
                        (y - paddle.top) / paddle.height, normal.x == 1
                    )
        else:
            if paddle.bouncing_ball:
                paddle.bouncing_ball = False

    def _ball_increase_speed(self):
        self._ball_speed += 30
        self._ball.velocity = self._ball.velocity.normalize() * self._ball_speed

    def _ball_modify_angle_by_position(self, hit_position: float, is_right: bool):
        """
        Adjust the ball's velocity angle based on hit position.
        - hit_position: 0 (top) to 1 (bottom)
        - is_right: True for rightward bounce (Player 1), False for leftward (Player 2)
        - Steps: Get current angle, add additional angle with sign constraint, clamp, apply
        """
        direction = 1 if is_right else -1

        current_angle = math.atan2(self._ball.velocity.y, self._ball.velocity.x)

        additional_angle = (hit_position - 0.5) * math.radians(60) * direction * 2
        new_angle = current_angle + additional_angle

        max_degree = 60
        if direction == 1:  # Player 1, rightward
            max_angle = math.radians(max_degree)  # 60°
            min_angle = -max_angle  # -60°
            if hit_position <= 0.5:  # Top: negative (right-up)
                if new_angle <= math.radians(0):
                    new_angle = max(min_angle, new_angle)
            else:  # Bottom: positive (right-down)
                if new_angle >= math.radians(0):
                    new_angle = min(max_angle, new_angle)  # [0°, 60°]
        else:  # Player 2, leftward
            if hit_position <= 0.5:  # (left-up)
                if new_angle > math.radians(-180):
                    max_angle = math.radians(-180 + max_degree)  # -120°
                    new_angle = min(max_angle, new_angle)
            else:  # Bottom: (left-down)
                if new_angle < math.radians(180):
                    min_angle = math.radians(180 - max_degree)  # 120°
                    new_angle = max(min_angle, new_angle)

        speed = self._ball_speed
        self._ball.velocity = (
            pygame.Vector2(math.cos(new_angle), math.sin(new_angle)) * speed
        )

    def _show_game_over_message(self, surface: pygame.Surface):
        """Display game over message with winner and reset instructions."""
        message = f"{self.winner} Wins! Press R to Restart"
        text = self.font.render(message, True, Color.WHITE)
        text_rect = text.get_rect(center=(self.width / 2, self.height / 2))
        surface.blit(text, text_rect)

    def _get_updatable_group(self):
        return (
            self.drawable,
            self.updatable,
        )

    def _init_objects(self):
        center_y = int(self.height // 2)
        center_x = int(self.width // 2)
        constraint_rect_width = self.width // 2 - 2 * Game.CONSTRAINT_PADDING
        paddle1_constraint = pygame.Rect(
            Game.CONSTRAINT_PADDING,
            0,
            constraint_rect_width,
            self.height,
        )
        paddle2_constraint = pygame.Rect(
            self.width // 2 + Game.CONSTRAINT_PADDING,
            0,
            constraint_rect_width,
            self.height,
        )
        self._paddle1 = self._build_paddle(
            Game.CONSTRAINT_PADDING + Game.PADDLE_WIDTH // 2,
            center_y,
            paddle1_constraint,
            player_id="1",
        )
        self._paddle2 = self._build_paddle(
            int(self.width) - Game.CONSTRAINT_PADDING - Game.PADDLE_WIDTH // 2,
            center_y,
            paddle2_constraint,
            player_id="2",
        )
        self._set_players_color()
        self._ball = self._build_ball(center_x, center_y)

    def _build_paddle(
        self,
        center_x: int,
        center_y: int,
        constraint_rect: pygame.Rect,
        player_id: str,
    ) -> Paddle:
        return Paddle(
            (center_x, center_y),
            constraint_rect,
            player_id,
            *self._get_updatable_group(),
        )

    def _build_ball(self, center_x: float, center_y: float) -> Ball:
        return Ball(
            pygame.Vector2(center_x, center_y),
            pygame.Vector2(-1, 1).normalize() * Game.BALL_MIN_SPEED,
            *self._get_updatable_group(),
        )

    def _set_players_color(self):
        self._paddle1.color = Color.PLAYER_1_RED
        self._paddle2.color = Color.PLAYER_2_BLUE

    def _reset_ball(self):
        center_x = self.width // 2
        center_y = self.height // 2
        self._ball.center = pygame.Vector2(center_x, center_y)
        self._ball.velocity = pygame.Vector2(-1, 1).normalize() * Game.BALL_MIN_SPEED
        self._ball_speed = Game.BALL_MIN_SPEED

    def _stop_ball(self):
        self._ball.velocity = pygame.Vector2(0, 0)

    def _reset_paddles(self):
        center_x = Game.CONSTRAINT_PADDING + Game.PADDLE_WIDTH // 2
        center_y = self.height / 2
        self._paddle1.center = pygame.Vector2(center_x, center_y)
        center_x = self.width - Game.CONSTRAINT_PADDING - Game.PADDLE_WIDTH // 2
        self._paddle2.center = pygame.Vector2(center_x, center_y)

    def _reset_game(self):
        self.player1_score = 0
        self.player2_score = 0
        self._reset_ball()
        self._reset_paddles()

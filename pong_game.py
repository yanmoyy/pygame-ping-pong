from pygame.sprite import Group

from constants import GameUI, Screen
from sprite import Circle, Rectangle


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

    def _get_collidable_groups(self):
        return (
            self.drawable,
            self.updatable,
            self.collidable,
        )

    def _init_objects(self):
        center_y = int(self.height // 2)
        center_x = int(self.width // 2)
        self.paddle1 = self._build_paddle(
            center_x=GameUI.PADDING,
            center_y=center_y,
        )
        self.paddle2 = self._build_paddle(
            center_x=int(self.width) - GameUI.PADDING,
            center_y=center_y,
        )
        self.ball = self._build_ball(center_x, center_y)

    def _build_paddle(self, center_x: int, center_y: int) -> Rectangle:
        return Rectangle(
            (center_x, center_y),
            GameUI.PADDLE_WIDTH,
            GameUI.PADDLE_HEIGHT,
            *self._get_collidable_groups(),
        )

    def _build_ball(self, center_x: float, center_y: float) -> Circle:
        return Circle(
            (center_x, center_y),
            GameUI.BALL_RADIUS,
            *self._get_collidable_groups(),
        )

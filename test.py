import unittest
from typing import cast

from pygame import Vector2
from pygame.sprite import Group

from pong_game.game import PongGame
from sprites import Circle


class TestGame(unittest.TestCase):
    def create_game(self):
        game = PongGame(Group(), Group(), Group())
        return game

    def test_update_ball(self):
        game = self.create_game()
        game._ball.velocity = Vector2(1, 1)
        cast(Circle, game._ball).center.y = game.height
        game._ball_update()
        self.assertEqual(
            game._ball.velocity,
            Vector2(1, -1),
        )


if __name__ == "__main__":
    unittest.main()

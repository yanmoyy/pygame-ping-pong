import pygame

from constants import Color, Screen
from pong_game.game import PongGame


def main():
    pygame.init()
    screen = pygame.display.set_mode((Screen.WIDTH, Screen.HEIGHT))

    clock = pygame.time.Clock()
    dt = 0
    running = True

    drawable = pygame.sprite.Group()
    updatable = pygame.sprite.Group()
    game = PongGame(drawable, updatable)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        game.update()

        updatable.update(dt)

        screen.fill(Color.BACK_GROUND_BLACK)

        for obj in drawable:
            obj.draw(screen)

        # flip() the display to put your work on screen
        pygame.display.flip()

        # limits FPS to 60
        dt = clock.tick(Screen.FPS) / 1000

    pygame.quit()


if __name__ == "__main__":
    main()

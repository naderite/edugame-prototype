# main_execution_file.py
import pygame
import sys

SCREENWIDTH, SCREENHEIGHT = 1280, 720
FPS = 60


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pygame.time.Clock()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
            self.clock.tick(FPS)


class Level:
    def __init__(self, display, gameStateManager) -> None:
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        self.display.fill("blue")


if __name__ == "__main__":
    game = Game()
    game.run()

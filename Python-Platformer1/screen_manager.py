# screen_manager.py

import pygame

pygame.init()

# Set up the game window
window = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("My Game")

screens = {}


def set_screen(screen_name):
    global screens

    # Handle screen transitions here
    if screen_name == "addition":
        import addition

        if "addition" not in screens:
            screens["addition"] = AdditionScreen(window)
        else:
            screens["addition"].reset()
        screens["addition"].run()
    elif screen_name == "main_level":
        import main_level

        if "main_level" not in screens:
            screens["main_level"] = MainLevelScreen(window)
        else:
            screens["main_level"].reset()
        screens["main_level"].run()

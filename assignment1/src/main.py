import pygame
from menus.MainMenu import MainMenu

""" Main function that initializes the game and runs the main menu.
"""


def main():
    pygame.init()

    screen_width, screen_height = 1250, 850
    screen = pygame.display.set_mode((screen_width, screen_height))

    main_menu = MainMenu(screen, screen_width, screen_height)
    main_menu.run()


""" Run the main function.
"""
if __name__ == "__main__":
    main()

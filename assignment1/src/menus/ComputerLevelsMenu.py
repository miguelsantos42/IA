import pygame
from .BaseMenu import BaseMenu
import GameController

class ComputerLevelsMenu(BaseMenu):
    """ Initializes the computer levels menu with UI elements for selecting difficulty levels.
        @param screen: The main game screen or surface where the menu will be drawn.
        @param screen_width: The width of the screen in pixels.
        @param screen_height: The height of the screen in pixels.
        @param mode: The game mode that determines the type of match (Player vs Computer, Computer vs Computer).
        @param board_size: The size of the game board, determining the number of rows and columns.
    """
    def __init__(self, screen, screen_width, screen_height, mode, board_size):
        super().__init__(screen, screen_width, screen_height, './imgs/computerLevels.png')
        self.mode = mode
        self.screen = screen
        self.levelB = 0
        self.levelR = 0
        self.button_blue = None
        self.button_red = None
        self.board_size = board_size

    """ Runs the computer levels menu, handling user input to select difficulty levels and start the game.
    """
    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(230, 325, 290, 71)  # posx, posy, largura, altura
            button_2 = pygame.Rect(230, 418, 290, 71)
            button_3 = pygame.Rect(230, 511, 290, 71)
            button_4 = pygame.Rect(230, 604, 290, 71)

            button_5 = pygame.Rect(725, 325, 290, 71)
            button_6 = pygame.Rect(725, 418, 290, 71)
            button_7 = pygame.Rect(725, 511, 290, 71)
            button_8 = pygame.Rect(725, 604, 290, 71)

            button_9 = pygame.Rect(70, 760, 250, 50)

            # buttons for computer BLUE levels
            if button_1.collidepoint((mx, my)):  # level 1
                if self.click:
                    self.levelB = 1
                    self.button_blue = button_1
            if button_2.collidepoint((mx, my)):  # level 2
                if self.click:
                    self.levelB = 2
                    self.button_blue = button_2
            if button_3.collidepoint((mx, my)):  # level 3
                if self.click:
                    self.levelB = 3
                    self.button_blue = button_3
            if button_4.collidepoint((mx, my)):  # level 4
                if self.click:
                    self.levelB = 4
                    self.button_blue = button_4

            # buttons for computer RED levels
            if button_5.collidepoint((mx, my)):  # level 1
                if self.click:
                    self.levelR = 1
                    self.button_red = button_5
            if button_6.collidepoint((mx, my)):  # level 2
                if self.click:
                    self.levelR = 2
                    self.button_red = button_6
            if button_7.collidepoint((mx, my)):  # level 3
                if self.click:
                    self.levelR = 3
                    self.button_red = button_7
            if button_8.collidepoint((mx, my)):  # level 4
                if self.click:
                    self.levelR = 4
                    self.button_red = button_8

            # Back button
            if button_9.collidepoint((mx, my)):
                if self.click:
                    running = False

            # if I click on the buttons, the levels are set to the selected level and a rectangle is drawn around the
            # selected level
            if self.button_blue is not None:
                pygame.draw.rect(self.screen, self.orange, self.button_blue, 5, border_radius=91)

            if self.button_red is not None:
                pygame.draw.rect(self.screen, self.orange, self.button_red, 5, border_radius=91)

            # if I click outside the buttons the levels are set to 0 and the rectangles are removed
            if not button_1.collidepoint((mx, my)) and not button_2.collidepoint((mx, my)) and not button_3.collidepoint((mx, my)) and not button_4.collidepoint((mx, my)) and not button_5.collidepoint((mx, my)) and not button_6.collidepoint((mx, my)) and not button_7.collidepoint((mx, my)) and not button_8.collidepoint((mx, my)):
                if self.click:
                    self.levelB = 0
                    self.button_blue = None
                    self.levelR = 0
                    self.button_red = None

            if self.levelB != 0 and self.levelR != 0:
                pygame.display.flip()
                self.start_game(self.mode, self.levelB, self.levelR)

            pygame.draw.rect(self.screen, self.orange, button_9)
            self.draw_text('Back', self.backColor, 90, 770)
            self.handle_events()
            self.update_display()

    """ Starts the game with the selected difficulty levels for the computer players.
        @param mode: The game mode to be used.
        @param difficulty1: The difficulty level for the first computer player.
        @param difficulty2: The difficulty level for the second computer player.
    """
    def start_game(self, mode, difficulty1, difficulty2):
        pygame.time.wait(1000)
        game = GameController.GameController(600, 600, self.board_size, mode, difficulty1, difficulty2)
        game.run()

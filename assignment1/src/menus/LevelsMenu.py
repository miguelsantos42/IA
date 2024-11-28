import pygame
from .BaseMenu import BaseMenu
import GameController


class LevelsMenu(BaseMenu):

    """ Initializes the levels menu with game settings and background.
        @param screen: The main game screen or surface where the menu will be drawn.
        @param screen_width: The width of the screen in pixels.
        @param screen_height: The height of the screen in pixels.
        @param mode: The game mode, determining how the game logic and interactions are handled.
        @param turn: Indicates who starts the game, the player or the computer.
        @param board_size: The size of the game board, determining the number of rows and columns.
    """
    def __init__(self, screen, screen_width, screen_height, mode, turn, board_size):
        super().__init__(screen, screen_width, screen_height, './imgs/difficultyLevels.png')
        self.mode = mode
        self.screen = screen
        self.turn = turn
        self.board_size = board_size
        self.button_clicked = None
        self.difficulty = 0

    """ Runs the levels menu, allowing the user to select a difficulty level for the game.
        Handles user input to select levels and start the game or go back to the previous menu.
    """
    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(450, 230, 355, 85)  # posx, posy, largura, altura
            button_2 = pygame.Rect(450, 357, 355, 85)
            button_3 = pygame.Rect(450, 485, 355, 85)
            button_4 = pygame.Rect(450, 612, 355, 85)
            button_5 = pygame.Rect(70, 760, 250, 50)

            if button_1.collidepoint((mx, my)):  # level 1
                if self.click:
                    self.button_clicked = button_1
                    self.difficulty = 1
            if button_2.collidepoint((mx, my)):  # level 2
                if self.click:
                    self.button_clicked = button_2
                    self.difficulty = 2
            if button_3.collidepoint((mx, my)):  # level 3
                if self.click:
                    self.button_clicked = button_3
                    self.difficulty = 3
            if button_4.collidepoint((mx, my)):  # level 4
                if self.click:
                    self.button_clicked = button_4
                    self.difficulty = 4
            if button_5.collidepoint((mx, my)):
                if self.click:
                    running = False

            pygame.draw.rect(self.screen, self.orange, button_5)
            self.draw_text('Back', self.backColor, 90, 770)

            if self.button_clicked is not None and self.difficulty > 0:
                pygame.draw.rect(self.screen, self.orange, self.button_clicked, 5, border_radius=91)
                pygame.display.flip()
                self.start_game(self.mode, self.difficulty, self.turn)

            self.handle_events()
            self.update_display()

    """ Starts a new game with the selected difficulty level.
        @param mode: The game mode, determining how the game logic and interactions are handled.
        @param difficulty: The difficulty level selected for the computer opponent.
        @param turn: Indicates who starts the game, the player or the computer.
    """
    def start_game(self, mode, difficulty, turn):
        pygame.time.wait(500)
        game = GameController.GameController(600, 600, self.board_size, mode, difficulty, None, turn)
        game.run()

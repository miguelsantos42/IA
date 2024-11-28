import pygame
from .BaseMenu import BaseMenu
import GameController


class PieceColorMenu(BaseMenu):
    """ Initializes the piece color selection menu with a background image and settings for the game's piece color selection menu.
        @param screen: The main game screen or surface where the menu will be drawn.
        @param screen_width: The width of the screen in pixels.
        @param screen_height: The height of the screen in pixels.
        @param board_size: The size of the game board, which is used to start a new game with the selected piece color.
    """
    def __init__(self, screen, screen_width, screen_height, board_size):
        super().__init__(screen, screen_width, screen_height, './imgs/selectColorMenu.png')
        self.red = (255, 0, 0)
        self.blue = (0, 0, 255)
        self.board_size = board_size
        self.button_clicked = None
        self.color_chosen = None

    """ Runs the piece color selection menu, displaying the menu options and handling user interactions.
    """
    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(449, 326, 355, 90)  # posx, posy, largura, altura
            button_2 = pygame.Rect(449, 475, 355, 90)
            button_4 = pygame.Rect(70, 760, 250, 50)

            if button_1.collidepoint((mx, my)):  # Start blue
                if self.click:
                    self.button_clicked = button_1
                    self.color_chosen = 'B'
            if button_2.collidepoint((mx, my)):  # Start red
                if self.click:
                    self.button_clicked = button_2
                    self.color_chosen = 'R'
            if button_4.collidepoint((mx, my)):
                if self.click:
                    running = False

            pygame.draw.rect(self.screen, self.orange, button_4)
            self.draw_text('Back', self.backColor, 90, 770)

            if not button_1.collidepoint((mx, my)) and not button_2.collidepoint((mx, my)):
                if self.click:
                    self.button_clicked = None
                    self.color_chosen = None

            if self.button_clicked is not None and self.color_chosen is not None:
                if self.color_chosen == 'B':
                    pygame.draw.rect(self.screen, self.blue, self.button_clicked, 5, border_radius=91)
                else:
                    pygame.draw.rect(self.screen, self.red, self.button_clicked, 5, border_radius=91)

                pygame.display.flip()
                self.start_game(1, None, self.color_chosen)

            self.handle_events()
            self.update_display()

    """ Starts a new game with the selected piece color.
        @param mode: The game mode, which is currently hardcoded to 1, implying a specific game mode.
        @param difficulty: Currently unused, placeholder for future game difficulty settings.
        @param turn: Indicates who starts the game, either 'B' for Blue or 'R' for Red.
    """
    def start_game(self, mode, difficulty, turn):
        pygame.time.wait(300)
        game = GameController.GameController(600, 600, self.board_size, mode, difficulty, None, turn)
        game.run()

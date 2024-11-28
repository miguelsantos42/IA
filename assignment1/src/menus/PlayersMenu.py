import pygame
from .BaseMenu import BaseMenu
from .ComputerLevelsMenu import ComputerLevelsMenu
from .PieceColorMenu import PieceColorMenu
from .PlayerComputerPieceChoice import PlayerComputerPieceChoice


class PlayersMenu(BaseMenu):
    """ Initializes the player menu with game settings and background.
        @param screen: The main game screen or surface where the menu will be drawn.
        @param screen_width: The width of the screen in pixels.
        @param screen_height: The height of the screen in pixels.
        @param board_size: The size of the game board, determining the number of rows and columns.
    """
    def __init__(self, screen, screen_width, screen_height, board_size):
        super().__init__(screen, screen_width, screen_height, './imgs/playersMenu.png')
        self.board_size = board_size
        self.button_clicked = None

    """ Runs the player menu, allowing the user to select the type of match to play.
    """
    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(448, 279, 355, 88)  # posx, posy, largura, altura
            button_2 = pygame.Rect(448, 426, 355, 88)
            button_3 = pygame.Rect(448, 576, 355, 88)
            button_4 = pygame.Rect(70, 760, 250, 50)

            if button_1.collidepoint((mx, my)):  # player vs player
                if self.click:
                    self.button_clicked = button_1
            if button_2.collidepoint((mx, my)):  # player vs computer
                if self.click:
                    self.button_clicked = button_2
            if button_3.collidepoint((mx, my)):  # computer vs computer
                if self.click:
                    self.button_clicked = button_3
            if button_4.collidepoint((mx, my)):
                if self.click:
                    running = False

            pygame.draw.rect(self.screen, self.orange, button_4)
            self.draw_text('Back', self.backColor, 90, 770)

            if not button_1.collidepoint((mx, my)) and not button_2.collidepoint(
                    (mx, my)) and not button_3.collidepoint((mx, my)):
                if self.click:
                    self.button_clicked = None

            if self.button_clicked is not None:
                pygame.draw.rect(self.screen, self.orange, self.button_clicked, 5, border_radius=91)
                pygame.display.flip()

                if self.button_clicked == button_1:
                    pygame.time.wait(200)
                    colors_menu = PieceColorMenu(self.screen, self.screen_width, self.screen_height, self.board_size)
                    colors_menu.run()

                elif self.button_clicked == button_2:
                    pygame.time.wait(200)
                    player_computer_menu = PlayerComputerPieceChoice(self.screen, self.screen_width, self.screen_height,
                                                                     self.board_size)
                    player_computer_menu.run()

                elif self.button_clicked == button_3:
                    pygame.time.wait(200)
                    computer_computer_menu = ComputerLevelsMenu(self.screen, self.screen_width, self.screen_height, 3,
                                                                self.board_size)
                    computer_computer_menu.run()

                self.button_clicked = None

            self.handle_events()
            self.update_display()

import pygame
from .BaseMenu import BaseMenu
from .PlayersMenu import PlayersMenu


class BoardSizeMenu(BaseMenu):
    """ Initializes the board size menu with a background image and settings.
        @param screen: The main game screen or surface where the menu will be drawn.
        @param screen_width: The width of the screen in pixels.
        @param screen_height: The height of the screen in pixels.
    """
    def __init__(self, screen, screen_width, screen_height):
        super().__init__(screen, screen_width, screen_height, './imgs/boardSize.png')
        self.screen = screen
        self.button_clicked = None
        self.board_chosen = 0

    """ Runs the board size menu, displaying the menu options and handling user interactions. 
    """
    def run(self):
        running = True
        while running:
            self.screen.blit(self.background_image, (0, 0))
            mx, my = pygame.mouse.get_pos()

            button_1 = pygame.Rect(449, 326, 355, 90)  # posx, posy, largura, altura
            button_2 = pygame.Rect(449, 475, 355, 90)
            button_4 = pygame.Rect(70, 760, 250, 50)

            if button_1.collidepoint((mx, my)):  # Board 8x8
                if self.click:
                    self.button_clicked = button_1
                    self.board_chosen = 8
            if button_2.collidepoint((mx, my)):  # Board 6x6
                if self.click:
                    self.button_clicked = button_2
                    self.board_chosen = 6
            if button_4.collidepoint((mx, my)):
                if self.click:
                    running = False

            pygame.draw.rect(self.screen, self.orange, button_4)
            self.draw_text('Back', self.backColor, 90, 770)

            # if I click outside the buttons the boards are set to 0 and the rectangles are removed
            if not button_1.collidepoint((mx, my)) and not button_2.collidepoint((mx, my)):
                if self.click:
                    self.button_clicked = None
                    self.board_chosen = 0

            if self.button_clicked is not None:
                pygame.draw.rect(self.screen, self.orange, self.button_clicked, 5, border_radius=91)
                pygame.display.flip()

                pygame.time.wait(200)

                players_menu = PlayersMenu(self.screen, self.screen_width, self.screen_height, self.board_chosen)
                players_menu.run()

                # after running deselect the button and set the board to 0
                self.button_clicked = None
                self.board_chosen = 0

            self.handle_events()
            self.update_display()

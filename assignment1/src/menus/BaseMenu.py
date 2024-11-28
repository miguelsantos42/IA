import pygame
import sys


class BaseMenu:

    """ Initializes the base menu with essential UI elements and settings.
        @param screen: The main game screen or surface where the menu will be drawn.
        @param screen_width: The width of the screen in pixels.
        @param screen_height: The height of the screen in pixels.
        @param background_image_path: Path to the background image file for the menu.
    """
    def __init__(self, screen, screen_width, screen_height, background_image_path):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.font = pygame.font.Font(None, 36)
        self.backColor = (255, 243, 228)
        self.yellow = (255, 190, 2)
        self.orange = (251, 90, 72)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.click = False
        self.background_image = pygame.image.load(background_image_path).convert()
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

    """ Draws text on the screen at a specified location with a specified color.
        @param text: The string of text to be displayed.
        @param color: The color of the text, given as an (R, G, B) tuple.
        @param x: The x-coordinate of the top-left corner where the text will be placed.
        @param y: The y-coordinate of the top-left corner where the text will be placed.
    """
    def draw_text(self, text, color, x, y):
        textobj = self.font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)

    """ Updates the entire screen to reflect any changes made to the surface.
    """
    def update_display(self):
        pygame.display.update()

    """ Handles events within the menu, including quitting the game and detecting mouse clicks.
    """
    def handle_events(self):
        self.click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.click = True

# mode: 1 - Player vs Player, 2 - Player vs Computer, 3 - Computer vs Computer
# difficulty: 1 - Easy, 2 - Medium, 3 - Hard, 4 - Expert
import random
import sys
import time

import pygame
from GameLogic import GameLogic
from GameView import GameView


class GameController:
    """ Initializes the game controller with settings for the game.
        @param width: The width of the game window in pixels.
        @param height: The height of the game window in pixels.
        @param board_size: The size of the game board (number of cells in width and height).
        @param mode: The game mode (1: Player vs Player, 2: Player vs Computer, 3: Computer vs Computer).
        @param difficulty1: The difficulty level for the first player (or only player in PvC mode).
        @param difficulty2: The difficulty level for the second player (in CvC mode).
        @param turn: The starting player ('B' for Blue, 'R' for Red).
    """
    def __init__(self, width, height, board_size=8, mode=None, difficulty1=None, difficulty2=None, turn='B'):
        self.width, self.height = width, height
        self.mode, self.difficulty1, self.difficulty2 = mode, difficulty1, difficulty2
        self.board_size = board_size
        self.game_logic = GameLogic(self.board_size, mode)
        self.game_view = GameView(self.game_logic, self.width, self.height)
        self.game_view.mode = mode
        self.game_view.difficulty1 = difficulty1
        self.game_view.difficulty2 = difficulty2
        self.clock = pygame.time.Clock()
        self.running = True
        self.game_ended = False
        self.valid_moves = []
        self.selected_piece = None
        self.placing_reserved = False
        self.winner = None
        self.last_move_time = time.time()
        self.display_hint = False
        self.current_hint = None
        self.hint_displayed = False
        self.game_logic.turn = turn

    """ Starts the game loop, handling game logic and rendering the game view.
    """
    def run(self):
        while self.running:
            current_time = time.time()
            if self.mode in [1, 2] and self.game_logic.player == 'human' and (current_time - self.last_move_time) >= 7:
                if not self.current_hint:
                    self.select_hint()
                    if not self.hint_displayed:  # Resize if hint not already displayed.
                        self.game_view.resize_window_for_hint(50)
                        self.hint_displayed = True
                self.display_hint = True
                self.game_view.display_hint(self.current_hint)
            else:
                if self.hint_displayed:  # Restore
                    self.game_view.restore_window_size()
                    self.hint_displayed = False
                self.display_hint = False

            self.render()
            self.game_logic.count_pieces()
            self.handle_events()
            self.update_game_state()
            self.game_logic.count_pieces()
            self.render()
            self.clock.tick(60)

        self.cleanup()

    """ Checks if the reserved button is clicked.
        @param mouse_pos: The position of the mouse click.
        @return: True if the reserved button is clicked, False otherwise.
    """
    def check_reserved_button(self, mouse_pos):
        if self.game_logic.player == 'computer':
            return False
        elif self.game_logic.player == 'human':
            if hasattr(self.game_view, 'button_rect') and self.game_view.button_rect.collidepoint(mouse_pos):
                if (self.game_logic.turn == 'B' and self.game_logic.blue_reserved > 0) or (
                        self.game_logic.turn == 'R' and self.game_logic.red_reserved > 0):
                    self.placing_reserved = True
                return True
        return False

    """ Handles all events captured by pygame, such as quitting the game or mouse clicks.
    """
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_ended:
                self.handle_mouse_click()

    """ Handles mouse click events within the game, determining actions based on game state and click location.
    """
    def handle_mouse_click(self):
        mouse_pos = pygame.mouse.get_pos()

        if self.check_reserved_button(mouse_pos):
            return

        row, col = self.get_cell_from_mouse_pos(mouse_pos)

        if self.placing_reserved:
            success = self.handle_reserved_placement(row, col)
            self.placing_reserved = False
            if success:
                self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
                self.current_hint = None
                self.last_move_time = time.time()
                self.hint_displayed = True
        else:
            # if clicked out of bounds or on an invalid piece, do nothing
            if row is None or col is None:
                return
            self.handle_piece_selection_or_movement(row, col)
            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)

    """ Handles the placement of a reserved piece onto the board.
        @param row: The row where the piece is to be placed.
        @param col: The column where the piece is to be placed.
        @return: True if the placement was successful, False otherwise.
    """
    def handle_reserved_placement(self, row, col):
        if row is not None and col is not None:
            success = self.game_logic.move_reserved_piece((row, col), self.game_logic.turn)
            if success:
                winner = self.game_logic.check_winner()
                if winner:
                    self.game_ended = True
                    self.winner = winner
                else:
                    self.game_logic.switch_turns()
            else:
                print("Invalid move")
            return success

    """ Handles the selection of a piece or the movement of a selected piece.
        @param row: The row of the selected or target cell.
        @param col: The column of the selected or target cell.
    """
    def handle_piece_selection_or_movement(self, row, col):
        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self.game_logic.move_stack(self.selected_piece, (row, col))
                self.selected_piece = None  # Deselect piece after moving
                self.valid_moves = []
                self.current_hint = None
                self.last_move_time = time.time()
                self.hint_displayed = True

                winner = self.game_logic.check_winner()
                if winner:
                    self.game_ended = True
                    self.winner = winner
                else:
                    self.game_logic.switch_turns()
            else:
                self.selected_piece = None
                self.valid_moves = []
        else:
            # Select a piece if it's the current player's turn and the piece belongs to them
            if (self.game_logic.board[row][col] != 'N' and
                    self.game_logic.board[row][col] != 'X' and
                    self.game_logic.turn == self.game_logic.board[row][col][-1]):
                self.selected_piece = (row, col)
                self.valid_moves = self.game_logic.get_valid_moves_for_position(row, col)

    """  Updates the game state, including checking for a winner and handling computer moves.
    """
    def update_game_state(self):

        if self.hint_displayed and self.game_logic.player == 'computer':  # Ensure hint is hidden when computer moves.
            self.current_hint = None
            self.hint_displayed = False
            self.game_view.restore_window_size()

        if self.mode == 2 and self.game_logic.player == 'computer':
            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
            self.handle_computer_move()
            self.last_move_time = time.time() # Reset timer after computer move

        elif self.mode == 3:
            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved)
            self.handle_computer_move()

        if not self.game_ended:
            self.check_for_winner()

    """ Handles the logic for computer moves, including determining moves based on the mode and difficulty settings.
    """
    def handle_computer_move(self):

        if self.mode == 2:
            self.game_logic.computer_move(self.mode, self.game_view, self.difficulty1, None)
        elif self.mode == 3:
            self.game_logic.computer_move(self.mode, self.game_view, self.difficulty1, self.difficulty2)

        pygame.time.delay(1000)
        self.game_logic.switch_turns()

    """ Checks if there's a winner and updates the game state accordingly.
    """
    def check_for_winner(self):
        self.winner = self.game_logic.check_winner()
        if self.winner:
            self.game_ended = True

    """ Renders the game view, including displaying the winner if the game has ended.
    """
    def render(self):
        if self.game_ended:
            if self.hint_displayed:
                self.game_view.restore_window_size()
                self.hint_displayed = False

            self.game_view.display_winner(self.winner)
            pygame.time.delay(3000)
            self.running = False
        else:
            if self.game_logic.player == 'computer':
                self.game_view.restore_window_size()
                self.hint_displayed = False

            hint_to_display = self.current_hint if self.display_hint else None
            if self.display_hint and not self.hint_displayed:
                self.game_view.resize_window_for_hint(50)  # Adjust for the hint height.
                self.hint_displayed = True
            elif not self.display_hint and self.hint_displayed:
                self.game_view.restore_window_size()
                self.hint_displayed = False

            self.game_view.draw_everything(self.valid_moves, self.selected_piece, self.placing_reserved,
                                           hint_to_display)

    """ Converts mouse position to cell coordinates on the board.
        @param mouse_pos: The position of the mouse click.
        @return: A tuple (row, col) representing the cell under the mouse. Returns (None, None) if outside the board.
    """
    def get_cell_from_mouse_pos(self, mouse_pos):
        cell_size = self.width // self.board_size
        x, y = mouse_pos

        if x < self.width and y < self.height:
            col = x // cell_size
            row = y // cell_size
            return row, col
        else:
            return None, None

    """ Selects a hint to display to the player.
    """
    def select_hint(self):
        hints = [
            "As the game nears its end, consider gathering reserve pieces. These are valuable and can lead to a win.",
            "Watch for stacks five pieces high under your opponent's control, with one of your pieces at the bottom. Adding one of your pieces on top lets you control the stack and earn a reserve piece.",
            "At the start of the game, aim to create many stacks that are two pieces high. Position these stacks two spaces apart in rows that meet, so you can easily combine them into a larger stack under your control.",
            "Avoid moving next to two or three of your opponent's single pieces. These are a threat because they're only one move away from taking over a stack."
        ]

        self.current_hint = random.choice(hints)

    """ Cleans up resources and exits the game.
    """
    def cleanup(self):
        if self.hint_displayed:
            self.game_view.restore_window_size()
        pygame.quit()
        sys.exit()

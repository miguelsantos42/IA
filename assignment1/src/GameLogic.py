import random
import pygame

from AI.MCTS import MCTS
from AI.MinimaxWithAlphaBeta import MinimaxWithAlphaBeta


class GameLogic:
    """ Initializes the game logic, including the board size and the starting state of the game.
        @param board_size: Size of the game board (e.g., 8 for a 8x8 board or 6 for a 6x6).
        @param mode: The game mode (1 for PvP, 2 for PvC, 3 for CvC).
    """
    def __init__(self, board_size, mode):
        self.board_size = board_size
        self.board = None
        self.initialize_board()
        self.turn = 'B'  # Blue player as default
        self.player = 'human'  # Human player as default
        self.mode = mode
        self.blue_reserved = 1
        self.red_reserved = 0
        self.blue_pieces = None
        self.red_pieces = None
        self.blue_captured = 0
        self.red_captured = 0

    """ Initializes the game board based on the predefined size. Sets up the starting positions of the pieces.
    """
    def initialize_board(self):
        if self.board_size == 8:

            # 8x8 board
            self.board = [
                ['N', 'N', 'X', 'X', 'X', 'X', 'N', 'N'],
                ['N', 'B', 'B', 'R', 'R', 'B', 'B', 'N'],
                ['X', 'R', 'R', 'B', 'B', 'R', 'R', 'X'],
                ['X', 'B', 'B', 'R', 'R', 'B', 'B', 'X'],
                ['X', 'R', 'R', 'B', 'B', 'R', 'R', 'X'],
                ['X', 'B', 'B', 'R', 'R', 'B', 'B', 'X'],
                ['N', 'R', 'R', 'B', 'B', 'R', 'R', 'N'],
                ['N', 'N', 'X', 'X', 'X', 'X', 'N', 'N']
            ]


        elif self.board_size == 6:

            self.board = [
                ['N', 'N', 'X', 'X', 'N', 'N'],
                ['N', 'R', 'R', 'B', 'B', 'N'],
                ['X', 'B', 'B', 'R', 'R', 'X'],
                ['X', 'R', 'R', 'B', 'B', 'X'],
                ['N', 'B', 'B', 'R', 'R', 'N'],
                ['N', 'N', 'X', 'X', 'N', 'N']
            ]


        self.count_pieces()

    """ Creates a deep copy of the current game state, including the board, turn, reserved pieces, and piece counts.
        @return: A new instance of GameLogic representing the current game state.
    """
    def copy(self):
        new_board = GameLogic(self.board_size, self.mode)
        new_board.board = [row.copy() for row in self.board]
        new_board.turn = self.turn
        new_board.blue_reserved = self.blue_reserved
        new_board.red_reserved = self.red_reserved
        new_board.blue_pieces = self.blue_pieces
        new_board.red_pieces = self.red_pieces
        return new_board

    """ Counts the total number of blue and red pieces on the board.
    """
    def count_pieces(self):
        self.blue_pieces = 0
        self.red_pieces = 0
        for row in self.board:
            for cell in row:
                if cell in ['N', 'X']:
                    continue
                self.blue_pieces += cell.count('B')
                self.red_pieces += cell.count('R')

    """ Checks if the game is over (i.e, a winner exists).
        @return: True if the game is over, False otherwise.
    """
    def check_gameover(self, mcts=False):
        return self.check_winner(mcts) is not None  # Game is over if there's a winner

    """ Determines the game result from the perspective of a specific player.
        @param player: The player ('B' or 'R') to check the result for.
        @return: 1 for a win, -1 for a loss, 0 for an ongoing game.
    """
    def get_result(self, player):
        winner = self.check_winner(mcts=True)  # Check the winner
        if winner == player:  # If the winner is the player
            return 1  # Win
        elif winner is None:
            return 0  # Game not done
        else:
            return -1  # Loss

    """ Checks if the game has a winner based on the current state of the board.
        @param mcts: Whether the check is being done for MCTS (doesn't take into account reserved pieces).
        @return: 'B' or 'R' if there's a winner, or None if the game is still ongoing.
    """
    def check_winner(self, mcts=False):

        top_pieces = {'B': False, 'R': False}  # Track presence of top pieces for both players
        can_move = {'B': False, 'R': False}  # Track if the player can move any pieces

        for row in range(self.board_size):
            for col in range(self.board_size):
                stack = self.board[row][col]

                if stack in ['N', 'X'] or not stack:
                    continue

                top_piece = stack[-1]  # top-most piece of the stack
                top_pieces[top_piece] = True  # If the top piece is 'B', set top_pieces['B'] to True and vice versa

                # Check if there are valid moves for the piece at this position
                if self.get_valid_moves_for_position(row, col):
                    can_move[top_piece] = True

        has_reserved = {'B': self.blue_reserved > 0, 'R': self.red_reserved > 0}

        if top_pieces['B'] and not top_pieces['R']:  # If only blue pieces are on top and no red pieces
            if mcts:  # don't count reserved for winning condition
                return 'B' if not can_move['R'] else None
            return 'B' if not has_reserved['R'] and not can_move['R'] else None
        elif top_pieces['R'] and not top_pieces['B']:
            if mcts:
                return 'R' if not can_move['B'] else None
            return 'R' if not has_reserved['B'] and not can_move['B'] else None
        return None

    """ Switches the turn from one player to the other. If the game is in PvC mode, the player is switched between
        human and computer.
    """
    def switch_turns(self):
        self.turn = 'B' if self.turn == 'R' else 'R'  # Switch turns between Blue and Red
        if self.mode == 1:
            self.player = 'human'
        elif self.mode == 3:
            self.player = 'computer'
        else:
            self.player = 'human' if self.player == 'computer' else 'computer'  # Switch player between human and computer

    """ Calculates all valid moves for a piece at a given position on the board.
        @param row: Row of the piece.
        @param col: Column of the piece.
        @return: A list of tuples representing valid move positions (row, col).
    """
    def get_valid_moves_for_position(self, row, col):
        stack = self.board[row][col]
        valid_moves = []

        num_pieces = len(stack)  # Number of pieces in the stack
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dr, dc in directions:  # Check each direction
            for i in range(1, num_pieces + 1):
                new_row, new_col = row + dr * i, col + dc * i
                if 0 <= new_row < self.board_size and 0 <= new_col < self.board_size:  # Check if new position is
                    # within bounds
                    if self.board[new_row][new_col] == 'N':
                        break
                    valid_moves.append((new_row, new_col))  # Add the move if the space is either empty ('X'),
                    # contains opponent's piece on top, or contains player's own pieces
                else:
                    break

        return valid_moves

    """ Determines all valid moves for the current player.
        @param player: The player ('B' for Blue, 'R' for Red) to calculate moves for.
        @return: A list of valid moves, where each move is a tuple (from_row, from_col, to_row, to_col).
    """
    def get_valid_moves_for_player(self, player):
        valid_moves = []
        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col][-1] == player:  # Check if the top piece belongs to the player
                    piece_valid_moves = self.get_valid_moves_for_position(row, col)
                    for to_row, to_col in piece_valid_moves:  # Add the valid moves for the piece
                        valid_moves.append((row, col, to_row, to_col))  # Add the move to the list of valid moves
        return valid_moves

    """ Updates the counts of pieces on the board and reserved pieces after a move.
        @param player: The player making the move ('B' or 'R').
        @param capture_count: The number of opponent pieces captured in the move.
        @param reserve_count: The number of pieces moved to reserve in the move.
    """
    def update_piece_counts(self, player, capture_count, reserve_count):
        if player == 'B':
            self.blue_reserved += reserve_count
            self.red_pieces -= capture_count
            self.red_captured += capture_count  # Increment the number of red pieces captured
        else:
            self.red_reserved += reserve_count
            self.blue_pieces -= capture_count
            self.blue_captured += capture_count  # Increment the number of blue pieces captured

    """ Calculates the distance between two positions on the board.
        @param from_pos: The starting position (row, col).
        @param to_pos: The ending position (row, col).
        @return: The distance as an integer.
    """
    def calculate_distance(self, from_pos, to_pos):
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        return abs(to_row - from_row) + abs(to_col - from_col)

    """ Handles the logic for moving a stack of pieces from one position to another.
        @param from_pos: The starting position of the move (row, col), or None for a reserved move.
        @param to_pos: The ending position of the move (row, col).
        @param player: The player ('B' or 'R') making the move.
        @param moving_pieces: The pieces being moved.
        @param distance: Optional. The distance of the move, used to limit the number of pieces moved.
        @return: A tuple (capture_count, reserve_count) representing the number of pieces captured and reserved.
    """
    def move_logic(self, from_pos, to_pos, player, moving_pieces, distance=None):
        to_row, to_col = to_pos

        if distance:
            moving_pieces = moving_pieces[-distance:] if len(moving_pieces) > distance else moving_pieces

        destination_stack = self.board[to_row][to_col] if self.board[to_row][to_col] != 'X' else ""
        final_stack = destination_stack + moving_pieces

        if len(final_stack) > 5:
            excess_pieces = final_stack[:len(final_stack) - 5]
            final_stack = final_stack[-5:]
        else:
            excess_pieces = ""

        capture_count = sum(1 for piece in excess_pieces if piece != player)
        reserve_count = len(excess_pieces) - capture_count

        if from_pos:
            from_row, from_col = from_pos
            self.board[from_row][from_col] = self.board[from_row][from_col][:-len(moving_pieces)] or 'X'

        self.board[to_row][to_col] = ''.join(final_stack) if final_stack else 'X'
        return capture_count, reserve_count

    """ Moves a stack of pieces from one position to another.
        @param from_pos: The starting position (row, col).
        @param to_pos: The ending position (row, col).
    """
    def move_stack(self, from_pos, to_pos):
        from_row, from_col = from_pos
        moving_stack = self.board[from_row][from_col]
        player_moving = moving_stack[-1]

        distance = self.calculate_distance(from_pos, to_pos)  # Calculate the distance between the two positions

        capture_count, reserve_count = self.move_logic(from_pos, to_pos, player_moving, moving_stack, distance)
        self.update_piece_counts(player_moving, capture_count, reserve_count)

    """ Places a reserved piece into the board.
        @param to_pos: The position (row, col) where the piece is to be placed.
        @param player: The player ('B' or 'R') making the move.
        @return: True, indicating the move was successful.
    """
    def move_reserved_piece(self, to_pos, player):
        capture_count, reserve_count = self.move_logic(None, to_pos, player, player)
        self.update_piece_counts(player, capture_count, reserve_count - 1)  # Subtract one since we're using one reserve
        return True

    """ Determines the position of the opponent's stack with the maximum length. If multiple stacks have the same 
        length, a random position is chosen. 
        @param player: The player ('B' or 'R') to find the opponent's stack for. 
        @return: The position (row, col) of the opponent's stack with the maximum length.
    """
    def get_maxstack_opponent_pos(self, player):
        max_stack = 0
        max_stack_positions = []
        for i in range(self.board_size):
            for j in range(self.board_size):
                stack_length = len(self.board[i][j])

                if self.board[i][j][-1] != player:
                    if stack_length > max_stack:
                        max_stack = stack_length
                        max_stack_positions = [(i, j)]
                    elif stack_length == max_stack:
                        max_stack_positions.append((i, j))

        if max_stack_positions:
            return random.choice(max_stack_positions)

    """ Determines the position of the player's stack with the maximum length and moves the reserved piece to the chosen position.
        If multiple stacks have the same length, a random position is chosen.
        @param game_view: The game view object.
    """
    def computer_reserved_play(self, game_view):
        if self.turn == 'R' and self.red_reserved > 0:
            # Choose higher stack controlled by opponent
            max_stack_pos = self.get_maxstack_opponent_pos(self.turn)

            if max_stack_pos:
                to_row, to_col = max_stack_pos

                self.highlight_and_move_computer(None, (to_row, to_col), is_reserved=True, game_view=game_view)
                pygame.display.flip()
            else:
                print("No valid moves available")
        elif self.turn == 'B' and self.blue_reserved > 0:

            # Choose higher stack controlled by opponent
            max_stack_pos = self.get_maxstack_opponent_pos(self.turn)

            if max_stack_pos:
                to_row, to_col = max_stack_pos

                self.highlight_and_move_computer(None, (to_row, to_col), is_reserved=True, game_view=game_view)
                pygame.display.flip()
            else:
                print("No valid moves available")

    """ Highlights potential moves and performs a move for the computer player.
        @param from_pos: The starting position of the move, or None for a reserved move.
        @param to_pos: The ending position of the move.
        @param is_reserved: Whether the move is using a reserved piece.
        @param game_view: The GameView instance for rendering.
    """
    def highlight_and_move_computer(self, from_pos, to_pos, is_reserved, game_view):
        if is_reserved:
            game_view.highlight_moves(
                [(i, j) for i in range(self.board_size) for j in range(self.board_size) if self.board[i][j] != 'N'],
                reserved=True)
        else:
            valid_positions = self.get_valid_moves_for_position(from_pos[0], from_pos[1])
            game_view.highlight_moves(valid_positions, reserved=False)

        pygame.display.flip()
        pygame.time.delay(1000)

        if is_reserved:
            self.move_reserved_piece(to_pos, self.turn)  # Hardcoded for now (computer is always red)
        else:
            self.move_stack(from_pos, to_pos)

    """ Determines and executes a move for the computer player based on the difficulty level.
        @param mode: The game mode (2 for Player vs Computer, 3 for Computer vs Computer).
        @param game_view: The GameView instance for rendering.
        @param difficulty1: The difficulty level for the first computer player.
        @param difficulty2: The difficulty level for the second computer player (in CvC mode).
    """
    def computer_move(self, mode, game_view, difficulty1, difficulty2):
        # if mode is 2 - only one computer player - only one difficulty
        # if mode is 3 - two computer players, difficulty might differ

        if mode == 2:
            difficulty = difficulty1
        elif mode == 3:
            if self.turn == 'B':  # First Player has difficulty1
                difficulty = difficulty1
            else:
                difficulty = difficulty2  # Second Player has difficulty2
        else:
            difficulty = None

        if difficulty == 1:  # Easy - MCTS
            mcts_tree = MCTS(self, self.turn, 10)
            selected_move = mcts_tree.search()

            if selected_move:
                valid_positions = self.get_valid_moves_for_position(selected_move[0], selected_move[1])
                game_view.highlight_moves(valid_positions, reserved=False)
                pygame.display.flip()

                pygame.time.delay(500)

                self.move_stack((selected_move[0], selected_move[1]), (selected_move[2], selected_move[3]))
            else:
                self.computer_reserved_play(game_view)  # If no valid moves are available but reserved pieces

        elif difficulty == 2 or difficulty == 3 or difficulty == 4:
            depth = 0

            if difficulty == 2:
                depth = 2
            elif difficulty == 3:
                depth = 2
            elif difficulty == 4:
                depth = 5

            minimax_algorithm = MinimaxWithAlphaBeta(depth, player=self.turn, game_level=difficulty)
            best_move = minimax_algorithm.find_best_move(self)

            if best_move:
                from_row, from_col, to_row, to_col = best_move
                self.highlight_and_move_computer((from_row, from_col), (to_row, to_col), is_reserved=False,
                                                 game_view=game_view)
            else:
                self.computer_reserved_play(game_view)  # If no valid moves are available but there are reserved pieces

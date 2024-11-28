import random


class MinimaxWithAlphaBeta:

    """ Initializes the Minimax object with Alpha-Beta pruning for game decision-making.
        @param depth: The maximum depth to explore in the game tree. A higher number increases the foresight of the AI.
        @param player: The player this AI represents, either 'B' for Blue or 'R' for Red.
        @game_level: The difficulty level of the game (2, 3, or 4).
    """
    def __init__(self, depth, player, game_level):
        self.depth = depth
        self.player = player  # 'B' ou 'R'
        self.game_level = game_level  # 2 or 3 or 4

    """ Evaluates the game board for the 'hard' difficulty setting by calculating the score based on controlled stacks, 
        reserved and captured pieces.
        @param game_logic: The current state of the game logic.
        @return score: The calculated score from the current player's perspective.
    """
    def evaluate_hard(self, game_logic):
        score = 0
        for row in game_logic.board:
            for cell in row:
                if cell not in ['N', 'X', '']:
                    stack_owner = cell[-1]
                    stack_points = len(cell)
                    if stack_owner == self.player:
                        score += stack_points
                    else:
                        score -= stack_points

        # Add to score if player has reserved pieces
        score += game_logic.blue_reserved if self.player == 'B' else game_logic.red_reserved

        # Add to score if player has captured opponent's pieces
        score += game_logic.red_captured if self.player == 'B' else game_logic.blue_captured

        return score

    """ Evaluates the game board for the 'medium' difficulty setting, emphasizing control of the central region of the 
        board.
        @param game_logic: The current state of the game logic.
        @return score: The calculated score focusing on board control.
    """
    def evaluate_medium(self, game_logic):
        score = 0
        center_areas = []

        # Basic Board Control: Slightly prioritize pieces in the central region of the board
        if game_logic.board_size == 6:
            center_areas = [(2, 2), (2, 3), (3, 2), (3, 3)]  # Central 4 squares for 6x6
        elif game_logic.board_size == 8:
            center_areas = [(3, 3), (3, 4), (4, 3), (4, 4),  # Center most 4 squares
                            (2, 3), (2, 4), (5, 3), (5, 4),  # Adjacent squares vertically
                            (3, 2), (3, 5), (4, 2), (4, 5)]  # Adjacent squares horizontally

        for x, y in center_areas:
            if game_logic.board[x][y].endswith(self.player):
                score += 1  # Each piece in the center is valued

        return score

    """ Recursively performs the Minimax algorithm with Alpha-Beta pruning to find the best score achievable from the 
    current state, considering both maximizing and minimizing scenarios.
        @param game_logic (object): The game logic containing the current state.
        @param depth (int): Current depth in the search tree.
        @param alpha (int): The current alpha value for Alpha-Beta pruning.
        @param beta (int): The current beta value for Alpha-Beta pruning.
        @param maximizingPlayer (bool): True if the current player is maximizing the score, False otherwise.
        @return maxEval or minEval: The best score found for the current branch of the game tree.
    """
    def minimax(self, game_logic, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or game_logic.check_gameover():
            if self.game_level == 3 or self.game_level == 4:
                eval = self.evaluate_hard(game_logic)
            elif self.game_level == 2:
                eval = self.evaluate_medium(game_logic)
            else:
                eval = 0
            return eval

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in game_logic.get_valid_moves_for_player(self.player):
                new_game_state = game_logic.copy()
                new_game_state.move_stack(move[:2], move[2:])
                eval = self.minimax(new_game_state, depth - 1, alpha, beta, False)
                maxEval = max(maxEval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = float('inf')
            opponent = 'B' if self.player == 'R' else 'R'
            for move in game_logic.get_valid_moves_for_player(opponent):
                new_game_state = game_logic.copy()
                new_game_state.move_stack(move[:2], move[2:])
                eval = self.minimax(new_game_state, depth - 1, alpha, beta, True)
                minEval = min(minEval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return minEval

    """ Determines the best move to make from the current game state by applying the Minimax algorithm with Alpha-Beta
        pruning across all valid moves.
        @param game_logic: The game logic containing the current state.
        @return selected_move: The best move found (or None if no valid moves).
    """
    def find_best_move(self, game_logic):
        best_moves = []
        best_score = float('-inf') if self.player == game_logic.turn else float('inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in game_logic.get_valid_moves_for_player(self.player):
            new_game_state = game_logic.copy()
            new_game_state.move_stack(move[:2], move[2:])
            # Calls minimax with the current move
            score = self.minimax(new_game_state, self.depth - 1, alpha, beta, game_logic.turn != self.player)
            # Logic to update the best move based on the score
            if (self.player == game_logic.turn and score > best_score) or \
                    (self.player != game_logic.turn and score < best_score):
                best_score = score
                best_moves = [move]  # Resets best_moves with the current move as it has the best score
                if self.player == game_logic.turn:
                    alpha = max(alpha, score)
                else:
                    beta = min(beta, score)
            elif score == best_score:
                best_moves.append(move)  # Adds move to best_moves if it shares the highest score

        if best_moves:
            selected_move = random.choice(best_moves)  # Randomly selects one of the best moves
            return selected_move
        else:
            return None

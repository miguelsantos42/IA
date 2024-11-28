class Minimax:
    """ Initializes the Minimax object with a specific search depth and the player it represents.
        Parameters:
        - depth (int): The maximum depth to explore in the game tree. A higher number increases the foresight of the AI.
        - player (str): The player this AI represents, either 'B' for Blue or 'R' for Red.
    """
    def __init__(self, depth, player):
        self.depth = depth
        self.player = player  # 'B' or 'R'

    """ Evaluates the current state of the game, returning a score from the perspective of the AI's player.
        @param game_logic: An object representing the current game state, including the board and reserved pieces.
        @return score (int): The evaluated score, where a higher score is better for the AI's player.
    """
    def evaluate(self, game_logic):
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
        score += game_logic.blue_reserved if self.player == 'B' else game_logic.red_reserved
        return score

    """ Recursively explores possible moves to find the best move, using the minimax algorithm.
        @param game_logic: The current game state.
        @param depth (int): Current depth in the game tree.
        @param maximizingPlayer (bool): True if the current turn is maximizing; otherwise, False.
        @return The best evaluated score for the current player at the given depth.
    """
    def minimax(self, game_logic, depth, maximizingPlayer):
        if depth == 0 or game_logic.check_gameover():
            return self.evaluate(game_logic)

        if maximizingPlayer:
            maxEval = float('-inf')
            for move in game_logic.get_valid_moves_for_player(self.player):
                new_game_state = game_logic.copy()
                new_game_state.move_stack(move[:2], move[2:])
                eval = self.minimax(new_game_state, depth - 1, False)
                maxEval = max(maxEval, eval)
            return maxEval
        else:
            minEval = float('inf')
            opponent = 'B' if self.player == 'R' else 'R'
            for move in game_logic.get_valid_moves_for_player(opponent):
                new_game_state = game_logic.copy()
                new_game_state.move_stack(move[:2], move[2:])
                eval = self.minimax(new_game_state, depth - 1, True)
                minEval = min(minEval, eval)
            return minEval

    """ Determines the best move for the current player, given the current state of the game.
        @param game_logic: The current game state.
        @return best_move: The move (start position to end position) that leads to the best outcome.
    """
    def find_best_move(self, game_logic):
        best_move = None
        best_score = float('-inf') if self.player == game_logic.turn else float('inf')

        for move in game_logic.get_valid_moves_for_player(self.player):
            new_game_state = game_logic.copy()
            new_game_state.move_stack(move[:2], move[2:])
            score = self.minimax(new_game_state, self.depth - 1, game_logic.turn != self.player)

            if self.player == game_logic.turn and score > best_score:
                best_score = score
                best_move = move
            elif self.player != game_logic.turn and score < best_score:
                best_score = score
                best_move = move

        return best_move

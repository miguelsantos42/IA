import math
import random


class MCTSNode:
    """ Represents a node in the Monte Carlo Tree Search.
        @param game_state: The game state of the node.
        @param turn: The turn of the player making the move.
        @param move: The move that led to this node.
        @param parent: The parent node of this node.
    """
    def __init__(self, game_state, turn, move=None, parent=None):
        self.game_state = game_state.copy()
        self.parent = parent
        self.move = move
        self.children = []
        self.visits = 0
        self.wins = 0
        self.turn = turn

    """ Determines if the node represents a terminal state (game over).
        @return: True if the node is terminal, False otherwise.
    """
    def is_terminal(self):
        return self.game_state.check_gameover(True)

    """ Checks if all possible moves from this node have been explored
        @return: True if the node is fully expanded, False otherwise.
    """
    def is_fully_expanded(self):
        return len(self.get_unvisited_moves()) == 0

    """ Retrieves all possible moves from this node's game state that have not yet been explored.
        @return: The unvisited moves of the node.
    """
    def get_unvisited_moves(self):
        valid_moves = self.game_state.get_valid_moves_for_player(self.game_state.turn)
        visited_moves = [child.move for child in self.children]
        return [move for move in valid_moves if move not in visited_moves]

    """ Expands the node by creating new children nodes for each valid, unvisited move.
    """
    def expand(self):
        for move_info in self.game_state.get_valid_moves_for_player(self.turn):
            from_row, from_col, to_row, to_col = move_info
            new_game_state = self.game_state.copy()
            new_game_state.move_stack((from_row, from_col), (to_row, to_col))
            new_game_state.switch_turns()

            child = MCTSNode(new_game_state, new_game_state.turn, move=move_info, parent=self)
            self.children.append(child)

    """ Selects a child node to explore next, using the UCT score for decision making.
        @param exploration_weight: The exploration weight for the UCT formula.
        @return: The selected child node.
    """
    def select(self, exploration_weight=1.4):
        best_score = float('-inf')
        best_node = None

        for child in self.children:
            if child.visits > 0:
                exploitation = child.wins / child.visits
                exploration = exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
                uct_score = exploitation + exploration
            else:
                uct_score = float('inf')

            if uct_score > best_score:
                best_score = uct_score
                best_node = child

        best_node.game_state.switch_turns() # Switch turns to match the child's turn

        return best_node

    """ Simulates a game play from this node's game state to a terminal state, using random moves.
        @return: The result of the simulation indicating win/loss.
    """
    def simulate(self):
        current_state = self.game_state.copy()

        while not current_state.check_gameover():
            valid_moves = current_state.get_valid_moves_for_player(current_state.turn)

            if not valid_moves:
                break

            move = random.choice(valid_moves)
            from_row, from_col, to_row, to_col = move

            current_state.move_stack((from_row, from_col), (to_row, to_col))
            current_state.switch_turns()

        return current_state.get_result(current_state.turn)

    """
        Backpropagates the result of a simulation up the tree, updating visits and wins counts.
        @param result: The result of the simulation to backpropagate.
    """
    def backpropagate(self, result):
        self.visits += 1
        self.wins += result
        if self.parent:
            self.parent.backpropagate(result)


class MCTS:
    """ Implements the Monte Carlo Tree Search algorithm.
        @param game_state: The game state of the MCTS.
        @param turn: The turn of the player making the move.
        @param max_iterations: The maximum number of iterations for the MCTS.
    """
    def __init__(self, game_state, turn, max_iterations):
        self.root = MCTSNode(game_state, turn)
        self.max_iterations = max_iterations

    """ Performs the MCTS search, selecting, expanding, simulating, and backpropagating to find the best move.
        @return: The best move found by the MCTS.
    """
    def search(self):
        for _ in range(self.max_iterations):
            node = self.root

            # Selection
            while not node.is_terminal() and node.is_fully_expanded():
                node = node.select()

            # Expansion
            if not node.is_terminal() and not node.is_fully_expanded():
                node.expand()
                if node.children:
                    node = random.choice(node.children)

            # Simulation
            result = node.simulate()

            # Backpropagation
            node.backpropagate(result)

        if not self.root.children:  # If there are no children
            return None
        else:
            most_wins = max(self.root.children, key=lambda child: child.wins).wins
            best_children = [child for child in self.root.children if child.wins == most_wins]
            best_child = random.choice(best_children)

            return best_child.move

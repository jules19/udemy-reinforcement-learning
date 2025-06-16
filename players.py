"""Collection of player strategies for the Tic-Tac-Toe game."""

from copy import deepcopy
import random
from board import Board, EMPTY_CELL
import utils


class RandomPlayer(object):
    """Player that selects moves uniformly at random."""

    def __init__(self, *, position):
        self.position = position

    @staticmethod
    def play(*, board):
        available_actions = utils.get_available_moves(board)
        return random.choice(available_actions)


class HumanPlayer(object):
    """Interactive player that prompts a user for each move."""

    def __init__(self, *, position):
        self.position = position

    @staticmethod
    def play(*, board):
        while True:
            try:
                # Ask the user for the input value
                move = input("Enter your move (e.g. A1): ").strip().upper()
                col = ord(move[0]) - ord('A')
                row = int(move[1:]) - 1
                if board.board[col][row] == EMPTY_CELL:
                    return row, col
                else:
                    print("Cell is already occupied. Try again please.")
            except (IndexError, ValueError):
                print("Invalid input. Please try again.")


class SimpleMinimaxPlayer(object):
    """Player that uses a depth-first minimax search to select moves."""

    def __init__(self, *, position, debug=False):
        self.position = position
        self.debug = debug

    def play(self, *, board):

        # Minimax algorithm to choose the optimal move
        best_score = float('-inf')
        best_move = None
        available_moves = utils.get_available_moves(board)
        random.shuffle(available_moves)  # Shuffle moves to add some randomness

        if self.debug:
            print("Evaluating moves:", available_moves)

        for row, col in available_moves:
            # Make the given move
            board.play_move(row=row, col=col)
            board.next_player()  # Switch player for minimax algorithm
            score = self._minimax(board, is_maximizing=False, depth=1)  # Calculate score using minimax algorithm
            board.board[col][row] = EMPTY_CELL  # Undo the move
            board.next_player()  # Switch back to the original player
            if self.debug:
                print(f"Move {(row, col)} -> score {score}")
            if score > best_score:
                best_score = score
                best_move = (row, col)

        if self.debug:
            print(f"Selected move {best_move} with score {best_score}")


        return best_move

    def _minimax(self, board, is_maximizing, depth):
        # Check if the game has ended
        game_ended, there_is_winner = board.game_has_ended()
        if game_ended:
            if there_is_winner:
                return 1 if not is_maximizing else -1
            return 0

        available_moves = utils.get_available_moves(board)
        random.shuffle(available_moves)  # Shuffle moves to add some randomness
        
        best_score = float('-inf') if is_maximizing else float('inf')
        for row, col in available_moves:
            # Make the given move
            board.play_move(row=row, col=col)
            board.next_player()  # Switch player for minimax algorithm
            score = self._minimax(board, not is_maximizing, depth + 1)  # Calculate score using minimax algorithm
            board.board[col][row] = EMPTY_CELL  # Undo the move
            board.next_player()  # Switch back to the original player
            if self.debug:
                indent = '  ' * depth
                role = 'Max' if is_maximizing else 'Min'
                print(f"{indent}{role} evaluating move {(row, col)} -> {score}")
            if is_maximizing:
                best_score = max(score, best_score)
            else:
                best_score = min(score, best_score)
        return best_score
    

class DynamicProgrammingPlayer(object):
    """Minimax player with memoization of board states."""

    def __init__(self, *, position):
        self.position = position
        self.state_values = {}

    def play(self, *, board):

        # Use dynamic programming to choose the optimal move
        best_score = float('-inf')
        best_move = None
        available_moves = utils.get_available_moves(board)
        random.shuffle(available_moves)  # Shuffle moves to add some randomness

        for row, col in available_moves:
            # Make the given move
            board.play_move(row=row, col=col)
            board.next_player()  # Switch player for minimax algorithm
            score = self._minimax_cached(board, is_maximizing=False)  # Calculate score using minimax algorithm
            board.board[col][row] = EMPTY_CELL  # Undo the move
            board.next_player()  # Switch back to the original player
            if score > best_score:
                best_score = score
                best_move = (row, col)

        return best_move
    
    def _minimax_cached(self, board, is_maximizing):
        state_key = repr(board)
        if state_key not in self.state_values:
            # Check if the game has ended
            game_ended, there_is_winner = board.game_has_ended()
            if game_ended:
                if there_is_winner:
                    best_score = 1 if not is_maximizing else -1
                else:
                    best_score = 0
            else:
                available_moves = utils.get_available_moves(board)
                random.shuffle(available_moves)  # Shuffle moves to add some randomness

                best_score = float('-inf') if is_maximizing else float('inf')
                for row, col in available_moves:
                    # Make the given move
                    board.play_move(row=row, col=col)
                    board.next_player()  # Switch player for minimax algorithm
                    score = self._minimax_cached(board, not is_maximizing)  # Calculate score using minimax algorithm
                    board.board[col][row] = EMPTY_CELL  # Undo the move
                    board.next_player()  # Switch back to the original player
                    
                    if is_maximizing:
                        best_score = max(score, best_score)
                    else:
                        best_score = min(score, best_score)
            
            # Update state value dictionary
            self.state_values[state_key] = best_score

        return self.state_values[state_key]

class MonteCarloPlayer(object):
    def __init__(self, *, position, num_simulations = 5000):
        self.position = position
        self.num_simulations = num_simulations

    def play(self, *, board):
        # Monte Carlo simulation to choose the best move
        best_move = None
        best_win_rate = float('-inf')
        available_moves = utils.get_available_moves(board)

        for row, col in available_moves:
            wins = 0
            board.play_move(row=row, col=col)
            board.next_player()

            game_ended, there_is_winner = board.game_has_ended()
            if game_ended:
                if there_is_winner:
                    board.board[col][row] = EMPTY_CELL # Undo the move
                    board.next_player() # Switch back to orginal player
                    return row, col
                if best_move is None:
                    best_move = (row, col)
            else:
                # Run simulations to estimate the win rate
                for _ in range(self.num_simulations):
                    wins += self._simulate_game(board)

                win_rate = wins / self.num_simulations
                if win_rate > best_win_rate:
                    best_win_rate = win_rate
                    best_move = (row, col)

            board.board[col][row] = EMPTY_CELL # Undo the move
            board.next_player() # Switch back to orginal player

        return best_move

    def _simulate_game(self, board):
        # Simulate a random game starting with a specific board configuration
        new_board = Board(rows=board.rows, cols=board.cols, connections_to_win=board.connections_to_win, 
                            board=deepcopy(board.board), player_to_move=board.current_player)
        opponents_move = True
        
        while True:
            available_moves = utils.get_available_moves(new_board)

            random_move = random.choice(available_moves)  # Pick a move at random
            new_board.play_move(row=random_move[0], col=random_move[1])
            new_board.next_player()

            game_ended, there_is_winner = new_board.game_has_ended()
            opponents_move = not opponents_move

            if game_ended:
                if there_is_winner:
                    return 1 if opponents_move else -1
                return 0  # Draw
                
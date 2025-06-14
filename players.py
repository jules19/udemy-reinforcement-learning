"""Collection of player strategies for the Tic-Tac-Toe game."""

import random
from board import PLAYER_ONE, PLAYER_TWO, EMPTY_CELL
import utils
import time


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



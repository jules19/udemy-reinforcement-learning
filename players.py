import random
from board import PLAYER_ONE, PLAYER_TWO, EMPTY_CELL
import utils


class RandomPlayer(object):

    def __init__(self, *, position):
        self.position = position

    @staticmethod
    def play(*, board):
        available_actions = utils.get_available_moves(board)
        return random.choice(available_actions)


class HumanPlayer(object):

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

    def __init__(self, *, position):
        self.position = position

    def play(self, *, board):
        # Minimax algorithm to choose the optimal move
        best_score = float('-inf')
        best_move = None
        available_moves = utils.get_available_moves(board)

        for row, col in available_moves:
            # Make the given move
            board.play_move(row=row, col=col)
            board.next_player()  # Switch player for minimax algorithm
            score = self._minimax(board, is_maximizing=False)  # Calculate score using minimax algorithm
            board.board[col][row] = EMPTY_CELL  # Undo the move
            board.next_player()  # Switch back to the original player
            if score > best_score:
                best_score = score
                best_move = (row, col)
        return best_move

    def _minimax(self, board, is_maximizing):
        # Check if the game has ended
        game_ended, there_is_winner = board.game_has_ended()
        if game_ended:
            if there_is_winner:
                return 1 if not is_maximizing else -1
            return 0

        available_moves = utils.get_available_moves(board)

        best_score = float('-inf') if is_maximizing else float('inf')
        for row, col in available_moves:
            # Make the given move
            board.play_move(row=row, col=col)
            board.next_player()  # Switch player for minimax algorithm
            score = self._minimax(board, not is_maximizing)  # Calculate score using minimax algorithm
            board.board[col][row] = EMPTY_CELL  # Undo the move
            board.next_player()  # Switch back to the original player
            if is_maximizing:
                best_score = max(score, best_score)
            else:
                best_score = min(score, best_score)
        return best_score

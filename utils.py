"""Utility helpers for working with Tic-Tac-Toe boards."""

from board import EMPTY_CELL


def get_available_moves(board):
    available_moves = []
    for col in range(board.cols):
        for row in range(board.rows):
            if board.board[col][row] == EMPTY_CELL:
                available_moves.append((row, col))
    return available_moves

import os
import sys
import random

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from board import Board, PLAYER_ONE, PLAYER_TWO, EMPTY_CELL
from players import RandomPlayer, SimpleMinimaxPlayer
import utils


def set_board_state(board, rows):
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            board.board[c][r] = value


def test_get_available_moves_and_random_player():
    board = Board(rows=3, cols=3, connections_to_win=3)
    state = [
        [PLAYER_ONE, PLAYER_TWO, EMPTY_CELL],
        [EMPTY_CELL, PLAYER_ONE, EMPTY_CELL],
        [PLAYER_TWO, EMPTY_CELL, PLAYER_TWO],
    ]
    set_board_state(board, state)
    moves = utils.get_available_moves(board)
    assert set(moves) == {(1, 0), (2, 1), (0, 2), (1, 2)}

    random.seed(0)
    player = RandomPlayer(position=PLAYER_TWO)
    move = player.play(board=board)
    assert move in moves


def test_simple_minimax_player_finds_winning_move():
    board = Board(rows=3, cols=3, connections_to_win=3)
    # Setup state where PLAYER_ONE can win with a horizontal move on row 1
    state = [
        [PLAYER_ONE, PLAYER_ONE, EMPTY_CELL],
        [PLAYER_TWO, PLAYER_TWO, EMPTY_CELL],
        [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
    ]
    set_board_state(board, state)
    board.current_player = PLAYER_ONE

    player = SimpleMinimaxPlayer(position=PLAYER_ONE)
    winning_move = player.play(board=board)
    assert winning_move == (0, 2)

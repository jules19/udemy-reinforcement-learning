import os
import sys
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from board import Board, PLAYER_ONE, PLAYER_TWO, EMPTY_CELL


def set_board_state(board, rows):
    """Helper to set board state using row-major list of lists."""
    for r, row in enumerate(rows):
        for c, value in enumerate(row):
            board.board[c][r] = value


def test_str_and_repr():
    board = Board(rows=3, cols=3, connections_to_win=3)
    state = [
        [PLAYER_ONE, PLAYER_TWO, EMPTY_CELL],
        [EMPTY_CELL, PLAYER_ONE, EMPTY_CELL],
        [PLAYER_TWO, EMPTY_CELL, PLAYER_TWO],
    ]
    set_board_state(board, state)
    board.current_player = PLAYER_ONE

    expected_str = (
        "  1 | X O -\n"
        "  2 | - X -\n"
        "  3 | O - O\n"
        "-----------\n"
        "      A B C\n"
    )
    assert str(board) == expected_str
    assert repr(board) == "1|102|210|002"


def test_next_player_and_play_move():
    board = Board(rows=3, cols=3, connections_to_win=3)
    assert board.current_player == PLAYER_ONE
    board.play_move(row=0, col=0)
    assert board.board[0][0] == PLAYER_ONE
    board.next_player()
    assert board.current_player == PLAYER_TWO
    board.play_move(row=1, col=1)
    assert board.board[1][1] == PLAYER_TWO


def test_horizontal_vertical_diagonal_wins():
    board = Board(rows=3, cols=3, connections_to_win=3)
    # horizontal win on first row
    state = [
        [PLAYER_ONE, PLAYER_ONE, PLAYER_ONE],
        [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
        [EMPTY_CELL, EMPTY_CELL, EMPTY_CELL],
    ]
    set_board_state(board, state)
    assert board._horizontal_check() is True
    assert board.game_has_ended() == (True, True)

    # vertical win on first column
    state = [
        [PLAYER_TWO, EMPTY_CELL, EMPTY_CELL],
        [PLAYER_TWO, EMPTY_CELL, EMPTY_CELL],
        [PLAYER_TWO, EMPTY_CELL, EMPTY_CELL],
    ]
    set_board_state(board, state)
    assert board._vertical_check() is True
    assert board.game_has_ended() == (True, True)

    # diagonal increasing
    state = [
        [PLAYER_ONE, EMPTY_CELL, EMPTY_CELL],
        [EMPTY_CELL, PLAYER_ONE, EMPTY_CELL],
        [EMPTY_CELL, EMPTY_CELL, PLAYER_ONE],
    ]
    set_board_state(board, state)
    assert board._diagonal_increasing_check() is True
    assert board.game_has_ended() == (True, True)

    # diagonal decreasing
    state = [
        [EMPTY_CELL, EMPTY_CELL, PLAYER_TWO],
        [EMPTY_CELL, PLAYER_TWO, EMPTY_CELL],
        [PLAYER_TWO, EMPTY_CELL, EMPTY_CELL],
    ]
    set_board_state(board, state)
    assert board._diagonal_decreasing_check() is True
    assert board.game_has_ended() == (True, True)


def test_draw_condition():
    board = Board(rows=3, cols=3, connections_to_win=3)
    state = [
        [PLAYER_ONE, PLAYER_TWO, PLAYER_ONE],
        [PLAYER_TWO, PLAYER_ONE, PLAYER_TWO],
        [PLAYER_TWO, PLAYER_ONE, PLAYER_TWO],
    ]
    set_board_state(board, state)
    assert board.game_has_ended() == (True, False)

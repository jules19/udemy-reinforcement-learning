"""Command line interface to play Tic-Tac-Toe with different player types."""

import argparse
from board import Board, PLAYER_ONE, PLAYER_TWO
from players import HumanPlayer, RandomPlayer, SimpleMinimaxPlayer, DynamicProgrammingPlayer, MonteCarloPlayer

_player_categories = {
    'human_user': HumanPlayer,
    'random_player': RandomPlayer,
    'minimax_player': SimpleMinimaxPlayer,
    'dp_player': DynamicProgrammingPlayer,
    'mc_player': MonteCarloPlayer,
}


class TicTacToe(object):
    """High level game controller managing turns and player interaction."""

    def __init__(self, *, player_one, player_two, display_board=True, debug_minimax=False):
        self.board = Board(rows=3, cols=3, connections_to_win=3)
        self.display_board = display_board
        if _player_categories[player_one] is SimpleMinimaxPlayer:
            self.current_player = _player_categories[player_one](position=PLAYER_ONE, debug=debug_minimax)
        else:
            self.current_player = _player_categories[player_one](position=PLAYER_ONE)
        if _player_categories[player_two] is SimpleMinimaxPlayer:
            self.next_player = _player_categories[player_two](position=PLAYER_TWO, debug=debug_minimax)
        else:
            self.next_player = _player_categories[player_two](position=PLAYER_TWO)

    def play_game(self):
        while True:
            if self.display_board:
                print(self.board)
                print(f"Player {'X' if self.current_player.position == PLAYER_ONE else 'O'}'s turn\n\n")
            row, col = self.current_player.play(board=self.board)
            self.board.play_move(row=row, col=col)
            game_ended, there_is_winner = self.board.game_has_ended()
            if game_ended:
                if self.display_board:
                    print(self.board)
                    if there_is_winner:
                        print(f"Player {'X' if self.current_player.position == PLAYER_ONE else 'O'} wins!")
                    else:
                        print("It's a draw!")
                break
            self.current_player, self.next_player = self.next_player, self.current_player
            self.board.next_player()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Play Tic-Tac-Toe')
    parser.add_argument('--player-one', choices=_player_categories.keys(), default='human_user')
    parser.add_argument('--player-two', choices=_player_categories.keys(), default='mc_player')
    parser.add_argument('--show-minimax', action='store_true', help='Display minimax evaluation steps')
    args = parser.parse_args()
    game = TicTacToe(player_one=args.player_one,
                     player_two=args.player_two,
                     debug_minimax=args.show_minimax)
    game.play_game()

from board import Board, PLAYER_ONE, PLAYER_TWO
from players import HumanPlayer, RandomPlayer, SimpleMinimaxPlayer

_player_categories = {
    'human_user': HumanPlayer,
    'random_player': RandomPlayer,
    'minimax_player': SimpleMinimaxPlayer,
}


class TicTacToe(object):

    def __init__(self, *, player_one, player_two, display_board=True):
        self.board = Board(rows=3, cols=3, connections_to_win=3)
        self.display_board = display_board
        self.current_player = _player_categories[player_one](position=PLAYER_ONE)
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
    game = TicTacToe(player_one='human_user', player_two='minimax_player')
    game.play_game()

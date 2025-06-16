# Tutorial

This short guide explains how to run and customize the Tic‑Tac‑Toe program in this repository.

## Choosing players

The `TicTacToe` class in `tic_tac_toe.py` accepts the names of the two players to create. The constructor looks up these names in an internal dictionary and instantiates the appropriate class. You can pick from:

- `human_user` – a player that asks for moves via the console.
- `random_player` – selects valid moves at random.
- `minimax_player` – uses a simple minimax search.
- `dp_player` – a dynamic programming version of minimax.
- `mc_player` – a Monte Carlo based strategy.

For example, the following snippet pits a random player against the minimax player:

```python
from tic_tac_toe import TicTacToe

game = TicTacToe(player_one='random_player', player_two='minimax_player')
```

These names are also exposed as command line options when running the script directly.

## Board indexing

Boards are represented as `board.board[col][row]`. The first index selects the column (A, B, C) and the second the row (1, 2, 3). Keep this in mind when manually manipulating the board in tests or extensions.

## Requirements

`requirements.txt` lists no external packages. Only Python’s standard library is needed to run the game and tests.

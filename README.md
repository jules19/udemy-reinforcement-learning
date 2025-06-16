# Tic-Tac-Toe Reinforcement Learning

This repository contains a simple implementation of a Tic-Tac-Toe game used in a reinforcement learning course. It allows different types of players to compete:

- **Human player** – interactively enters moves.
- **Random player** – selects moves randomly.
- **Minimax player** – uses a basic minimax search.
- **Dynamic programming player** – memoizes board states during minimax search.
- **Monte Carlo player** – estimates move quality via random simulations.

The game uses a 3x3 board and is run entirely in the console.

## Running the game

Execute the game script directly with Python:

```bash
python tic_tac_toe.py
```

To see how the minimax player evaluates each move, run with the `--show-minimax` flag:

```bash
python tic_tac_toe.py --show-minimax
```

By default a human player faces the minimax player. When prompted, input moves in the format `A1`, `B2`, etc.

## Requirements

There are no external dependencies besides Python 3.

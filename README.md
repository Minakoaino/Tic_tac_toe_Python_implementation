# Tic-Tac-Toe Game :game_die:

Welcome to the interactive **Tic-Tac-Toe game**! This Python-based application allows you to play the classic game against an AI with three levels of difficulty. You can choose to go first or second and select your preferred symbol, 'X' or 'O'.

## :memo: Requirements

Make sure you have Python 3 installed. If not, you can download it from [here](https://www.python.org/downloads/).

## :rocket: How to Run the Program

1. Download the .py file of the program.
2. Open your terminal or command prompt.
3. Navigate to the directory containing the file.
4. Run the following command:

```sh
python TicTacToe_Python.py
```

## :video_game: How to Play

Once the program is running, you'll be prompted to choose the difficulty level:

- **Easy**: The computer makes moves at random.
- **Medium**: The computer makes strategic moves but doesn't always play optimally.
- **Hard**: The computer uses the Minimax algorithm to determine the best move, making it a tough opponent.

Next, the game board will be displayed. The board is a 3x3 grid, corresponding to positions 1 through 9 as follows:

◻️ | ◻️ | ◻️

◻️ | ❌ | ◻️

◻️ | ◻️ | ⭕




You'll be asked to select a position on the board for your move. For instance, if you want to place your symbol in the top-left corner of the board, enter '1'. If the chosen position is already occupied or is not a valid number between 1 and 9, you'll be asked to try again.

The game continues, alternating between you and the computer, until there is a winner or all positions on the board are filled (resulting in a draw). The game automatically checks for a win after each move. The win conditions are any row, column, or diagonal filled with the same symbol.

After a game ends, you have the option to play again, quit, or return to the main menu to change the difficulty level. :trophy:

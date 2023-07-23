# Importing libraries
import random
import time
import sqlite3


print(' _______________________________________________________________ ')
print("|  _____  _  ____     _____  ____  ____     _____  ____  _____  |")
print("| /__ __\/ \/   _\   /__ __\/  _ \/   _\   /__ __\/  _ \/  __/  |")
print("|   / \  | ||  / _____ / \  | / \||  / _____ / \  | / \||  \    |")
print("|   | |  | ||  \_\____\| |  | |-|||  \_\____\| |  | \_/||  /_   |")
print("|   \_/  \_/\____/     \_/  \_/ \|\____/     \_/  \____/\____\  |")
print('|_______________________________________________________________|\n')
print(20 * ' ', "   reference:    ")
print(20 * ' ', '     |    |      ')
print(20 * ' ', '  1  | 2  | 3    ')
print(20 * ' ', "-----+----+----- ")
print(20 * ' ', "     |    |      ")
print(20 * ' ', "  4  | 5  | 6    ")
print(20 * ' ', "-----+----+----- ")
print(20 * ' ', "     |    |      ")
print(20 * ' ', "  7  | 8  | 9    \n")


def show_board(b):
    print("   |   |   ")
    print(f" {b[0][0]} | {b[0][1]} | {b[0][2]} ")
    print("   |   |   ")
    print("---+---+---")
    print("   |   |   ")
    print(f" {b[1][0]} | {b[1][1]} | {b[1][2]} ")
    print("   |   |   ")
    print("---+---+---")
    print("   |   |   ")
    print(f" {b[2][0]} | {b[2][1]} | {b[2][2]} ")
    print("   |   |   ")

# Function for a human player's move, asking for input
def human_to_human(b):
    while True:
        try:
            a = int(input("Choose a position from 1 to 9:"))
            if a > 0 and a < 10:
                # Check if the position is occupied
                row = (a - 1) // 3
                col = (a - 1) % 3
                if board[row][col] == -5:
                    break
                else:
                    print("The position is already occupied. Please choose another.")
            else:
                print("Error")
        except:
            print("Error")
    return a

# The function to check if a player has won
def check_win(board, player):

    # Check for a win in the rows
    for row in board:
        if all(c == player for c in row):
            return True

    # Check for a win in the columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check for a win in the diagonals
    if all(board[i][i] == player for i in range(3)):
        return True
    if all(board[i][2 - i] == player for i in range(3)):
        return True
    return False
  
# The function for a random move by the computer player     
def random_move(board):

    while True:
        row = random.randint(0, 2)
        col = random.randint(0, 2)
        if board[row][col] == ' ':
            return row, col        
     
# The function for a strategic move by the computer player (medium difficulty)
def computer_move(board, current_symbol):
    # Check if the opponent can win on the next turn
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = current_symbol
                if check_win(board, current_symbol):
                    return i, j
                board[i][j] = ' '  # undo the move if it doesn't win

    # Block a potential win by the opponent
    player_symbol = 'O' if current_symbol == 'X' else 'X'
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = player_symbol
                if check_win(board, player_symbol):
                    board[i][j] = current_symbol
                    return i, j
                board[i][j] = ' '  

    # Play in the center position, if it's available
    if board[1][1] == ' ':
        return 1, 1

    # Play in a corner position, if one is available
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    for corner in corners:
        if board[corner[0]][corner[1]] == ' ':
            return corner

    # Play in a free middle position
    sides = [(0, 1), (1, 0), (1, 2), (2, 1)]
    for side in sides:
        if board[side[0]][side[1]] == ' ':
            return side

    # If there are no other options, play in the first available position
    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                return i, j

# Minimax algorithm
def minimax(board, depth, is_maximizing):
    if check_win(board, 'X'):
        return 1, None
    if check_win(board, 'O'):
        return -1, None
    if depth == 9:
        return 0, None

    if is_maximizing:
        best_score = float('-inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'X'
                    score, _ = minimax(board, depth + 1, False)
                    board[row][col] = ' '
                    if score > best_score:
                        best_score = score
                        best_move = (row, col)
        return best_score, best_move
    else:
        best_score = float('inf')
        best_move = None
        for row in range(3):
            for col in range(3):
                if board[row][col] == ' ':
                    board[row][col] = 'O'
                    score, _ = minimax(board, depth + 1, True)
                    board[row][col] = ' '
                    if score < best_score:
                        best_score = score
                        best_move = (row, col)
        return best_score, best_move
    
# This function creates the game_results table in the SQLite database if it doesn't already exist
def create_table():
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect("game_results.db")
        cursor = conn.cursor()
        
        # Execute a SQL command to create the game_results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS game_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                player1_name TEXT,
                player2_name TEXT,
                result TEXT,
                turns INTEGER
            )
        """)
        
        # Commit changes and close the connection to the database
        conn.commit()
    except sqlite3.Error as e:
        # Print any SQLite error that occurs when trying to connect to the database or execute SQL commands
        print(f"An error occurred while trying to connect to the database: {e}")
    finally:
        # Always close the connection, even if an error occurred
        if conn:
            conn.close()
            
# This function inserts a new row into the game_results table in the SQLite database
def insert_game_result(player1_name, player2_name, result, turns):
    try:
        # Establish a connection to the SQLite database
        conn = sqlite3.connect("game_results.db")
        cursor = conn.cursor()

        # Check that the arguments are of the expected types
        if not (isinstance(player1_name, str) and isinstance(player2_name, str) and 
                isinstance(result, str) and isinstance(turns, int)):
            raise ValueError("Input values are not of the expected data type.")
        
        # Execute a SQL command to insert a new row into the game_results table
        cursor.execute("""
            INSERT INTO game_results (player1_name, player2_name, result, turns)
            VALUES (?, ?, ?, ?)
        """, (player1_name, player2_name, result, turns))
        
        # Commit changes and close the connection to the database
        conn.commit()
    except sqlite3.Error as e:
        # Print any SQLite error that occurs when trying to connect to the database or execute SQL commands
        print(f"An error occurred while trying to connect to the database or insert data: {e}")
    except ValueError as ve:
        # Print any ValueError that occurs when checking the types of the arguments
        print(f"An error occurred due to invalid input data: {ve}")
    finally:
        # Close the connection
        if conn:
            conn.close()


## άνθρωπος vs υπολογιστή
def computer_vs_human(difficulty):
    turns = 1   # Αρχικοποίηση των γύρων
    # Δημιουργία του αρχικού πίνακα
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    players = ['Computer', 'Human'] # Two players: Computer and Human
    symbols = ['X', 'O'] # The symbols used by the players
    current_player_index = 0 # Random choice of the player who will play first
    '''
    The game continues in a loop until there is a winner or a draw.
    In each turn, the current player makes a move (random for the Computer,
    selected by the Human), the board is displayed, and then it is checked
    if there is a winner or a draw.
    '''
    while True:
        current_player = players[current_player_index]
        current_symbol = symbols[current_player_index]
        print(f"\nTurn: {turns}, it's player's turn:\n{current_player} ({current_symbol})")

        if current_player == 'Computer':
            print("The computer is choosing...")
            time.sleep(2)            
            #Choosing move based on difficulty
            if difficulty == 1:
                row, col = random_move(board)
                move = (row*3 + col) + 1
                                                         
            elif difficulty == 2:
                row, col = computer_move(board, current_symbol)
                move = (row*3 + col) + 1                          
                
            elif difficulty == 3:
                best_score, best_move = minimax(board, turns, True)
                if best_move is not None:
                    row, col = best_move
                    move = (row*3 + col) + 1
                                  
            board[row][col] = current_symbol  # Update the board with the current player's symbol
            show_board(board) 
            print(f"The computer ({current_symbol}) chose position {move}")            
                 
        else:
            while True:
                try:
                    move = int(input("Choose a position from 1 to 9: "))
                    if 1 <= move <= 9:
                        row = (move - 1) // 3
                        col = (move - 1) % 3
                        if board[row][col] == ' ':
                            break
                    print("Invalid position. Please choose a position from 1 to 9.")
                except ValueError:
                    print("Error: please enter a number.")
                    
            board[row][col] = current_symbol  # Update the board with the current player's symbol
            show_board(board)
        turns += 1
                                    
        '''
        The move is added to the board and it is checked for win or draw.
        If the player wins, the game ends. If the game reaches the 9th round 
        without a winner, a draw is declared. The results are stored in the table in the database
        '''
        if check_win(board, current_symbol):
            print(f"Ο παίκτης {current_player} ({current_symbol}) κέρδισε!")
            show_board(board)
            result = "Human" if current_player == "Άνθρωπος" else "Computer"
            break
        if turns == 10:
            print("\nΙσοπαλία!")
            show_board(board)
            result = "Draw" 
            break

        current_player_index = 1 - current_player_index

    # After the game ends and we have the game result
    player1_name = "Human"
    player2_name = "Computer"
    turns = turns
    insert_game_result(player1_name, player2_name, result, turns)
    
    
    # After the game ends, the player can choose to play again or end the program           
    while True:
        '''
        If the player chooses to play again, the game starts from the beginning. 
        Otherwise, the program ends. The results are stored in the table in the database
        '''
        try:
            play_again = int(input("Do you want a rematch?\n1. Yes\n2. No: \n3.Return to main menu:"))
            if play_again == 1:
                print("\nStarting a new game...")
                computer_vs_human(difficulty)                
                break
            elif play_again == 2:
                print("Thank you for playing!")
                quit()        
            elif play_again == 3:
                main()                                                       
        except ValueError:
            print("Error: please enter 1 for 'Yes' or 2 for 'No'.")

def computer_vs_computer(difficulty):
    turns = 0
    board = [[' ', ' ', ' '],
             [' ', ' ', ' '],
             [' ', ' ', ' ']]
    players = ['Computer 1', 'Computer 2']
    symbols = ['X', 'O']
    current_player_index = random.randint(0, 1)
    game_over = False  # Flag variable for game status
    
    while not game_over:
        current_player = players[current_player_index]
        current_symbol = symbols[current_player_index]
        print(f"\nTurn: {turns}")
        print(f"\n{current_player}'s ({current_symbol}) turn")
        print(f"\n{current_player} is choosing...")
        time.sleep(2)
        
        if difficulty == 1:
            row, col = random_move(board)
            move = (row*3 + col) + 1
            
        elif difficulty == 2:
            row, col = computer_move(board, current_symbol)
            move = (row*3 + col) + 1            

        elif difficulty == 3:
            is_maximizing = True if current_player_index == 0 else False
            best_score, best_move = minimax(board, turns, is_maximizing)
            if best_move is not None:
                row, col = best_move
                move = (row*3 + col) + 1

        board[row][col] = current_symbol
        print(f"{current_player} ({current_symbol}) selected the position {move}")    
        show_board(board)
       
        # Check for a winner
        if check_win(board, current_symbol):
            print("\n")
            show_board(board)
            print(f"{current_player} ({current_symbol}) wins!")
            game_over = True
            break
        
        # Check for a tie
        if turns == 8:
            print("\n")
            show_board(board)
            print("\nDraw!")
            game_over = True
            break
    
        turns += 1
        current_player_index = 1 - current_player_index

        
    # After the game ends and we have the game result
    player1_name = "Computer 1"
    player2_name = "Computer 2"
    result = "Draw" if turns == 9 else f"Computer {current_player_index+1}"
    insert_game_result(player1_name, player2_name, result, turns)
      
    while True:
        try:
            play_again = int(input("Do you want to play again?\n1. Yes\n2. No\n3. Return to main menu:"))
            if play_again == 1:
                print("\nStarting a new game...")
                computer_vs_computer(board, difficulty)  # Pass the difficulty as well
                break  # Break out of the loop after the game ends
            elif play_again == 2:
                print("Thank you for playing!")
                quit()
            elif play_again == 3:
                main()
                break  # Break out of the loop after the game ends
        except ValueError:
            print("Error: please enter 1 for 'Yes' or 2 for 'No'.")


def main():
    create_table()
    global board
    first_turn = 0
    board = ([-5, -5, -5], [-5, -5, -5], [-5, -5, -5])
    board_trans = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
   
    while True:       
        while True:
            try:
                mode = int(input("Choose:\n1. Human vs Human\n2. Human vs Computer\n3. Computer vs Computer\n4. Exit:"))
                if mode >= 1 and mode <= 4:
                    break
                elif mode == 4:
                    quit()
            except:
                print("Error")

        if mode == 1:
            # Human vs. Human
            while True:
                try:
                    a = int(input("Choose who goes first:\n1. Player (X)\n2. Player (O)\n"))
                    if a == 1 or a == 2:
                        # Ask players for their names at the beginning
                        player1_name = input("First player's name (X): ")
                        player2_name = input("Second player's name (O): ")
                        break
                except:
                    print("Error")

            if a == 1:
                first_turn = 0
            elif a == 2:
                first_turn = 1
                          
        # Για τις επιλογές 2 και 3 
        elif mode == 2 or mode ==3:
            
            while True:
                try:
                    # Choose difficulty level
                    print("Difficulty Levels:")
                    print("1. Easy")
                    print("2. Medium")
                    print("3. Hard")
                    difficulty = int(input("Choose difficulty level (1-3) or 4 to return to main menu: "))
                    if difficulty >= 1 and difficulty <= 3:
                        break
                    elif difficulty == 4:
                        main()
                    else:
                        print("Invalid response")
                except:
                    print("Error")

        elif mode == 4:
            print("Thank you for playing!")
            break     
              
        while True:           
            score_O = 0
            score_X = 0
            win = False
            turn = first_turn
            turns = 0

            while win == False and turns < 9:
                print(f"Turn {turns}")
                if turn == 0:
                    # print(f"Player {player1_name} (X)")
                     print(f"Player (X)")
                   
                else:
                    print(f"Player {player2_name} (O)")
                    # print(f"Player {player1_name} (X)")                    
                show_board(board_trans)
                # After the game ends and we have the game result

                match mode:
                    case 1:
                        a = human_to_human(board)                       
                    case 2:
                        a = computer_vs_human(difficulty)
                    case 3:
                        a = computer_vs_computer(difficulty)
                     
                turn_check = False
                while turn_check == False:                    
                    # Position selection is made here
                    match a:
                        case 1:
                            if turn == 0:
                                board[0][0] = 0
                                board_trans[0][0] = "X"
                                turn_check = True
                            else:
                                board[0][0] = 1
                                board_trans[0][0] = "O"
                                turn_check = True  

                        case 2:
                            if turn == 0:
                                board[0][1] = 0
                                board_trans[0][1] = "X"
                                turn_check = True
                            else:
                                board[0][1] = 1
                                board_trans[0][1] = "O"
                                turn_check = True  

                        case 3:
                            if turn == 0:
                                board[0][2] = 0
                                board_trans[0][2] = "X"
                                turn_check = True
                            else:
                                board[0][2] = 1
                                board_trans[0][2] = "O"
                                turn_check = True  

                        case 4:
                            if turn == 0:
                                board[1][0] = 0
                                board_trans[1][0] = "X"
                                turn_check = True
                            else:
                                board[1][0] = 1
                                board_trans[1][0] = "O"
                                turn_check = True  

                        case 5:
                            if turn == 0:
                                board[1][1] = 0
                                board_trans[1][1] = "X"
                                turn_check = True
                            else:
                                board[1][1] = 1
                                board_trans[1][1] = "O"
                                turn_check = True  

                        case 6:
                            if turn == 0:
                                board[1][2] = 0
                                board_trans[1][2] = "X"
                                turn_check = True
                            else:
                                board[1][2] = 1
                                board_trans[1][2] = "O"
                                turn_check = True  

                        case 7:
                            if turn == 0:
                                board[2][0] = 0
                                board_trans[2][0] = "X"
                                turn_check = True
                            else:
                                board[2][0] = 1
                                board_trans[2][0] = "O"
                                turn_check = True  

                        case 8:
                            if turn == 0:
                                board[2][1] = 0
                                board_trans[2][1] = "X"
                                turn_check = True
                            else:
                                board[2][1] = 1
                                board_trans[2][1] = "O"
                                turn_check = True  

                        case 9:
                            if turn == 0:
                                board[2][2] = 0
                                board_trans[2][2] = "X"
                                turn_check = True
                            else:
                                board[2][2] = 1
                                board_trans[2][2] = "O"
                                turn_check = True  

                    # Έλεγχος για νίκη ή ισοπαλία
                    win = check_win(board, turn)
                    if win:
                        show_board(board_trans)
                        if turn == 0:
                            print(f"Player {player1_name} (X) won")
                            score_X += 1
                        else:
                            print(f"Second player {player2_name} (O) won")
                            score_O += 1
                        
                    turns += 1
                    turn = 1 - turn

                if win == False and turns==9:
                    show_board(board_trans)             
                    print("Draw!")
            
            result = "Draw" if turns == 9 else f"{player1_name} (X)" if turn == 0 else f"{player2_name} (O)"
            insert_game_result(player1_name, player2_name, result, turns)     
                            
            while True:
                try:
                    board = ([-5, -5, -5], [-5, -5, -5], [-5, -5, -5])  # Επαναφορά του πίνακα σε κενή κατάσταση
                    board_trans = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]  # Επαναφορά του μεταφρασμένου πίνακα
                    a = int(input("Do you want to play again?\n1. Yes\n2. No \n3. Return to main menu:"))
                    if a == 3:
                        main()  
                    elif a == 2:
                        print("Thank you for playing!")
                        break 
                    elif a == 1:
                        show_board(board_trans)  # Show the empty board
                        break
                except:
                    print("Error")  


                match a:
                    case 1:
                        # Here is the system for changing the first player and alternating them:
                        if first_turn == 0:
                            first_turn = 1
                        else:
                            first_turn = 0
                        continue
            if a==2:
                break
        if a==2:
            break

            
if __name__ == "__main__":
    main()

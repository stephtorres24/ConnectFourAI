# Stephanie Torres
# Final Project: Connect Four AI
# COMP 151 AI

import random
import copy
import time
from datetime import datetime # for real time 

# global counter for node evaluations
node_count = 0

def create_board(): # function to create the initial game board 
    return [[0 for _ in range(7)] for _ in range(6)] 

def print_board(board): # printing the current state of the game board 
    print("\nConnect Four AI Game:")
    for row in reversed(board):
        row_str = '  '.join(
            '\033[95mX\033[0m' if cell == 1 else '\033[93mO\033[0m' if cell == 2 else '.' for cell in row # purple for the X and yellow for the O 
        )
        print(row_str)
    print("0  1  2  3  4  5  6") # column #s

def make_move(board, column, player): # placing the player's discs in the chosen column 
    for row in range(6):
        if board[row][column] == 0:
            board[row][column] = player
            return True
    return False 

def check_win(board, player): # checking to see if current player has won 
    for c in range(7):
        for r in range(6): # checking horizontal, vertical, and diagonal lines for a win
            if (c + 3 < 7 and all(board[r][c + i] == player for i in range(4))) or \
               (r + 3 < 6 and all(board[r + i][c] == player for i in range(4))) or \
               (c + 3 < 7 and r + 3 < 6 and all(board[r + i][c + i] == player for i in range(4))) or \
               (c + 3 < 7 and r - 3 >= 0 and all(board[r - i][c + i] == player for i in range(4))):
                return True
    return False

def is_valid_location(board, col): # to see if column choice is not full 
    return board[5][col] == 0

# minimax algo w/ alpha beta pruning
def minimax(board, depth, alpha, beta, is_maximizing, use_alpha_beta=True):
    global node_count
    node_count += 1

    result = check_terminal_state(board)
    if result != 0 or depth == 0:
        return result
    
    columns = list(range(7)) 
    random.shuffle(columns) # randomized column order to add variability to AIs play 

    if is_maximizing:
        max_eval = float('-inf')
        for col in columns:
            if is_valid_location(board, col):
                temp_board = copy.deepcopy(board)
                make_move(temp_board, col, 2)  # AI is player 2
                eval = minimax(temp_board, depth - 1, alpha, beta, False, use_alpha_beta)
                max_eval = max(max_eval, eval)
                if use_alpha_beta:
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for col in columns:
            if is_valid_location(board, col):
                temp_board = copy.deepcopy(board)
                make_move(temp_board, col, 1)  # human is player 1
                eval = minimax(temp_board, depth - 1, alpha, beta, True, use_alpha_beta)
                min_eval = min(min_eval, eval)
                if use_alpha_beta:
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def check_terminal_state(board): # to see if game has ended 
    if check_win(board, 1):
        return -1000
    elif check_win(board, 2):
        return 1000
    elif not any(0 in row for row in board):
        return 0
    return 0

def get_best_move(board, depth, use_alpha_beta=True): # determining best move for the AI 
    global node_count
    node_count = 0  # reseting node count for each move

    start_time = time.time()

    best_score = float('-inf')
    best_cols = []
    #best_col = random.choice([c for c in range(7) if is_valid_location(board, c)])
    for col in range(7):
        if is_valid_location(board, col):
            temp_board = copy.deepcopy(board)
            make_move(temp_board, col, 2)
            score = minimax(temp_board, depth - 1, float('-inf'), float('inf'), False, use_alpha_beta)
            if score > best_score:
                best_score = score
                best_cols = [col]
            elif score == best_score:
                best_cols.append(col)

    end_time = time.time()
    time_taken = end_time - start_time
    # randomly choosing best_cols
    best_col = random.choice(best_cols) if best_cols else random.choice([c for c in range(7) if is_valid_location(board, c)])

    return best_col, time_taken, node_count

def get_player_move(board): # to get the player's move
    while True:
        try:
            column = int(input("Your turn! Choose a column (0-6): "))
            if 0 <= column <= 6 and is_valid_location(board, column):
                return column
            else:
                print("Invalid column. Please choose a number between 0 and 6.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def play_game(mode, use_alpha_beta=True, result_file="game_results.txt"): # function so the game can be played 
    board = create_board()
    game_over = False
    current_player = 1  # starting with player 1 (human)
    ai_times = [] # to store times for AI moves
    ai_nodes = [] # to store nodes evaluated for AI moves 

    while not game_over:
        print_board(board)
        print(f"Player {'X' if current_player == 1 else 'O'}'s turn.")

        if mode == 1 and current_player == 1:  # human's turn in player vs AI mode
            column = get_player_move(board)
        else:  # AI's turn in both modes 
            print("AI is thinking...")
            time.sleep(1)
            column, time_taken, node_evaluated = get_best_move(board, 4, use_alpha_beta)
            ai_times.append(time_taken)
            ai_nodes.append(node_evaluated)
            print(f"AI placed in column {column}.")

        make_move(board, column, current_player)
        
        if check_win(board, current_player):
            game_over = True
            print_board(board)
            winner_symbol = 'X' if current_player == 1 else 'O'
            print(f"Player {winner_symbol} wins!")
        elif not any(0 in row for row in board):  # checking for tie
            game_over = True
            print_board(board)
            print("The game is a tie!")

        current_player = 3 - current_player  # switch players
    # storing the results in a file after game is over to see the difference adding Alpha-Beta pruning to minimax makes 
    with open(result_file, "a") as file:
        file.write(f"Game type: {'AI vs AI' if mode == 2 else 'Player vs AI'}, played {'with' if use_alpha_beta else 'without'} Alpha-Beta Pruning\n")
        file.write(f"Total time for AI moves: {sum(ai_times)} seconds\n")
        file.write(f"Total nodes evaluated for AI moves: {sum(ai_nodes)}\n")
        file.write(f"Individual move times: {ai_times}\n")
        file.write(f"Individual move nodes: {ai_nodes}\n")
        file.write(f"Game End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write("------------------------------------------------------------------------------\n\n")

    print("Thanks for playing!")

def show_menu(): # UI for game selection (two modes: Player vs AI or AI vs AI)
    print("Welcome to Connect Four AI!")
    print("1. Play against AI")
    print("2. AI vs AI")

    while True:
        try:
            choice = int(input("Please select a mode by entering the number (1 or 2): "))
            if choice in [1, 2]:
                return choice
            else:
                print("Invalid input. Please enter 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def main():
    user_choice = show_menu()

    # for storing results
    result_file_ai = "ai_vs_ai_results.txt"
    result_file_human = "human_vs_ai_results.txt"

    #open(result_file_ai, 'w').close() # clears previous results
    #open(result_file_human, 'w').close()

    if user_choice == 1:
        print("You selected: Play against AI.") # play against AI mode
        print("Playing w/ Alpha-Beta Pruning")
        play_game(mode=1, use_alpha_beta=True, result_file=result_file_human)
        print("\nPlaying w/out Alpha-Beta Pruning")
        play_game(mode=1, use_alpha_beta=False, result_file=result_file_human)
    elif user_choice == 2:
        print("You selected: AI vs AI.") # AI vs AI mode 
        print("Playing w/ Alpha-Beta Pruning")
        play_game(mode=2, use_alpha_beta=True, result_file=result_file_ai)
        print("\nPlaying w/out Alpha-Beta Pruning")
        play_game(mode=2, use_alpha_beta=False, result_file=result_file_ai)

if __name__ == "__main__":
    main()
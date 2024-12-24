import numpy as np
from connect4 import Connect4

PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4

connect4 = Connect4()

def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, connect4.COLUMN_COUNT//2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(connect4.ROW_COUNT):
        row_array = [int(i) for i in list(board[r,:])]
        for c in range(connect4.COLUMN_COUNT-3):
            window = row_array[c:c+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(connect4.COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:,c])]
        for r in range(connect4.ROW_COUNT-3):
            window = col_array[r:r+WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(connect4.ROW_COUNT-3):
        for c in range(connect4.COLUMN_COUNT-3):
            window = [board[r+i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(connect4.ROW_COUNT-3):
        for c in range(connect4.COLUMN_COUNT-3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == PLAYER_PIECE:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def is_terminal_node(board):
    return connect4.winning_move(PLAYER_PIECE) or connect4.winning_move(AI_PIECE) or len(get_valid_locations(board)) == 0

def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if connect4.winning_move(AI_PIECE):
                return (None, 100000000000000)
            elif connect4.winning_move(PLAYER_PIECE):
                return (None, -10000000000000)
            else: # Game is over, no more valid moves
                return (None, 0)
        else: # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if maximizingPlayer:
        value = -np.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = connect4.get_next_open_row(col)
            b_copy = board.copy()
            connect4.drop_piece(row, col, AI_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else: # Minimizing player
        value = np.inf
        column = np.random.choice(valid_locations)
        for col in valid_locations:
            row = connect4.get_next_open_row(col)
            b_copy = board.copy()
            connect4.drop_piece(row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth-1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

def get_valid_locations(board):
    valid_locations = []
    for col in range(connect4.COLUMN_COUNT):
        if connect4.is_valid_location(col):
            valid_locations.append(col)
    return valid_locations

def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = np.random.choice(valid_locations)
    for col in valid_locations:
        row = connect4.get_next_open_row(col)
        temp_board = board.copy()
        connect4.drop_piece(row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

def get_ai_move(board):
    col, minimax_score = minimax(board, 5, -np.inf, np.inf, True)
    return col

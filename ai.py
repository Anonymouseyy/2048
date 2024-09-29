import copy

import helpers as h

all_moves = [h.move_up, h.move_down, h.move_left, h.move_right]


def calculate_final_score(board):
    pass


def calculate_move_score(board, current_depth, max_depth):
    best_score = 0

    for move in all_moves:
        new_board = move(board)
        if new_board != board:
            score = generate_score(new_board, current_depth+1, max_depth)
            best_score = max(best_score, score)

    return best_score


def generate_score(board, current_depth=0, max_depth=4):
    if current_depth >= max_depth:
        return calculate_final_score(board)

    total_score = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if not board[i][j]:
                new_board_2 = copy.deepcopy(board)
                new_board_2[i][j] = 2
                move_score_2 = calculate_move_score(new_board_2, current_depth, max_depth)

                new_board_4 = copy.deepcopy(board)
                new_board_4[i][j] = 4
                move_score_4 = calculate_move_score(new_board_4, current_depth, max_depth)

                total_score += 0.9 * move_score_2 + 0.1 * move_score_4

    return total_score


def simulate_move(board, move):
    new_board = move(board)

    if new_board == board:
        return 0
    else:
        return generate_score(new_board)


def find_best_move(board):
    best_move = None
    best_score = -1

    for move in all_moves:
        score = simulate_move(board, move)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

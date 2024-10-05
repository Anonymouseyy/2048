import copy

import helpers as h

all_moves = [h.move_up, h.move_down, h.move_left, h.move_right]

MERGE_BIAS = 1
MONOTONICITY_BIAS = 1


def num_merges(selection):
    merges = 0
    i = 0
    while i < len(selection) - 1:
        if selection[i] == selection[i + 1] and selection[i] != 0:
            merges += 1
            i += 2
        else:
            i += 1
    return merges


def monotonicity(selection):
    mono = 0

    for i in range(len(selection) - 1):
        if selection[i] < selection[i+1]:
            mono += 1

    return mono


def calculate_final_score(board):
    score = 0

    for row in board:
        score += MERGE_BIAS * num_merges(row)
        score += MONOTONICITY_BIAS * monotonicity(row)

    col_board = [[board[i][j] for j in range(len(board))] for i in range(len(board))]

    for col in col_board:
        score += MERGE_BIAS * num_merges(col)
        score += MONOTONICITY_BIAS * monotonicity(col)

    print(score)
    return score


def calculate_move_score(board, current_depth, max_depth):
    best_score = 0

    for move in all_moves:
        new_board = move(board)[0]
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
    new_board = move(board)[0]

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

import copy
import helpers as h

all_moves = [h.move_up, h.move_down, h.move_left, h.move_right]

MERGE_BIAS = 1
MERGE_SCORE_BIAS = 2
HORIZONTAL_MONOTONICITY_BIAS = 500
VERTICAL_MONOTONICITY_BIAS = 300
EMPTY_TILE_BIAS = 100

GRADIENT = [
    [1,     8,     4,     2],
    [16,    32,    64,    128],
    [2048,  1024,  512,   256],
    [4096,  8192,  16384, 32768],
]


def num_merges(selection):
    merges = 0
    score = 0
    i = 0
    while i < len(selection) - 1:
        if selection[i] == selection[i + 1] and selection[i] != 0:
            merges += 1
            score += 2 * selection[i]
            i += 2
        else:
            i += 1
    return merges, score


def monotonicity(selection):
    inc, dec = 0, 0
    for i in range(len(selection) - 1):
        if selection[i] <= selection[i + 1]:
            inc += 1
        elif selection[i] >= selection[i + 1]:
            dec += 1
    return max(inc, dec)


def calculate_final_score(board):
    score = 0
    merge_score = 0
    empty_tiles = 0

    for row in board:
        merges, m_score = num_merges(row)
        merge_score += m_score
        score += MERGE_BIAS * merges
        score += HORIZONTAL_MONOTONICITY_BIAS * monotonicity(row)
        empty_tiles += row.count(0)

    for j in range(4):
        col = [board[i][j] for i in range(4)]
        merges, m_score = num_merges(col)
        merge_score += m_score
        score += MERGE_BIAS * merges
        score += VERTICAL_MONOTONICITY_BIAS * monotonicity(col)

    for i in range(4):
        for j in range(4):
            score += board[i][j] * GRADIENT[i][j]

    score += EMPTY_TILE_BIAS * empty_tiles
    score += MERGE_SCORE_BIAS * merge_score

    return score


def calculate_move_score(board, current_depth, max_depth):
    best_score = 0
    for move in all_moves:
        new_board = move(copy.deepcopy(board))[0]
        if new_board != board:
            score = generate_score(new_board, current_depth + 1, max_depth)
            best_score = max(best_score, score)
    return best_score


def generate_score(board, current_depth=0, max_depth=2):
    if current_depth >= max_depth:
        return calculate_final_score(board)

    total_score = 0
    empty = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]

    if not empty:
        return calculate_final_score(board)

    for i, j in empty:
        board_2 = copy.deepcopy(board)
        board_2[i][j] = 2
        score_2 = calculate_move_score(board_2, current_depth, max_depth)

        board_4 = copy.deepcopy(board)
        board_4[i][j] = 4
        score_4 = calculate_move_score(board_4, current_depth, max_depth)

        total_score += 0.9 * score_2 + 0.1 * score_4

    return total_score / len(empty)


def find_best_move(board):
    best_move = None
    best_score = float('-inf')

    for move in all_moves:
        new_board = move(copy.deepcopy(board))[0]
        if new_board != board:
            score = generate_score(new_board)
            if score > best_score:
                best_score = score
                best_move = move

    return best_move

import helpers as h

all_moves = [h.move_up, h.move_down, h.move_left, h.move_right]


def simulate_move(board, move):
    new_board = move(board)
    score = 0

    return score


def find_best_move(board):
    best_move = None
    best_score = -1

    for move in all_moves:
        score = simulate_move(board, move)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

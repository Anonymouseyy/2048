import helpers as h

all_moves = [h.move_up, h.move_down, h.move_left, h.move_right]


def generate_score(board, current_depth=0, max_depth=4):
    pass


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

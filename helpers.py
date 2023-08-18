import copy

import pygame as pg
import random


def empty_state():
    return [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]


def get_empty_spaces(board):
    empty = []

    for i in range(len(board)):
        for j in range(len(board[i])):
            if not board[i][j]:
                empty.append((i, j))

    return empty


def insert_random(board, valids=None):
    if valids is None:
        valids = [2, 2, 2, 4]

    empty = get_empty_spaces(board)
    i, j = random.choice(empty)
    board[i][j] = random.choice(valids)
    return board


def initial_state():
    board = empty_state()

    for _ in range(2):
        board = insert_random(board)

    return board


def move_up(board):
    points = 0

    for i in range(len(board)):
        # Create list of column elements
        col = [board[x][i] for x in range(len(board))]

        if col.count(0) == len(col):
            continue

        # Move all elements to the left
        j = 0
        while j <= len(col) - 1:
            if not col[j]:
                col.pop(j)
                col.append(0)

                if not any(col[j + 1:]):
                    break
            else:
                j += 1

        # Combine like elements
        j = 0
        while j <= len(col) - 2:
            if col[j] == col[j + 1]:
                points += 2*col[j]
                col[j] += col[j]
                col.pop(j + 1)
                col.append(0)
            j += 1

        # Insert column into board
        for j in range(len(board)):
            board[j][i] = col[j]

    return board, points


def move_down(board):
    points = 0

    for i in range(len(board)):
        # Create list of column elements
        col = [board[x][i] for x in range(len(board))]

        if col.count(0) == len(col):
            continue

        # Move all elements to right of list (down)
        j = len(col) - 1
        while j >= 0:
            if not col[j]:
                col.pop(j)
                col.insert(0, 0)

                if not any(col[:j + 1]):
                    break
            else:
                j -= 1

        # Combine like elements
        j = len(col) - 1
        while j >= 1:
            if col[j] == col[j - 1]:
                points += 2*col[j]
                col[j] += col[j]
                col.pop(j - 1)
                col.insert(0, 0)
            j -= 1

        # Insert column into board
        for j in range(len(board)):
            board[j][i] = col[j]

    return board, points


def move_left(board):
    points = 0

    for i in range(len(board)):
        row = board[i]

        if row.count(0) == len(row):
            continue

        # Move all elements to the left
        j = 0
        while j <= len(row)-1:
            if not row[j]:
                row.pop(j)
                row.append(0)

                if not any(row[j + 1:]):
                    break
            else:
                j += 1

        # Combine like elements
        j = 0
        while j <= len(row) - 2:
            if row[j] == row[j+1]:
                points += 2*row[j]
                row[j] += row[j]
                row.pop(j+1)
                row.append(0)
            j += 1

    return board, points


def move_right(board):
    points = 0

    for i in range(len(board)):
        row = board[i]

        if row.count(0) == len(row):
            continue

        # Move all elements to right
        j = len(row)-1
        while j >= 0:
            if not row[j]:
                row.pop(j)
                row.insert(0, 0)

                if not any(row[:j + 1]):
                    break
            else:
                j -= 1

        # Combine like elements
        j = len(row) - 1
        while j >= 1:
            if row[j] == row[j-1]:
                points += 2*row[j]
                row[j] += row[j]
                row.pop(j-1)
                row.insert(0, 0)
            j -= 1

    return board, points


def check_lost_state(board):
    if any([not all(r) for r in board]):
        return False

    return move_up(board)[0] == board and move_down(board)[0] == board and move_left(board)[0] == board and move_right(board)[0] == board

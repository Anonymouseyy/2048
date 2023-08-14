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


def move_right(board):
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
                row[j] += row[j]
                row.pop(j-1)
                row.insert(0, 0)
            j -= 1

    return board


def move_left(board):
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
                row[j] += row[j]
                row.pop(j+1)
                row.append(0)
            j += 1

    return board

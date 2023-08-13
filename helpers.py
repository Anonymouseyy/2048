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


def insert_random(board, valids):
    empty = get_empty_spaces(board)
    i, j = random.choice(empty)
    board[i][j] = random.choice(valids)
    return board


def initial_state():
    board = empty_state()
    valid_start = [2, 2, 2, 4]

    for _ in range(2):
        board = insert_random(board, valid_start)

    return board

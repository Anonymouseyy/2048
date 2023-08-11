import pygame as pg
import random


def empty_state():
    return [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]


def initial_state():
    board = empty_state()
    valid_start = [2, 4, 2048]

    j, k = random.randint(0, 1), random.randint(0, 3)
    board[j][k] = random.choice(valid_start)

    j, k = random.randint(2, 3), random.randint(0, 3)
    board[j][k] = random.choice(valid_start)

    return board

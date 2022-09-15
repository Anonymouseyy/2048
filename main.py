import pygame as pg
import sys

import helpers as h

pg.init()
size = width, height = 600, 700

black = (0, 0, 0)
white = (255, 255, 255)
bg_gray = (250, 248, 239)

screen = pg.display.set_mode(size)
pg.display.set_caption('2048')

mediumFont = pg.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pg.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pg.font.Font("OpenSans-Regular.ttf", 60)

board = h.initial_state()

while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()
    
    screen.fill(bg_gray)

    pg.display.flip()
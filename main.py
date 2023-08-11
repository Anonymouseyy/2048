import pygame as pg
import sys

import helpers as h

pg.init()
width, height = 600, 700

black = (0, 0, 0)
white = (255, 255, 255)
bg_gray = (250, 248, 239)
board_color = (187, 173, 160)
tile_colors = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (241, 173, 113),
    16: (245, 149, 99),
    32: (246, 124, 96),
    64: (246, 94, 59),
    128: (237, 207, 115),
    256: (237, 204, 98),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 45)
}
empty_color = (205, 193, 180)

screen = pg.display.set_mode((width, height), pg.RESIZABLE)
pg.display.set_caption('2048')

mediumFont = pg.font.Font("OpenSans-Regular.ttf", 28)
largeFont = pg.font.Font("OpenSans-Regular.ttf", 40)
moveFont = pg.font.Font("OpenSans-Regular.ttf", 60)

board = h.initial_state()


def draw_board():
    global board, screen, board_color

    dim = min((5*width)/6, (5*height)/7)
    board_back = pg.Rect(0, 0, dim ,dim)
    board_back.center = (width//2, height//2+(5*height)/70)
    pg.draw.rect(screen, board_color, board_back, border_radius=10)

    for row_num, row in enumerate(board):
        for spot_num, spot in enumerate(row):
            spot_rect = pg.Rect(0, 0, 0.23*dim, 0.23*dim)
            spot_rect.topleft = (board_back.topleft[0]+(row_num*(0.246*dim)+(0.016*dim)),
                                 board_back.topleft[1]+(spot_num*(0.246*dim)+(0.016*dim)))
            tile_color = tile_colors[spot] if spot in tile_colors else (60, 58, 50)
            pg.draw.rect(screen, tile_color, spot_rect, border_radius=5)

            if not spot == 0:
                num = largeFont.render(f'{spot}', True, (34, 34, 34) if spot == 2 or spot == 4 else (249, 246, 242))
                num_rect = num.get_rect()
                num_rect.center = spot_rect.center
                screen.blit(num, num_rect)


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

    width, height = screen.get_size()
    screen.fill(bg_gray)
    draw_board()

    pg.display.flip()
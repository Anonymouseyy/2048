import pygame as pg
import sys, copy, time

import helpers as h

pg.init()
clock = pg.time.Clock()
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
score = 0

screen = pg.display.set_mode((width, height), pg.RESIZABLE)
pg.display.set_caption('2048')

moveFont = pg.font.Font("OpenSans-Regular.ttf", 40)
textFont = pg.font.Font("OpenSans-Regular.ttf", 40)
moveFont.bold = True

board = h.initial_state()
c_board = h.initial_state()
lost = False
transition = 0
transition_steps = 10


def other_ui():
    dim = min((5 * width) / 6, (5 * height) / 7)
    board_back = pg.Rect(0, 0, dim, dim)
    board_back.center = (width // 2, height // 2 + (5 * height) / 70)

    score_back = pg.Rect(board_back.topleft[0], height / 20, dim / 3, height / 10)
    pg.draw.rect(screen, board_color, score_back, border_radius=10)

    score_text = moveFont.render(f'{score}', True, (34, 34, 34))
    score_text_rect = score_text.get_rect()
    score_text_rect.center = score_back.center
    screen.blit(score_text, score_text_rect)

    restart_button = pg.Rect(board_back.topright[0] - dim / 3, height / 20, dim / 3, height / 10)
    restart = textFont.render("Restart", True, black)
    restart_rect = restart.get_rect()
    restart_rect.center = restart_button.center
    pg.draw.rect(screen, (157, 143, 130) if restart_button.collidepoint(pg.mouse.get_pos()) else board_color,
                 restart_button, border_radius=10)
    screen.blit(restart, restart_rect)

    return restart_button


def draw_board():
    dim = min((5 * width) / 6, (5 * height) / 7)
    board_back = pg.Rect(0, 0, dim, dim)
    board_back.center = (width // 2, height // 2 + (5 * height) / 70)
    pg.draw.rect(screen, board_color, board_back, border_radius=10)

    for row_num, row in enumerate(board):
        for spot_num, spot in enumerate(row):
            spot_rect = pg.Rect(0, 0, 0.23*dim, 0.23*dim)
            spot_rect.topleft = (board_back.topleft[0]+(spot_num*(0.246*dim)+(0.016*dim)),
                                 board_back.topleft[1]+(row_num*(0.246*dim)+(0.016*dim)))
            tile_color = tile_colors[spot] if spot in tile_colors else (60, 58, 50)
            pg.draw.rect(screen, tile_color, spot_rect, border_radius=5)

            if spot:
                num = moveFont.render(f'{spot}', True, (34, 34, 34) if spot == 2 or spot == 4 else (249, 246, 242))
                num_rect = num.get_rect()
                num_rect.center = spot_rect.center
                screen.blit(num, num_rect)


def transition_board(step):
    pass


def lost_display():
    dim = min((5 * width) / 6, (5 * height) / 7)
    overlay = pg.Surface((dim, dim))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, ((width//2)-dim/2, height//2+(5*height)/70-dim/2))

    lost_back = pg.Rect(0, 0, dim / 2, height / 10)
    lost_back.center = (width // 2, height // 2)
    pg.draw.rect(screen, board_color, lost_back, border_radius=10)

    lost_text = textFont.render('Game Over', True, (34, 34, 34))
    lost_text_rect = lost_text.get_rect()
    lost_text_rect.center = lost_back.center
    screen.blit(lost_text, lost_text_rect)

    retry_button = pg.Rect(0, 0, dim / 2.5, height / 10)
    retry_button.center = lost_text_rect.center
    retry_button.y += height / 8
    retry = textFont.render("Try Again", True, black)
    retry_rect = retry.get_rect()
    retry_rect.center = retry_button.center
    pg.draw.rect(screen, (157, 143, 130) if retry_button.collidepoint(pg.mouse.get_pos()) else board_color,
                 retry_button, border_radius=10)
    screen.blit(retry, retry_rect)

    return retry_button


while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            sys.exit()

        if event.type == pg.KEYDOWN and not transition:
            points = None

            if event.key == pg.K_w or event.key == pg.K_UP and not lost:
                c_board = copy.deepcopy(board)
                board, points = h.move_up(board)

            if event.key == pg.K_s or event.key == pg.K_DOWN and not lost:
                c_board = copy.deepcopy(board)
                board, points = h.move_down(board)

            if event.key == pg.K_a or event.key == pg.K_LEFT and not lost:
                c_board = copy.deepcopy(board)
                board, points = h.move_left(board)

            if event.key == pg.K_d or event.key == pg.K_RIGHT and not lost:
                c_board = copy.deepcopy(board)
                board, points = h.move_right(board)

            if c_board != board:
                transition = 1
                board = h.insert_random(board)
                score += points

            if event.key == pg.K_r:
                board, score = h.initial_state(), 0
                lost = False
                transition = 0

    width, height = screen.get_size()
    lost = h.check_lost_state(copy.deepcopy(board))
    screen.fill(bg_gray)

    if transition and transition < transition_steps:
        transition_board(transition)
    elif transition == transition_steps:
        transition = 0
    else:
        draw_board()

    restart_button = other_ui()
    lost_button = None
    if lost:
        lost_button = lost_display()

    click, _, _ = pg.mouse.get_pressed()
    if click == 1:
        mouse = pg.mouse.get_pos()

        if restart_button.collidepoint(mouse):
            time.sleep(0.2)
            board, score = h.initial_state(), 0
            lost = False
            transition = 0

        if lost and lost_button.collidepoint(mouse):
            time.sleep(0.2)
            board, score = h.initial_state(), 0
            lost = transition = 0

    clock.tick(60)
    pg.display.flip()

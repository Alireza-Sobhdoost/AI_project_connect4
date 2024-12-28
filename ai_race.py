import pygame
import sys
from min_max import get_ai_move
from connect4 import (
    create_board,
    drop_piece,
    is_valid_location,
    get_next_open_row,
    print_board,
    winning_move,
    draw_board,
    RED,
    YELLOW,
    BLACK,
    SQUARESIZE,
    width,
    size,
    RADIUS
)

AI1 = 0
AI2 = 1

if __name__ == '__main__':
    board = create_board()
    print_board(board)
    game_over = False
    turn = AI1

    pygame.init()

    screen = pygame.display.set_mode(size)
    draw_board(board, screen)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        if turn == AI1 and not game_over:
            col = get_ai_move(board, 6)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 1)

                if winning_move(board, 1):
                    label = myfont.render("AI 1 wins!!", 1, RED)
                    screen.blit(label, (40,10))
                    game_over = True

                print_board(board)
                draw_board(board, screen)

                turn = AI2

        if turn == AI2 and not game_over:
            col = get_ai_move(board, 6)

            if is_valid_location(board, col):
                pygame.time.wait(500)
                row = get_next_open_row(board, col)
                drop_piece(board, row, col, 2)

                if winning_move(board, 2):
                    label = myfont.render("AI 2 wins!!", 1, YELLOW)
                    screen.blit(label, (40,10))
                    game_over = True

                print_board(board)
                draw_board(board, screen)

                turn = AI1

        if game_over:
            pygame.time.wait(3000)

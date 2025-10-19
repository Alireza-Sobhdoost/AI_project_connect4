import pygame
import sys
import math
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


PLAYER = 0
AI = 1

if __name__ == '__main__':
    board = create_board()
    print_board(board)
    game_over = False
    turn = PLAYER

    pygame.init()

    screen = pygame.display.set_mode(size)
    draw_board(board, screen)
    pygame.display.update()

    myfont = pygame.font.SysFont("monospace", 75)

    while True:    

        while not game_over:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if turn == PLAYER:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                    if turn == PLAYER:
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))

                        if is_valid_location(board, col):
                            row = get_next_open_row(board, col)
                            drop_piece(board, row, col, 1)

                            if winning_move(board, 1):
                                label = myfont.render("Player 1 wins!!", 1, RED)
                                screen.blit(label, (40,10))
                                game_over = True

                            turn = AI
                            print_board(board)
                            draw_board(board, screen)

            if turn == AI and not game_over:
                col = get_ai_move(board, 5)

                if is_valid_location(board, col):
                    pygame.time.wait(500)
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("AI wins!!", 1, YELLOW)
                        screen.blit(label, (40,10))
                        game_over = True

                    print_board(board)
                    draw_board(board, screen)

                    turn = PLAYER

            if game_over:
                pygame.time.wait(3000)

                board = create_board()
                print_board(board)
                draw_board(board, screen)
                game_over = False
                turn = PLAYER

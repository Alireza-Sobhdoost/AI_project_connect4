import numpy as np
import pygame
import sys
import math
from min_max import get_ai_move
from connect4 import Connect4


if __name__ == '__main__':
    game = Connect4()
    game_over = False
    turn = game.PLAYER

    pygame.init()

    screen = pygame.display.set_mode(game.size)
    game.draw_board(screen)
    pygame.display.update()

    my_font = pygame.font.SysFont("monospace", 75)

    while not game_over:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, game.BLACK, (0, 0, game.width, game.SQUARESIZE))
                posx = event.pos[0]
                if turn == game.PLAYER:
                    pygame.draw.circle(screen, game.RED, (posx, int(game.SQUARESIZE / 2)), game.RADIUS)
            pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, game.BLACK, (0, 0, game.width, game.SQUARESIZE))
                if turn == game.PLAYER:
                    posx = event.pos[0]
                    col = int(math.floor(posx / game.SQUARESIZE))

                    if game.is_valid_location(col):
                        row = game.get_next_open_row(col)
                        game.drop_piece(row, col, 1)

                        if game.winning_move(1):
                            label = my_font.render("Player 1 wins!!", 1, game.RED)
                            screen.blit(label, (40, 10))
                            game_over = True

                        turn = game.AI
                        game.print_board()
                        game.draw_board(screen)

        if turn == game.AI and not game_over:
            col = get_ai_move(game.board)

            if game.is_valid_location(col):
                pygame.time.wait(500)
                row = game.get_next_open_row(col)
                game.drop_piece(row, col, 2)

                if game.winning_move(2):
                    label = my_font.render("AI wins!!", 1, game.YELLOW)
                    screen.blit(label, (40, 10))
                    game_over = True

                game.print_board()
                game.draw_board(screen)

                turn = game.PLAYER

        if game_over:
            pygame.time.wait(3000)

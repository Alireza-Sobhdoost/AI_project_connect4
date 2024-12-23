import pygame
import sys
import math
from Board import Board  # Import the refactored Board class
from Mcts import *
import time
# from test import tune_mcts
# Define colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
COLUMN_COUNT = 7
ROW_COUNT = 6
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# Initialize pygame
pygame.init()

# Define screen dimensions
width = COLUMN_COUNT* SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE
size = (width, height)

screen = pygame.display.set_mode(size)
pygame.display.set_caption("Connect Four")

# Font for rendering text
myfont = pygame.font.SysFont("monospace", 75)


def draw_board(board: Board):
    """Draw the game board on the screen."""
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for (row, col), piece in board.position.items():
        if piece == 1:
            pygame.draw.circle(screen, RED, (int(col * SQUARESIZE + SQUARESIZE / 2), height - int(row * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
        elif piece == 2:
            pygame.draw.circle(screen, YELLOW, (int(col * SQUARESIZE + SQUARESIZE / 2), height - int(row * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


def main():
    # Create the board
    board = Board()
    Agent = MCTS()
    draw_board(board)

    game_over = False
    turn = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                color = RED if turn == 0 else YELLOW
                pygame.draw.circle(screen, color, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARESIZE))

                if board.is_valid_location(col):
                    row = board.get_next_open_row(col)
                    board.drop_piece(row, col, board.player_1 if turn == 0 else board.player_2)

                    if board.winning_move(board.player_1 if turn == 0 else board.player_2):
                        winner = "Player 1" if turn == 0 else "Player 2"
                        label = myfont.render(f"{winner} wins!!", 1, RED if turn == 0 else YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

                    draw_board(board)
                    if game_over:
                        pygame.time.wait(3000)
                    turn = (turn + 1) % 2
                    
                if not game_over:
                    best_move = Agent.search(board)
                    board = best_move.board
                    if board.winning_move(2):
                        winner = "Player 1" if turn == 0 else "Player 2"
                        label = myfont.render(f"{winner} wins!!", 1, RED if turn == 0 else YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True
                    turn = (turn + 1) % 2
                draw_board(board)
                if game_over:
                    pygame.time.wait(1000)


if __name__ == "__main__":
	main()
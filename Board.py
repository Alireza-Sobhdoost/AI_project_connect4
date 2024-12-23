from copy import deepcopy
import numpy as np


class Board:

    def __init__(self, row_count = 6, column_count = 7 ,board=None):
        # define players
        self.player_1 = 1
        self.player_2 = 2
        self.empty_square = 0
        self.row_count = row_count
        self.column_count = column_count
        self.position = {}
        self.create_board()


        if board is not None:
            self.__dict__ = deepcopy(board.__dict__)


    def create_board(self):
        for i in range (self.row_count):
            for j in range (self.column_count): 
                self.position[i,j] = self.empty_square

    

    def drop_piece(self, row, col, piece):
        self.position[row, col] = piece

    def is_valid_location(self, col):
        return self.position[self.row_count - 1, col] == 0

    def get_next_open_row(self, col):
        for r in range(self.row_count):
            if self.position[r, col] == 0:
                return r
        return None

    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.position[::-1]])

    def winning_move(self, piece):
        # Check horizontal locations for win
        for c in range(self.column_count-3):
            for r in range(self.row_count):
                if self.position[r,c] == piece and self.position[r,c+1] == piece and self.position[r,c+2] == piece and self.position[r,c+3] == piece:
                    return True

        # Check vertical locations for win
        for c in range(self.column_count):
            for r in range(self.row_count-3):
                if self.position[r,c] == piece and self.position[r+1,c] == piece and self.position[r+2,c] == piece and self.position[r+3,c] == piece:
                    return True

        # Check positively sloped diaganols
        for c in range(self.column_count-3):
            for r in range(self.row_count-3):
                if self.position[r,c] == piece and self.position[r+1,c+1] == piece and self.position[r+2,c+2] == piece and self.position[r+3,c+3] == piece:
                    return True

        # Check negatively sloped diaganols
        for c in range(self.column_count-3):
            for r in range(3, self.row_count):
                if self.position[r,c] == piece and self.position[r-1,c+1] == piece and self.position[r-2,c+2] == piece and self.position[r-3,c+3] == piece:
                    return True

    def check_draw(self):
        count = 0
        for i in range(self.row_count):
            for j in range(self.column_count):
                if self.position[i, j] == 0:
                    count += 1
        return count
    def generate_states(self):
        states = []
        for col in range(self.column_count):
            if self.is_valid_location(col):
                new_state = deepcopy(self)
                row = new_state.get_next_open_row(col)
                new_state.drop_piece(row, col, self.player_2)
                states.append(new_state)
        return states
    
    def potential_winning_lines(self):
        lines = []
        rows, cols = self.row_count , self.column_count

        # Horizontal lines
        for r in range(rows):
            for c in range(cols - 3):
                line = [self.position[r, c + i] for i in range(4)]
                lines.append(line)

        # Vertical lines
        for c in range(cols):
            for r in range(rows - 3):
                line = [self.position[r + i, c] for i in range(4)]
                lines.append(line)

        # Positive diagonal lines
        for r in range(rows - 3):
            for c in range(cols - 3):
                line = [self.position[r + i, c + i] for i in range(4)]
                lines.append(line)

        # Negative diagonal lines
        for r in range(3, rows):
            for c in range(cols - 3):
                line = [self.position[r - i, c + i] for i in range(4)]
                lines.append(line)

        return lines

b = Board()
print(b.position)
b.is_valid_location(0)
'''
Minesweeper python project.
it build the classic minesweeper game in the command line. This project focuses on recursion and classes.
'''

import random
import re

class Board:
    def __init__(self, dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs
        self.board = self.make_new_board()
        self.assign_values_to_board()
        self.dug = set()

    def make_new_board(self):
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        bombs_planted = 0

        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1)
            row, col = divmod(loc, self.dim_size)

            if board[row][col] == '*':
                continue

            board[row][col] = '*'
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] != '*':
                    self.board[r][c] = self.get_num_neighboring_bombs(r, c)

    def get_num_neighboring_bombs(self, row, col):
        count = 0
        for r in range(max(0, row-1), min(self.dim_size, row+2)):
            for c in range(max(0, col-1), min(self.dim_size, col+2)):
                if r == row and c == col:
                    continue
                if self.board[r][c] == '*':
                    count += 1
        return count

    def dig(self, row, col):
        self.dug.add((row, col))

        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True

        for r in range(max(0, row-1), min(self.dim_size, row+2)):
            for c in range(max(0, col-1), min(self.dim_size, col+2)):
                if (r, c) not in self.dug:
                    self.dig(r, c)

        return True

    def __str__(self):
        visible_board = [[' ' for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if (r, c) in self.dug:
                    visible_board[r][c] = str(self.board[r][c])

        display = '   ' + ' '.join([f'{i}' for i in range(self.dim_size)]) + '\n'
        for i, row in enumerate(visible_board):
            display += f'{i} |' + '|'.join(row) + '|\n'
        return display

def play(dim_size=10, num_bombs=10):
    board = Board(dim_size, num_bombs)
    safe = True

    while len(board.dug) < dim_size ** 2 - num_bombs:
        print(board)
        try:
            user_input = input("Where would you like to dig? (row,col): ")
            row, col = map(int, re.findall(r'\d+', user_input))
            if row not in range(dim_size) or col not in range(dim_size):
                print("Invalid location. Try again.")
                continue
        except (ValueError, IndexError):
            print("Invalid input format. Use row,col (e.g. 1,3)")
            continue

        safe = board.dig(row, col)
        if not safe:
            break

    if safe:
        print("🎉 Congratulations! You cleared the minefield!")
    else:
        print("💥 Game Over. You hit a bomb.")
        board.dug = {(r, c) for r in range(dim_size) for c in range(dim_size)}
        print(board)

if __name__ == '__main__':
    play()

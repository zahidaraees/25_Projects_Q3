'''
Tic-Tac-Toe Python Project

'''

import math
import random

class Player:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        pass


class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        available = game.available_moves()
        if not available:
            return None  # Prevent error if no moves left
        return random.choice(available)


class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        valid_square = False
        val = None
        while not valid_square:
            square = input(self.letter + "'s turn. Input move (0-8): ").strip()

            if not square.isdigit():  # Ensures input is a number
                print("Invalid input! Please enter a number between 0 and 8.")
                
                continue  # This was outside the while loop

            val = int(square)  # Convert to integer safely

            if val not in game.available_moves():
                print("Invalid square. Try again!")
            else:
                valid_square = True  # Valid input, exit loop

        return val
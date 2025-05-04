'''
What is a Sudoku Puzzle?
In the Sudoku puzzle, we need to fill in every empty box with an integer between 1 and 9 in such a way that every number from 1 up to 9 appears once in every row, every column, and every one of the small 3 by 3 boxes highlighted with thick borders.
'''
import re

def display_sudoku(puzzle):
    """Display the Sudoku grid properly formatted."""
    print("\n🎯 Sudoku Grid:\n")
    for i, row in enumerate(puzzle):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  # Draw horizontal separator after every 3 rows
        
        row_display = ""
        for j, num in enumerate(row):
            if j % 3 == 0 and j != 0:
                row_display += " | "  # Vertical separator after every 3 columns
            
            row_display += str(num if num != -1 else ".") + " "  # Display empty cells as "."
        
        print(row_display)
    print("\n")

def is_valid(puzzle, guess, row, col):
    """Check if a number can be placed at (row, col)."""
    if guess in puzzle[row]:
        return False  # Number exists in row

    if guess in [puzzle[i][col] for i in range(9)]:
        return False  # Number exists in column  

    row_start, col_start = (row // 3) * 3, (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False  # Number exists in 3x3 grid

    return True  # If all checks pass, return True

def is_solved(puzzle):
    """Check if the puzzle is solved (no empty spaces left)."""
    for row in puzzle:
        if -1 in row:
            return False  # Still unsolved
    return True

def play_sudoku(puzzle):
    """Let the user play the Sudoku game."""
    while not is_solved(puzzle):
        display_sudoku(puzzle)

        try:
            user_input = input("📍 Enter move (row,col,number) or 'q' to quit: ")
            if user_input.lower() == 'q':
                print("👋 Exiting the game. See you next time!")
                return
            
            user_input = re.split(r',\s*', user_input)  # Allow inputs like "1,2,3" or "1, 2, 3"
            if len(user_input) != 3:
                print("❌ Invalid format! Use 'row,col,number' (Example: 1,2,3)")
                continue

            row, col, guess = map(int, user_input)
            row, col = row - 1, col - 1  # Convert to 0-based index

            if row < 0 or row >= 9 or col < 0 or col >= 9:
                print("❌ Invalid row/column! Must be between 1-9.")
                continue

            if puzzle[row][col] != -1:
                print("❌ Cell already filled! Choose an empty spot.")
                continue

            if not (1 <= guess <= 9):
                print("❌ Invalid number! Enter a number between 1-9.")
                continue

            if is_valid(puzzle, guess, row, col):
                puzzle[row][col] = guess  # Place the guess
                print("✅ Move accepted!")
            else:
                print("❌ Invalid move! This number cannot be placed here.")

        except ValueError:
            print("❌ Invalid input! Enter numbers only (Example: 1,2,3)")

    print("🎉 Congratulations! You've solved the Sudoku puzzle! 🎯")
    display_sudoku(puzzle)

def main():
    """Start the Sudoku game for the user."""
    sudoku_puzzle = [
        [5, 3, -1, -1, 7, -1, -1, -1, -1],
        [6, -1, -1, 1, 9, 5, -1, -1, -1],
        [-1, 9, 8, -1, -1, -1, -1, 6, -1],
        [8, -1, -1, -1, 6, -1, -1, -1, 3],
        [4, -1, -1, 8, -1, 3, -1, -1, 1],
        [7, -1, -1, -1, 2, -1, -1, -1, 6],
        [-1, 6, -1, -1, -1, -1, 2, 8, -1],
        [-1, -1, -1, 4, 1, 9, -1, -1, 5],
        [-1, -1, -1, -1, 8, -1, -1, 7, 9]
    ]

    print("🎮 Welcome to Sudoku! Fill the missing numbers. Type 'q' to quit anytime.")
    play_sudoku(sudoku_puzzle)

# Run the game
if __name__ == "__main__":
    main()
import tkinter as tk
from tkinter import messagebox

def is_valid(board, num, pos):
    row, col = pos

    # Check row
    for i in range(9):
        if board[row][i] == num and col != i:
            return False

    # Check column
    for i in range(9):
        if board[i][col] == num and row != i:
            return False

    # Check 3x3 box
    box_x = col // 3
    box_y = row // 3
    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if board[i][j] == num and (i, j) != pos:
                return False
    return True


def find_empty(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None


def solve(board):
    empty = find_empty(board)
    if not empty:
        return True
    else:
        row, col = empty

    for num in range(1, 10):
        if is_valid(board, num, (row, col)):
            board[row][col] = num
            if solve(board):
                return True
            board[row][col] = 0  # Backtrack
    return False


class SudokuGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Solver")
        self.entries = []

        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(root, width=3, font=("Arial", 18), justify='center')
                entry.grid(row=i, column=j, padx=1, pady=1)
                row.append(entry)
            self.entries.append(row)

        solve_button = tk.Button(root, text="Solve", command=self.solve_gui)
        solve_button.grid(row=9, column=0, columnspan=9, pady=10)

    def get_board(self):
        board = []
        for i in range(9):
            row = []
            for j in range(9):
                val = self.entries[i][j].get()
                if val == "":
                    row.append(0)
                else:
                    try:
                        num = int(val)
                        if 1 <= num <= 9:
                            row.append(num)
                        else:
                            raise ValueError
                    except ValueError:
                        messagebox.showerror("Invalid input", f"Invalid number at ({i+1},{j+1})")
                        return None
            board.append(row)
        return board

    def set_board(self, board):
        for i in range(9):
            for j in range(9):
                self.entries[i][j].delete(0, tk.END)
                if board[i][j] != 0:
                    self.entries[i][j].insert(0, str(board[i][j]))

    def solve_gui(self):
        board = self.get_board()
        if board and solve(board):
            self.set_board(board)
        elif board:
            messagebox.showinfo("No Solution", "This Sudoku puzzle has no solution.")


if __name__ == "__main__":
    root = tk.Tk()
    gui = SudokuGUI(root)
    root.mainloop()

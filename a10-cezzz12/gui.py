import tkinter as tk
from tkinter import messagebox
from domain.domain import CellState, Position
import time


class GUI(tk.Tk):
    def __init__(self, service):
        super().__init__()

        self._service = service
        self.title("Connect Four")
        self.CELL_SIZE = 60
        self.board = self._service._repository.get_board()

        # Calculate window size based on board dimensions
        self.canvas_width = self.board.cols * self.CELL_SIZE
        self.canvas_height = self.board.rows * self.CELL_SIZE

        # Create canvas
        self.canvas = tk.Canvas(
            self,
            width=self.canvas_width,
            height=self.canvas_height,
            bg='blue'
        )
        self.canvas.pack(pady=10)

        # Bind click event
        self.canvas.bind('<Button-1>', self.handle_click)

        # Initialize the board display
        self.draw_board()

        # Add reset button
        self.reset_button = tk.Button(self, text="New Game", command=self.reset_game)
        self.reset_button.pack(pady=5)

        self.game_active = True

    def draw_board(self):
        """Draw the current state of the board"""
        self.canvas.delete("all")

        # Draw cells
        for row in range(self.board.rows):
            for col in range(self.board.cols):
                x = col * self.CELL_SIZE + self.CELL_SIZE // 2
                y = row * self.CELL_SIZE + self.CELL_SIZE // 2

                # Draw cell background
                cell_state = self.board.get_cell(Position(row, col))
                if cell_state == CellState.EMPTY:
                    color = 'white'
                elif cell_state == CellState.PLAYER:
                    color = 'red'
                else:
                    color = 'yellow'

                # Draw circle
                self.canvas.create_oval(
                    x - self.CELL_SIZE // 2 + 5,
                    y - self.CELL_SIZE // 2 + 5,
                    x + self.CELL_SIZE // 2 - 5,
                    y + self.CELL_SIZE // 2 - 5,
                    fill=color,
                    outline='black'
                )

    def handle_click(self, event):
        """Handle mouse click event"""
        if not self.game_active:
            return

        # Convert click coordinates to column
        col = event.x // self.CELL_SIZE

        # Make player move
        if self._service.make_move(col, CellState.PLAYER):
            self.draw_board()

            # Check if player won
            if self._service.check_win(CellState.PLAYER):
                messagebox.showinfo("Game Over", "You win!")
                self.game_active = False
                return

            # Check for draw
            if self._service.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.game_active = False
                return

            # Make computer move
            self.after(500, self.make_computer_move)
        else:
            messagebox.showwarning("Invalid Move", "That column is full!")

    def make_computer_move(self):
        """Make computer move with animation"""
        col = self._service.computer_move()
        if col is not None:
            self._service.make_move(col, CellState.COMPUTER)
            self.draw_board()

            # Check if computer won
            if self._service.check_win(CellState.COMPUTER):
                messagebox.showinfo("Game Over", "Computer wins!")
                self.game_active = False
                return

            # Check for draw
            if self._service.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.game_active = False
                return

    def reset_game(self):
        """Reset the game state"""
        self._service._repository.reset_board()
        self.board = self._service._repository.get_board()
        self.game_active = True
        self.draw_board()

    def run(self):
        """Start the GUI main loop"""
        self.mainloop()
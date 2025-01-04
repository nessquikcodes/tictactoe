import tkinter as tk
from tkmacosx import Button
from tkinter import DISABLED, messagebox
from typing import List
import random

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.config(background='#E6B0AA', padx=30, pady=10)
        
        # Game state
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons: List[List[Button]] = []
        
        # Style configuration
        self.BUTTON_FONT = ('Helvetica', 40, 'bold')
        self.LABEL_FONT = ('Helvetica', 36)
        self.COLORS = {
            'bg': "#E6B0AA",
            "text": "white",
            "win": "#27ae60"
        }
        
        self._setup_ui()
        
    def _setup_ui(self):
        """ Initialize game """
        # Status label
        self.status_label = tk.Label(
            self.window,
            text=f'Player {self.current_player}\'s turn',
            font=self.LABEL_FONT,
            bg=self.COLORS['bg'],
            fg=self.COLORS['text']
        )
        self.status_label.pack(padx=10, pady=[5,20], fill='both')
        
        # Game board
        board_frame = tk.Frame(self.window, bg=self.COLORS['bg'])
        board_frame.pack(padx=40, fill='y', expand=1)
        
        for i in range(3):
            row = []
            for j in range(3):
                button = Button(
                    board_frame,
                    text=' ',
                    font=self.BUTTON_FONT,
                    width=60,
                    height=60,
                    bg=self.COLORS['bg'],
                    fg=self.COLORS['text'],
                    activebackground=self.COLORS['bg'],
                    focusthickness=0,
                    borderless=1,
                    state='normal',
                    command=lambda row=i, col=j: self._handle_click(row, col)
                )
                button.grid(row=i, column=j, padx=3, pady=3)
                row.append(button)
            self.buttons.append(row)
        
        # Reset Button
        reset_btn = Button(
            self.window,
            text='Reset Game',
            font=('Helvetica', 24),
            bg=self.COLORS['bg'],
            fg=self.COLORS['text'],
            activebackground=self.COLORS['bg'],
            borderless=1,
            focuscolor=self.COLORS['text'],
            focusthickness=1,
            command=self._reset_game
        )
        reset_btn.pack(pady=[20, 5], fill='y', expand=0)
        
    def _handle_click(self, row: int, col:int):
        """ Handles the players move """
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(state=DISABLED, text=self.current_player, disabledforeground=self.COLORS['text'], disabledbackground=self.COLORS['bg'])

            if self._check_winner(row, col):
                self._highlight_winner()
                messagebox.showinfo('Game Over', f'Player {self.current_player} wins!')
                self.end_game()
            elif self._is_board_full():
                messagebox.showinfo('Game Over', 'It\'s a tie!')
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.status_label.config(text=f'Player {self.current_player}\'s turn') 

    def _check_winner(self, row:int, col:int):
        """ Check if current player has won. """
        # Check rows
        if all(self.board[row][i] == self.current_player for i in range(3)):
            return True
    
        # Check columns
        if all(self.board[i][col] == self.current_player for i in range(3)):
            return True
    
        # Check diagonals
        if row == col and all(self.board[i][i] == self.current_player for i in range(3)):
            return True
    
        elif row + col == 2 and all(self.board[i][2-i] == self.current_player for i in range(3)):
            return True
        else:
            return False
    
    def _highlight_winner(self):
        """ Highlight winning combination """
        # Rows
        for row in range(3):
            if self.buttons[row][0]['text'] == self.buttons[row][1]['text'] == self.buttons[row][2]['text'] != ' ':
                self.buttons[row][0].config(bg=self.COLORS['win'])
                self.buttons[row][1].config(bg=self.COLORS['win'])
                self.buttons[row][2].config(bg=self.COLORS['win'])
        
        # Columns
        for col in range(3):
            if self.buttons[0][col]['text'] == self.buttons[1][col]['text'] == self.buttons[2][col]['text'] != ' ':
                self.buttons[0][col].config(bg=self.COLORS['win'])
                self.buttons[1][col].config(bg=self.COLORS['win'])
                self.buttons[2][col].config(bg=self.COLORS['win'])
        
        # Diagonal from bottom left to top right
        if self.buttons[2][0]['text'] == self.buttons[1][1]['text'] == self.buttons[0][2]['text'] != ' ':
            self.buttons[2][0].config(bg=self.COLORS['win'])
            self.buttons[1][1].config(bg=self.COLORS['win'])
            self.buttons[0][2].config(bg=self.COLORS['win'])
        
        # Diagonal from top right to bottom left
        elif self.buttons[0][0]['text'] == self.buttons[1][1]['text'] == self.buttons[2][2]['text'] != ' ':
            self.buttons[0][0].config(bg=self.COLORS['win'])
            self.buttons[1][1].config(bg=self.COLORS['win'])
            self.buttons[2][2].config(bg=self.COLORS['win'])
                 
    def _is_board_full(self):
        """ Check if the board is full """
        return all(self.board[i][j] != ' ' for i in range(3) for j in range(3))
    
    def _reset_game(self):
        """ Resets the game to initial state """
        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text=' ',
                    bg=self.COLORS['bg'],
                    fg=self.COLORS['text'],
                    state='normal'
                )
        self.status_label.config(text=f'Player {self.current_player}\'s turn')
    
    def end_game(self):
        """ Disables any empty remaining buttons """
        for i in range(3):
            for j in range(3):
                if self.buttons[i][j]['text'] == ' ':
                    self.buttons[i][j].config(state=DISABLED, disabledforeground=self.COLORS['text'], disabledbackground=self.COLORS['bg'])
    
    def run(self):
        """ Starts the game """
        self.window.mainloop()
        
if __name__ == '__main__':
    game = TicTacToe()
    game.run()
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
        
        # Delay constants in milliseconds
        self.MOVE_DELAY = 500
        self.MESSAGE_DELAY = 300
        
        # Game state
        self.players = ['X', 'O']
        self.current_player = self.players[0]
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons: List[List[Button]] = []
        
        # Style configuration
        self.BUTTON_FONT = ('Helvetica', 40, 'bold')
        self.LABEL_FONT = ('Helvetica', 36)
        self.COLORS = {
            'bg': "#E6B0AA",
            "text": "white",
            "win": "#d06a5e"
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
                    command=lambda row=i, col=j: self._get_player_move(row, col)
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
        reset_btn.pack(pady=[20, 5], padx=15, expand=0, side='left')
        
        # Exit Button
        exit_btn = Button(
            self.window,
            text='Exit Game',
            font=('Helvetica', 24),
            bg=self.COLORS['bg'],
            fg=self.COLORS['text'],
            activebackground=self.COLORS['bg'],
            borderless=1,
            focuscolor=self.COLORS['text'],
            focusthickness=1,
            command=self._exit_game
        )
        exit_btn.pack(pady=[20, 5], padx=15, expand=0, side='left')
        
    def _get_player_move(self, row: int, col:int):
        """ Handles the players move with delays """
        if self.current_player == self.players[0] and self.board[row][col] == ' ':
            # Disables all buttons during animation
            self._set_all_btns_state('disabled')
            
            # Updates the board with player move
            self._update_board(row, col)    
            
            # Check for game end after player move
            if self._check_winner(row, col, self.current_player):
                self.window.after(self.MESSAGE_DELAY, self._handle_win)
                return
            
            # Check for tie after player move
            if self._is_board_full():
                self.window.after(self.MESSAGE_DELAY, self._handle_tie)
                return
            
            # Switch to AI's turn with delay
            self.window.after(self.MOVE_DELAY, self._handle_ai_turn)
        
    def _handle_ai_turn(self):
        """ Handle AI move with delays """
        self.current_player = self.players[1]
        self._refresh_player_status()
        
        # Get and make AI move
        (row, col) = self._get_smart_ai_move()
        self._update_board(row, col)
        
        # Check for game end after AI move
        if self._check_winner(row, col, self.current_player):
            self.window.after(self.MESSAGE_DELAY, self._handle_win)
            return
        
        # Switch back to player's turn
        self.current_player = self.players[0]
        self.window.after(self.MESSAGE_DELAY, self._enable_valid_moves)
        self.window.after(self.MESSAGE_DELAY, self._refresh_player_status)
        
    def _get_smart_ai_move(self):
        """ Checks if AI can win with next move or needs to block. Otherwise, plays randomly """
        # Checks for a winning move for the AI
        winning_move = self._find_winning_move(self.players[1])
        if winning_move:
            return winning_move
        
        # Checks if AI needs to block the players move
        blocking_move = self._find_winning_move(self.players[0])
        if blocking_move:
            return blocking_move
        
        # Plays randomly
        return self._get_random_ai_move()    
    
    def _find_winning_move(self, player:str):
        """ Checks if the next placement will result in a win """
        for row in range(3):
            for col in range(3):
                if self.board[row][col] == ' ': 
                    # Temporarily place current player's symbol on board
                    self.board[row][col] = player
                    # If True, return the winning coordinates
                    if self._check_winner(row, col, player):
                        # Undo the move
                        self.board[row][col] = ' '
                        return (row, col)
                    self.board[row][col] = ' '
        return None    

    def _get_random_ai_move(self):
        """ Creates a tuple of the remaining empty spaces on the board and selects one at random. If board is full, returns None """
        empty_spaces = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ' ']
            
        if empty_spaces:
            return random.choice(empty_spaces)

    def _set_all_btns_state(self, state:str):
        """ Enable/Disable all buttons """
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.buttons[i][j].config(state=state, disabledforeground=self.COLORS['text'], disabledbackground=self.COLORS['bg'])
                    
    def _enable_valid_moves(self):
        """ Enable buttons for empty spaces """
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.buttons[i][j].config(state='normal', disabledforeground=self.COLORS['text'], disabledbackground=self.COLORS['bg'])
                    
    def _handle_win(self):
        """ Handle win condition with delay """
        self._highlight_winner()
        messagebox.showinfo('Game Over', f'Player {self.current_player} wins!')
        self.end_game()
        
    def _handle_tie(self):
        """ Handle tie condition with delay """
        messagebox.showinfo('Game Over', 'It\'s a tie!')
        self.end_game()

    def _update_board(self, row: int, col: int):
        self.board[row][col] = self.current_player
        self.buttons[row][col].config(state=DISABLED, text=self.current_player, disabledforeground=self.COLORS['text'], disabledbackground=self.COLORS['bg'])
            
    def _refresh_player_status(self):        
        self.status_label.config( text=f'Player {self.current_player}\'s turn')
        
    def _check_winner(self, row:int, col:int, player: str):
        """ Check if player has won. """
        # Check rows
        if all(self.board[row][i] == player for i in range(3)):
            return True
    
        # Check columns
        if all(self.board[i][col] == player for i in range(3)):
            return True
    
        # Check diagonals
        if row == col and all(self.board[i][i] == player for i in range(3)):
            return True
    
        elif row + col == 2 and all(self.board[i][2-i] == player for i in range(3)):
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
        self.current_player = self.players[0]
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text=' ',
                    bg=self.COLORS['bg'],
                    fg=self.COLORS['text'],
                    state='normal'
                )
        self._refresh_player_status()
    
    def end_game(self):
        """ Disables any empty remaining buttons """
        if self._is_board_full() is False: 
            for i in range(3):
                for j in range(3):
                    if self.buttons[i][j]['text'] == ' ':
                        self.buttons[i][j].config(state=DISABLED, disabledforeground=self.COLORS['text'], disabledbackground=self.COLORS['bg'])
        
    def _exit_game(self):
        self.window.destroy()
        
    def run(self):
        """ Starts the game """
        self.window.mainloop()
        
if __name__ == '__main__':
    game = TicTacToe()
    game.run()
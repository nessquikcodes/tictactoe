from tkinter import *
from tkmacosx import Button
import random

def next_turn(row, column):
    global player
    
    if buttons[row][column]['text'] == ' ' and check_winner() is False:
        if player == players[0]:
            buttons[row][column]['text'] = player
            update_label(player)
            player = players[1]
        else:
            buttons[row][column]['text'] = player
            update_label(player)
            player = players[0]
        
"""
Update the label to show the current player's turn, or the result of the game if there is a winner or a tie.
"""
def update_label(player):    
    if check_winner() is True:
        label.config(text=player + ' Wins!')
    elif check_winner() == 'Tie':
        label.config(text='It\'s a Tie!')
    else:
        if player == 'X':
            label.config(text=players[1] + '\'s Turn')
        else:
            label.config(text=players[0] + '\'s Turn')
            
"""
Check if there is a winner or a tie in the game.
Returns True if there is a winner, 'Tie' if the game is a tie, and False otherwise.
"""
def check_winner():
    # Check rows for a winner
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != ' ':
            buttons[row][0]['background']='red'
            buttons[row][1]['background']='red'
            buttons[row][2]['background']='red'
            return True

    # Check columns for a winner
    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != ' ':
            buttons[0][column]['background']='red'
            buttons[1][column]['background']='red'
            buttons[2][column]['background']='red'
            return True
        
    # Check diagonal from top left to bottom right
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != ' ':
        buttons[0][0]['background']='red'
        buttons[1][1]['background']='red'
        buttons[2][2]['background']='red'
        return True
    
    # Check diagonal from bottom left to top right
    elif buttons[2][0]['text'] == buttons[1][1]['text'] == buttons[0][2]['text'] != ' ':
        buttons[2][0]['background']='red'
        buttons[1][1]['background']='red'
        buttons[0][2]['background']='red'
        return True

    # If there are no more empty spaces on the board, return 'Tie'
    elif empty_spaces() is False:
        return 'Tie'
    
    else:
        return False

"""
Loops through grid and uses counter to track the number of empty spaces left on the board.    
Returns false if there are no remaining spaces, otherwise True 
"""
def empty_spaces():
    spaces = 9
    
    for row in range(3):
        for column in range(3):
            if buttons[row][column]['text'] != ' ':
                spaces -= 1
                
    if spaces == 0:
        return False
    else:
        return True

def new_game():
    pass

window = Tk()
window.config(background='#E6B0AA', padx=20, pady=10)
window.title('Tic-Tac-Toe Game')
players = ['X', 'O']
player = random.choice(players)
buttons = [[0,0,0],
           [0,0,0],
           [0,0,0]]

label = Label(text=player + '\'s Turn', font=('Helvetica',36), fg='white', background='#E6B0AA')
label.pack(side='top', fill='x')

frame = Frame(window, background='#E6B0AA', pady=15)
frame.pack(fill='both', expand=True)

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text=' ', font=('Arial', 24), width=50, 
                                     height=50, fg='white', background='#E6B0AA', border=0, borderless=1, command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

reset_btn = Button(window, text='Reset', font=('Arial', 18), width=65, height=25, fg='white', background='#E6B0AA', border=0, borderless=1, command=new_game)
reset_btn.pack(side='bottom', ipady=1)
window.mainloop()

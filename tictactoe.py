from tkinter import *
import random

def next_turn(row, column):
    global player
    
    if buttons[row][column]['text'] == ' ' and check_winner() is False:
        if player == players[0]:
            buttons[row][column]['text'] = player
            
            if check_winner() is False:
                player = players[1]
                label.config(text=(player + ' Turn'))
            elif check_winner() is True:
                label.config(text=(players[0] + ' Wins!'))

            elif check_winner() == 'Tie':
                label.config(text=('Tie!'))
        else:
            if player == players[1]:
                buttons[row][column]['text'] = player
            
            if check_winner() is False:
                player = players[0]
                label.config(text=player + ' Turn')
            elif check_winner() is True:
                label.config(text=players[1] + ' Wins!')

            elif check_winner() == 'Tie':
                label.config(text='It\'s a Tie!')

def check_winner():
    for row in range(3):
        if buttons[row][0]['text'] == buttons[row][1]['text'] == buttons[row][2]['text'] != ' ':
            return True

    for column in range(3):
        if buttons[0][column]['text'] == buttons[1][column]['text'] == buttons[2][column]['text'] != ' ':
            return True
        
    if buttons[0][0]['text'] == buttons[1][1]['text'] == buttons[2][2]['text'] != ' ':
        return True
    
    elif buttons[2][0]['text'] == buttons[1][1]['text'] == buttons[0][2]['text'] != ' ':
        return True

    elif empty_spaces() is False:
        return 'Tie'
    
    else:
        return False

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
window.title = 'Tic-Tac-Toe Game'
players = ['X', 'O']
player = random.choice(players)
buttons = [[0,0,0],
           [0,0,0],
           [0,0,0]]

label = Label(text=player + '\'s Turn', font=('Helvetica',36), fg='white', background='#E6B0AA')
label.pack(side='top', fill='x')

frame = Frame(window)
frame.pack(fill='both')

for row in range(3):
    for column in range(3):
        buttons[row][column] = Button(frame, text=' ', font=('Arial', 24), width=5, 
                                     height=2, border=0, highlightbackground='#E6B0AA', command=lambda row=row, column=column: next_turn(row, column))
        buttons[row][column].grid(row=row, column=column)

reset_btn = Button(text='Reset', font=('Arial', 18), width=10, height=2, highlightbackground='#E6B0AA', command=new_game)
reset_btn.pack(side='bottom', fill='x')
window.mainloop()

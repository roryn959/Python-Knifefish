from tkinter import *
    
def FENHelp():
    global FEN_Help_Window
    try:
        #If there's already a window open, just focus on it, don't open a new one
        if FEN_Help_Window.state() == "normal":
            FEN_Help_Window.focus()            
    except:
        #If there isn't a window open, FEN_Help_Window should be non-existent, so will flag an error, and create a new one
        FEN_Help_Window = Toplevel()
        FEN_Help_Window.geometry('607x470')
        Title_Label = Label(FEN_Help_Window, text='Forsyth-Edwards Notation (FEN)', font=('Helvetica', '12'))
        Title_Label.place(x=200)
        Info_Labels = []
        Info_Labels.append(Label(FEN_Help_Window, text='FEN is a way of expressing a custom board layout as a string of characters, row by row'))
        Info_Labels.append(Label(FEN_Help_Window, text=''))
        Info_Labels.append(Label(FEN_Help_Window, text='It works by using letters and numbers to denote the piece, or lack of a piece, in a given square, starting from the'))
        Info_Labels.append(Label(FEN_Help_Window, text='top left, ending at the bottom right. Rows are seperated by a slash, and black is always in the top of the board.'))
        Info_Labels.append(Label(FEN_Help_Window, text=''))
        Info_Labels.append(Label(FEN_Help_Window, text='White pieces are represented using capital letters (P/N/B/R/Q/K), and black pieces with lower case (p/n/b/r/q/k)'))
        Info_Labels.append(Label(FEN_Help_Window, text='while spaces are represented as a number of how many spaces there are in a row.'))
        Info_Labels.append(Label(FEN_Help_Window, text=''))
        Info_Labels.append(Label(FEN_Help_Window, text="Next, you use 'w' or 'b' to represent who's turn it is, meaning it's white or black's turn respectively."))
        Info_Labels.append(Label(FEN_Help_Window, text=''))
        Info_Labels.append(Label(FEN_Help_Window, text='Then, after showing all pieces and spaces on the board, castling permissions are represented (K/Q/k/q). Each'))
        Info_Labels.append(Label(FEN_Help_Window, text='letter represents a castling permission. K and Q mean white can castle kingside and queenside respectively, and '))
        Info_Labels.append(Label(FEN_Help_Window, text='k and q represent the same for black. A lack of a certain letter means the corresponding castling permission is lost.'))
        Info_Labels.append(Label(FEN_Help_Window, text='A dash "-" means there are no castling permissions.'))
        Info_Labels.append(Label(FEN_Help_Window, text='For example, (K/Q/k) would mean white can still castle on either side, but black can only do so on the kingside.'))
        Info_Labels.append(Label(FEN_Help_Window, text=''))
        Info_Labels.append(Label(FEN_Help_Window, text="Finally, en passant squares are determined. '-' means there are no en passant squares active, while"))
        Info_Labels.append(Label(FEN_Help_Window, text="typing a square such as 'E4' would mean that square is designated as an en passant square."))
        Info_Labels.append(Label(FEN_Help_Window, text=''))
        Info_Labels.append(Label(FEN_Help_Window, text='Examples:'))
        Info_Labels.append(Label(FEN_Help_Window, text="To show the starting position, you would type 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -'"))
        Info_Labels.append(Label(FEN_Help_Window, text="If white then made the move 'e4', it's now 'rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3'"))
        for i in range(0, len(Info_Labels)):
            Info_Labels[i].place(x=0, y=i*20+30)

def EvalHelp():
    global Eval_Help_Window
    try:
        #If there's already a window open, just focus on it, don't open a new one
        if Eval_Help_Window.state() == "normal":
            Eval_Help_Window.focus()            
    except:
        #If there isn't a window open, Eval_Help_Window should be non-existent, so will flag an error, and create a new one
        Eval_Help_Window = Toplevel()
        Eval_Help_Window.geometry('530x500')
        Title_Label = Label(Eval_Help_Window, text='Evaluation', font=('Helvetica', '12'))
        Title_Label.place(x=220)
        Info_Labels = []
        Info_Labels.append(Label(Eval_Help_Window, text='The evaluation section aims to provide the user with a view of how the game is going so far,'))
        Info_Labels.append(Label(Eval_Help_Window, text='while giving a slightly more detailed evaluation, if the user requests it, as well as help'))
        Info_Labels.append(Label(Eval_Help_Window, text='if they get into trouble.'))
        Info_Labels.append(Label(Eval_Help_Window, text=''))
        Info_Labels.append(Label(Eval_Help_Window, text="To request an evaluation from the engine, press 'Evaluate Board'. This will result is two values:"))
        Info_Labels.append(Label(Eval_Help_Window, text="•'CE' stands for 'current evaluation' - how does the board look at the moment; which side is"))
        Info_Labels.append(Label(Eval_Help_Window, text='  in terms of current material'))
        Info_Labels.append(Label(Eval_Help_Window, text=''))
        Info_Labels.append(Label(Eval_Help_Window, text="•'PE' stands for 'predicted evaluation' - provided that both sides make the best moves"))
        Info_Labels.append(Label(Eval_Help_Window, text='  as far as the AI can find, what will the board look like in a few moves? If this value is very'))
        Info_Labels.append(Label(Eval_Help_Window, text='  different to the current evaluation, this suggests one side has the opportunity to make a'))
        Info_Labels.append(Label(Eval_Help_Window, text='  good move. The AI will look between 4-7 moves ahead, depending on how volatile the position is.'))
        Info_Labels.append(Label(Eval_Help_Window, text=''))
        Info_Labels.append(Label(Eval_Help_Window, text='A positive value indicates white has an advantage, and negative is good for black.'))
        Info_Labels.append(Label(Eval_Help_Window, text=''))
        Info_Labels.append(Label(Eval_Help_Window, text='A pawn is worth 100. So, if the current evaluation is -100, black is ahead by one pawn.'))
        Info_Labels.append(Label(Eval_Help_Window, text=''))
        Info_Labels.append(Label(Eval_Help_Window, text='There are various positional advantages. For example, a knight in the middle of the board tends to'))
        Info_Labels.append(Label(Eval_Help_Window, text='be much more useful than one in the corner. So, if an evaluation comes out as +30, this'))
        Info_Labels.append(Label(Eval_Help_Window, text="may suggest material is fairly even, but white's pieces are slightly better placed."))
        Info_Labels.append(Label(Eval_Help_Window, text=''))
        Info_Labels.append(Label(Eval_Help_Window, text='The evaluation section also contains buttons to undo a move, or ask the AI to suggest a move,'))
        Info_Labels.append(Label(Eval_Help_Window, text='to help you out of a sticky situation.'))
        for i in range(0, len(Info_Labels)):
            Info_Labels[i].place(x=0, y=i*20+30)

def End_Window(winner, condition, board):
    global Finish_Window, NameEntry, NameLabel, SaveButton    
    Finish_Window = Toplevel()
    Finish_Window.geometry('300x100')    
    TitleLabel = Label(Finish_Window, text='Game Over', font=('Helvetica', '20', 'bold'))
    TitleLabel.place(x=70)
    if winner == None:
        TempString = 'Game drawn by stalemate'
    else:
        TempString = winner+' wins by '+condition+'!'    
    WinnerLabel = Label(Finish_Window, text=TempString, font=('Helvetica', '16'))
    WinnerLabel.place(x=25, y=50)    
    try:
        if winner.lower() == board.Player_Colour.lower(): #If the player won, give the option of saving their win
            Finish_Window.geometry('300x180')
            NameLabel = Label(Finish_Window, text='Name:')
            NameLabel.place(x=40, y=90)
            NameEntry = Entry(Finish_Window)
            NameEntry.place(x=85, y=93)
            
            SaveButton = Button(Finish_Window, text='Save Game', command=lambda:SaveGame(board))
            SaveButton.place(x=85, y=120)
    except: #If error raised, it was a two player game, in which case no option to save is needed.
        pass

def SaveGame(board):
    if NameEntry.get() == '': #If they've left the name entry widget blank, don't save yet, and prompt them by highlighting widget.
        NameEntry.config(bd=3)
    else:    
        file = open("highscores.txt",'a+')
        tempString = '\n'+NameEntry.get()+'/'+str(board.Difficulty)+'/'+board.Player_Colour+'/'+str(board.moveCounter//2)
        file.write(tempString)
        file.close()
        NameLabel.config(text=f'Game successfully saved as {NameEntry.get()}.')
        NameLabel.place(x=55, y=90)
        NameEntry.destroy()
        SaveButton.destroy()













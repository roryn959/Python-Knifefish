import random, time, copy, math, threading
from tkinter import *
from PieceSquares import *
from ZobristVals import *
from Windows import *
from Constants import *

root = Tk()

playerAmount = IntVar() #1 player or two?
playerAmount.set(1) #Default play amount is 1
player1Colour = IntVar() #Which colour is player 1?
player1Colour.set(1) #0 = White, 1 = Black
customLayout = IntVar() #Do they want to use a custom layout
customLayout.set(0) #Default is that they don't want to use their own layout
difficulties = [1, 2, 3, 4] #Range of difficulties to choose from
difficulty = IntVar()
difficulty.set(difficulties[0]) #Default difficulty is '0'
times = ["--", "30", "1", "3", "5", "10", "20"] #Range of time conditions to adhere to. Store as string in case no time conditions chosen ('--')
timer = StringVar(root)
timer.set(times[0]) #Default no time conditions chosen

def Convert(square): #Takes square name 'E7' and gives board index, or vice versa
    if type(square) is str: #If in form 'E7'
        b = COLUMN_VALUES[square[0]] #Each letter will correspond to a specific second digit. E.g. Every square in the B file will have an index ending in '2'
        a = 10-int(square[1]) #Each rank's number corresponds to a specific first digit. E.g. the 7th rank will have an index starting with '3'.
        return int(str(a)+str(b)) #Return the two digits found as an integer
    else: #If in form '78'
        a = REVERSE_COLUMN_VALUES[str(square)[1]]
        b = 10-int(str(square)[0])
        return str(a)+str(b)

def Set_Sunk(index, reset): #Either sets a certain button to be sunk and coloured as the user's chosen button, or resets whichever buttons are sunk.
    global SunkButton
    if not(reset): #If function just needs to sink a button
        if len(SunkButton) != 0: #If there is a button already sunk, unsink it
            ResetButton(SunkButton[0])
            SunkButton = []
        SunkButton.append(index) #Record which button is sunk
        ButtonList[index].config(relief='sunken', bg='skyblue3') #Sink and colour button
    else: #If function needs to raise and uncolour all buttons
        for button in SunkButton:
            ResetButton(button)
            SunkButton = []

def SubmitButton(pressed):
    global SunkButton
    if Orientation == 1: #If the board is flipped, convert the submitted button accordingly
        pressed = Convert(pressed) #Convert index number to number and letter format ('E7')
        first = pressed[0]
        second = pressed[1]
        first = REVERSE_COLUMN_VALUES[str(9-COLUMN_VALUES[first])] #To convert, pick the 'opposite' letter. So A -> H, B -> G etc.
        second = 9-int(second) #Similarly, the 'opposite' number can be found by subtracting it from 9
        pressed = Convert(str(first)+str(second)) #Once opposite square found, join and convert back to index
    if playerAmount.get() == 1: #If just a one player game
        Submit1(pressed) #Execute subroutine for one player button submissions
    elif playerAmount.get() == 2: #Else if a two player game
        Submit2(pressed) #Execute subroutine for two player button submissions

def StartTimer():
    while True: #Constantly run
        if Main.time_active: #If time conditions are actually chosen.
            if Main.active_colour == 'white':
                Main.white_time -= 0.1 #Decrement time from relevant side                                      
                Update_Label('white', Main.white_time) #Update the timer label for white
            elif Main.active_colour == 'black': #If active colour is black
                Main.black_time -= 0.1 #Decrement time from relevant side
                Update_Label('black', Main.black_time) #Update timer label for black
        time.sleep(0.1) #Increment time every 0.1 seconds. Smaller interval gives more accurate time tracking, but requires more processing allocation

def Update_Label(colour, time):
    if time == '--': #If time is not being used for current game
        whiteTimerLabel.config(text='--') #Make timer just show dashed lines
        blackTimerLabel.config(text='--') #''
    else:
        if colour == 'white': #If updating white's timer
            time = int(time//1) #Update time label
            if time <= 0: #If side has run out of time
                whiteTimerLabel.config(text='--') #Show a dashed line
            else: #If the given player hasn't run out of time
                tempString = str(time//60)+':'   #String = minutes + ':'              
                if (n := time%60) < 10: #Statement to avoid the label from showing '2:5' rather than '2:05', adds a '0' in middle if needed
                    tempString = tempString+'0'+str(n) #Adds minutes with 0 if needed
                else:
                    tempString = tempString+str(n) #If two digit number, just add minutes as they are
                whiteTimerLabel.config(text=tempString)
        else:
            time = int(time//1) #Update time label
            if time <= 0: #If side has run out of time, show a dashed line
                blackTimerLabel.config(text='--')            
            else:
                tempString = str(time//60)+':'               
                if (n := time%60) < 10: #Statement to avoid the label from showing '2:5' rather than '2:05'
                    tempString = tempString+'0'+str(n)
                else:
                    tempString = tempString+str(n)
                blackTimerLabel.config(text=tempString)
                
def EvalBoard():
    global iterations, extensions    
    CEValLabel.config(text=Main.Evaluate()) #Update current evaluation label
    iterations = 0
    extensions = 0
    if Main.moveCounter%2 == 0:
        PEValLabel.config(text=Main.Alphabeta(3, -(math.inf), math.inf, 'white')[1]) #To get predicted evaluation, run alphabeta at depth 3
    else:
        PEValLabel.config(text=Main.Alphabeta(3, -(math.inf), math.inf, 'black')[1])

def SuggestMove():
    global iterations, extensions
    iterations = 0 #Used to track number of nodes searched by alphabeta
    extensions = 0 #Number of nodes searched by quiescence
    if Main.moveCounter%2 == 0: #Who's turn is it?
        Move = Main.Alphabeta(3, -(math.inf), (math.inf), 'white')[0] #Find move for white at depth 3
    else: #If odd number of moves made, it's black's move
        Move = Main.Alphabeta(3, -(math.inf), (math.inf), 'black')[0] #Find move for black at depth 3
    try: #Display move found. If error raised, it's a castle move
        TempString = 'Suggested move:'+' '+Convert(Move[0])+' '+Convert(Move[1]) #Suggest move by naming the square the piece starts on, and square it moves to
        DialogueLabel.config(text=TempString) #Update dialogue label with move suggestion
    except:
        if Move[1] == 'K': #If move found is a kingside castle
            TempString = 'Suggested move: Kingside Castle'
            DialogueLabel.config(text=TempString) #Update dialogue label with move suggestion
        else: #Else move is queenside castle
            TempString = 'Suggested move: Queenside Castle'
            DialogueLabel.config(text=TempString) #Update dialogue label with move suggestion

def MainUndo():
    global Main
    if Main.Get_boardHistory().length()>0: #First, check if there are actually enough moves made to undo - if no move have been made, can't undo move
        Main.UndoMove() #Undo move
        if playerAmount.get() == 1: #If it's a one-player game, need to undo move twice to undo both AI's last move and player's last move
            Main.UndoMove() #Undo second time if needed
        Main.MoveChoice = []
        Main.PickMode = 1
        Main.Display() #Update GUI display with all pieces
    else: #If insufficient number of moves made to undo move
        DialogueLabel.config(text="Not enough space to undo move") #Update dialogue label
    RefreshGUI() #Refresh GUI to remove coloured and sunken squares

def RefreshGUI():
    global SunkButton
    for i in range(0, len(ButtonList)): #For each element in the button list
        if ButtonList[i] != None: #If there's a button there
            ResetButton(i) #Reset button
    if len(SunkButton) !=0 : #If there are buttons still listed as sunk
        SunkButton = [] #Reset sunk buttons list

def ResetButton(button):
    if ((button//10)+(button%10))%2 == 0: #If row number plus column number give an even number, the square is a dark square
        ButtonList[button].config(bg='grey', relief='raised') #Reset square as grey
    else: #Else if square is light square
        ButtonList[button].config(bg='white', relief='raised') #Reset square as white

def CreateGame():
    global Main, Timer_Thread
    DialogueLabel.config(text='')
    RefreshGUI() #Reset all buttons which may be coloured or sunk
    Main = Board(DEFAULT_SETUP.copy(), [1, 1, 1, 1], []) #Initialise board with default layout
    if customLayout.get() == 0: #If they don't want to use a custom layout
        if playerAmount.get() == 1: #If a one player game and AI is white, make first move
            if Main.AI_Colour == 'white':
                Main.CPUMove()
    else: #If they want to use a custom board layout        
        if Main.FromFEN(FENEntry.get()) == 'failed': #If FEN string is invalid, break from subroutine and disable button clicks. If not, board will change
            Main.PickMode = None
            return None    
    try: #If there is already a timer thread running, exception won't be raised, so don't create another
        Timer_Thread.is_alive()
    except: #An exception means there is no timer thread alive, in which case create one
        Timer_Thread = threading.Thread(target=StartTimer, args=())
        Timer_Thread.start() #Start thread to keep track of each colour's time
    if Main.time_active:
        Update_Label('white', Main.white_time)
        Update_Label('black', Main.black_time)
    else:
        Update_Label('white', '--')
        Update_Label('black', '--')        
    Main.Display() #Display the board

def Submit1(pressed):
    if Main.PickMode == 1: #Starting square choice
        if Main.board[pressed] == ' ': #If user's first square choice is an empty square, they have clearly made an mistake when pressing a square
            DialogueLabel.config(text="Invalid starting square")
            RefreshGUI()
        else:
            if Main.Player_Colour == 'white':
                if Main.board[pressed] in WHITE_TYPES: #If they picked a piece belonging to them. If not, it's a mistake
                    Main.MoveChoice.append(pressed) #Add user's starting square choice
                    Main.PickMode = 2 #Next button pressed will be the chosen destination square of the user
                    Set_Sunk(pressed, False) #Highlight the chosen square to help the user remember which piece they chose to move
                else:
                    DialogueLabel.config(text="Invalid starting square")
            else:
                if Main.board[pressed] in BLACK_TYPES: #If they picked a piece belonging to them. If not, it's a mistake
                    Main.MoveChoice.append(pressed) #Add user's starting square choice
                    Main.PickMode = 2 #Next button pressed will be the chosen destination square of the user
                    Set_Sunk(pressed, False) #Highlight the chosen square to help the user remember which piece they chose to move
                else:
                    DialogueLabel.config(text="Invalid starting square")
    elif Main.PickMode == 2: #Destination square choice
        if Main.Player_Colour == 'white':
            if Main.board[pressed] in WHITE_TYPES: #If they picked a piece belonging to them and then picked another, they most likely just changed their mind about which piece to move.
                Main.MoveChoice[0] = pressed #Change the piece chosen to move to the newly pressed piece
                Set_Sunk(pressed, False) #Change highlighted square to new chosen piece
                return None #Halt subroutine - don't execute the rest of this branch of the subroutine as they haven't actually chosen a move
        else:
            if Main.board[pressed] in BLACK_TYPES: #If they picked a piece belonging to them and then picked another, they most likely just changed their mind about which piece to move.
                Main.MoveChoice[0] = pressed #Change the piece chosen to move to the newly pressed piece
                Set_Sunk(pressed, False) #Change highlighted square to new chosen piece
                return None #Halt subroutine - don't execute the rest of this branch of the subroutine as they haven't actually chosen a move
        Main.MoveChoice.append(pressed)        
        if Main.Player_Colour == 'white': #Designating the type of move. 1 is a normal move, 2 is a castle, 3 is an en passant
            if Main.board[Main.MoveChoice[0]] == wK and Main.MoveChoice[1] in [93, 97] and Main.MoveChoice[0] == 95: #Is the move they're attempting a castle move?
                if Main.MoveChoice[1] == 93: #If they are trying to castle queenside
                    Main.MoveChoice = [0, 'Q', 2]
                elif Main.MoveChoice[1] == 97: #If they are trying to castle kingside
                    Main.MoveChoice = [0, 'K', 2]
            elif Main.MoveChoice[1] in Main.enpasSquares and Main.board[Main.MoveChoice[0]] == wP: #If the destination square chosen is an en passant square and piece is pawn
                Main.MoveChoice.append(3) #Assign the move as type en passant
            else: #Else, it's a normal move
                Main.MoveChoice.append(1) #Assign the move as normal type
                
        else:
            if Main.board[Main.MoveChoice[0]] == bK and Main.MoveChoice[1] in [23, 27] and Main.MoveChoice[0] == 25: #Is the move a castle?
                if Main.MoveChoice[1] == 23: #Queenside
                    Main.MoveChoice = [1, 'Q', 2]
                elif Main.MoveChoice[1] == 27: #Kingside
                    Main.MoveChoice = [1, 'K', 2]
            elif Main.MoveChoice[1] in Main.enpasSquares and Main.board[Main.MoveChoice[0]] == bP: #If the destination square chosen is an en passant square and piece is pawn
                Main.MoveChoice.append(3) #Assign the move as type en passant
            else: #Else, it's a normal move
                Main.MoveChoice.append(1)#Assign the move as normal type
        if Main.MoveChoice in Main.FindLegalMoves(Main.Player_Colour): #If move choice is legal move
            Main.MakeMove(Main.MoveChoice) #Make the move
            moveCounterNumLabel.config(text=Main.moveCounter//2+1) #Update move counter label
            Main.MoveChoice = [] #Reset move choice
            Main.PickMode = 1 #Reset pick mode
            if Main.CheckWin() == None: #Check if game ends after player turn
                Main.CPUMove() #If game has not finished, carry on
            if Main.CheckWin() != None: #Check if game has ended after CPU move
                Main.End_Game()
        else: #If choice isn't legal
            DialogueLabel.config(text="Invalid move") #Update dialogue label to let user know
            Main.MoveChoice = [] #Reset move choice
            Main.PickMode = 1 #Reset PickMode
            Set_Sunk(None, True) #Unsink any highlighted selected buttons
    Main.Display() #Update the board display

def Submit2(pressed):
    if Main.PickMode == 1:
        if Main.board[pressed] == ' ':
            DialogueLabel.config(text="Empty square chosen")
        else:
            if Main.moveCounter%2 == 0: #If it's white's turn (even number of moves made)
                if Main.board[pressed] in WHITE_TYPES:
                    Main.MoveChoice.append(pressed)
                    Main.PickMode = 2
                    Set_Sunk(pressed, False)
                else:
                    DialogueLabel.config(text="Invalid square chosen")
            else:
                if Main.board[pressed] in BLACK_TYPES:
                    Main.MoveChoice.append(pressed)
                    Main.PickMode = 2
                    Set_Sunk(pressed, False)
                else:
                    DialogueLabel.config(text="Invalid square chosen")
    elif Main.PickMode == 2:
        if Main.moveCounter%2 == 0:
            if Main.board[pressed] in WHITE_TYPES:
                Main.MoveChoice[0] = pressed
                Set_Sunk(pressed, False)
                return None
        else:
            if Main.board[pressed] in BLACK_TYPES:
                Main.MoveChoice[0] = pressed
                Set_Sunk(pressed, False)
                return None
        Main.MoveChoice.append(pressed)
        if Main.moveCounter%2 == 0: #If the remainder of division by 2 is 0, there have been an even number of moves, so it's white's turn
            if Main.board[Main.MoveChoice[0]] == wK and Main.MoveChoice[1] in [93, 97] and Main.MoveChoice[0] == 95: #If the player has picked a king followed by a rook they are probably trying to castle
                if Main.MoveChoice[1] == 93: #If they are trying to castle queenside
                    Main.MoveChoice = [0, 'Q', 2]
                elif Main.MoveChoice[1] == 97: #If they are trying to castle kingside
                    Main.MoveChoice = [0, 'K', 2]
            elif Main.MoveChoice[1] in Main.enpasSquares and Main.board[Main.MoveChoice[0]] == wP: #If not a castling move, is it an en passant move?
                Main.MoveChoice.append(3)
            else:
                Main.MoveChoice.append(1)#Else, it's a normal move
            if Main.MoveChoice in Main.FindLegalMoves('white'): #After establishing the type of move and the colour of the player moving, attempt move
                Main.MakeMove(Main.MoveChoice) #If move is valid, make move
                Main.active_colour = 'black'
            else:
                DialogueLabel.config(text="Invalid move")
                Main.MoveChoice = []
                Main.PickMode = 1
        else:
            if Main.board[Main.MoveChoice[0]] == bK and Main.MoveChoice[1] in [23, 27] and Main.MoveChoice[0] == 25:
                if Main.MoveChoice[1] == 23: #Queenside
                    Main.MoveChoice = [1, 'Q', 2]
                elif Main.MoveChoice[1] == 27: #Kingside
                    Main.MoveChoice = [1, 'K', 2]
            elif Main.MoveChoice[1] in Main.enpasSquares and Main.board[Main.MoveChoice[0]] == bP:
                Main.MoveChoice.append(3)
            else:
                Main.MoveChoice.append(1)#Else, it's a normal move
            if Main.MoveChoice in Main.FindLegalMoves('black'):
                Main.MakeMove(Main.MoveChoice) #If move is valid, make move
                Main.active_colour = 'white'
            else:
                DialogueLabel.config(text="Invalid move")
                Main.MoveChoice = []
                Main.PickMode = 1
                moveCounterNumLabel.config(text=Main.moveCounter//2+1) #Update move counter label
        Main.MoveChoice = [] #Reset move choice
        Main.PickMode = 1 #Reset pick mode
        Set_Sunk(None, True)
        if Main.CheckWin() != None:
            Main.End_Game()
    else:
        DialogueLabel.config(text="Invalid move")
        Main.MoveChoice = []
        Main.PickMode = 1
        Set_Sunk(None, True)
    Main.Display() #Update the board display

def XOR(a, b):
    newList = []
    for i in range(0, len(a)): #For every number in each list
        if a[i] != b[i]: #XOR them
            newList.append(1)
        else:
            newList.append(0)
    return newList
                
class Board:
    def __init__(self, newBoard, newCastlePerms, newEnpasSquares):
        self.board = newBoard #The 120 long list representing the board layout
        self.__boardHistory = Stack() #A stack containing all the positions in board so far
        self.__castleHistory = Stack() #A stack containing the history of castling permissions in the past
        self.__enpasHistory = Stack() #A stack containing the history of all en passant squares in the past
        self.__piecePosHistory = Stack() #A stack containing the history of all piece positions in history.
        self.__moveHistory = Stack() #A stack containing a history of all the moves made
        self.__piecePositions = {wP:[], bP:[], wKN:[], bKN:[], wB:[], bB:[], wR:[], bR:[], wQ:[], bQ:[], wK:[], bK:[]} #The indexes of all the pieces on the board
        self.castles = newCastlePerms #A list of length 4; [WQ, WK, BQ, BK]
        self.moveCounter = 0 #Number of moves made so far in game
        self.enpasSquares = newEnpasSquares #Squares designated as en passant squares
        self.FindPieces() #Find all the pieces on the board
        self.Zobrist = [] #An array representing the zobrist hash of the board. Initialised as empty, but will be immediately calculated.
        self.Hash() #Hash the board
        self.PickMode = 1 #Helps distinguish between button clicks. If 1, the square clicked is the piece to be moved. If 2, the square clicked is a destination
        self.MoveChoice = [] #The choice of move so far chosen by the user. [Starting square, destination square, move type]
        if timer.get() == '--': #If time conditions requested, make play clock active and set appropriate time.
            self.time_active = False #Time is not active in this game. Timer doesn't function.
        else:
            self.time_active = True #Time is active in this game. Timer functions.
            if (n := int(timer.get())) == 30: #If the 30 setting is chosen, 30 seconds. Else, convert time selected from minutes to seconds.
                self.white_time = n #Assigns both white and black time as 30 using walrus operator.
                self.black_time = n
            else:
                self.white_time = n*60 #Assigns both white and black time as corresponding time using walrus operator.
                self.black_time = n*60
            self.active_colour = 'white' #Initially timer is set to count down white's time, as it's white's turn initially
        if playerAmount.get() == 1: #If single player
            if player1Colour.get() == 0: #If user chooses to be white
                self.Player_Colour, self.AI_Colour = 'white', 'black' #Player = white, AI = black
            else:
                self.Player_Colour, self.AI_Colour = 'black', 'white' #Player = black, AI = white
        self.Difficulty = difficulty.get() #Sets game difficulty as that chosen by the user. This makes it unchangeable by the user throughout the game.

    def Get_boardHistory(self):
        return self.__boardHistory

    def TextResponse(self, PE):
        if self.AI_Colour == 'black': #Using the predicted evaluation to dreate dialogue. First, measure how good the game is from AI perspective.
            PE = PE*-1
        if PE>0:
            if PE>600:
                DialogueLabel.config(text=TAUNTS[random.randint(0, len(TAUNTS)-1)])
            elif PE>400:
                DialogueLabel.config(text='Yawn...')
            elif PE>100:
                DialogueLabel.config(text=':)')
            else:
                DialogueLabel.config(text='...')
        else:
            if PE<-1000:
                DialogueLabel.config(text='AI feels uneasy...')
            elif PE<-300:
                DialogueLabel.config(text=':/')
            else:
                DialogueLabel.config(text='...')

    def End_Game(self):        
        state = self.CheckWin()
        if state == 0: #If stalemate
            End_Window(None, 'stalemate', self)
        elif state == 1: #If black won
            winning_colour = 'Black'
            if self.time_active: #Check if win is by timeout or checkmate
                if self.white_time <= 0:
                    End_Window('Black', 'timeout', self)
                else:
                    End_Window('Black', 'checkmate', self)
            else:
                End_Window('Black', 'checkmate', self)
        else: #If white won
            winning_colour = 'White'
            if self.time_active:
                if self.black_time <= 0:
                    End_Window('White', 'timeout', self)
                else:
                    End_Window('White', 'checkmate', self)
            else:
                End_Window('White', 'checkmate', self)                     
        Main.PickMode = None
        Main.time_active = False
        Set_Sunk(None, True)

    def Hash(self):
        self.Zobrist = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0] #An array of 33 zeroes.
        for piece in self.__piecePositions: #For every piece type
            for index in self.__piecePositions[piece]: #For every poisition of that piece
                self.Zobrist = XOR(self.Zobrist, ZOB_DICT[piece][index]) #XOR corresponding seed with hash digest
        for i in range(4): #For every castle permission
            if self.castles[i] == 1: #If permission is allowed, apply corresponding XOR
                self.Zobrist = XOR(self.Zobrist, castlezob[i])

    def FindPieces(self):
        for key in self.__piecePositions: #Reset all positions
            self.__piecePositions[key] = []            
        for r in range(2, 10): #For every square on board
            for t in range(1, 9):
                index = r*10+t
                if not(self.board[index] == ' '): #If found a piece
                    self.__piecePositions[self.board[index]].append(index) #Add piece position to dict

    def Display(self):
        global ButtonList
        for i in range(120):
            if not(ButtonList[i] == None): #If there's a button in this index
                ButtonList[i].config(text=self.board[i])

    def FromFEN(self, FEN): #FEN is the string which will be used to build the board
        tempBoard = [] #Temporary board. 
        pointer = 0 #Used to iterate through string
        width = 0
        rows = 0
        if FEN == '':
            DialogueLabel.config(text="Error in initialisation. No FEN input detected.")
            return 'failed'
        while True and pointer<len(FEN): #Loop goes through the first word of the string, and builds a 64-long board list out of it
            current = FEN[pointer] #Current is the currently viewed letter
            if current == ' ': #If the current character is a space, either there was an input error or it is the end of the initial word
                if rows != 7: #If it isn't the end of the board word, there is an error. 7 because the last row isn't 
                    DialogueLabel.config(text="Error in initialisation. There should be 8 rows")
                    return 'failed'
                else:
                    if width != 8: #Width of the last row should also be 8
                        DialogueLabel.config(text="Error in initialisation. Rows should have a length of 8")
                        return 'failed'
                    else:
                        break #Else, if a space is shown it should be the end of the board word
            elif current == '/': #New row. Check if current row is 8 long. Else, error.
                if width == 8: #When starting a new line, the length of the previous row should be 8. If not, error
                    width = 0 #Reset width as it's a new row
                    rows += 1 #Increment the number of rows by 1
                else:
                    DialogueLabel.config(text="Error in initialisation. Rows should have a length of 8")
                    return 'failed'
            else: #If current isn't space, should be either letter indicating piece or number indicating space
                try:
                    current = int(current) #Check if current can be turned into integer. If so, add this many spaces
                    for i in range(current):
                        tempBoard.append(' ')
                        width += 1
                except: #If it isn't an integer, it's a character.
                    try:
                        tempBoard.append(FENletters[current]) #If the character is not a space, add it to tempBoard. If an error is raised, it should be a key error, so print that a character isn't recognised
                        width += 1
                    except:
                        tempString = "Error in initialisation. Character '"+current+"' not recognised"
                        DialogueLabel.config(text=tempString)
                        return 'failed'
            if width>8:
                DialogueLabel.config(text="Error in initialisation. Rows should have a length of 8")
                return 'failed'
            pointer += 1 #Increment pointer
        pointer += 1 #Add to the pointer. This is because after the end of the board string, the program should go to the next character and find it's a string. Then, the next character indicates who's turn it is
        if FEN[pointer] == 'w':
            turn = 'white'
        elif FEN[pointer] == 'b':
            turn = 'black'
        else:
            DialogueLabel.config(text="Error in initialisation. Turn incorrectly identified")
            return 'failed'
        pointer += 2 #Increment pointer twice as there's a space between the next word
        self.castles = [0, 0, 0, 0]
        while FEN[pointer] != ' ': #Until the end of the current word. Castling permissions
            try:
                if FEN[pointer] == 'Q':
                    self.castles[0] = 1
                elif FEN[pointer] == 'K':
                    self.castles[1] = 1
                elif FEN[pointer] == 'q':
                    self.castles[2] = 1
                elif FEN[pointer] == 'k':
                    self.castles[3] = 1
                elif FEN[pointer] == '-':
                    self.castles = [0, 0, 0, 0]
                    pointer += 1
                    break
                else:
                    DialogueLabel.config(text="Error in initialisation. Castling permissions not recognised")
                    return 'failed'
                pointer += 1
            except:
                DialogueLabel.config(text="Error in initialisation. Please enter '-' to denote no castling permissions.")
                return 'failed'
        pointer += 1 #Increment pointer once because the previous loop already incremented when it ended, so space already accounted for
        if FEN[pointer] == '-': #If no en passant squares indicated, pass
            pass
        else: #Else there should be a valid en passant square indicated
            try:
                self.enpasSquares.append(Convert(FEN[pointer:pointer+2].upper())) #Try to convert the indicated square into an index, and then mark as en passant square
            except:
                DialogueLabel.config(text="Error in initialisation. En passant square not recognised")
                return 'failed'
        pointer = 0
        for r in range(2, 10): #For every square on board
            for t in range(1, 9):
                self.board[r*10+t] = tempBoard[pointer] #Iterate through all active squares on board, and then assign as corresponding tempBoard element
                pointer += 1
        self.FindPieces() #Find pieces on the board
        if not(len(self.__piecePositions[wK]) == 1 and len(self.__piecePositions[bK])) == 1:
            DialogueLabel.config(text="Error in initialisation. Both sides must have one king.")
            return 'failed'
        if turn == 'black':
            self.moveCounter = 1
        if playerAmount.get() == 1:
            if turn != self.Player_Colour:
                self.CPUMove()
        DialogueLabel.config(text='')
        if Main.CheckWin() != None:
            Main.End_Game()

    def Evaluate(self):
        total = 0
        for piece in EVAL_KEYS_WHITE: #For every white piece
            for index in self.__piecePositions[piece]: #For every square holding this type of piece
                total += PSTables[piece][index] #Add the value of the piece in the given square
        for piece in EVAL_KEYS_BLACK: #For every black piece
            for index in self.__piecePositions[piece]: #For every square holding this type of piece
                total -= PSTables[piece][index] #Subtract value of piece in given square from total
        if len(self.__piecePositions[bKN])+len(self.__piecePositions[bB])+len(self.__piecePositions[bR])>1 and len(self.__piecePositions[bQ])>0: #Early game criteria
            total += PSTables['wKstart'][self.__piecePositions[wK][0]] #Use piece-square table for early game king
        else: #Else if it's an end game situation
            total += PSTables['wKend'][self.__piecePositions[wK][0]] #Else use end game king piece square table
        if len(self.__piecePositions[wKN])+len(self.__piecePositions[wB])+len(self.__piecePositions[wR])>1 and len(self.__piecePositions[wQ])>0: #Early game criteria
            total -= PSTables['bKstart'][self.__piecePositions[bK][0]] #Use piece-square table for early game king
        else: #Else if it's an end game situation
            total -= PSTables['bKend'][self.__piecePositions[bK][0]] #Else use end game king piece square table
        return total

    def CheckWin(self): #0, 1, 2 = stalemate, black win, white win
        if self.time_active:
            if self.white_time <= 0: #If white has run out of time
                return 1
            elif self.black_time <= 0: #If black has run out of time
                return 2
        if self.moveCounter%2 == 0:
            if len(self.FindLegalMoves('white')) == 0: #If there are no moves white can make
                if self.SQAttacked(self.__piecePositions[wK][0], 'black'): #If king is in check, then it's checkmate and black wins
                    return 1
                else: #If king is not in check, there are no moves white can make, so stalemate
                    return 0
        else:
            if len(self.FindLegalMoves('black')) == 0: #If there are no moves black can make
                if self.SQAttacked(self.__piecePositions[bK][0], 'white'): #If king is in check, then it's checkmate and white wins
                    return 2
                else:
                    return 0
        return None
    
    def CPUMove(self):
        global iterations, extensions
        self.active_colour = None #Stop the timer thread from decrementing times. Time taken to find move is calculated inside this method and then subtracted seperately from timer thread.
        self.Hash() #Hash this position, to find if it's in the playbook
        RefreshGUI() #Reset GUI. Remove all coloured squares and sunk reliefs.
        if join(self.Zobrist) in PLAYBOOK: #If there position is in the playbook, make the listed move
            if len(PLAYBOOK[join(self.Zobrist)]) == 1: #If there's only one listed move for the position, make it.
                Move = PLAYBOOK[join(self.Zobrist)][0]
            else:
                Move = PLAYBOOK[join(self.Zobrist)][random.randint(0, len(PLAYBOOK[join(self.Zobrist)])-1)] #If there are multiple moves suggested in the playbook for a certain position, pick a random one and play it
            TempString = 'CPU making move from playbook: '+Convert(Move[0])+' '+Convert(Move[1]) #Update dialogue label
            DialogueLabel.config(text=TempString)
            self.MakeMove(Move) #Make the move
            self.active_colour = self.Player_Colour #Set player as the active colour
        else: #If position not in playbook, search for best move
            iterations = 0 #Variable used to track the number of nodes searched by alphabeta.
            extensions = 0 #Variable used to track the number of nodes searched by quiescience.
            start_time = time.perf_counter() #Starting time for alphabeta.
            if self.time_active:
                if self.AI_Colour == 'white': #If AI is white, get remaining time for white. This will be used to make sure the AI doesn't lose easily on time conditions
                    time_slot = self.white_time
                else:
                    time_slot = self.black_time
                if time_slot <= AI_MINIMAL_BOUND: #If AI has very low time remaining, play to a difficulty of 1 for maximum speed
                    Move, PE = self.Alphabeta(1, -(math.inf), math.inf, self.AI_Colour)
                elif time_slot <= AI_LOWER_BOUND: #If AI has fairly low time remaining, play to a difficulty of 2 for increased speed
                    Move, PE = self.Alphabeta(2, -(math.inf), (math.inf), self.AI_Colour)
                else: #Else AI has sufficient time, play to chosen difficulty
                    Move, PE = self.Alphabeta(self.Difficulty, -(math.inf), (math.inf), self.AI_Colour)
                time_taken = time.perf_counter()-start_time #The current_time-start_time = time taken by AI to find move.
                if self.AI_Colour == 'white': #If AI is white, update white's time with how long CPU took and update white's time label.
                    self.white_time -= time_taken
                    Update_Label('white', self.white_time)
                else: #Else, '' but with black time and label.
                    self.black_time -= time_taken
                    Update_Label('black', self.black_time)
                self.active_colour = self.Player_Colour
            else:
                Move, PE = self.Alphabeta(difficulty.get(), -(math.inf), (math.inf), self.AI_Colour)
                time_taken = time.perf_counter()-start_time #The current_time-start_time = time taken by AI to find move.
            print("Time taken to find move:", time_taken, "\nProcessed", iterations+extensions, "nodes, for a speed of", (iterations+extensions)/time_taken, "nps")
            print("Alphabeta searched", iterations, "nodes")
            print("Quiescience searched", extensions, "extensions\n")
            Legal_Moves = self.FindLegalMoves(self.AI_Colour)
            if Move in Legal_Moves:
                self.MakeMove(Move)
            else:
                self.MakeMove(Legal_Moves[random.randint(0, len(Legal_Moves)-1)])
            self.TextResponse(PE)
        try: #Change colour of squares involved in move. If castle move, colour corresponding squares
            ButtonList[Move[0]].config(bg='light goldenrod')
            ButtonList[Move[1]].config(bg='gold')
        except:
            if Move[1] == 'K':
                if self.AI_Colour == 'white':
                    ButtonList[95].config(bg='light goldenrod')
                    ButtonList[97].config(bg='gold')
                else:
                    ButtonList[25].config(bg='light goldenrod')
                    ButtonList[27].config(bg='gold')
            else:
                if self.AI_Colour == 'white':
                    ButtonList[95].config(bg='light goldenrod')
                    ButtonList[93].config(bg='gold')
                else:
                    ButtonList[25].config(bg='light goldenrod')
                    ButtonList[23].config(bg='gold')
        
    def Alphabeta(self, depth, alpha, beta, colour):
        global iterations
        iterations += 1 #Number of nodes search in initial tree
        if len(self.__piecePositions[wK]) == 0:
            return [None, -30000]
        elif len(self.__piecePositions[bK]) == 0:
            return [None, 30000]
        elif depth == 0:
            return [None, self.Quiescence_Search(3, alpha, beta, colour, None)]
        moves = self.GenMoves(colour)
        if colour == 'white': #If colour is white
            best = [None, -(math.inf)] #Define best
            for move in self.GenMoves('white'): #For every move
                self.MakeMove(move) #Make move
                score = self.Alphabeta(depth-1, alpha, beta, 'black')[1] #From this child node, apply the algorithm recursively
                self.UndoMove() #Undo move
                if score>best[1]:
                    best[1] = score
                    best[0] = move
                alpha = max(best[1], alpha)
                if alpha>=beta:
                    break
            return best
        else: #If colour is black
            best = [None, math.inf]
            for move in self.GenMoves('black'): #For every move
                self.MakeMove(move)
                score = self.Alphabeta(depth-1, alpha, beta, 'white')[1]
                self.UndoMove()
                if score<best[1]:
                    best[1] = score
                    best[0] = move
                beta = min(best[1], beta)
                if alpha>=beta:
                    break
            return best

    def Quiescence_Search(self, depth, alpha, beta, colour, previous_evaluation):
        global extensions
        extensions += 1 #Tracking number of nodes searched by quiescence extension
        if len(self.__piecePositions[wK]) == 0: #If node is terminal
            return -30000 #Quiescience doesn't need to return a move, just a more accurate evaluation
        elif len(self.__piecePositions[bK]) == 0:
            return 30000
        else:
            current_evaluation = self.Evaluate() #If node isn't terminal, evaluate node
        if depth == 0: #If maximum depth reached
            return current_evaluation
        elif previous_evaluation != None and abs(previous_evaluation-current_evaluation) < 100: #If there's less than a pawns difference between the previous evaluation and the current, node is stable
            return current_evaluation
        if colour == 'white': #If node unstable, extend tree search in similar way to alphabeta
            best = -(math.inf)
            for move in self.GenMoves('white'):
                self.MakeMove(move)
                score = self.Quiescence_Search(depth-1, alpha, beta, 'black', current_evaluation)
                self.UndoMove()
                best = max(score, best)
                alpha = max(alpha, best)
                if alpha>=beta:
                    break
            return best
        else: #If colour is black
            best = math.inf
            for move in self.GenMoves('black'):
                self.MakeMove(move)
                score = self.Quiescence_Search(depth-1, alpha, beta, 'white', current_evaluation)
                self.UndoMove()
                best = min(score, best)
                beta = min(beta, best)
                if alpha>=beta:
                    break
            return best
        
    def UndoMove(self):
        self.board = self.__boardHistory.pop() #Return all stored variables of board to the values of the previous board, and remove from stack (pop)
        self.castles = self.__castleHistory.pop()
        self.enpasSquares = self.__enpasHistory.pop()
        self.__piecePositions = self.__piecePosHistory.pop()
        self.moveCounter -= 1

    def MakeMove(self, move):
        self.__boardHistory.push(self.board.copy()) #Store details of board for future use
        self.__castleHistory.push(self.castles.copy())
        self.__enpasHistory.push(self.enpasSquares.copy())
        self.__piecePosHistory.push(copy.deepcopy(self.__piecePositions))
        self.__moveHistory.push(move)
        self.moveCounter += 1 #Increment move counter
        self.enpasSquares = [] #Reset en passant squares
        if move[2] == 1: #If normal move
            sPiece = self.board[move[0]] #Moving piece
            dPiece = self.board[move[1]] #Destination square/piece
            self.Replace(move[0], move[1]) #Replace the destination square with the moving piece
            self.__piecePositions[sPiece].remove(move[0]) #Update piece positions
            self.__piecePositions[sPiece].append(move[1])
            if dPiece != ' ':
                self.__piecePositions[dPiece].remove(move[1])
            if sPiece == wP and move[0]-move[1] == 20: #If the piece moving is a pawn and it has moved two squares
                self.enpasSquares.append(move[0]-10) #Create en passant square
            elif sPiece == bP and move[1]-move[0] == 20:
                self.enpasSquares.append(move[0]+10)
            if move[0] in CASTLE_SQUARES: #If king or rook is moved, can't castle anymore
                if sPiece in WHITE_TYPES:
                    if sPiece == wK:
                        if self.castles[0] != 0:
                            self.castles[0] = 0
                        if self.castles[1] != 0:
                            self.castles[1] = 0
                    elif sPiece == wR:
                        if move[0] == 91:
                            if self.castles[0] != 0:
                                self.castles[0] = 0
                        elif move[0] == 98:
                            if self.castles[1] != 0:
                                self.castles[1] = 0
                else:
                    if sPiece == bK:
                        if self.castles[2] != 0:
                            self.castles[2] = 0
                        if self.castles[3] != 0:
                            self.castles[3] = 0
                    elif sPiece == bR:
                        if move[0] == 21:
                            if self.castles[2] != 0:
                                self.castles[2] = 0
                        elif move[0] == 28:
                            if self.castles[3] != 0:
                                self.castles[3] = 0            
            if sPiece == wP: #Promotions
                if move[1]//10 == 2:
                    self.board[move[1]] = wQ
                    self.__piecePositions[wP].remove(move[1])
                    self.__piecePositions[wQ].append(move[1])
            elif sPiece == bP:
                if move[1]//10 == 9:
                    self.board[move[1]] = bQ
                    self.__piecePositions[bP].remove(move[1])
                    self.__piecePositions[bQ].append(move[1])
        elif move[2] == 2: #Castle move. Move will tell whether it's white or black, short or long.
            if move[0] == 0: #If colour is white
                if move[1] == 'Q':
                    self.Replace(95, 93)
                    self.__piecePositions[wK][0] = 93
                    self.Replace(91, 94)
                    self.__piecePositions[wR].remove(91)
                    self.__piecePositions[wR].append(94)
                elif move[1] == 'K':
                    self.Replace(95, 97)
                    self.__piecePositions[wK][0] = 97
                    self.Replace(98, 96)
                    self.__piecePositions[wR].remove(98)
                    self.__piecePositions[wR].append(96)
                self.castles[0] = 0 #Disallow any future castles from white
                self.castles[1] = 0
            elif move[0] == 1:
                if move[1] == 'Q':
                    self.Replace(25, 23)
                    self.__piecePositions[bK][0] = 23
                    self.Replace(21, 24)
                    self.__piecePositions[bR].remove(21)
                    self.__piecePositions[bR].append(24)
                elif move[1] == 'K':
                    self.Replace(25, 27)
                    self.__piecePositions[bK][0] = 27
                    self.Replace(28, 26)
                    self.__piecePositions[bR].remove(28)
                    self.__piecePositions[bR].append(26)
                self.castles[2] = 0
                self.castles[3] = 0
        elif move[2] == 3: #En passant move
            sPiece = self.board[move[0]]
            self.Replace(move[0], move[1])
            self.__piecePositions[sPiece].remove(move[0]) #Update piece positions
            self.__piecePositions[sPiece].append(move[1])
            if sPiece == wP:
                self.board[move[1]+10] = ' '
                self.__piecePositions[bP].remove(move[1]+10)
            else:
                self.board[move[1]-10] = ' '
                self.__piecePositions[wP].remove(move[1]-10)
                
    def Replace(self, start, dest): #Starting square index, destination square index
        sPiece = self.board[start] #Get the piece in the starting index
        self.board[dest] = sPiece #Put the chosen piece in the destintation square
        self.board[start] = ' ' #Define the initial square as empty
        
    def GenMoves(self, colour):
        quietMoves = []
        captures = []
        enpas = []
        if colour == 'white': #If finding white moves
            for index in self.__piecePositions[wP]: #For every white pawn on board
                if self.board[index-10] == ' ': #Pawn move 1 ahead
                    quietMoves.append([index, index-10, 1])
                    if self.board[index-20] == ' ' and index//10 == 8: #Pawn move 2 ahead. If space is clear and on the correct row
                        quietMoves.append([index, index-20, 1])
                if self.board[index-11] in BLACK_TYPES: #If piece is diagonal, can capture
                    captures.append([index, index-11, 1])
                elif index-11 in self.enpasSquares and index//10 != 8: #If there is an en passant square diagonally, and it's not just one created by the side's own pawn moving forwards, can capture
                    enpas.append([index, index-11, 3])
                if self.board[index-9] in BLACK_TYPES:
                    captures.append([index, index-9, 1])
                elif index-9 in self.enpasSquares and index//10 != 8:
                    enpas.append([index, index-9, 3])
            for index in self.__piecePositions[wKN]: #For every white knight on board
                for num in MOVES_KNIGHT: #For every square the current knight can go to
                    if self.board[index+num] == ' ':
                        quietMoves.append([index, index+num, 1])
                    elif self.board[index+num] in BLACK_TYPES:
                        captures.append([index, index+num, 1])
            for index in self.__piecePositions[wB]:
                for num in MOVES_BISHOP:
                    cont = True
                    q = num
                    while cont == True:
                        c = self.board[index+q]
                        if c==None or c in WHITE_TYPES:
                            cont = False
                        elif c in BLACK_TYPES:
                            cont = False
                            captures.append([index, index+q, 1])
                        elif c == ' ':
                            quietMoves.append([index, index+q, 1])
                        q=q+num
            for index in self.__piecePositions[wR]:
                for num in MOVES_ROOK:
                    cont = True
                    q = num
                    while cont == True:
                        c = self.board[index+q]
                        if c == None or c in WHITE_TYPES:
                            cont = False
                        elif c in BLACK_TYPES:
                            cont = False
                            captures.append([index, index+q, 1])
                        elif c == ' ':
                            quietMoves.append([index, index+q, 1])
                        q = q+num
            for index in self.__piecePositions[wQ]:
                for num in MOVES_BISHOP:
                    cont = True
                    q = num
                    while cont == True:
                        c = self.board[index+q]
                        if c == None or c in WHITE_TYPES:
                            cont = False
                        elif c in BLACK_TYPES:
                            cont = False
                            captures.append([index, index+q, 1])
                        elif c == ' ':
                            quietMoves.append([index, index+q, 1])
                        q = q+num
                for num in MOVES_ROOK:
                    cont = True
                    q = num
                    while cont == True:
                        c = self.board[index+q]
                        if c == None or c in WHITE_TYPES:
                            cont = False
                        elif c in BLACK_TYPES:
                            cont = False
                            captures.append([index, index+q, 1])
                        elif c == ' ':
                            quietMoves.append([index, index+q, 1])
                        q = q+num
            for index in self.__piecePositions[wK]:
                for num in MOVES_KING:
                    if self.board[index+num] == ' ':
                        quietMoves.append([index, index+num, 1])
                    elif self.board[index+num] in BLACK_TYPES:
                        captures.append([index, index+num, 1])
        if colour == 'black': #If finding black moves
            for index in self.__piecePositions[bP]: #For every white pawn on board
                if self.board[index+10] == ' ': #Pawn move 1 ahead
                    quietMoves.append([index, index+10, 1])
                    if self.board[index+20] == ' ' and index//10 == 3: #Pawn move 2 ahead. If space is clear and on the correct row
                        quietMoves.append([index, index+20, 1])

                if self.board[index+11] in WHITE_TYPES: #If piece is diagonal, can capture
                    captures.append([index, index+11, 1])
                elif index+11 in self.enpasSquares and index//10 != 3:
                    enpas.append([index, index+11, 3])
                    
                if self.board[index+9] in WHITE_TYPES:
                    captures.append([index, index+9, 1])
                elif index+9 in self.enpasSquares and index//10 != 3:
                    enpas.append([index, index+9, 3])
            for index in self.__piecePositions[bKN]: #For every white knight on board
                for num in MOVES_KNIGHT: #For every square the current knight can go to
                    if self.board[index+num] == ' ':
                        quietMoves.append([index, index+num, 1])
                    elif self.board[index+num] in WHITE_TYPES:
                        captures.append([index, index+num, 1])
            for index in self.__piecePositions[bB]:
                for num in MOVES_BISHOP:
                    cont = True
                    q = num
                    while cont == True:
                        c = self.board[index+q]
                        if c==None or c in BLACK_TYPES:
                            cont = False
                        elif c in WHITE_TYPES:
                            cont = False
                            captures.append([index, index+q, 1])
                        elif c == ' ':
                            quietMoves.append([index, index+q, 1])
                        q=q+num
            for index in self.__piecePositions[bR]:
                for num in MOVES_ROOK:
                    cont = True
                    q = num
                    while cont == True:
                        c = self.board[index+q]
                        if c == None or c in BLACK_TYPES:
                            cont = False
                        elif c in WHITE_TYPES:
                            cont = False
                            captures.append([index, index+q, 1])
                        elif c == ' ':
                            quietMoves.append([index, index+q, 1])
                        q = q+num
            for index in self.__piecePositions[bQ]:
                for num in MOVES_BISHOP:
                    cont = True
                    q = num
                    while cont == True:
                        c = self.board[index+q]
                        if c == None or c in BLACK_TYPES:
                            cont = False
                        elif c in WHITE_TYPES:
                            cont = False
                            captures.append([index, index+q, 1])
                        elif c == ' ':
                            quietMoves.append([index, index+q, 1])
                        q = q+num
                for num in MOVES_ROOK:
                    cont = True
                    q = num
                    while cont == True:
                        c = self.board[index+q]
                        if c == None or c in BLACK_TYPES:
                            cont = False
                        elif c in WHITE_TYPES:
                            cont = False
                            captures.append([index, index+q, 1])
                        elif c == ' ':
                            quietMoves.append([index, index+q, 1])
                        q = q+num
            for index in self.__piecePositions[bK]:
                for num in MOVES_KING:
                    if self.board[index+num] == ' ':
                        quietMoves.append([index, index+num, 1])
                    elif self.board[index+num] in WHITE_TYPES:
                        captures.append([index, index+num, 1])
        if colour == 'white': #Find castle moves
            if self.castles[0] == 1: #If WQ castle is valid
                if self.board[91] == wR and self.board[95] == wK:
                    if self.board[92] == ' ' and self.board[93] == ' ' and self.board[94] == ' ' and self.SQAttacked(93, 'black') == False and self.SQAttacked(94, 'black') == False and self.SQAttacked(95, 'black') == False:
                        quietMoves.append([0, 'Q', 2])
            if self.castles[1] == 1: #WK
                if self.board[98] == wR and self.board[95] == wK:
                    if self.board[96] == ' ' and self.board[97] == ' ' and self.SQAttacked(96, 'black') == False and self.SQAttacked(97, 'black') == False and self.SQAttacked(95, 'black') == False:
                        quietMoves.append([0, 'K', 2])
        else: #Black
            if self.castles[2] == 1: #If BQ castle is valid
                if self.board[21] == bR and self.board[25] == bK:
                    if self.board[22] == ' ' and self.board[23] == ' ' and self.board[24] == ' ' and self.SQAttacked(23, 'white') == False and self.SQAttacked(24, 'white') == False and self.SQAttacked(25, 'white') == False:
                        quietMoves.append([1, 'Q', 2])
            if self.castles[3] == 1: #BK
                if self.board[28] == bR and self.board[25] == bK:
                    if self.board[26] == ' ' and self.board[27] == ' ' and self.SQAttacked(26, 'white') == False and self.SQAttacked(27, 'white') == False and self.SQAttacked(25, 'white') == False:
                        quietMoves.append([1, 'K', 2])
        if captures != []: #If the captures list is not empty, sort it in order of LVA/MVV
            captures = self.SortMoves(captures)
        return captures+enpas+quietMoves

    def SortMoves(self, newList): #A merge sort algorithm to sort moves based on LVA/MVV
        if len(newList) == 1:
            return newList
        left = newList[:len(newList)//2] #Split list into two halves
        right = newList[len(newList)//2:]
        left = self.SortMoves(left)
        right = self.SortMoves(right)
        newList = self.Merge_Moves(left, right) #Merge the two now sorted halves based on the move values
        return newList #Return the sorted list

    def Merge_Moves(self, left, right):
        newList = []
        j = 0 #Left iteration. Helps to iterate through left list of moves without needing to delete values from the list
        k = 0 #Right iteration ''
        while j<len(left) and k<len(right):
            if ABSOLUTE_VALUES[self.board[left[j][1]]] - ABSOLUTE_VALUES[self.board[left[j][0]]] > ABSOLUTE_VALUES[self.board[right[k][1]]] - ABSOLUTE_VALUES[self.board[right[k][0]]]:
                newList.append(left[j]) #If the value of the current moves of left is higher than the move of right, add left
                j += 1                  #If left.(value_of_victim - value_of_attacker) > right.(value_of_victim - value_of_attacker)
            else:                       #THEN left move is better, add left move
                newList.append(right[k])
                k += 1
        while j<len(left):
            newList.append(left[j])
            j += 1
        while k<len(right):
            newList.append(right[k])
            k += 1
        return newList

    def FindLegalMoves(self, colour):
        moves = self.GenMoves(colour)
        delList = []
        if colour == 'white':
            for move in moves: #For every move
                Main.Display()
                self.MakeMove(move) #Make the move, and if it leaves the king attacked, it's illegal
                if self.SQAttacked(self.__piecePositions[wK][0], 'black'):
                    delList.append(move)
                self.UndoMove()
        else:
            for move in moves:
                self.MakeMove(move)
                if self.SQAttacked(self.__piecePositions[bK][0], 'white'):
                    delList.append(move)
                self.UndoMove()
        for move in delList: #For every move which resulted in the king being in check, remove the move from list of legal moves
            moves.remove(move)
        return moves

    def SQAttacked(self, index, col):
        if col == 'white': #Attacked by white?            
            if self.board[index+9] == wP or self.board[index+11] == wP:
                return True
            for num in MOVES_KNIGHT:
                if self.board[index+num] == wKN or self.board[index-num] == wKN:
                    return True
            for num in MOVES_KING:
                if self.board[index+num] == wK or self.board[index-num] == wK:
                    return True
            for num in MOVES_BISHOP:
                cont = True
                q = num
                while cont:
                    c = self.board[index+q]
                    if c == wB or c == wQ:
                        return True
                    elif c in WHITE_TYPES or c in BLACK_TYPES or c==None:
                        cont = False
                    q+=num
            for num in MOVES_ROOK:
                cont = True
                q = num
                while cont:
                    c = self.board[index+q]
                    if c == wR or c == wQ:
                        return True
                    elif c in WHITE_TYPES or c in BLACK_TYPES or c==None:
                        cont = False
                    q+=num                    
        else: #Attacked by black?            
            if self.board[index-9] == bP or self.board[index-11] == bP:
                return True
            for num in MOVES_KNIGHT:
                if self.board[index+num] == bKN or self.board[index-num] == bKN:
                    return True
            for num in MOVES_KING:
                if self.board[index+num] == bK or self.board[index-num] == bK:
                    return True
            for num in MOVES_BISHOP:
                cont = True
                q = num
                while cont:
                    c = self.board[index+q]
                    if c == bB or c == bQ:
                        return True
                    elif c in WHITE_TYPES or c in BLACK_TYPES or c==None:
                        cont = False
                    q+=num
            for num in MOVES_ROOK:
                cont = True
                q = num
                while cont:
                    c = self.board[index+q]
                    if c == bR or c == bQ:
                        return True
                    elif c in WHITE_TYPES or c in BLACK_TYPES or c==None:
                        cont = False
                    q+=num
        return False
        
class MainWindow(Frame):
    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()
        
    def init_window(self):
        global ButtonList, FENEntry, moveCounterNumLabel, CEValLabel, PEValLabel, DialogueLabel, whiteTimerLabel, blackTimerLabel
        self.master.title("Chess Game")
        root.geometry("1000x650+100+6")
        myCanvas = Canvas(root, width=1000, height=650)
        myCanvas.pack()
        myCanvas.create_rectangle(3, 3, 611, 595) #Board
        myCanvas.create_rectangle(3, 595, 611, 647, fill='white') #Move log
        myCanvas.create_rectangle(615, 3, 806, 100, fill='white') #White timer label space
        myCanvas.create_rectangle(806, 3, 997, 100, fill='black') #Black timer label space
        whiteTimerLabel = Label(text="--", font=('Helvetica', '30'), bg='white') #White timer
        whiteTimerLabel.place(x=655, y=28)
        blackTimerLabel = Label(text="--", font=('Helvetica', '30'), bg='black', fg='white') #Black timer
        blackTimerLabel.place(x=845, y=28)
        myCanvas.create_rectangle(615, 103, 997, 170) #Evaluation
        myCanvas.create_rectangle(615, 173, 997, 397) #New game
        myCanvas.create_rectangle(615, 400, 997, 647) #Leaderboard
        moveCounterLabel = Label(text='Move Counter:', bg='white')
        moveCounterLabel.place(x=495, y=597)
        moveCounterNumLabel = Label(text=0, bg='white')
        moveCounterNumLabel.place(x=580, y=597)
        DialogueLabel = Label(text='', font='Helvetica', bg='white')
        DialogueLabel.place(x=20, y=615)
        EvalLabel = Label(text='Evaluation:')
        EvalLabel.place(x=620, y=106)
        currentEvalLabel = Label(text='CE:')
        currentEvalLabel.place(x=687, y=106)
        predictedEvalLabel = Label(text='PE:')
        predictedEvalLabel.place(x=687, y=125)
        CEValLabel = Label(text='-')
        CEValLabel.place(x=710, y=106)
        PEValLabel = Label(text='-')
        PEValLabel.place(x=710, y=125)
        reqEvalButton = Button(text='Evaluate Board', command=lambda:EvalBoard(), width = 14)
        reqEvalButton.place(x=750, y=106)
        suggestMoveButton = Button(text='Suggest Move', command = lambda:SuggestMove(), width=14)
        suggestMoveButton.place(x=880, y=106)
        evalHelpButton = Button(text='?', font=('Helvetica', '10'), width = 12, command=lambda:EvalHelp())
        evalHelpButton.place(x=881, y=134)
        UndoButton = Button(text='Undo', command=lambda:MainUndo(), width=14)
        UndoButton.place(x=750, y=135)
        newGameLabel = Label(text='New Game', font=("Helvetica", "14"))
        newGameLabel.place(x=750, y=182)
        playerAmountLabel = Label(text='How many players:')
        playerAmountLabel.place(x=630, y=220)
        twoPlayerRad = Radiobutton(text='Two Player', variable=playerAmount, value=2)
        twoPlayerRad.place(x=850, y=218)
        singlePlayerRad = Radiobutton(text='Single Player', variable=playerAmount, value=1)
        singlePlayerRad.place(x=745, y=218)
        player1ColourLabel = Label(text='Player Colour:')
        player1ColourLabel.place(x=630, y=245)
        
        player1ColourB = Radiobutton(text='Black', variable=player1Colour, value=1)
        player1ColourB.place(x=780, y=243)
        player1ColourW = Radiobutton(text='White', variable=player1Colour, value=0)
        
        player1ColourW.place(x=710, y=243)
        diffLabel = Label(text='Difficulty: ')
        diffLabel.place(x=630, y=268)
        diffDropBox = OptionMenu(root, difficulty, *difficulties)
        diffDropBox.place(x=690, y=263)
        timeLabel = Label(text='Time (seconds/minutes): ')
        timeLabel.place(x=750, y=268)
        timeDropBox = OptionMenu(root, timer, *times)
        timeDropBox.place(x=890, y=263)
        createGameButton = Button(text="Start Game", command=lambda:CreateGame())
        createGameButton.place(x=630, y=363)
        FENLabel = Label(text='FEN:')
        FENLabel.place(x=630, y=303)
        customLayoutLabel = Label(text='Custom Layout:')
        customLayoutLabel.place(x=630, y=333)
        customRadY = Radiobutton(text="Yes", variable=customLayout, value=1)
        customRadY.place(x=720, y=333)
        customRadN = Radiobutton(text="No", variable=customLayout, value=0)
        customRadN.place(x=770, y=333)
        FENEntry = Entry(width=30)
        FENEntry.insert(END, 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -')
        FENEntry.place(x=660, y=303)
        FENHelpButton = Button(text='?', font=('Helvetica', '10'), command=lambda:FENHelp())
        FENHelpButton.place(x=850, y=300)
        FlipButton = Button(text='Flip Board', command = lambda:self.FlipBoard())
        FlipButton.place(x=720, y=363)
        LeaderboardLabel = Label(text='Leaderboard', font=('Helvetica', '14'))
        LeaderboardLabel.place(x=740, y=405)        
        Records = Sort_Scores(Get_Scores())
        Records = Records[3]+Records[2]+Records[1]+Records[0]
        ScoreLabels = []
        counter = 0
        while len(ScoreLabels)<10 and counter<len(Records): #Getting ten (or fewer) records for the leaderboard and creating list of them
            tempString = f'{counter+1}. {Records[counter].Get_Name()} won against difficulty {Records[counter].Get_Difficulty()} as {Records[counter].Get_Colour()} in {Records[counter].Get_MoveCount()} moves' 
            ScoreLabels.append(Label(text=tempString))
            counter += 1
        for i in range(0, len(ScoreLabels)):
            ScoreLabels[i].place(x=620, y=i*20+435) #Place the chosen list of records, with a gap of 20 pixels between them
        ButtonList = [] #Initialise a list of buttons
        for i in range(120):
            ButtonList.append(None)
        for r in range(2, 10): #For every square on board, create a button and store in corresponding index of button list.
            for t in range(1, 9):
                index = r*10+t
                if (r+t)%2 == 0: #If the two digits of the number are even, it is a grey square
                    ButtonList[index] = Button(text=' ', font=('Helvetica', '28'), bg='grey', width=3, height=1, command=lambda index=index:SubmitButton(index))
                else:
                    ButtonList[index] = Button(text=' ', font=('Helvetica', '28'), bg='white', width=3, height=1, command=lambda index=index:SubmitButton(index))
        for i in range(len(ButtonList)): #Placing every button
            if ButtonList[i] != None:
                ButtonList[i].place(x=i%10*76-72, y=i//10*74-144)#button.place(x=column*gap_between_columns-adjustment1, y=row*gap_between_rows-adjustment2)
        self.aColumnLabel = Label(text='A', bg='grey')
        self.aColumnLabel.place(x=5, y=573)
        self.bColumnLabel = Label(text='B', bg='white')
        self.bColumnLabel.place(x=81, y=573)
        self.cColumnLabel = Label(text='C', bg='grey')
        self.cColumnLabel.place(x=157, y=573)
        self.dColumnLabel = Label(text='D', bg='white')
        self.dColumnLabel.place(x=233, y=573)
        self.eColumnLabel = Label(text='E', bg='grey')
        self.eColumnLabel.place(x=309, y=573)
        self.fColumnLabel = Label(text='F', bg='white')
        self.fColumnLabel.place(x=385, y=573)
        self.gColumnLabel = Label(text='G', bg='grey')
        self.gColumnLabel.place(x=461, y=573)
        self.hColumnLabel = Label(text='H', bg='white')
        self.hColumnLabel.place(x=537, y=573)
        self.oneRowLabel = Label(text='1', bg='grey')
        self.oneRowLabel.place(x=5, y=524)
        self.twoRowLabel = Label(text='2', bg='white')
        self.twoRowLabel.place(x=5, y=449)
        self.threeRowLabel = Label(text='3', bg='grey')
        self.threeRowLabel.place(x=5, y=375)
        self.fourRowLabel = Label(text='4', bg='white')
        self.fourRowLabel.place(x=5, y=301)
        self.fiveRowLabel = Label(text='5', bg='grey')
        self.fiveRowLabel.place(x=5, y=227)
        self.sixRowLabel = Label(text='6', bg='white')
        self.sixRowLabel.place(x=5, y=153)
        self.sevenRowLabel = Label(text='7', bg='grey')
        self.sevenRowLabel.place(x=5, y=79)
        self.eightRowLabel = Label(text='8', bg='white')
        self.eightRowLabel.place(x=5, y=5)

    def FlipBoard(self):
        global ButtonList, Orientation
        if Orientation == 0:
            Orientation = 1
        else:
            Orientation = 0
        ButtonList = ButtonList[::-1]
        for i in range(0, len(ButtonList)):
            if ButtonList[i] != None:
                ResetButton(i)
        if Orientation == 1:
            self.aColumnLabel.place(x=537, y=573)
            self.aColumnLabel.config(bg='white')
            self.bColumnLabel.place(x=461, y=573)
            self.bColumnLabel.config(bg='grey')
            self.cColumnLabel.place(x=385, y=573)
            self.cColumnLabel.config(bg='white')
            self.dColumnLabel.place(x=309, y=573)
            self.dColumnLabel.config(bg='grey')
            self.eColumnLabel.place(x=233, y=573)
            self.eColumnLabel.config(bg='white')
            self.fColumnLabel.place(x=157, y=573)
            self.fColumnLabel.config(bg='grey')
            self.gColumnLabel.place(x=81, y=573)
            self.gColumnLabel.config(bg='white')
            self.hColumnLabel.place(x=5, y=573)
            self.hColumnLabel.config(bg='grey')
            self.oneRowLabel.place(x=5, y=5)
            self.oneRowLabel.config(bg='white')
            self.twoRowLabel.place(x=5, y=79)
            self.twoRowLabel.config(bg='grey')
            self.threeRowLabel.place(x=5, y=153)
            self.threeRowLabel.config(bg='white')
            self.fourRowLabel.place(x=5, y=227)
            self.fourRowLabel.config(bg='grey')
            self.fiveRowLabel.place(x=5, y=301)
            self.fiveRowLabel.config(bg='white')
            self.sixRowLabel.place(x=5, y=375)
            self.sixRowLabel.config(bg='grey')
            self.sevenRowLabel.place(x=5, y=449)
            self.sevenRowLabel.config(bg='white')
            self.eightRowLabel.place(x=5, y=524)
            self.eightRowLabel.config(bg='grey')
        elif Orientation == 0:
            self.hColumnLabel.place(x=537, y=573)
            self.hColumnLabel.config(bg='white')
            self.gColumnLabel.place(x=461, y=573)
            self.gColumnLabel.config(bg='grey')
            self.fColumnLabel.place(x=385, y=573)
            self.fColumnLabel.config(bg='white')
            self.eColumnLabel.place(x=309, y=573)
            self.eColumnLabel.config(bg='grey')
            self.dColumnLabel.place(x=233, y=573)
            self.dColumnLabel.config(bg='white')
            self.cColumnLabel.place(x=157, y=573)
            self.cColumnLabel.config(bg='grey')
            self.bColumnLabel.place(x=81, y=573)
            self.bColumnLabel.config(bg='white')
            self.aColumnLabel.place(x=5, y=573)
            self.aColumnLabel.config(bg='grey')
            self.eightRowLabel.place(x=5, y=5)
            self.eightRowLabel.config(bg='white')
            self.sevenRowLabel.place(x=5, y=79)
            self.sevenRowLabel.config(bg='grey')
            self.sixRowLabel.place(x=5, y=153)
            self.sixRowLabel.config(bg='white')
            self.fiveRowLabel.place(x=5, y=227)
            self.fiveRowLabel.config(bg='grey')
            self.fourRowLabel.place(x=5, y=301)
            self.fourRowLabel.config(bg='white')
            self.threeRowLabel.place(x=5, y=375)
            self.threeRowLabel.config(bg='grey')
            self.twoRowLabel.place(x=5, y=449)
            self.twoRowLabel.config(bg='white')
            self.oneRowLabel.place(x=5, y=524)
            self.oneRowLabel.config(bg='grey')
        Main.Display()

app = MainWindow(root)
root.mainloop()

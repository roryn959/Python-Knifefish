bR = "♜"
bKN = "♞"
bB = "♝"
bK = "♚"
bQ = "♛"
bP = "♟"
wR = "♖"
wKN = "♘"
wB = "♗"
wK = "♔"
wQ = "♕"
wP = "♙"
DEFAULT_SETUP = [None,None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, bR, bKN, bB, bQ, bK, bB, bKN, bR, None, None, bP, bP, bP, bP, bP, bP, bP, bP, None, None, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', None, None, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', None, None, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', None, None, ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', None, None, wP, wP, wP, wP, wP, wP, wP, wP, None, None, wR, wKN, wB, wQ, wK, wB, wKN, wR, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
WHITE_TYPES = [wP, wKN, wB, wR, wQ, wK]
BLACK_TYPES = [bP, bKN, bB, bR, bQ, bK]
EVAL_KEYS_WHITE = [wP, wKN, wB, wR, wQ] #When evaluating board, iterate through these pieces.
EVAL_KEYS_BLACK = [bP, bKN, bB, bR, bQ] #Kings not included because they have two Piece-Square tables, which need to be called seperately
RECORD_LIST = []
COLUMN_VALUES = {'A':1, 'B':2, 'C':3, 'D':4, 'E':5, 'F':6, 'G':7, 'H':8}
ABSOLUTE_VALUES = {wP:1, bP:1, wKN:2, bKN:2, wB:3, bB:3, wR:5, bR:5, wQ:9, bQ:9, wK:13, bK:13}
REVERSE_COLUMN_VALUES = {str(v):k for k, v in COLUMN_VALUES.items()}
FENletters = {'p':bP, 'n':bKN, 'b':bB, 'r':bR, 'q':bQ, 'k':bK, 'P':wP, 'N':wKN, 'B':wB, 'R':wR, 'Q':wQ, 'K':wK}
MOVES_KNIGHT = [8, 12, 19, 21, -8, -12, -19, -21]
MOVES_KING = [1, 9, 10, 11, -1, -9, -10, -11]
MOVES_BISHOP = [-9, 9, -11, 11]
MOVES_ROOK = [-1, 1, -10, 10]
CASTLE_SQUARES = [21, 25, 28, 91, 95, 98]
TAUNTS = ['Have you tried lessons?', 'Are you going to resign now, or do I need to finish this myself?', 'Try a lower difficulty next time.', 'GG', 'Nice to have an ego boost now and then...']
Orientation = 0
SunkButton = []
#            Starting position                    e4           d4            After e4-d4                          Nf3          Bc4          Nc3          After e4-d4-Nf3-nc6                   Bc4          Nc3           Urusov gambit after nf6              d4            Urusov opponent takes with pawn     Nf3            Urusov opponent takes with knight    dxe5   >>      Queen e7                                            Bd6                                                 f6                                              bb4                                                 #After e4                           e5           c5            
PLAYBOOK = {'000000111110100110011100111110111':[[85, 65, 1]], '110011011011110000111000011110110':[[97, 76, 1], [96, 63, 1], [92, 73, 1]], '001111001100000011001111011101101':[[96, 63, 1], [92, 73, 1]], '001010011000001011110111000100011':[[84, 64, 1]], '100100000110101111100001001001000':[[97, 76, 1]], '011010100100110000101111000000101':[[64, 55, 1]], '011000100010111010001100100111101':[[94, 76, 1]], '111010101010001000010001100001100':[[94, 76, 1]], '111001011010101110110011001100111':[[94, 76, 1]], '101101001001000100001011001101100':[[83, 73, 1]], '110000101000111101101011000001011':[[35, 55, 1], [33, 53, 1]], '011011001101011010001001111111001':[[22, 43, 1]], '101010001111101101011000100000111':[[27, 46, 1]]}
AI_MINIMAL_BOUND = 5 #When AI has 5 seconds or fewer, lower the difficulty to 1 (near instant decision making)
AI_LOWER_BOUND = 30 #When AI has 30 seconds or fewer, lower difficulty to 2

def join(exList):
    exString = ''
    for item in exList:
        exString += str(item)
    return exString

def Get_Scores():
    data = [] #A list of data.
    file = open('highscores.txt', 'r') #Open the file containing the data
    for line in file: #For each line in file, add info to data list
        if line != '\n': #If this isn't a blank line, add the data it contains to the list of records.
            if data[-1:] == '\n': #Add data from the line to the list of data. If the line isn't the last, it will have a '\n' at the end, which is omitted.
                data.append(line[:-1]) #Add all data except the '\n'
            else:
                data.append(line) #If no '\n' at end of line, just add to data set. Data recorded as 'Name/Difficulty/Player Colour/Move Count.
    file.close() #Close file
    for item in data: #For each piece of data
        counter = 0 #Used to run through the string of data.
        name = ''
        while item[counter] != '/': #Until first slash met, name is being read
            name += item[counter] #Until the end of the name denotion, add characters to the name detail of the record.
            counter += 1 #Iterates through the characters of the piece of data.
        counter += 1
        difficulty = item[counter] #Set denoted difficulty
        counter += 2
        if item[counter] == 'w': #Colour should be represented in the data.
            colour = 'white'
        else:
            colour = 'black'
        counter += 6
        moves = ''
        while True:
            try:
                int(item[counter]) #If the current character can be converted into integer, it's a number.
                moves += item[counter] #Add character of number to moves counter. Keep as string, to allow two (or more) digit numbers to be recorded.
                counter += 1
            except:
                break #When non-integer character hit, end of move count denotion, break loop
        moves = int(moves) #Now convert the move counter to integer.
        RECORD_LIST.append(Record(name, difficulty, colour, moves)) #Add record of the details read from this line of the data to a list of all the records.
    return RECORD_LIST

def Sort_Scores(Records):
    groups = [[], [], [], []] #Different difficulties grouped into seperate lists to simplify the sorting.
    for record in Records:
        groups[record.Get_Difficulty()-1].append(record) #At to group corresponding to given difficulty.      
    for group in groups: #For each difficulty group, bubble sort based on moves taken in ascending order
        n = len(group) #Commence bubble sorting of list of records.
        swapped = True
        while swapped == True:
            swapped = False
            for i in range(0, n-1):
                if group[i].Get_MoveCount() > group[i+1].Get_MoveCount():
                    temp = group[i+1]
                    group[i+1] = group[i]
                    group[i] = temp
                    swapped = True
    return groups

class Stack:
    def __init__(self):
        self.__List = []
    def push(self, element):
        self.__List.append(element)
    def pop(self):
        return self.__List.pop()
    def length(self):
        return len(self.__List)
    def clear(self):
        self.__List = []

class Record:
    def __init__(self, name, difficulty, colour, moves):
        self.__Name = name
        self.__Difficulty = int(difficulty)
        self.__Colour = colour
        self.__MoveCount = int(moves)
    def Get_Name(self):
        return self.__Name
    def Get_Difficulty(self):
        return self.__Difficulty
    def Get_Colour(self):
        return self.__Colour
    def Get_MoveCount(self):
        return self.__MoveCount




        

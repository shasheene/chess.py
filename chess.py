#!/usr/bin/python
"""
shasheene 2013-12-15

Text-based chess game.
"""

import sys


class Piece(object):
    def __init__(self, col, whitePieceUnicodeCodepoint):
        self.hasNeverMoved = True
        self.col = col
        self.type = "_"
        if self.col == "white":
            self.enemyCol = "black"
            self.forwardDir = -1
            self.unicodeSymbol = chr(int(whitePieceUnicodeCodepoint, 16)).encode('utf-8')
        elif self.col == "black":
            self.enemyCol = "white"
            self.forwardDir = +1
            self.unicodeSymbol = chr(int(whitePieceUnicodeCodepoint, 16) + 6).encode('utf-8')

    def getMoveSet(self, pieceLocation):
        return []

    # Useful method for checkmate detection
    def getAttackSet(self, pieceLocation):
        return self.getMoveSet(pieceLocation)


class Pawn(Piece):
    def __init__(self, col):
        super(Pawn, self).__init__(col, '2659')
        self.attackSet = []
        self.moveSet = []
        self.type = "p"

    def getMoveSet(self, pieceLocation):
        self.moveSet = []
        # Is space directly forward from us free?
        if (pieceAt(pieceLocation[0] + self.forwardDir,
                    pieceLocation[1]).type == "_"):
            self.moveSet.append([pieceLocation[0] + self.forwardDir, pieceLocation[1]])
            # If we haven't moved, is the space TWO forward from us free?
            if self.hasNeverMoved and (pieceAt(pieceLocation[0] + self.forwardDir * 2, pieceLocation[1]).type == "_"):
                # Append pawn jump move
                self.moveSet.append([pieceLocation[0] + self.forwardDir * 2, pieceLocation[1]])
        self.hasNeverMoved = False
        return self.moveSet

    def getAttackSet(self, pieceLocation):
        self.attackSet = []
        if (pieceAt(pieceLocation[0] + self.forwardDir,
                    # Attack north west (from white's perspective)
                    pieceLocation[1] - 1).col == self.enemyCol):
            self.attackSet.append([pieceLocation[0] + self.forwardDir, pieceLocation[1] - 1])
        if (pieceAt(pieceLocation[0] + self.forwardDir,
                    # Attack "north east"
                    pieceLocation[1] + 1).col == self.enemyCol):
            self.moveSet.append([pieceLocation[0] + self.forwardDir, pieceLocation[1] + 1])
        return self.attackSet


class AdvancedPiece(Piece):
    def __init__(self, col, listOfUnitMoves, movementStyle, whitePieceUnicodeCodepoint):
        super(AdvancedPiece, self).__init__(col, whitePieceUnicodeCodepoint)
        self.myVectorSet = listOfUnitMoves
        # movementStyle either "slider" (ie rook,bishop,queen) or "teleporter" (king,knight) with respect to moveVectors
        self.movementStyle = movementStyle

    def getMoveSet(self, pieceLocation):
        self.moveSet = []
        for vector in self.myVectorSet:
            self.i = pieceLocation[0] + vector[0]
            self.j = pieceLocation[1] + vector[1]
            # print 'Checking vector',
            # print vector
            if self.movementStyle == "slider":
                hitEnemyThisDir = False  # Slide until first enemy
                while (isOffEdge(self.i, self.j) == 0 and pieceAt(self.i,
                                                                  self.j).col != self.col and hitEnemyThisDir == False):
                    # print 'Adding: ' + str(self.i) + "," + str(self.j)
                    self.moveSet.append([self.i, self.j])
                    if (pieceAt(self.i, self.j).col == oppositeCol(self.col)):
                        hitEnemyThisDir = True  # stop sliding this dir if hit enemy
                    self.i += vector[0]
                    self.j += vector[1]

            elif self.movementStyle == "teleporter":
                if (isOffEdge(self.i, self.j) == 0 and pieceAt(self.i, self.j).col != self.col):
                    # print 'Adding: ' + str(self.i) + "," + str(self.j)
                    self.moveSet.append([self.i, self.j])

        self.hasNeverMoved = True
        return self.moveSet


class Rook(AdvancedPiece):
    def __init__(self, col):
        self.myVectorSet = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        super(Rook, self).__init__(col, self.myVectorSet, "slider", '2656')
        self.type = "r"


class Bishop(AdvancedPiece):
    def __init__(self, col):
        self.myVectorSet = [[-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(Bishop, self).__init__(col, self.myVectorSet, "slider", '2657')
        self.type = "b"


class Queen(AdvancedPiece):
    def __init__(self, col):  # Both rook AND bishop's movesets
        self.myVectorSet = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(Queen, self).__init__(col, self.myVectorSet, "slider", '2655')
        self.type = "q"


class King(AdvancedPiece):
    def __init__(self, col):  # same as queen in vectorset, but parent class makes moveset smaller
        self.myVectorSet = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(King, self).__init__(col, self.myVectorSet, "teleporter", '2654')
        self.type = "k"
        # Castling:


"""		def getMoveSet(self,pieceLocation): #teleporter overridden to get castling
			self.moveSet=[]
			for vector in self.myVectorSet:
				self.i = pieceLocation[0]+vector[0]
				self.j = pieceLocation[1]+vector[1]
				if (isOffEdge(self.i,self.j)==0 and pieceAt(self.i,self.j).col!=self.col):
					#print 'Adding: ' + str(self.i) + "," + str(self.j)
					self.moveSet.append([self.i,self.j])
				global board
				if self.col=="white":
					home_row = 7
				else:
					home_row = 0
				rookA = pieceAtCoords([home_row,0]) #Potential rook
				rookB = pieceAtCoords([home_row,0])
				if (rookA.type="r" and rookA.moved=0):
					print"""


class Knight(AdvancedPiece):
    def __init__(self, col):  # similar vector set/moveset relationship as king (see parent class)
        self.myVectorSet = [[-2, -1], [-2, 1], [1, 2], [-1, 2], [2, -1], [2, 1], [-1, -2], [1, -2]]
        super(Knight, self).__init__(col, self.myVectorSet, "teleporter", '2658')
        self.type = "h"  # h for 'horse', as king is taken 'k'


def pieceAt(row, column):  # Conveniant notation
    return board[row][column]


def pieceAtCoords(coords):  # Conveniant notation
    return board[coords[0]][coords[1]]


def isOffEdge(i, j):  # Remember internal board is indexed 0 to 7, not 1 to 8
    if i >= 7 or i < 0 or j >= 7 or j < 0:
        return 1
    return 0


def a1ToPythonConvert(pair):
    """ Converts chess coords system to a list with origin top-left.

    Chess has origin bottom-left and counts colums a to h and rows numbered 1 to 8. 
    Computers index differently, from top-left and count from 0 rather than 1.

    Example: 'a8' returns [0,0]. 'a1' returns [7,0].
    
    Note: No error checking yet - assumes user enters valid input currently
    """
    # print "Checking pair: " + pair
    col = ord(pair[0].lower()) - 97  # In ascii, 'a'=97
    # print "Letter is " + str(pair[0]) + " -> " + str(col)
    row = 8 - int(pair[1])  # Chess counts from 1, not 0. (the row component of coords 'e2' to is 1, not 2.)
    return row, col


def pythonToa1Convert(pair):
    col = chr(pair[1] + 97)  # In ascii, 'a'=97
    row = str(8 - pair[0])  # Chess counts from 1, not 0. (the row component of coords 'e2' to is 1, not 2.)
    return (col + row)


def take_input():
    r = input()
    # Ignore things after spaces
    return r.split()[0:1]


def printBoard(board):
    print('  a b c d e f g h')
    rowNumber = 8
    for row in board[:]:
        print(rowNumber, end=' ')
        for piece in row[:]:
            if piece.type != "_":
                print(piece.unicodeSymbol.decode("utf-8", "ignore"), end=' ')
            else:
                # just for prettyness
                print('_', end=' ')
        rowNumber = rowNumber - 1
        print(end='\n')  # next row
    print('  a b c d e f g h')


# Create board:
global board
board = []

# Board creation:
r = Rook("black")
h = Knight("black")
b = Bishop("black")
q = Queen("black")
k = King("black")
board.append([r, h, b, q, k, b, h, r])
board.append([]);
for i in range(0, 8):
    p = Pawn("black")
    board[1].append(p);
blankPiece = Piece("", '0123')  # test only
for i in range(2, 6):
    board.append([blankPiece, blankPiece, blankPiece, blankPiece, blankPiece, blankPiece, blankPiece, blankPiece])
board.append([]);
for i in range(0, 8):
    p = Pawn("white")
    board[6].append(p);
r = Rook("white")
h = Knight("white")
b = Bishop("white")
q = Queen("white")
k = King("white")
board.append([r, h, b, k, q, b, h, r])

# print 'WELCOME TO TEXT BASED CHESS'
playerTurn = "white"


def findKing(colour):  # Temporary, will get all mechanics implemented even inefficently THEN improve algo/design
    global board
    row = 0
    for r in board:
        column = 0
        for piece in r:
            if piece.type == "k" and piece.col == colour:
                return ([int(row), int(column)])
            column = (column + 1) % 7
        row = row + 1


def getTeamAttackSet(col):
    teamAttackSet = []
    row = 0
    for r in board:
        column = 0
        for piece in r:
            if piece.col == col:  # eg. what's white attack set?
                pieceLoc = [row, column]
                pieceAttackSet = piece.getAttackSet(pieceLoc)
                teamAttackSet.append(pieceAttackSet)

                '''print pythonToa1Convert(pieceLoc) + " " + pieceAtCoords(pieceLoc).type + ": ", 
                for a in pieceAttackSet:
                    print pythonToa1Convert(a),
                print'''
            column = (column + 1) % 7
        row = row + 1
    return teamAttackSet


def isBeingChecked(col):  # eg. isBeingChecked("black")
    kingLoc = findKing(col)
    teamAttackSet = getTeamAttackSet(oppositeCol(col))

    # print "King is at :" + str(kingLoc)
    for pieceAttackSet in teamAttackSet:
        if kingLoc in pieceAttackSet:
            return True
            # otherwise
    return False


def oppositeCol(col):
    if col == "white":
        return "black"
    if col == "black":
        return "white"
    if col == "_":
        sys.exit()  #
        # return None


while 1:
    printBoard(board)
    print(playerTurn + 's turn. Select piece')

    validSelection = 0
    while (validSelection == 0):
        print(' Select piece to move. Example: e2 ')
        selected = take_input()

        selected = a1ToPythonConvert(selected[0])

        selectedPiecePossibleMoves = pieceAtCoords(selected).getMoveSet(selected)
        selectedPiecePossibleMoves += pieceAtCoords(selected).getAttackSet(selected)

        print('Selected: \'' + pieceAtCoords(selected).type + '\'.', )
        moveSetSize = len(selectedPiecePossibleMoves)
        if moveSetSize == 0 or pieceAtCoords(selected).col != playerTurn:
            print('\n ...Error no moves available. Choose another piece')
        else:
            print('Possible moves: ', )
            for i in selectedPiecePossibleMoves:
                print(pythonToa1Convert(i), )
            print()
            validSelection = 1

            # Choose end location:
    legalMoveChoice = 0
    while (legalMoveChoice == 0):
        print(' Select location to move piece to: ')
        moveTo = take_input()
        moveTo = a1ToPythonConvert(moveTo[0])  # e4 becomes [4,4]?

        for i in range(0, len(selectedPiecePossibleMoves)):  # Search selectedMoveSet for moveTo[0]:
            # quick hack to compare list value with tuple value (find better way later):

            check = isBeingChecked(playerTurn)
            if selectedPiecePossibleMoves[i][0] == moveTo[0] and selectedPiecePossibleMoves[i][1] == moveTo[1] and check == False:
                legalMoveChoice = 1
                end = selectedPiecePossibleMoves[i]
            if check == True:
                print("**THIS MOVE WILL CAUSE A CHECK**")

    board[end[0]][end[1]] = board[selected[0]][selected[1]]
    board[selected[0]][selected[1]] = blankPiece

    if isBeingChecked(oppositeCol(playerTurn)):
        print('***********CHECK!!!!!!!!!!!!!!!!!!')

        # Will only allow legal move if isBeingChecked(myself)=false if this move proceeds

        # Algorithm for end of game:
        # 1.) Determine if enemy is being checked.
        # For every attack in player.getAttackSet(), if enemyKing.location==attack then return true

        # 2.) Determine if checked enemy can recover
        # For every move in moveSet that can remove 'check', if every myKing.location==any enemyPlayer.getAttackSet(), then CHECKMATE msg and exit

        # Next turn
    playerTurn = oppositeCol(playerTurn)

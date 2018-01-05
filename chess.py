#!/usr/bin/python
"""
shasheene 2013-12-15

Text-based chess game.
"""

import sys

from copy import deepcopy


class Piece(object):
    def __init__(self, col, whitePieceUnicodeCodepoint):
        self.hasNeverMoved = True
        self.col = col
        self.type = "_"
        if self.col == "white":
            self.enemyCol = "black"
            self.homeRank = 7
            self.enemyHomeRank = 0
            self.forwardDir = -1
            self.unicodeSymbol = chr(int(whitePieceUnicodeCodepoint, 16)).encode('utf-8')
        elif self.col == "black":
            self.enemyCol = "white"
            self.forwardDir = +1
            self.homeRank = 0
            self.enemyHomeRank = 7
            self.unicodeSymbol = chr(int(whitePieceUnicodeCodepoint, 16) + 6).encode('utf-8')

    def getMoveSet(self, board, pieceLocation):
        return []

    # Useful method for checkmate detection
    def getAttackSet(self, board, pieceLocation):
        return []


class Pawn(Piece):
    def __init__(self, col):
        super(Pawn, self).__init__(col, '2659')
        self.attackSet = []
        self.moveSet = []
        self.type = "p"
        # Pawn's relative column offset to get north east and north west (from white's perspective)
        self.columnAttackOffset = [-1, 1]

    def getMoveSet(self, board, pieceLocation):
        self.moveSet = []
        # Is space directly forward from us free?
        if (pieceAt(board, pieceLocation[0] + self.forwardDir,
                    pieceLocation[1]).type == "_"):
            self.moveSet.append([pieceLocation[0] + self.forwardDir, pieceLocation[1]])
            # If we haven't moved, is the space TWO forward from us free?
            if self.hasNeverMoved and (pieceAt(board, pieceLocation[0] + self.forwardDir * 2, pieceLocation[1]).type == "_"):
                # Append pawn jump move
                self.moveSet.append([pieceLocation[0] + self.forwardDir * 2, pieceLocation[1]])
        self.hasNeverMoved = False
        return self.moveSet

    def getAttackSet(self, board, pieceLocation):
        self.attackSet = []

        for colOffset in self.columnAttackOffset:
            self.i = pieceLocation[0] + self.forwardDir
            self.j = pieceLocation[1] + colOffset
            if not isOffEdge(self.i, self.j) and (pieceAt(board, self.i, self.j).col == self.enemyCol):
                self.attackSet.append([self.i, self.j])
        return self.attackSet


class AdvancedPiece(Piece):
    def __init__(self, col, listOfUnitMoves, movementStyle, whitePieceUnicodeCodepoint):
        super(AdvancedPiece, self).__init__(col, whitePieceUnicodeCodepoint)
        self.myVectorSet = listOfUnitMoves
        # movementStyle either "slider" (ie rook,bishop,queen) or "teleporter" (king,knight) with respect to moveVectors
        self.movementStyle = movementStyle

    def getAttackSet(self, board, pieceLocation):
        self.attackSet = []
        for vector in self.myVectorSet:
            self.i = pieceLocation[0] + vector[0]
            self.j = pieceLocation[1] + vector[1]
            # print 'Checking vector',
            # print vector
            if self.movementStyle == "slider":
                hitEnemyThisDir = False  # Slide until first enemy
                while (not isOffEdge(self.i, self.j) and pieceAt(board, self.i,
                                                                  self.j).col != self.col and hitEnemyThisDir == False):
                    # print 'Adding: ' + str(self.i) + "," + str(self.j)
                    self.attackSet.append([self.i, self.j])
                    if (pieceAt(board, self.i, self.j).col == oppositeCol(self.col)):
                        hitEnemyThisDir = True  # stop sliding this dir if hit enemy
                    self.i += vector[0]
                    self.j += vector[1]

            elif self.movementStyle == "teleporter":
                if (not isOffEdge(self.i, self.j) and pieceAt(board, self.i, self.j).col != self.col):
                    # print 'Adding: ' + str(self.i) + "," + str(self.j)
                    self.attackSet.append([self.i, self.j])

        self.hasNeverMoved = True
        return self.attackSet


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
        if col == "white":
            self.leftwardsColIndexIncrement = -1
            self.rightwardsColIndexIncrement = 1
        else:
            self.leftwardsColIndexIncrement = 1
            self.rightwardsColIndexIncrement = -1

    def _getCastlingPositions(self):
        self.castlingPositions = [[self.homeRank, "1"], [self.homeRank, "6"]]

    # Override teleporter to get castling
    def getAttackSet(self, board, pieceLocation):
        self.attackSet=super(King,self).getAttackSet(board, pieceLocation)
        self.attackSet += self.getCastlingSet(board, pieceLocation)
        return self.attackSet

    def getCastlingSet(self, board, pieceLocation):
        castlingSet = []
        if self.hasNeverMoved:
            # Ensure the positions to the left of king are empty
            if selectedPiece(board, [self.homeRank, pieceLocation[1] + self.leftwardsColIndexIncrement * 1]).type == "_" \
                    and selectedPiece(board, [self.homeRank, pieceLocation[1] + self.leftwardsColIndexIncrement * 2]).type == "_":
                # And the left rook has never moved
                leftRook = selectedPiece(board, [self.homeRank, pieceLocation[1] + self.leftwardsColIndexIncrement * 3])
                if leftRook.type=="r" and leftRook.hasNeverMoved:
                    castlingSet.append([self.homeRank, pieceLocation[1] + self.leftwardsColIndexIncrement * 2])
            # Ensure the positions to the right of king are empty
            if selectedPiece(board, [self.homeRank, pieceLocation[1] + self.rightwardsColIndexIncrement * 1]).type == "_" \
                    and selectedPiece(board, [self.homeRank, pieceLocation[1] + self.rightwardsColIndexIncrement * 2]).type == "_" \
                    and selectedPiece(board, [self.homeRank, pieceLocation[1] + self.rightwardsColIndexIncrement * 3]).type == "_":
                # And the right rook has never moved
                rightRook = selectedPiece(board, [self.homeRank, pieceLocation[1] + self.rightwardsColIndexIncrement * 4])
                if rightRook.type=="r" and rightRook.hasNeverMoved:
                    castlingSet.append([self.homeRank,  pieceLocation[1] + self.rightwardsColIndexIncrement * 3])
        return castlingSet



class Knight(AdvancedPiece):
    def __init__(self, col):  # similar vector set/moveset relationship as king (see parent class)
        self.myVectorSet = [[-2, -1], [-2, 1], [1, 2], [-1, 2], [2, -1], [2, 1], [-1, -2], [1, -2]]
        super(Knight, self).__init__(col, self.myVectorSet, "teleporter", '2658')
        self.type = "h"  # h for 'horse', as king is taken 'k'


def pieceAt(board, row, column):  # Conveniant notation
    return board[row][column]


def selectedPiece(board, coords):  # Conveniant notation
    return board[coords[0]][coords[1]]


# Recall, internal board (unlike raw user input) is indexed 0 to 7, not 1 to 8.
def isOffEdge(i, j):
    if i > 7 or i < 0 or j > 7 or j < 0:
        return True
    return False


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
    print()
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
gameBoard = []

# Board creation:
r = Rook("black")
h = Knight("black")
b = Bishop("black")
q = Queen("black")
k = King("black")
gameBoard.append([r, h, b, q, k, b, h, r])
gameBoard.append([]);
for i in range(0, 8):
    p = Pawn("black")
    gameBoard[1].append(p);
blankPiece = Piece("", '0123')  # test only
for i in range(2, 6):
    gameBoard.append([blankPiece, blankPiece, blankPiece, blankPiece, blankPiece, blankPiece, blankPiece, blankPiece])
gameBoard.append([]);
for i in range(0, 8):
    p = Pawn("white")
    gameBoard[6].append(p);
r = Rook("white")
h = Knight("white")
b = Bishop("white")
q = Queen("white")
k = King("white")
gameBoard.append([r, h, b, k, q, b, h, r])

# print 'WELCOME TO TEXT BASED CHESS'
playerTurn = "white"


def findKing(board, colour):  # Temporary, will get all mechanics implemented even inefficently THEN improve algo/design
    row = 0
    for r in board:
        column = 0
        for piece in r:
            if piece.type == "k" and piece.col == colour:
                return ([int(row), int(column)])
            column = (column + 1)
        row = row + 1


def getTeamMoveSet(board, col, option):
    teamMoveSet = []
    row = 0
    for r in board:
        column = 0
        for piece in r:
            if piece.col == col:  # eg. what's white attack set?
                pieceLoc = [row, column]
                if option == "moveset":
                    teamMoveSet += pieceAt(board, pieceLoc[0],  pieceLoc[1]).getMoveSet(board, pieceLoc)
                else:
                    teamMoveSet += pieceAt(board, pieceLoc[0], pieceLoc[1]).getAttackSet(board, pieceLoc)
            column = (column + 1)
        row = row + 1
    return teamMoveSet


def isBeingChecked(board, col):  # eg. isBeingChecked("black")
    kingLoc = findKing(board, col)
    teamAttackSet = getTeamMoveSet(board, oppositeCol(col), "attackset")

    # print "King is at :" + str(kingLoc)
    if kingLoc in teamAttackSet:
        return True
    return False


def oppositeCol(col):
    if col == "white":
        return "black"
    if col == "black":
        return "white"
    if col == "_":
        sys.exit()  #
        # return None

def requestUserMove(message):
    print(message)
    rawInput = take_input()
    if len(rawInput) == 0:
        print("No input given.\n")
        return False

    try:
        # e4 becomes [3,3]
        move = a1ToPythonConvert(rawInput[0])
    except (ValueError, Exception):
        print("Error occurred processing input. Please try again.\n")
        return False
    return move

def conductMove(existingBoard, startCoords, endCoords, playerCol):
    """ Uses the supplied move on the existing board and returns a new board if the move is valid.
    
    If the move causes current player to be checked, False is returned. Does NOT modify existingBoard.
    
    Note: Does minimal verification of validity of move   
    """

    # Copy old 2D board array
    newBoard = deepcopy(existingBoard)
    if selectedPiece(newBoard, startCoords).col != playerCol:
        return False
    if selectedPiece(newBoard, startCoords).type == "k":
        castlingSet = selectedPiece(newBoard, startCoords).getCastlingSet(newBoard, startCoords)
        if len(castlingSet) > 0:
            print("**NOTE: Castling move detected, but not yet implemented -- simply moving king only**")

    newBoard[endCoords[0]][endCoords[1]] = newBoard[startCoords[0]][startCoords[1]]
    newBoard[startCoords[0]][startCoords[1]] = blankPiece
    return newBoard


def filterSelfCheckingMoves(board, selectedPieceCoords, listOfMoves, playerTurn):
    """ Returns new list without the moves that causes own player to become checked"""
    pieceLegalMoveSet = []
    for candidateMove in listOfMoves:
        newBoard = conductMove(board, selectedPieceCoords, candidateMove, playerTurn)
        if not newBoard:
            continue
        # if it doesn't cause self to become checked, move is valid!
        if not isBeingChecked(newBoard, playerTurn):
            pieceLegalMoveSet.append(candidateMove)
    return pieceLegalMoveSet


def canPlayerLeaveCheckState(board, playerTurn):
    legalMoveSet = []
    row = 0
    for r in board:
        column = 0
        for piece in r:
            if piece.col == playerTurn:
                pieceCoords = [row, column]
                pieceTotalMoveSet = selectedPiece(board, pieceCoords).getMoveSet(board, pieceCoords)
                pieceTotalMoveSet += selectedPiece(board, pieceCoords).getAttackSet(board, pieceCoords)
                legalMoveSet += filterSelfCheckingMoves(gameBoard, pieceCoords, pieceTotalMoveSet, playerTurn)
            column = (column + 1)
        row = row + 1
    return len(legalMoveSet) != 0

while 1:
    printBoard(gameBoard)
    print(playerTurn + 's turn. Select piece')

    validSelection = False
    coords = False
    while not validSelection:
        coords = requestUserMove(' Select piece to move. Example: e2 \n')
        if not coords:
            continue
        if selectedPiece(gameBoard, coords).type == "_":
            print('...Error invalid piece. Choose another piece\n')
            continue
        if selectedPiece(gameBoard, coords).col != playerTurn:
            print('...Error selected opponents\' piece. Choose another piece\n')
            continue

        pieceTotalMoveSet = selectedPiece(gameBoard, coords).getMoveSet(gameBoard, coords)
        pieceTotalMoveSet += selectedPiece(gameBoard, coords).getAttackSet(gameBoard, coords)
        pieceLegalMoveSet = filterSelfCheckingMoves(gameBoard, coords, pieceTotalMoveSet, playerTurn)
        if len(pieceLegalMoveSet) == 0:
            print('...Error no legal moves available. Choose another piece\n')
            continue
        validSelection = True

        print('Selected: \'' + selectedPiece(gameBoard, coords).type + '\'.', )
        print('Possible moves: ', )
        for i in pieceLegalMoveSet:
            print(pythonToa1Convert(i), )
        print()

        # Choose end location:
        legalMoveChoice = False
        while not legalMoveChoice:
            moveTo = requestUserMove(' Select location to move piece to: ')
            if not moveTo:
                continue
            for move in pieceLegalMoveSet:
                if move[0] == moveTo[0] and move[1] == moveTo[1]:
                    legalMoveChoice = True
            if not legalMoveChoice:
                print('Invalid move')
                continue

    gameBoard = conductMove(gameBoard, coords, moveTo, playerTurn)
    if not gameBoard:
        print("Illegal move not caught by game logic")

    if isBeingChecked(gameBoard, oppositeCol(playerTurn)):
        if canPlayerLeaveCheckState(gameBoard, oppositeCol(playerTurn)):
            print('CHECK\n')
        else:
            printBoard(gameBoard)
            print('CHECKMATE. ' + playerTurn + ' wins!\n')
            exit(0)

    playerTurn = oppositeCol(playerTurn)

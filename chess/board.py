from builtins import ValueError, range, len, int
from copy import deepcopy

from chess.utils import selectedPiece, oppositeCol, pieceAt
from chess.pieces import Knight, Rook, Bishop, King, Queen, Pawn

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
                legalMoveSet += filterSelfCheckingMoves(board, pieceCoords, pieceTotalMoveSet, playerTurn)
            column = (column + 1)
        row = row + 1
    return len(legalMoveSet) != 0


def filterSelfCheckingMoves(board, selectedPieceCoords, listOfMoves, playerTurn, blankPiece):
    """ Returns new list without the moves that causes own player to become checked"""
    pieceLegalMoveSet = []
    for candidateMove in listOfMoves:
        newBoard = conductMove(board, selectedPieceCoords, candidateMove, playerTurn, blankPiece)
        if not newBoard:
            continue
        # if it doesn't cause self to become checked, move is valid!
        if not isBeingChecked(newBoard, playerTurn):
            pieceLegalMoveSet.append(candidateMove)
    return pieceLegalMoveSet


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

def conductMove(existingBoard, startCoords, endCoords, playerCol, blankPiece):
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


def create(blankPiece):
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
    return gameBoard
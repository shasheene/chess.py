#!/usr/bin/python
"""
shasheene 2013-12-15

Text-based chess game.
"""

import sys
from builtins import ValueError, Exception, len, input, chr, str, ord, int, KeyboardInterrupt

from chess.board import create, isBeingChecked, canPlayerLeaveCheckState, printBoard, oppositeCol, \
    filterSelfCheckingMoves, conductMove, selectedPiece

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


def main():
    playerTurn = "white"

    gameBoard = create()

    while 1:
        printBoard(gameBoard)
        print(playerTurn + 's turn. Select piece')

        validSelection = False
        coords = False
        while not validSelection:
            coords = requestUserMove(' Select piece to move. Example: e2 \n')
            if not coords:
                continue
            if selectedPiece(gameBoard, coords).isBlankPiece:
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
                sys.exit(0)

        playerTurn = oppositeCol(playerTurn)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
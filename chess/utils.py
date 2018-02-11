# Recall, internal board (unlike raw user input) is indexed 0 to 7, not 1 to 8.
def isOffEdge(i, j):
    if i > 7 or i < 0 or j > 7 or j < 0:
        return True
    return False


def pieceAt(board, row, column):  # Convenient notation
    return board[row][column]


def selectedPiece(board, coords):  # Convenient notation
    return board[coords[0]][coords[1]]

def oppositeCol(col):
    if col == "white":
        return "black"
    if col == "black":
        return "white"
    if col == "_":
        raise ValueError()
        # return None

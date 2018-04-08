# Recall, internal board (unlike raw user input) is indexed 0 to 7, not 1 to 8.
def is_off_edge(i, j):
    if i > 7 or i < 0 or j > 7 or j < 0:
        return True
    return False


def is_off_edge_pos(pos):
    if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
        return True
    return False


def piece_at(board, row, column):  # Convenient notation
    return board[row][column]


def piece_at_pos(board, pos):
    return board[pos[0]][pos[1]]


def selected_piece(board, coords):  # Convenient notation
    return board[coords[0]][coords[1]]


def opposite_col(col):
    if col == "white":
        return "black"
    if col == "black":
        return "white"
    if col == "_":
        raise ValueError()
        # return None

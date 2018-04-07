from builtins import range, len, int
from copy import deepcopy

from chess.move import MoveType, Move
from chess.pieces import Knight, Rook, Bishop, King, Queen, Pawn, BlankPiece
from chess.utils import selected_piece, opposite_col, piece_at


def can_player_leave_check_state(board, player_turn):
    legal_move_set = []
    row = 0
    for r in board:
        column = 0
        for piece in r:
            if piece.col == player_turn:
                piece_coords = [row, column]
                piece_total_move_set = selected_piece(board, piece_coords).get_move_set(board, piece_coords)
                piece_total_move_set += selected_piece(board, piece_coords).get_attack_set(board, piece_coords)
                legal_move_set += filter_self_checking_moves(board, piece_total_move_set, player_turn)
            column = (column + 1)
        row = row + 1
    return len(legal_move_set) != 0


def filter_self_checking_moves(board, list_of_moves, player_turn):
    """ Returns new list without the moves that causes own player to become checked"""
    piece_legal_move_set = []
    for candidate_move in list_of_moves:
        new_board = conduct_move(board, candidate_move, player_turn)
        if not new_board:
            continue
        # if it doesn't cause self to become checked, move is valid!
        if not is_being_checked(new_board, player_turn):
            piece_legal_move_set.append(candidate_move)
    return piece_legal_move_set


def print_board(board):
    print('  a b c d e f g h')
    row_number = 8
    for row in board[:]:
        print(row_number, end=' ')
        for piece in row[:]:
            if not piece.is_blank_piece:
                print(piece.unicode_symbol.decode("utf-8", "ignore"), end=' ')
            else:
                # just for prettiness
                print('_', end=' ')
        row_number = row_number - 1
        print(end='\n')  # next row
    print('  a b c d e f g h')


def find_king(board, colour):
    row = 0
    for r in board:
        column = 0
        for piece in r:
            if piece.type == "k" and piece.col == colour:
                return [int(row), int(column)]
            column = (column + 1)
        row = row + 1


def get_team_move_set(board, col, option):
    team_move_set = []
    row = 0
    for r in board:
        column = 0
        for piece in r:
            if piece.col == col:  # eg. what's white attack set?
                piece_loc = [row, column]
                if option == "moveset":
                    team_move_set += piece_at(board, piece_loc[0], piece_loc[1]).get_move_set(board, piece_loc)
                else:
                    team_move_set += piece_at(board, piece_loc[0], piece_loc[1]).get_attack_set(board, piece_loc)
            column = (column + 1)
        row = row + 1
    return team_move_set


def is_being_checked(board, col):
    king_loc = find_king(board, col)
    team_attack_set = get_team_move_set(board, opposite_col(col), "attackset")

    for move in team_attack_set:
        if move.end_coords[0] == king_loc[0] and move.end_coords[1] == king_loc[1]:
            return True
    return False


def conduct_move(existing_board, candidate_move, player_col):
    """ Uses the supplied move on the existing board and returns a new board if the move is valid.

    If the move causes current player to be checked, False is returned. Does NOT modify existing_board.

    Note: Does minimal verification of validity of move   
    """

    # Copy old 2D board array
    new_board = deepcopy(existing_board)

    start_coords = candidate_move.start_coords
    end_coords = candidate_move.end_coords

    if selected_piece(new_board, start_coords).col != player_col:
        return False
    if candidate_move.move_type == MoveType.NORMAL:
        move_piece_inplace(new_board, start_coords, end_coords)
    elif candidate_move.move_type == MoveType.CASTLING:
        if candidate_move.end_coords[1] < King.KING_HOME_COL:
            # Move column a rook to other side of where King will move
            rook = new_board[start_coords[0]][0]
            new_board[start_coords[0]][2] = rook
            new_board[start_coords[0]][0] = BlankPiece()
            rook.has_never_moved = False
            move_piece_inplace(new_board, start_coords, end_coords)
        else:
            # Move column h rook to other side of where King will move
            rook = new_board[start_coords[0]][7]
            new_board[start_coords[0]][5] = rook
            new_board[start_coords[0]][7] = BlankPiece()
            rook.has_never_moved = False
            move_piece_inplace(new_board, start_coords, end_coords)
    elif candidate_move.move_type == MoveType.PROMOTION:
        # Advance pawn to final row
        move_piece_inplace(new_board, start_coords, end_coords)
        # Then replace it with selected piece in-place
        new_board[end_coords[0]][end_coords[1]] = candidate_move.promotion_piece

    return new_board


def move_piece_inplace(board, start_coords, end_coords):
    """
    Moves the piece at start_coords to end_coords, and replaces the first pieces with a blank piece

    Board is modified in-place.
    """
    piece = board[start_coords[0]][start_coords[1]]
    board[end_coords[0]][end_coords[1]] = piece
    piece.has_never_moved = False
    board[start_coords[0]][start_coords[1]] = BlankPiece()


def is_stalemate(board, player_turn):
        player_total_move_set = get_team_move_set(board, player_turn, "attackset")
        player_total_move_set += get_team_move_set(board, player_turn, "moveset")
        player_legal_move_set = filter_self_checking_moves(board, player_total_move_set, player_turn)

        return len(player_legal_move_set) == 0


def create():
    b = [[Rook("black"), Knight("black"), Bishop("black"), Queen("black"), King("black"), Bishop("black"),
          Knight("black"), Rook("black")],
         [Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"), Pawn("black"),
          Pawn("black")]]

    for i in range(2, 6):
        b.append([BlankPiece(), BlankPiece(), BlankPiece(), BlankPiece(), BlankPiece(), BlankPiece(), BlankPiece(), BlankPiece()])

    b.append([Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white"), Pawn("white")])
    b.append([Rook("white"), Knight("white"), Bishop("white"), Queen("white"), King("white"), Bishop("white"), Knight("white"), Rook("white")])
    return b

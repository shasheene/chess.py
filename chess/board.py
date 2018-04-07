from builtins import range, len, int
from copy import deepcopy

from chess.move import MoveType
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


def _get_all_pieces(board, color):
    pieces = []

    row = 0
    for r in board:
        column = 0
        for piece in r:
            if piece.col == color:
                pieces.append({'piece': piece, 'location': [row, column], 'type': piece.type})
            column = (column + 1)
        row = row + 1
    return pieces


def is_impossible_to_reach_checkmate(board):
    return _is_impossible_to_reach_checkmate(board, "white") or _is_impossible_to_reach_checkmate(board, "black")


def _is_impossible_to_reach_checkmate(board, color):
    player_pieces = _get_all_pieces(board, color)
    opponent_pieces = _get_all_pieces(board, opposite_col(color))
    if len(player_pieces) == 1 and len(opponent_pieces) == 1:
        # King v King
        return True
    if len(player_pieces) == 1 and len(opponent_pieces) == 2:
        for entry in opponent_pieces:
            opp_piece_type = entry.get('type')
            if opp_piece_type == 'b':
                    # King v King and Bishop
                    return True
            if opp_piece_type == 'h':
                    # King v King and Knight
                    return True

    # King and Bishop(s) VS King and Bishop(s), if they're all on the same checkerboard color
    if len(player_pieces) >= 2 and len(opponent_pieces) >= 2:
        player_bishops = []
        for entry in player_pieces:
            if entry.get("type") == 'b':
                player_bishops.append(entry)
            elif entry.get("type") != 'k':
                return False

        opponent_bishops = []
        for entry in opponent_pieces:
            if entry.get("type") == 'b':
                opponent_bishops.append(entry)
            elif entry.get("type") != 'k':
                return False

        if len(player_bishops) == 0 or len(opponent_bishops) == 0:
            return False
        else:
            opp_first_bishop_col = is_checkerboard_position_white(opponent_bishops[0].get("location"))
            # Ensure all player bishop's checkerboard colors are same as first opponent bishop.
            for player_bishop in player_bishops:
                if opp_first_bishop_col != is_checkerboard_position_white(player_bishop.get("location")):
                    return False
            # Ensure all opponent's bishop's checkerboard colors are consistent within itself
            for opponent_bishop in opponent_bishops:
                if opp_first_bishop_col != is_checkerboard_position_white(opponent_bishop.get("location")):
                    return False
            return True

    return False


def is_checkerboard_position_white(location):
    """
    Converts row/column into a checkboard color.

    :param location: [ Row indexed zero to 7, Column indexed zero 7 ]
    :return: True if position is white, and False is position is black
    """

    # Black square
    x = False
    # White square
    _ = True

    #    0  1  2  3  4  5  6  7
    col = [
        [x, _, x, _, x, _, x, _],   # 0
        [_, x, _, x, _, x, _, x],  # 1
        [x, _, x, _, x, _, x, _],  # 2
        [_, x, _, x, _, x, _, x],  # 3
        [x, _, x, _, x, _, x, _],  # 4
        [_, x, _, x, _, x, _, x],  # 5
        [x, _, x, _, x, _, x, _],  # 6
        [_, x, _, x, _, x, _, x],  # 7
    ]

    return col[location[0]][location[1]]


def update_move_history(board, move_history_list, player_turn):
    """Maintains threefold repetition list from the beginning of the game."""

    # Throw the attack and movement sets together (note: not maintaining information of which move is which at this
    # stage)
    player_opponent_combined_moveset = []
    player_opponent_combined_moveset.extend(get_team_move_set(board, "white", "moveset"))
    player_opponent_combined_moveset.extend(get_team_move_set(board, "white", "attackset"))
    player_opponent_combined_moveset.extend(get_team_move_set(board, "black", "moveset"))
    player_opponent_combined_moveset.extend(get_team_move_set(board, "black", "attackset"))

    # The turn of the player matters as well as the moveset
    element = {'players_turn': player_turn, 'moveset': player_opponent_combined_moveset}
    # Maintain a list with each element containing a list of movesets
    move_history_list.append(element)


def is_threefold_repetition_stalemate(move_history_list):
    """ See https://en.wikipedia.org/wiki/Threefold_repetition for explanation of the rule.

    :return: True if stalemate, False otherwise
    """

    for candidate_move in move_history_list:
        count = 0
        for move in move_history_list:
            if candidate_move == move:
                count += 1
                if count == 3:
                    return True
    return False


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


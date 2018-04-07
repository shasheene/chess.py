from chess.move import MoveType, Move
from chess.pieces import BlankPiece, Pawn, King, Rook, Knight
from test.unit_test_fn import assert_length, assert_contains, create_list_of_moves, assert_true
from chess.board import conduct_move


def assert_castling_rows_contain_same_type_elements(expected_row, actual_row):
    assert_true("Unexpected home row length", len(actual_row) == len(expected_row))
    for col in range(0, 8):
        assert_true("Rows types different."
                    + "\nExpected=" + str(expected_row)
                    + "\nActual  =" + str(actual_row), expected_row[col].type == actual_row[col].type)


def get_castling_board():
    # Home rank is just a constant in the castling implementation
    # so it's asserted unit testing only white piece's castling is sufficient
    __ = BlankPiece()

    p = Pawn("white")
    k = King("white")
    r1 = Rook("white")
    r2 = Rook("white")

    #     0   1   2   3   4   5   6   7
    return [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, __, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, __],  # 3
        [__, __, __, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, __, __],  # 5
        [__, __, __,  p,  p,  p, __, __],  # 6
        [r1, __, __, __,  k, __, __, r2]   # 7
    ]


def test_castling_movesets():
    board = get_castling_board()

    assert_contains(board[7][4].get_attack_set(board, [7, 4]),
                    create_list_of_moves(MoveType.NORMAL, [7, 4], [[7, 3], [7, 5]]))

    assert_contains(board[7][4].get_move_set(board, [7, 4]),
                    create_list_of_moves(MoveType.CASTLING, [7, 4], [[7, 1], [7, 6]]))

    # Pretend that r1 has moved and show it is removed from the castling set
    board[7][0].has_never_moved = False
    assert_contains(board[7][4].get_move_set(board, [7, 4]),
                    create_list_of_moves(MoveType.CASTLING, [7, 4], [[7, 6]]))

    # Add a Knight next to the r2 to show it removes it's option for castling
    board[7][6] = Knight("white")
    assert_length(board[7][4].get_move_set(board, [7, 4]), 0)


def test_conducting_col_a_castle_move():
    board = get_castling_board()
    col_a_castle = Move(MoveType.CASTLING, [7, 4], [7, 1])
    board, move_history_element = conduct_move(board, col_a_castle, "white")

    _ = BlankPiece()
    expected_row = [_, King("white"), Rook("white"), _, _, _, _, Rook("white")]
    actual_row = board[7]
    assert_castling_rows_contain_same_type_elements(expected_row, actual_row)


def test_conducting_col_h_castle_move():
    board = get_castling_board()
    col_h_castle = Move(MoveType.CASTLING, [7, 4], [7, 6])
    board, move_history_element = conduct_move(board, col_h_castle, "white")

    _ = BlankPiece()
    expected_row = [Rook("white"), _, _, _, _, Rook("white"), King("white"), _]
    actual_row = board[7]
    assert_castling_rows_contain_same_type_elements(expected_row, actual_row)


test_conducting_col_a_castle_move()
test_conducting_col_h_castle_move()

from chess.board import is_being_checked, can_player_leave_check_state
from chess.move import MoveType
from chess.pieces import BlankPiece, Rook, Pawn, King, Bishop, Queen, Knight
from test.unit_test_fn import assert_length, assert_contains, assert_false, assert_true, create_list_of_moves


def test_sliding_pieces(player_col, opponent_col):
    _ = BlankPiece()
    r = Rook(player_col)
    b = Bishop(player_col)
    q = Queen(player_col)

    # Enemy rook
    e = Rook(opponent_col)
    # Friendly Pawn
    f = Pawn(player_col)
    f.has_never_moved = False

    #            0  1  2  3  4  5  6  7
    board = [
                [r, _, _, e, _, _, _, _],  # 0
                [_, _, _, _, _, _, r, _],  # 1
                [_, _, q, _, _, _, f, _],  # 2
                [_, _, _, _, _, _, _, _],  # 3
                [_, _, _, _, _, _, _, _],  # 4
                [_, _, _, b, _, _, _, _],  # 5
                [_, _, _, _, _, _, _, _],  # 6
                [_, _, e, _, _, _, _, f]   # 7
            ]

    # Top-left rook
    assert_length(board[0][0].get_move_set(board, [0, 0]), 0)
    assert_contains(board[0][0].get_attack_set(board, [0, 0]),
                    create_list_of_moves(MoveType.NORMAL, [0, 0],
                                         [   # Down
                                      [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0],
                                      # Right
                                      [0, 1], [0, 2], [0, 3]
                                  ]))

    # Second rook
    assert_length(board[1][6].get_move_set(board, [1, 6]), 0)
    assert_contains(board[1][6].get_attack_set(board, [1, 6]),
                    create_list_of_moves(MoveType.NORMAL, [1, 6],
                                         [   # Up
                                      [0, 6],
                                      # Left
                                      [1, 5], [1, 4], [1, 3], [1, 2], [1, 1], [1, 0],
                                      # Right
                                      [1, 7]
                                  ]))

    # Bishop
    assert_length(board[5][3].get_move_set(board, [5, 3]), 0)
    assert_contains(board[5][3].get_attack_set(board, [5, 3]),
                    create_list_of_moves(MoveType.NORMAL, [5, 3],
                                         [   # North-west
                                      [4, 2], [3, 1], [2, 0],
                                      # North-east
                                      [4, 4], [3, 5],
                                      # South-west
                                      [6, 2], [7, 1],
                                      # South-east
                                      [6, 4], [7, 5]
                                  ]))

    # Queen
    assert_length(board[2][2].get_move_set(board, [2, 2]), 0)
    assert_contains(board[2][2].get_attack_set(board, [2, 2]),
                    create_list_of_moves(MoveType.NORMAL, [2, 2],
                                         [   # Down
                                      [3, 2], [4, 2], [5, 2], [6, 2], [7, 2],
                                      # Up
                                      [1, 2], [0, 2],
                                      # Left
                                      [2, 0], [2, 1],
                                      # Right
                                      [2, 3], [2, 4], [2, 5],
                                      # North-west
                                      [1, 1],
                                      # North-east
                                      [1, 3], [0, 4],
                                      # South-west
                                      [3, 1], [4, 0],
                                      # South-east
                                      [3, 3], [4, 4], [5, 5], [6, 6]
                                  ]))


def test_teleporting_pieces(player_col, opponent_col):
    _ = BlankPiece()

    k = King(player_col)
    k.has_never_moved = False
    h = Knight(player_col)

    # Enemy rook
    e = Rook(opponent_col)
    # Friendly Pawn
    f = Pawn(player_col)
    f.has_never_moved = False

    #        0  1  2  3  4  5  6  7
    board = [
                [h, _, _, _, _, _, _, _],  # 0
                [_, _, _, _, _, _, _, _],  # 1
                [_, _, _, f, _, e, _, _],  # 2
                [_, _, _, _, _, _, _, _],  # 3
                [_, _, _, _, h, _, _, _],  # 4
                [_, _, _, _, _, _, _, _],  # 5
                [_, h, _, _, _, _, _, _],  # 6
                [_, _, _, _, _, _, _, k]   # 7
            ]
    # Top-left knight
    assert_length(board[0][0].get_move_set(board, [0, 0]), 0)
    assert_contains(board[0][0].get_attack_set(board, [0, 0]),
                    create_list_of_moves(MoveType.NORMAL, [0, 0],
                                         [
                                      [1, 2],
                                      [2, 1],
                                  ]))

    # Knight near bottom
    assert_length(board[6][1].get_move_set(board, [6, 1]), 0)
    assert_contains(board[6][1].get_attack_set(board, [6, 1]),
                    create_list_of_moves(MoveType.NORMAL, [6, 1],
                                         [
                                      [4, 0],
                                      [4, 2],
                                      [5, 3],
                                      [7, 3]
                                  ]))

    # Middle knight
    assert_length(board[4][4].get_move_set(board, [4, 4]), 0)
    assert_contains(board[4][4].get_attack_set(board, [4, 4]),
                    create_list_of_moves(MoveType.NORMAL, [4, 4],
                                         [
                                      [2, 5],
                                      [6, 5],
                                      [6, 3],
                                      [3, 2],
                                      [5, 2],
                                      [3, 6],
                                      [5, 6]
                                  ]))

    # Bottom-right king
    assert_length(board[7][7].get_move_set(board, [7, 7]), 0)
    assert_contains(board[7][7].get_attack_set(board, [7, 7]),
                    create_list_of_moves(MoveType.NORMAL, [7, 7],
                                         [   # Up
                                      [6, 7],
                                      # Left
                                      [7, 6],
                                      # north-east
                                      [6, 6]
                                  ]))


def test_white_pawn_movements():
    __ = BlankPiece()

    p1 = Pawn("white")
    p2 = Pawn("white")
    p3 = Pawn("white")
    p3.has_never_moved = False

    # Enemy rook
    rr = Rook("black")

    #             0   1   2   3   4   5   6   7
    board = [
                [__, __, __, __, __, __, __, __],  # 0
                [__, __, __, __, __, __, __, __],  # 1
                [__, __, __, __, __, __, __, __],  # 2
                [__, __, __, __, __, __, rr, rr],  # 3
                [__, __, __, __, __, __, __, p3],  # 4
                [__, __, __, __, rr, __, __, __],  # 5
                [p1, __, __, __, __, p2, __, __],  # 6
                [__, __, __, __, __, __, __, __]  # 7
            ]
    # Left-most pawn
    assert_length(board[6][0].get_attack_set(board, [6, 0]), 0)
    assert_contains(board[6][0].get_move_set(board, [6, 0]),
                    create_list_of_moves(MoveType.NORMAL, [6, 0], [[5, 0], [4, 0]]))

    assert_contains(board[6][5].get_attack_set(board, [6, 5]),
                    create_list_of_moves(MoveType.NORMAL, [6, 5], [[5, 4]]))
    assert_contains(board[6][5].get_move_set(board, [6, 5]),
                    create_list_of_moves(MoveType.NORMAL, [6, 5], [[5, 5], [4, 5]]))

    assert_contains(board[4][7].get_attack_set(board, [4, 7]), create_list_of_moves(MoveType.NORMAL, [4, 7], [[3, 6]]))
    assert_length(board[4][7].get_move_set(board, [4, 7]), 0)


def test_black_pawn_movements():
    __ = BlankPiece()

    p1 = Pawn("black")
    p2 = Pawn("black")
    p3 = Pawn("black")

    # Enemy rook
    rr = Rook("white")

    #             0   1   2   3   4   5   6   7
    board = [
                [__, __, __, __, __, __, __, __],  # 0
                [p1, __, __, __, __, p2, __, __],  # 1
                [__, __, __, __, rr, __, __, __],  # 2
                [__, __, __, __, __, __, __, p3],  # 3
                [__, __, __, __, __, __, rr, rr],  # 4
                [__, __, __, __, __, __, __, __],  # 5
                [__, __, __, __, __, __, __, __],  # 6
                [__, __, __, __, __, __, __, __]  # 7
            ]
    # Left-most pawn
    assert_length(board[1][0].get_attack_set(board, [1, 0]), 0)
    assert_contains(board[1][0].get_move_set(board, [1, 0]),
                    create_list_of_moves(MoveType.NORMAL, [1, 0], [[2, 0], [3, 0]]))

    assert_contains(board[1][5].get_attack_set(board, [1, 5]),
                    create_list_of_moves(MoveType.NORMAL, [1, 5], [[2, 4]]))
    assert_contains(board[1][5].get_move_set(board, [1, 5]),
                    create_list_of_moves(MoveType.NORMAL, [1, 5], [[2, 5], [3, 5]]))

    assert_contains(board[3][7].get_attack_set(board, [3, 7]), create_list_of_moves(MoveType.NORMAL, [3, 7], [[4, 6]]))
    assert_length(board[3][7].get_move_set(board, [3, 7]), 0)


def test_check():
    # Opposite col test omitted as it requires an alternate implementation *and* player color doesn't effect this test.

    _ = BlankPiece()

    k = King("white")
    k.has_never_moved = False

    p = Pawn("black")
    p.has_never_moved = False

    #            0  1  2  3  4  5  6  7
    board = [
                [_, _, _, _, _, _, _, _],  # 0
                [_, _, _, _, _, _, _, _],  # 1
                [_, _, _, _, _, p, _, _],  # 2
                [_, _, _, _, k, _, _, _],  # 3
                [_, _, _, _, _, _, _, _],  # 4
                [_, _, _, _, _, _, _, _],  # 5
                [_, _, _, _, _, _, _, _],  # 6
                [_, _, _, _, _, _, _, _]   # 7
            ]
    assert_true("King should be checked", is_being_checked(board, "white"))

    # Enemy rook
    r = Rook("black")
    q = Queen("black")

    #            0  1  2  3  4  5  6  7
    board = [
                [_, _, _, _, _, _, _, _],  # 0
                [_, _, _, _, _, _, _, _],  # 1
                [_, _, _, _, _, _, _, _],  # 2
                [_, _, _, _, _, _, _, _],  # 3
                [_, _, _, _, _, _, _, _],  # 4
                [_, _, _, _, _, _, _, _],  # 5
                [_, _, _, _, _, _, r, _],  # 6
                [_, _, k, _, _, _, _, q]   # 7
            ]
    assert_false("Should be checkmate", can_player_leave_check_state(board, "white"))


colors = [{'player': "white", 'opponent': "black"}, {'player': "black", 'opponent': "white"}]
for color in colors:
    test_sliding_pieces(color['player'], color['opponent'])
    test_teleporting_pieces(color['player'], color['opponent'])

test_white_pawn_movements()
test_black_pawn_movements()
test_check()

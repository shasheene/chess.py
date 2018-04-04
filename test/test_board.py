from chess.move import Move, MoveType
from chess.pieces import BlankPiece, Rook, Pawn, King, Bishop, Queen, Knight


def assert_contains(actual_move_list, expected_move_list):
    if len(actual_move_list) != len(expected_move_list):
        raise AssertionError("Length " + str(len(actual_move_list)) + " != " + str(len(expected_move_list)))
    for expectedMove in expected_move_list:
        for actualMove in actual_move_list:
            if actualMove == expectedMove:
                break
        else:
            raise AssertionError(str(expectedMove) + " expected, but was not present in " + str(actual_move_list))


def assert_length(input_list, length):
    if len(input_list) != length:
        raise AssertionError("Expected list of length " + str(length) + " but was " + str(len(input_list)))


def create_list_of_moves(move_type, start_coord, end_coord_list):
    to_return = []
    for end_coord in end_coord_list:
        to_return.append(Move(move_type, start_coord, end_coord))
    return to_return


def test_sliders():
    board = []
    _ = BlankPiece()
    r = Rook("white")
    b = Bishop("white")
    q = Queen("white")

    # Enemy rook
    e = Rook("black")
    # Friendly Pawn
    f = Pawn("white")
    f.has_never_moved = False

    # Recall      0  1  2  3  4  5  6  7 indexing
    board.append([r, _, _, e, _, _, _, _])
    board.append([_, _, _, _, _, _, r, _])
    board.append([_, _, q, _, _, _, f, _])
    board.append([_, _, _, _, _, _, _, _])
    board.append([_, _, _, _, _, _, _, _])
    board.append([_, _, _, b, _, _, _, _])
    board.append([_, _, _, _, _, _, _, _])
    board.append([_, _, e, _, _, _, _, f])

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


def test_teleporters():
    board = []
    _ = BlankPiece()

    k = King("white")
    k.has_never_moved = False
    h = Knight("white")

    # Enemy rook
    e = Rook("black")
    # Friendly Pawn
    f = Pawn("white")
    f.has_never_moved = False

    # Recall      0  1  2  3  4  5  6  7 indexing
    board.append([h, _, _, _, _, _, _, _])
    board.append([_, _, _, _, _, _, _, _])
    board.append([_, _, _, f, _, e, _, _])
    board.append([_, _, _, _, _, _, _, _])
    board.append([_, _, _, _, h, _, _, _])
    board.append([_, _, _, _, _, _, _, _])
    board.append([_, h, _, _, _, _, _, _])
    board.append([_, _, _, _, _, _, _, k])

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


def test_pawn_movements():
    board = []
    __ = BlankPiece()

    p1 = Pawn("white")
    p2 = Pawn("white")
    p3 = Pawn("white")
    p3.has_never_moved = False

    # Enemy rook
    rr = Rook("black")

    # Recall       0   1   2   3   4   5   6   7  indexing
    board.append([__, __, __, __, __, __, __, __])
    board.append([__, __, __, __, __, __, __, __])
    board.append([__, __, __, __, __, __, __, __])
    board.append([__, __, __, __, __, __, rr, rr])
    board.append([__, __, __, __, __, __, __, p3])
    board.append([__, __, __, __, rr, __, __, __])
    board.append([p1, __, __, __, __, p2, __, __])
    board.append([__, __, __, __, __, __, __, __])

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


test_sliders()
test_teleporters()
test_pawn_movements()

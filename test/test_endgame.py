from chess.board import is_being_checked, can_player_leave_check_state, is_stalemate, is_impossible_to_reach_checkmate
from chess.pieces import BlankPiece, Rook, Pawn, King, Queen, Bishop, Knight
from test.unit_test_fn import assert_false, assert_true


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


def test_stalemate():
    # Opposite col test omitted as player color doesn't effect this test.

    __ = BlankPiece()
    wk= King("white")

    r = Rook("black")
    q = Queen("black")
    bk = King("black")

    #             0   1   2   3   4   5   6   7
    board = [
                [__, __, __, __, __, __, __, __],  # 0
                [__, __, __, __, __, __, __, __],  # 1
                [__, __, __, __, __, __, __, __],  # 2
                [__,  r, __, __, __, __, __, __],  # 3
                [__, __, __, __, __, __, __, bk],  # 4
                [__, __, __, __, __, __, __, __],  # 5
                [__, __, __, __,  q, __, __, __],  # 6
                [wk, __, __, __, __, __, __, __]   # 7
            ]
    assert_false("White should NOT be a check state", is_being_checked(board, "white"))
    assert_true("White should be in stalemate", is_stalemate(board, "white"))
    assert_false("Black should NOT be in stalemate state", is_stalemate(board, "black"))


def test_insufficient_material_states():
    __ = BlankPiece()
    wk = King("white")
    bk = King("black")

    #             0   1   2   3   4   5   6   7
    board = [
                [__, __, __, __, __, __, __, __],  # 0
                [__, __, __, __, __, __, __, __],  # 1
                [__, __, __, __, __, __, wk, __],  # 2
                [__, __, __, __, __, __, __, __],  # 3
                [__, __, bk, __, __, __, __, __],  # 4
                [__, __, __, __, __, __, __, __],  # 5
                [__, __, __, __, __, __, __, __],  # 6
                [__, __, __, __, __, __, __, __]   # 7
            ]
    assert_true("Just kings should impossible to checkmate", is_impossible_to_reach_checkmate(board))

    bB = Bishop("black")
    #     0   1   2   3   4   5   6   7
    board = [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, __, __, __, __, wk, __],  # 2
        [__, __, __, __, __, __, __, __],  # 3
        [__, __, bk, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, bB, __],  # 5
        [__, __, __, __, __, __, __, __],  # 6
        [__, __, __, __, __, __, __, __]  # 7
    ]
    assert_true("King vs King and bishop should be impossible to checkmate", is_impossible_to_reach_checkmate(board))

    bH = Knight("black")
    #     0   1   2   3   4   5   6   7
    board = [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, __, __, __, __, wk, __],  # 2
        [__, __, __, __, __, __, __, __],  # 3
        [__, __, bk, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, bH, __],  # 5
        [__, __, __, __, __, __, __, __],  # 6
        [__, __, __, __, __, __, __, __]  # 7
    ]
    assert_true("King vs King and Knight should be impossible checkmate", is_impossible_to_reach_checkmate(board))

    wb = Bishop("white")
    bb = Bishop("black")
    #     0   1   2   3   4   5   6   7
    board = [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, wk, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, wb],  # 3
        [__, __, bk, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, __, bb],  # 5
        [__, __, __, __, __, __, __, __],  # 6
        [__, __, __, __, __, __, __, __]  # 7
    ]
    assert_true("King and Bishop vs King and Bishop should be impossible if they are on the same color square",
                is_impossible_to_reach_checkmate(board))

    #     0   1   2   3   4   5   6   7
    board = [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, wk, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, wb],  # 3
        [__, __, bk, __, __, __, __, bb],  # 4
        [__, __, __, __, __, __, __, __],  # 5
        [__, __, __, __, __, __, __, __],  # 6
        [__, __, __, __, __, __, __, __]  # 7
    ]
    assert_false("King and Bishop vs King and Bishop should be POSSIBLE to reach checkmate if they're on different "
                 "colours", is_impossible_to_reach_checkmate(board))

    # Does not matter the amount of Bishops as long as they are on the same color square
    #     0   1   2   3   4   5   6   7
    board = [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, __, wb, __, __],  # 1
        [__, __, wk, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, wb],  # 3
        [__, __, bk, __, __, __, __, __],  # 4
        [__, __, __, __, __, wb, __, bb],  # 5
        [__, __, __, __, __, __, __, __],  # 6
        [__, __, __, __, __, __, __, wb]  # 7
    ]
    assert_true("King and Bishop(s) vs King and Bishop(s) should be impossible if they are on the same color square",
                is_impossible_to_reach_checkmate(board))

    #     0   1   2   3   4   5   6   7
    board = [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, __, wb, __, __],  # 1
        [__, __, wk, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, wb],  # 3
        [__, __, bk, __, __, __, __, __],  # 4
        [__, __, __, __, __, wb, __, bb],  # 5
        [__, __, __, __, __, __, __, wb],  # 6
        [__, __, __, __, __, __, __, wb]  # 7
    ]
    assert_false("King and Bishop(s) vs King and Bishop(s) should be POSSIBLE as not all on same color square",
                is_impossible_to_reach_checkmate(board))


test_check()
test_stalemate()
test_insufficient_material_states()

from collections import deque

from chess.board import is_being_checked, can_player_leave_check_state, is_stalemate, is_impossible_to_reach_checkmate, \
    is_threefold_repetition_stalemate, update_move_history, conduct_move, is_fifty_move_rule_draw
from chess.move import Move, MoveType
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
        [_, _, _, _, _, _, _, _]  # 7
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
        [_, _, k, _, _, _, _, q]  # 7
    ]
    assert_false("Should be checkmate", can_player_leave_check_state(board, "white"))


def test_stalemate():
    # Opposite col test omitted as player color doesn't effect this test.

    __ = BlankPiece()
    wk = King("white")

    r = Rook("black")
    q = Queen("black")
    bk = King("black")

    #             0   1   2   3   4   5   6   7
    board = [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, __, __, __, __, __, __],  # 2
        [__, r, __, __, __, __, __, __],  # 3
        [__, __, __, __, __, __, __, bk],  # 4
        [__, __, __, __, __, __, __, __],  # 5
        [__, __, __, __, q, __, __, __],  # 6
        [wk, __, __, __, __, __, __, __]  # 7
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
        [__, __, __, __, __, __, __, __]  # 7
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


def test_threefold_repetition():
    move_list = []

    __ = BlankPiece()
    wk = King("white")
    bk = King("black")

    #     0   1   2   3   4   5   6   7
    board0 = [
        [__, __, __, bk, __, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, __, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, __],  # 3
        [__, __, __, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, __, __],  # 5
        [__, __, __, __, __, __, __, __],  # 6
        [__, __, __, __, wk, __, __, __]  # 7
    ]

    #     0   1   2   3   4   5   6   7
    board1 = [
        [__, __, __, __, bk, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, __, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, __],  # 3
        [__, __, __, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, __, __],  # 5
        [__, __, __, __, __, __, __, __],  # 6
        [__, __, __, __, wk, __, __, __]  # 7
    ]

    board2 = [
        [__, __, __, __, bk, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, __, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, __],  # 3
        [__, __, __, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, __, __],  # 5
        [__, __, __, __, wk, __, __, __],  # 6
        [__, __, __, __, __, __, __, __]  # 7
    ]

    board3 = [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, bk, __, __, __],  # 1
        [__, __, __, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, __],  # 3
        [__, __, __, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, __, __],  # 5
        [__, __, __, __, wk, __, __, __],  # 6
        [__, __, __, __, __, __, __, __]  # 7
    ]

    board4 = [
        [__, __, __, __, __, __, __, __],  # 0
        [__, __, __, __, bk, __, __, __],  # 1
        [__, __, __, __, __, __, __, __],  # 2
        [__, __, __, __, __, __, __, __],  # 3
        [__, __, __, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, __, __],  # 5
        [__, __, __, __, __, __, __, __],  # 6
        [__, __, __, __, wk, __, __, __]  # 7
    ]

    msg = "Expected to not yet have 3 repetitions"

    # Initial state
    update_move_history(board0, move_list, "black")
    assert_false(msg, is_threefold_repetition_stalemate(move_list))

    # Board state repeated once
    update_move_history(board1, move_list, "white")
    assert_false(msg, is_threefold_repetition_stalemate(move_list))
    update_move_history(board2, move_list, "black")
    assert_false(msg, is_threefold_repetition_stalemate(move_list))
    update_move_history(board3, move_list, "white")
    assert_false(msg, is_threefold_repetition_stalemate(move_list))
    update_move_history(board4, move_list, "black")
    assert_false(msg, is_threefold_repetition_stalemate(move_list))
    # Board state repeated twice
    update_move_history(board1, move_list, "white")
    assert_false(msg, is_threefold_repetition_stalemate(move_list))
    update_move_history(board2, move_list, "black")
    assert_false(msg, is_threefold_repetition_stalemate(move_list))
    update_move_history(board3, move_list, "white")
    assert_false(msg, is_threefold_repetition_stalemate(move_list))
    update_move_history(board4, move_list, "black")
    assert_false(msg, is_threefold_repetition_stalemate(move_list))
    # Board state repeated three times
    update_move_history(board1, move_list, "white")
    assert_true("Expected threefold repetition stalemate", is_threefold_repetition_stalemate(move_list))


def get_fifty_move_rule_board():
    """
    Helper function to run through the first 3 moves in a "four move rule" (use a smaller deque for sanity here -- 50
    is a lot),
    """
    #
    conducted_move_history = deque([], 4)

    __ = BlankPiece()
    wk = King("white")
    wp = Pawn("white")
    br = Rook("black")
    bk = King("black")

    #     0   1   2   3   4   5   6   7
    board = [
        [__, __, __, bk, __, __, __, __],  # 0
        [__, __, __, __, __, __, __, __],  # 1
        [__, __, __, __, __, __, __, __],  # 2
        [__, br, __, __, __, __, __, __],  # 3
        [__, __, __, __, __, __, __, __],  # 4
        [__, __, __, __, __, __, __, __],  # 5
        [__, wp, __, __, __, __, __, __],  # 6
        [__, __, __, __, wk, __, __, __]  # 7
    ]

    msg = "Should NOT be 50-move rule draw"

    board, move_history_element = conduct_move(board, Move(MoveType.NORMAL, [7, 4], [7, 1]), "white")
    conducted_move_history.append(move_history_element)
    assert_false(msg, is_fifty_move_rule_draw(conducted_move_history))

    board, move_history_element = conduct_move(board, Move(MoveType.NORMAL, [7, 1], [7, 2]), "white")
    conducted_move_history.append(move_history_element)
    assert_false(msg, is_fifty_move_rule_draw(conducted_move_history))

    board, move_history_element = conduct_move(board, Move(MoveType.NORMAL, [7, 2], [7, 3]), "white")
    conducted_move_history.append(move_history_element)
    assert_false(msg, is_fifty_move_rule_draw(conducted_move_history))
    return board, conducted_move_history


def test_fifty_move_rule():
    # Test moving white King to cause a 50-move rule draw
    board, conducted_move_history = get_fifty_move_rule_board()
    board, move_history_element = conduct_move(board, Move(MoveType.NORMAL, [7, 3], [7, 4]), "white")
    conducted_move_history.append(move_history_element)
    assert_true("Should be 50-move rule draw", is_fifty_move_rule_draw(conducted_move_history))

    # Black rook captures white pawn to prevent 50-move rule draw (via piece-capture code-path)
    board, conducted_move_history = get_fifty_move_rule_board()
    board, move_history_element = conduct_move(board, Move(MoveType.NORMAL, [3, 1], [6, 1]), "black")
    conducted_move_history.append(move_history_element)
    assert_false("Should NOT be draw", is_fifty_move_rule_draw(conducted_move_history))

    # Advance a pawn to prevent 50-move rule draw (via Pawn-type movement code-path)
    board, conducted_move_history = get_fifty_move_rule_board()
    board, move_history_element = conduct_move(board, Move(MoveType.NORMAL, [6, 1], [5, 2]), "white")
    conducted_move_history.append(move_history_element)
    assert_false("Should NOT be draw", is_fifty_move_rule_draw(conducted_move_history))


test_check()
test_stalemate()
test_insufficient_material_states()
test_threefold_repetition()
test_fifty_move_rule()

from chess.board import conduct_move
from chess.move import MoveType, Move
from chess.pieces import BlankPiece, Rook, Pawn, Queen, Bishop, Knight
from test.unit_test_fn import assert_length, assert_contains, create_list_of_moves, \
    assert_row_contain_same_type_elements


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
    assert_length(board[6][0].get_attack_set(board, [6, 0], []), 0)
    assert_contains(board[6][0].get_move_set(board, [6, 0], []),
                    create_list_of_moves(MoveType.NORMAL, [6, 0], [[5, 0], [4, 0]]))

    assert_contains(board[6][5].get_attack_set(board, [6, 5], []),
                    create_list_of_moves(MoveType.NORMAL, [6, 5], [[5, 4]]))
    assert_contains(board[6][5].get_move_set(board, [6, 5], []),
                    create_list_of_moves(MoveType.NORMAL, [6, 5], [[5, 5], [4, 5]]))

    assert_contains(board[4][7].get_attack_set(board, [4, 7], []), create_list_of_moves(MoveType.NORMAL, [4, 7], [[3, 6]]))
    assert_length(board[4][7].get_move_set(board, [4, 7], []), 0)


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
    assert_length(board[1][0].get_attack_set(board, [1, 0], []), 0)
    assert_contains(board[1][0].get_move_set(board, [1, 0], []),
                    create_list_of_moves(MoveType.NORMAL, [1, 0], [[2, 0], [3, 0]]))

    assert_contains(board[1][5].get_attack_set(board, [1, 5], []),
                    create_list_of_moves(MoveType.NORMAL, [1, 5], [[2, 4]]))
    assert_contains(board[1][5].get_move_set(board, [1, 5], []),
                    create_list_of_moves(MoveType.NORMAL, [1, 5], [[2, 5], [3, 5]]))

    assert_contains(board[3][7].get_attack_set(board, [3, 7], []), create_list_of_moves(MoveType.NORMAL, [3, 7], [[4, 6]]))
    assert_length(board[3][7].get_move_set(board, [3, 7], []), 0)


def test_white_pawn_promotion():
    __ = BlankPiece()

    p1 = Pawn("white")
    p2 = Pawn("white")

    # Enemy rook
    rr = Rook("black")

    #             0   1   2   3   4   5   6   7
    board = [
                [__, __, __, __, __, rr, __, __],  # 0
                [__, __, p1, __, __, p2, __, __],  # 1
                [__, __, __, __, __, __, __, __],  # 2
                [__, __, __, __, __, __, __, __],  # 3
                [__, __, __, __, __, __, __, __],  # 4
                [__, __, __, __, __, __, __, __],  # 5
                [__, __, __, __, __, __, __, __],  # 6
                [__, __, __, __, __, __, __, __]  # 7
            ]
    # Left-most pawn
    assert_length(board[1][2].get_attack_set(board, [1, 2], []), 0)
    assert_contains(board[1][2].get_move_set(board, [1, 2], []),
                    [
                        Move.pawn_promotion([1, 2], [0, 2], Queen("white")),
                        Move.pawn_promotion([1, 2], [0, 2], Bishop("white")),
                        Move.pawn_promotion([1, 2], [0, 2], Knight("white")),
                        Move.pawn_promotion([1, 2], [0, 2], Rook("white"))
                    ])
    assert_length(board[1][5].get_attack_set(board, [1, 5], []), 0)
    assert_length(board[1][5].get_move_set(board, [1, 5], []), 0)


def test_black_pawn_promotion():
    __ = BlankPiece()

    p1 = Pawn("black")
    p2 = Pawn("black")

    # Enemy rook
    rr = Rook("white")

    #             0   1   2   3   4   5   6   7
    board = [
                [__, __, __, __, __, __, __, __],  # 0
                [__, __, __, __, __, __, __, __],  # 1
                [__, __, __, __, __, __, __, __],  # 2
                [__, __, __, __, __, __, __, __],  # 3
                [__, __, __, __, __, __, __, __],  # 4
                [__, __, __, __, __, __, __, __],  # 5
                [p1, __, __, __, p2, __, __, __],  # 6
                [__, __, __, __, rr, __, __, __]  # 7
            ]
    # Left-most pawn
    assert_length(board[6][0].get_attack_set(board, [6, 0], []), 0)
    assert_contains(board[6][0].get_move_set(board, [6, 0], []),
                    [
                        Move.pawn_promotion([6, 0], [7, 0], Queen("black")),
                        Move.pawn_promotion([6, 0], [7, 0], Bishop("black")),
                        Move.pawn_promotion([6, 0], [7, 0], Knight("black")),
                        Move.pawn_promotion([6, 0], [7, 0], Rook("black"))
                    ])
    assert_length(board[6][4].get_attack_set(board, [6, 4], []), 0)
    assert_length(board[6][4].get_move_set(board, [6, 4], []), 0)


def get_enpassant_board():
    __ = BlankPiece()
    p1 = Pawn("black")
    p2 = Pawn("black")
    wp = Pawn("white")
    wp.has_never_moved = False

    #             0   1   2   3   4   5   6   7
    board = [
                [__, __, __, __, __, __, __, __],  # 0
                [__, __, __, __, __, p1, __, p2],  # 1
                [__, __, __, __, __, __, __, __],  # 2
                [__, __, __, __, __, __, wp, __],  # 3
                [__, __, __, __, __, __, __, __],  # 4
                [__, __, __, __, __, __, __, __],  # 5
                [__, __, __, __, __, __, __, __],  # 6
                [__, __, __, __, __, __, __, __]  # 7
            ]

    assert_length(board[3][6].get_attack_set(board, [3, 6], []), 0)
    assert_contains(
        board[3][6].get_move_set(board, [3, 6], []),
        [
            Move(MoveType.NORMAL, [3, 6], [2, 6])
        ]
    )
    return board


def test_board_state_without_pawn_enpassant():
    conducted_move_history = []
    board = get_enpassant_board()
    board, move_history_element = conduct_move(board, Move(MoveType.NORMAL, [1,  5], [2, 5]), "black")
    conducted_move_history.append(move_history_element)

    # Assert white pawn can only do regular attack and one space advance
    assert_contains(
        board[3][6].get_attack_set(board, [3, 6], conducted_move_history),
        [
            Move(MoveType.NORMAL, [3, 6], [2, 5])
        ]
    )
    assert_contains(
        board[3][6].get_move_set(board, [3, 6], conducted_move_history),
        [Move(MoveType.NORMAL, [3, 6], [2, 6])]
    )

    # Advance the black pawn one more space
    board, move_history_element = conduct_move(board, Move(MoveType.NORMAL, [2, 5], [3, 5]), "black")
    conducted_move_history.append(move_history_element)

    # Assert white pawn can only do do a one space advance
    assert_length(board[3][6].get_attack_set(board, [3, 6], []), 0)
    assert_contains(
        board[3][6].get_move_set(board, [3, 6], []),
        [
            Move(MoveType.NORMAL, [3, 6], [2, 6])
        ]
    )


def test_pawn_enpassant():
    # Advance pawn by two spaces
    conducted_move_history = []
    board = get_enpassant_board()
    board, move_history_element = conduct_move(board, Move(MoveType.NORMAL, [1, 5], [3, 5]), "black")
    conducted_move_history.append(move_history_element)

    # Assert white pawn can only do regular attack, one space advance AND enpassant
    en_passant_move = Move.en_passant([3, 6], [2, 5])
    assert_contains(
        board[3][6].get_attack_set(board, [3, 6], conducted_move_history),
        [
            en_passant_move
        ]
    )

    # Actually execute en passant move
    board, move_history_element = conduct_move(board, en_passant_move, "white")
    conducted_move_history.append(move_history_element)

    __ = BlankPiece()
    p2 = Pawn("black")
    wp = Pawn("white")
    #             0   1   2   3   4   5   6   7
    expected_board = [
                [__, __, __, __, __, __, __, __],  # 0
                [__, __, __, __, __, __, __, p2],  # 1
                [__, __, __, __, __, wp, __, __],  # 2
                [__, __, __, __, __, __, __, __],  # 3
                [__, __, __, __, __, __, __, __],  # 4
                [__, __, __, __, __, __, __, __],  # 5
                [__, __, __, __, __, __, __, __],  # 6
                [__, __, __, __, __, __, __, __]  # 7
            ]
    assert_row_contain_same_type_elements(expected_board[1], board[1])
    assert_row_contain_same_type_elements(expected_board[2], board[2])
    assert_row_contain_same_type_elements(expected_board[3], board[3])


test_white_pawn_movements()
test_black_pawn_movements()
test_white_pawn_promotion()
test_black_pawn_promotion()
test_board_state_without_pawn_enpassant()
test_pawn_enpassant()

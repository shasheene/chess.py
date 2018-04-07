#!/usr/bin/python
"""
shasheene 2013-12-15

Text-based chess game.
"""

import sys
from builtins import ValueError, Exception, len, input, chr, str, ord, int, KeyboardInterrupt

from chess.board import create, is_being_checked, can_player_leave_check_state, print_board, opposite_col, \
    filter_self_checking_moves, conduct_move, selected_piece, is_stalemate
from chess.move import MoveType


def a1_to_py_convert(pair):
    """ Converts chess coords system to a list with origin top-left.

    Chess has origin bottom-left and counts colums a to h and rows numbered 1 to 8. 
    Computers index differently, from top-left and count from 0 rather than 1.

    Example: 'a8' returns [0,0]. 'a1' returns [7,0].
    
    Note: No error checking yet - assumes user enters valid input currently
    """
    # print "Checking pair: " + pair
    col = ord(pair[0].lower()) - 97  # In ascii, 'a'=97
    # print "Letter is " + str(pair[0]) + " -> " + str(col)
    row = 8 - int(pair[1])  # Chess counts from 1, not 0. (the row component of coords 'e2' to is 1, not 2.)
    return row, col


def py_to_a1_convert(pair):
    col = chr(pair[1] + 97)  # In ascii, 'a'=97
    row = str(8 - pair[0])  # Chess counts from 1, not 0. (the row component of coords 'e2' to is 1, not 2.)
    return col + row


def take_input():
    r = input()
    print()
    # Ignore things after spaces
    return r.split()[0:1]


def request_user_move(message):
    print(message)
    raw_input = take_input()
    if len(raw_input) == 0:
        print("No input given.\n")
        return False

    try:
        # e4 becomes [3,3]
        move = a1_to_py_convert(raw_input[0])
    except (ValueError, Exception):
        print("Error occurred processing input. Please try again.\n")
        return False
    return move


def request_promotion_type(piece_legal_move_set):
    print("Please choose type 'Queen', 'Bishop', 'Knight' or 'Rook'")
    piece_string = take_input()
    if len(piece_string) == 0:
        print("No piece_string given.\n")
        return False

    # Take the element out of the list
    piece_string = piece_string[0]

    if piece_string != "Queen" and piece_string != "Bishop" and piece_string != "Knight" and piece_string != "Rook":
        return False

    for move in piece_legal_move_set:
        if type(move.promotion_piece).__name__ == piece_string:
            return move
    return False


def main():
    player_turn = "white"

    game_board = create()

    while 1:
        print_board(game_board)
        print(player_turn + 's turn. Select piece')

        valid_selection = False
        while not valid_selection:
            coords = request_user_move(' Select piece to move. Example: e2 \n')
            if not coords:
                continue
            if selected_piece(game_board, coords).is_blank_piece:
                print('...Error invalid piece. Choose another piece\n')
                continue
            if selected_piece(game_board, coords).col != player_turn:
                print('...Error selected opponents\' piece. Choose another piece\n')
                continue

            piece_total_move_set = selected_piece(game_board, coords).get_move_set(game_board, coords)
            piece_total_move_set += selected_piece(game_board, coords).get_attack_set(game_board, coords)
            piece_legal_move_set = filter_self_checking_moves(game_board, piece_total_move_set, player_turn)
            if len(piece_legal_move_set) == 0:
                print('...Error no legal moves available. Choose another piece\n')
                continue
            valid_selection = True

            print('Selected: \'' + selected_piece(game_board, coords).type + '\'.', )
            print('Possible moves: ', )
            for move in piece_legal_move_set:
                print(move, ": ", py_to_a1_convert(move.end_coords))
            print()

            # Choose end location:
            chosen_move = False
            while not chosen_move:
                user_end_coords = request_user_move(' Select location to move piece to: ')
                if not user_end_coords:
                    continue
                for move in piece_legal_move_set:
                    if move.end_coords[0] == user_end_coords[0] and move.end_coords[1] == user_end_coords[1]:
                        chosen_move = move
                if chosen_move.move_type == MoveType.PROMOTION:
                    # If we chose one a promotion end coordinates, we need to find the exact promotion choice we desire
                    chosen_move = request_promotion_type(piece_legal_move_set)
                if not chosen_move:
                    print('Invalid move\n')
                    continue

        game_board = conduct_move(game_board, chosen_move, player_turn)
        if not game_board:
            print("Illegal move not caught by game logic")

        if is_being_checked(game_board, opposite_col(player_turn)):
            if can_player_leave_check_state(game_board, opposite_col(player_turn)):
                print('CHECK\n')
            else:
                print_board(game_board)
                print('CHECKMATE. ' + player_turn + ' wins!\n')
                sys.exit(0)

        player_turn = opposite_col(player_turn)
        if is_stalemate(game_board, player_turn):
            print('DRAW (STALEMATE)\n')
            sys.exit(0)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)

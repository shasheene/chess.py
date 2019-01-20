#!/usr/bin/python
import socket
import sys
from builtins import ValueError, Exception, len, input, chr, str, ord, int, KeyboardInterrupt
from time import sleep

from chess.board import print_board, convert_from_string_gameboard
from chess.utils import send_msg, recv_msg, wrap, CREATE_SESSION, unwrap, ERROR, GET_GAME_STATE, GET_MOVES, MAKE_MOVE, \
    GET_SESSIONS, JOIN_SESSION


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
    return [row, col]


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
    HOST = ''
    PORT = 8000
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((HOST, PORT))

        send_msg(client_socket, wrap(GET_SESSIONS, {}))
        get_sessions_msg = unwrap(recv_msg(client_socket))
        if get_sessions_msg['message_type'] == ERROR:
            print("Error occurred:" + get_sessions_msg['description'])
            return
        else:
            print("sessions are: " + str(get_sessions_msg))
            sessions = get_sessions_msg['payload']['sessions']
            if len(sessions) == 0:
                # Create new session
                send_msg(client_socket, wrap(CREATE_SESSION, {'desired_color': "white"}))
                return_msg = unwrap(recv_msg(client_socket))
                if return_msg['message_type'] == ERROR:
                    print("Error occurred:" + return_msg['payload']['description'])
                    return
                else:

                    session = return_msg['payload']
            else:
                print("sessions is" + str(sessions))
                # Join existing session
                send_msg(client_socket, wrap(JOIN_SESSION, {'name': sessions[0]}))
                return_msg = unwrap(recv_msg(client_socket))
                if return_msg['message_type'] == ERROR:
                    print("Error occurred:" + return_msg['payload']['description'])
                    return
                else:
                    session = return_msg['payload']

        send_msg(client_socket, wrap(GET_GAME_STATE, {'session': session}))
        game_state_msg = unwrap(recv_msg(client_socket))
        if game_state_msg['message_type'] == ERROR:
            print("Error occurred:" + return_msg['payload']['description'])
            return
        player_col = game_state_msg['payload']['your_color']
        print("Connected to game session: " + session['name'] + ". Player is color " + player_col)

        while 1:
            send_msg(client_socket, wrap(GET_GAME_STATE, {'session': session}))
            game_state_msg = unwrap(recv_msg(client_socket))
            if game_state_msg['message_type'] == ERROR:
                print("Error occurred:" + return_msg['payload']['description'])
                continue

            if game_state_msg['payload']['player_turn'] != player_col:
                sleep(2)
                continue

            game_board = convert_from_string_gameboard(game_state_msg['payload']['board'])
            print_board(player_col, game_board)

            progress_state = game_state_msg['payload']['progress_state']
            if progress_state['state'] == "CHECK":
                print(progress_state['description'])
                return
            if progress_state['state'] == "GAMEOVER":
                print(progress_state['description'])
                return

            print('Your turn. Select piece')
            valid_selection = False
            coords = False
            while not valid_selection:
                coords = request_user_move(' Select piece to move. Example: e2 \n')
                if not coords:
                    continue
                valid_selection = True

            send_msg(client_socket, wrap(GET_MOVES, {'session': session, 'piece_coords': coords}))
            return_msg = unwrap(recv_msg(client_socket))
            if return_msg['message_type'] == ERROR:
                print("Error occurred:" + return_msg['payload']['description'])
                return
            possible_moves = return_msg['payload']
            print("Received possible moves " + str(possible_moves))

            # Choose end location:
            chosen_move = False
            while not chosen_move:
                user_end_coords = request_user_move(' Select location to move piece to: ')
                if not user_end_coords:
                    continue
                for move in possible_moves:
                    if move['end_coords'][0] == user_end_coords[0] and move['end_coords'][1] == user_end_coords[1]:
                        chosen_move = move
                if not chosen_move:
                    continue

            send_msg(client_socket, wrap(MAKE_MOVE, {'session': session, 'desired_move': chosen_move}))
            game_state_msg = unwrap(recv_msg(client_socket))
            if game_state_msg['message_type'] == ERROR:
                print("Error occurred:" + return_msg['payload']['description'])
                continue
            game_board = convert_from_string_gameboard(game_state_msg['payload']['board'])
            print_board(player_col, game_board)

            progress_state = game_state_msg['payload']['progress_state']
            if progress_state['state'] == "CHECK":
                print(progress_state['description'])
            if progress_state['state'] == "GAMEOVER":
                print(progress_state['description'])
                continue

            print('Opponents turn. Please wait..')
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Shutting down.")

    client_socket.close()
    sys.exit(0)


if __name__ == "__main__":
    main()

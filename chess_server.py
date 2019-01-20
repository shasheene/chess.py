#!/usr/bin/python
import selectors
import socket
from builtins import str

from chess.session import Session
from chess.utils import wrap, CREATE_SESSION, GET_SESSIONS, GET_GAME_STATE, MAKE_MOVE, \
    GET_MOVES, JOIN_SESSION, unwrap, recv_msg2, send_msg2, wrap_error

HOST = ''
LISTENING_SOCKET_PORT = 8000


class GameServer(object):
    def __init__(self):
        self.temp_session_name = 'temp-game-session-id'
        self.sessions = {}

    def _generate_access_key(self, remove_later):
        return remove_later

    def process(self, message):
        if 'message_type' not in message or 'payload' not in message:
            return wrap_error("Malformed message")
   
        msg_type = message['message_type']   
        # SESSION MANAGEMENT
        if msg_type == CREATE_SESSION:
            desired_color = message['payload']['desired_color']
            self.sessions[self.temp_session_name] = \
                {'session': Session(), 'access_keys': {'white': self._generate_access_key("white_player"),
                                                       'black': self._generate_access_key("black_player")}}
            white_key = {'name': self.temp_session_name,
                         "access_key": self.sessions[self.temp_session_name]['access_keys']['white']}
            print("CREATED_SESSION " + str(self.sessions))
            return wrap(CREATE_SESSION, white_key)
        elif msg_type == GET_SESSIONS:
            print("sessions is " + str(self.sessions))
            return wrap(GET_SESSIONS, {'sessions': list(dict.keys(self.sessions))})

        if msg_type == JOIN_SESSION:
            join_name = message['payload']['name']
            black_key = {"name": join_name, "access_key": self.sessions[join_name]['access_keys']['black']}
            return wrap(JOIN_SESSION, black_key)

        name = message['payload']['session']['name']
        if name not in self.sessions:
            return wrap_error("Session name does not exist")
    
        current_session = self.sessions[name]
        provided_access_key = message['payload']['session']['access_key']
        if provided_access_key == current_session['access_keys']['white']:
            player_color = "white"
        elif provided_access_key == current_session['access_keys']['black']:
            player_color = "black"
        else:
            return wrap_error("Provided access key is invalid")

        # GAME MANAGEMENT
        if msg_type == GET_GAME_STATE:
            return wrap(GET_GAME_STATE, current_session['session'].get_game_state(player_color))
        elif msg_type == GET_MOVES:
            moves = current_session['session'].get_moves(player_color, message['payload']['piece_coords'])
            if not moves:
                return wrap_error("Not your turn")
            else:
                return wrap(GET_MOVES, moves)
        elif msg_type == MAKE_MOVE:
            if not current_session['session'].make_move(player_color, message['payload']['desired_move']):
                return wrap_error("Not your turn")
            else:
                return wrap(MAKE_MOVE, current_session['session'].get_game_state(player_color))
        else:
            return wrap_error("Undefined message type")


def main():
    game_server = GameServer()

    sel = selectors.DefaultSelector()

    def accept(sock, mask):
        conn, addr = sock.accept()  # Should be ready
        print('Accepted', conn, 'from', addr)
        conn.setblocking(False)
        sel.register(conn, selectors.EVENT_READ, read)

    def read(conn, mask):
        data = recv_msg2(conn)  # Should be ready
        if data:
            to_send = game_server.process(unwrap(data))
            send_msg2(conn, to_send)
        else:
            sel.unregister(conn)
            conn.close()

    sock = socket.socket()
    sock.bind((HOST, LISTENING_SOCKET_PORT))
    sock.listen(100)
    sock.setblocking(False)
    sel.register(sock, selectors.EVENT_READ, accept)

    try:
        while True:
            events = sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Shutting down.")


if __name__ == "__main__":
    main()

import json
import struct
from enum import Enum


class ProgressState(Enum):
    IN_PROGRESS = 1
    CHECK = 2
    CHECKMATE = 3
    DRAW_STALEMATE = 4
    DRAW_INSUFFICIENT_MATERIALS = 5
    DRAW_THREEFOLD_REPETITION = 6
    DRAW_FIFTY_MOVE_RULE = 7

    def readable(self):
        if self == ProgressState.IN_PROGRESS:
            return "INPROGRESS"
        elif self == ProgressState.CHECK:
            return "CHECK"
        elif self == ProgressState.CHECKMATE:
            return "CHECKMATE"
        elif self == ProgressState.DRAW_STALEMATE:
            return "DRAW (STALEMATE)"
        elif self == ProgressState.DRAW_INSUFFICIENT_MATERIALS:
            return "DRAW (INSUFFICIENT MATERIALS)"
        elif self == ProgressState.DRAW_THREEFOLD_REPETITION:
            return "DRAW (THREEFOLD REPETITION)"
        elif self == ProgressState.DRAW_FIFTY_MOVE_RULE:
            return "DRAW (FIFTY-MOVE RULE)"

    def to_serializable(self):
        if self == ProgressState.IN_PROGRESS:
            return {'state': "INPROGRESS", 'description': ""}
        elif self == ProgressState.CHECK:
            return {'state': "CHECK", 'description': ""}
        else:
            return {'state': "GAMEOVER", 'description': self.readable()}

# Session States
CREATE_SESSION = "CREATE_SESSION"
GET_SESSIONS = "GET_SESSIONS"
JOIN_SESSION = "JOIN_SESSION"
GET_GAME_STATE = "GET_GAME_STATE"
GET_MOVES = "GET_MOVES"
MAKE_MOVE = "MAKE_MOVE"
ERROR = "ERROR"


def send_msg(connection, data):
    length = len(data)
    connection.sendall(struct.pack('!I', length))
    connection.sendall(data)


def send_msg2(connection, data):
    length = len(data)
    connection.send(struct.pack('!I', length))
    connection.sendall(data)


def recv_msg2(connection):
    packed_length = connection.recv(4)
    if packed_length:
        length, = struct.unpack('!I', packed_length)
        connection.setblocking(True)
        received_data = connection.recv(length)
        connection.setblocking(False)
        return received_data
    else:
        return False


def recv_msg(connection):
    length = recvall(connection, 4)
    length, = struct.unpack('!I', length)
    return recvall(connection, length)


def recvall(connection, count):
    buffer = b''
    while count:
        new_buffer = connection.recv(count)
        if not new_buffer:
            return None
        buffer += new_buffer
        count -= len(new_buffer)
    return buffer


def wrap_error(description):
    return wrap("ERROR", {'description': description})


def wrap(message_type, payload):
    return json.dumps({'message_type': message_type, "payload": payload}).encode('utf-8')


def unwrap(message):
    return json.loads(message.decode('utf-8'))


# Recall, internal board (unlike raw user input) is indexed 0 to 7, not 1 to 8.
def is_off_edge(i, j):
    if i > 7 or i < 0 or j > 7 or j < 0:
        return True
    return False


def is_off_edge_pos(pos):
    if pos[0] > 7 or pos[0] < 0 or pos[1] > 7 or pos[1] < 0:
        return True
    return False


def piece_at(board, row, column):  # Convenient notation
    return board[row][column]


def piece_at_pos(board, pos):
    return board[pos[0]][pos[1]]


def selected_piece(board, coords):  # Convenient notation
    return board[coords[0]][coords[1]]


def opposite_col(col):
    if col == "white":
        return "black"
    if col == "black":
        return "white"
    if col == "_":
        raise ValueError()
        # return None

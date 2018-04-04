from chess.move import Move, MoveType
from chess.utils import piece_at, selected_piece, is_off_edge, opposite_col


class Piece(object):
    def __init__(self, col, white_piece_unicode_codepoint, ascii_char):
        self.has_never_moved = True
        self.col = col
        self.is_blank_piece = False
        self.type = ascii_char
        if self.col == "white":
            self.enemy_col = "black"
            self.home_rank = 7
            self.enemy_home_rank = 0
            self.forward_dir = -1
            self.unicode_symbol = chr(int(white_piece_unicode_codepoint, 16)).encode('utf-8')
        elif self.col == "black":
            self.enemy_col = "white"
            self.forward_dir = +1
            self.home_rank = 0
            self.enemy_home_rank = 7
            self.unicode_symbol = chr(int(white_piece_unicode_codepoint, 16) + 6).encode('utf-8')

    def get_move_set(self, board, piece_location):
        return []

    # Useful method for checkmate detection
    def get_attack_set(self, board, piece_location):
        return []


class BlankPiece(Piece):
    def __init__(self):
        super(BlankPiece, self).__init__("", '0123', "_")
        self.is_blank_piece = True


class Pawn(Piece):
    def __init__(self, col):
        super(Pawn, self).__init__(col, '2659', "p")
        # Pawn's relative column offset to get north east and north west (from white's perspective)
        self.column_attack_offset = [-1, 1]

    def get_move_set(self, board, piece_location):
        move_set = []
        i = piece_location[0] + self.forward_dir
        j = piece_location[1]
        # Is space directly forward from us free?
        if not is_off_edge(i, j) and piece_at(board, i, j).is_blank_piece:
            move_set.append(Move(MoveType.NORMAL, piece_location, [i, j]))

            i = piece_location[0] + self.forward_dir * 2
            j = piece_location[1]
            # If we haven't moved, is the space TWO forward from us free?
            if self.is_on_pawn_home_row(piece_location) and piece_at(board, i, j).is_blank_piece:
                # Append pawn jump move
                move_set.append(Move(MoveType.NORMAL, piece_location, [i, j]))
        return move_set

    def get_attack_set(self, board, piece_location):
        attack_set = []

        for col_offset in self.column_attack_offset:
            i = piece_location[0] + self.forward_dir
            j = piece_location[1] + col_offset
            if not is_off_edge(i, j) and (piece_at(board, i, j).col == self.enemy_col):
                attack_set.append(Move(MoveType.NORMAL, piece_location, [i, j]))
        return attack_set

    def is_on_pawn_home_row(self, piece_location):
        current_col_pawn_staring_rank = self.home_rank + self.forward_dir
        return piece_location[0] == current_col_pawn_staring_rank


class SlidingPiece(Piece):
    def __init__(self, col, list_of_unit_moves, white_piece_unicode_codepoint, ascii_char):
        super(SlidingPiece, self).__init__(col, white_piece_unicode_codepoint, ascii_char)
        self.vector_dir = list_of_unit_moves

    def get_attack_set(self, board, piece_location):
        attack_set = []
        for vector in self.vector_dir:
            i = piece_location[0] + vector[0]
            j = piece_location[1] + vector[1]
            # Slide until first enemy
            hit_enemy_this_dir = False
            while not is_off_edge(i, j) and piece_at(board, i, j).col != self.col and not hit_enemy_this_dir:
                attack_set.append(Move(MoveType.NORMAL, piece_location, [i, j]))
                if piece_at(board, i, j).col == opposite_col(self.col):
                    # Stop sliding this dir if hit enemy.
                    hit_enemy_this_dir = True
                i += vector[0]
                j += vector[1]
        return attack_set


class TeleportingPiece(Piece):
    def __init__(self, col, list_of_teleport_offsets, white_piece_unicode_codepoint, ascii_char):
        super(TeleportingPiece, self).__init__(col, white_piece_unicode_codepoint, ascii_char)
        self.teleport_offsets = list_of_teleport_offsets

    def get_attack_set(self, board, piece_location):
        attack_set = []
        for offset in self.teleport_offsets:
            i = piece_location[0] + offset[0]
            j = piece_location[1] + offset[1]
            if not is_off_edge(i, j) and piece_at(board, i, j).col != self.col:
                attack_set.append(Move(MoveType.NORMAL, piece_location, [i, j]))
        return attack_set


class Rook(SlidingPiece):
    def __init__(self, col):
        self.vector_dir = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        super(Rook, self).__init__(col, self.vector_dir,  '2656', "r")


class Bishop(SlidingPiece):
    def __init__(self, col):
        self.vector_dir = [[-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(Bishop, self).__init__(col, self.vector_dir,  '2657', "b")


class Queen(SlidingPiece):
    def __init__(self, col):  # Both rook AND bishop's movesets
        self.vector_dir = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(Queen, self).__init__(col, self.vector_dir,  '2655', "q")


class King(TeleportingPiece):
    KING_HOME_COL = 4

    def __init__(self, col):  # same as queen in vectorset, but parent class makes moveset smaller
        self.teleport_offsets = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(King, self).__init__(col, self.teleport_offsets, '2654', "k")

    def get_move_set(self, board, piece_location):
        return self.get_castling_set(board, piece_location)

    def get_castling_set(self, board, piece_location):
        castling_set = []
        if self.has_never_moved:
            if King.can_castle_on_col_a_rook(board, self.home_rank):
                castling_set.append(Move(MoveType.CASTLING, piece_location,
                                         [self.home_rank, 1]))

            if King.can_castle_on_col_h_rook(board, self.home_rank):
                castling_set.append(Move(MoveType.CASTLING, piece_location,
                                         [self.home_rank, 6]))

        return castling_set

    @staticmethod
    def can_castle_on_col_a_rook(board, home_rank):
        # Check the three positions to the rook in column A
        a_col_piece = selected_piece(board, [home_rank, 0])
        return (selected_piece(board, [home_rank, 3]).is_blank_piece
                and selected_piece(board, [home_rank, 2]).is_blank_piece
                and selected_piece(board, [home_rank, 1]).is_blank_piece
                and a_col_piece.type == "r" and a_col_piece.has_never_moved)

    @staticmethod
    def can_castle_on_col_h_rook(board, home_rank):
        # Check the three positions to the rook in column H
        h_col_piece = selected_piece(board, [home_rank, 7])
        return (selected_piece(board, [home_rank, 5]).is_blank_piece
                and selected_piece(board, [home_rank, 6]).is_blank_piece
                and h_col_piece.type == "r" and h_col_piece.has_never_moved)


class Knight(TeleportingPiece):
    def __init__(self, col):
        self.teleport_offsets = [[-2, -1], [-2, 1], [1, 2], [-1, 2], [2, -1], [2, 1], [-1, -2], [1, -2]]
        # h for 'horse', as king is taken 'k'
        super(Knight, self).__init__(col, self.teleport_offsets, '2658', "h")

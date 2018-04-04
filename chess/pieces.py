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
        # Is space directly forward from us free?
        if (piece_at(board, piece_location[0] + self.forward_dir,
                     piece_location[1]).is_blank_piece):
            move_set.append(Move(MoveType.NORMAL, piece_location, [piece_location[0] + self.forward_dir,
                                                                   piece_location[1]]))
            # If we haven't moved, is the space TWO forward from us free?
            if self.has_never_moved and piece_at(board, piece_location[0] + self.forward_dir * 2,
                                                 piece_location[1]).is_blank_piece:
                # Append pawn jump move
                move_set.append(Move(MoveType.NORMAL, piece_location, [piece_location[0] + self.forward_dir * 2,
                                                                       piece_location[1]]))
        self.has_never_moved = False
        return move_set

    def get_attack_set(self, board, piece_location):
        attack_set = []

        for col_offset in self.column_attack_offset:
            i = piece_location[0] + self.forward_dir
            j = piece_location[1] + col_offset
            if not is_off_edge(i, j) and (piece_at(board, i, j).col == self.enemy_col):
                attack_set.append(Move(MoveType.NORMAL, piece_location, [i, j]))
        return attack_set


class AdvancedPiece(Piece):
    def __init__(self, col, list_of_unit_moves, movement_style, white_piece_unicode_codepoint, ascii_char):
        super(AdvancedPiece, self).__init__(col, white_piece_unicode_codepoint, ascii_char)
        self.vector_dir = list_of_unit_moves
        # movement_style either "slider" (ie rook,bishop,queen)
        # or "teleporter" (king,knight) with respect to move vectors
        self.movement_style = movement_style

    def get_attack_set(self, board, piece_location):
        attack_set = []
        for vector in self.vector_dir:
            i = piece_location[0] + vector[0]
            j = piece_location[1] + vector[1]
            # print 'Checking vector',
            # print vector
            if self.movement_style == "slider":
                hit_enemy_this_dir = False  # Slide until first enemy
                while not is_off_edge(i, j) and piece_at(board, i, j).col != self.col and not hit_enemy_this_dir:
                    # print 'Adding: ' + str(i) + "," + str(j)
                    attack_set.append(Move(MoveType.NORMAL, piece_location, [i, j]))
                    if piece_at(board, i, j).col == opposite_col(self.col):
                        hit_enemy_this_dir = True  # stop sliding this dir if hit enemy
                    i += vector[0]
                    j += vector[1]

            elif self.movement_style == "teleporter":
                if not is_off_edge(i, j) and piece_at(board, i, j).col != self.col:
                    # print 'Adding: ' + str(i) + "," + str(j)
                    attack_set.append(Move(MoveType.NORMAL, piece_location, [i, j]))

        return attack_set


class Rook(AdvancedPiece):
    def __init__(self, col):
        self.vector_dir = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        super(Rook, self).__init__(col, self.vector_dir, "slider", '2656', "r")


class Bishop(AdvancedPiece):
    def __init__(self, col):
        self.vector_dir = [[-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(Bishop, self).__init__(col, self.vector_dir, "slider", '2657', "b")


class Queen(AdvancedPiece):
    def __init__(self, col):  # Both rook AND bishop's movesets
        self.vector_dir = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(Queen, self).__init__(col, self.vector_dir, "slider", '2655', "q")


class King(AdvancedPiece):
    def __init__(self, col):  # same as queen in vectorset, but parent class makes moveset smaller
        self.vector_dir = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(King, self).__init__(col, self.vector_dir, "teleporter", '2654', "k")
        if col == "white":
            self.leftwards_col_index_increment = -1
            self.rightwards_col_index_increment = 1
        else:
            self.leftwards_col_index_increment = 1
            self.rightwards_col_index_increment = -1

    def _get_castling_positions(self):
        self.castlingPositions = [[self.home_rank, "1"], [self.home_rank, "6"]]

    # Override teleporter to get castling
    def get_attack_set(self, board, piece_location):
        attack_set = super(King, self).get_attack_set(board, piece_location)
        attack_set += self.get_castling_set(board, piece_location)
        return attack_set

    def get_castling_set(self, board, piece_location):
        castling_set = []
        if self.has_never_moved:
            # Ensure the positions to the left of king are empty
            if selected_piece(board,
                              [self.home_rank, piece_location[1] + self.leftwards_col_index_increment * 1]).is_blank_piece \
                    and selected_piece(board, [self.home_rank,
                                               piece_location[1] + self.leftwards_col_index_increment * 2]).is_blank_piece:
                # And the left rook has never moved
                left_rook = selected_piece(board,
                                           [self.home_rank, piece_location[1] + self.leftwards_col_index_increment * 3])
                if left_rook.type == "r" and left_rook.has_never_moved:
                    castling_set.append(Move(MoveType.CASTLING, piece_location,
                                             [self.home_rank, piece_location[1] + self.leftwards_col_index_increment * 2]))
            # Ensure the positions to the right of king are empty
            if selected_piece(board,
                              [self.home_rank, piece_location[1] + self.rightwards_col_index_increment * 1]).is_blank_piece \
                    and selected_piece(board, [self.home_rank,
                                               piece_location[1] + self.rightwards_col_index_increment * 2]).is_blank_piece \
                    and selected_piece(board, [self.home_rank, piece_location[
                                                                   1] + self.rightwards_col_index_increment * 3]).is_blank_piece:
                # And the right rook has never moved
                right_rook = selected_piece(board,
                                            [self.home_rank, piece_location[1] + self.rightwards_col_index_increment * 4])
                if right_rook.type == "r" and right_rook.has_never_moved:
                    castling_set.append(Move(MoveType.CASTLING, piece_location, [self.home_rank, piece_location[
                        1] + self.rightwards_col_index_increment * 3]))
        return castling_set


class Knight(AdvancedPiece):
    def __init__(self, col):  # similar vector set/moveset relationship as king (see parent class)
        self.vector_dir = [[-2, -1], [-2, 1], [1, 2], [-1, 2], [2, -1], [2, 1], [-1, -2], [1, -2]]
        # h for 'horse', as king is taken 'k'
        super(Knight, self).__init__(col, self.vector_dir, "teleporter", '2658', "h")

from enum import Enum


class MoveType(Enum):
    NORMAL = 1
    CASTLING = 2
    EN_PASSANT = 3
    PROMOTION = 4


class Move(object):
    def __init__(self, move_type, start_coords, end_coords):
        self.move_type = move_type
        self.start_coords = start_coords
        self.end_coords = end_coords
        self.promotion_piece = False

    @classmethod
    def en_passant(cls, start_coords, end_coords, promote_to):
        cls.move_type = MoveType.EN_PASSANT
        cls.start_coords = start_coords
        cls.end_coords = end_coords
        cls.promotion_piece = promote_to

    def __repr__(self):
        str_repr = "" + str(self.move_type) + " " + str(self.start_coords) + " " + str(self.end_coords)
        if self.move_type == MoveType.PROMOTION:
            str_repr += " " + str(self.promotion_piece)
        return str_repr

    def __eq__(self, obj):
        return (self.move_type == obj.move_type) and (self.start_coords == obj.start_coords) \
               and (self.end_coords == obj.end_coords) and (self.promotion_piece == obj.promotion_piece)


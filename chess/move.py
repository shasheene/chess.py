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
    def en_passant(cls, start_coords, end_coords):
        move = cls(MoveType.EN_PASSANT, start_coords, end_coords)
        return move

    @classmethod
    def pawn_promotion(cls, start_coords, end_coords, promote_choice):
        move = cls(MoveType.PROMOTION, start_coords, end_coords)
        move.promotion_piece = promote_choice
        return move

    # Cannot serialize enum as JSON, so for clients usage, manually convert it to dict
    # TODO: Replace with a cleaner mechanism.
    def convert_to_dict(self):
        return {'move_type': self.move_type.name,
                'start_coords': self.start_coords,
                'end_coords': self.end_coords,
                'promotion_piece': self.promotion_piece}

    @classmethod
    def create_from_dict(cls, dict):
        move_type = MoveType.__dict__[dict['move_type']]
        if dict['move_type'] == MoveType.EN_PASSANT.name:
            return Move.en_passant(dict['start_coords'], dict['end_coords'])
        elif dict['move_type'] == MoveType.PROMOTION.name:
            # TODO: Fix this
            return Move.pawn_promotion(dict['start_coords'], dict['end_coords'], dict['promotion_piece'])
        else:
            return Move(move_type, dict['start_coords'], dict['end_coords'])

    def __repr__(self):
        str_repr = str(self.move_type) + " " + str(self.start_coords) + " " + str(self.end_coords)
        if self.move_type == MoveType.PROMOTION:
            str_repr += " " + str(self.promotion_piece)
        return str_repr

    def __eq__(self, obj):
        return (self.move_type == obj.move_type) and (self.start_coords == obj.start_coords) \
               and (self.end_coords == obj.end_coords) and (self.promotion_piece == obj.promotion_piece)

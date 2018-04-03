from enum import Enum


class MoveType(Enum):
    NORMAL = 1
    CASTLING = 2
    EN_PASSANT = 3
    PROMOTION = 4


class Move(object):
    def __init__(self, moveType, startCoords, endCoords):
        self.moveType = moveType
        self.startCoords = startCoords
        self.endCoords = endCoords
        self.promotionPiece = False

    @classmethod
    def en_passant(self, startCoords, endCoords, promoteTo):
        self.moveType = MoveType.EN_PASSANT
        self.startCoords = startCoords
        self.endCoords = endCoords
        self.promotionPiece = promoteTo

    def __repr__(self):
        strRepr = "" + str(self.moveType) + " " + str(self.startCoords) + " " + str(self.endCoords)
        if self.moveType == MoveType.PROMOTION:
            strRepr += " " + str(self.promoteTo)
        return strRepr

    def __eq__(self, obj):
        return (self.moveType == obj.moveType) and (self.startCoords == obj.startCoords)\
               and (self.endCoords == obj.endCoords) and (self.promotionPiece == obj.promotionPiece)


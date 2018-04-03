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

    def __init__(self, startCoords, endCoords, promoteTo):
        self.moveType = MoveType.EN_PASSANT
        self.startCoords = startCoords
        self.endCoords = endCoords
        self.promotionPiece = promoteTo

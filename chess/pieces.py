from chess.utils import pieceAt, selectedPiece, isOffEdge, oppositeCol


class Piece(object):
    def __init__(self, col, whitePieceUnicodeCodepoint):
        self.hasNeverMoved = True
        self.col = col
        self.type = "_"
        if self.col == "white":
            self.enemyCol = "black"
            self.homeRank = 7
            self.enemyHomeRank = 0
            self.forwardDir = -1
            self.unicodeSymbol = chr(int(whitePieceUnicodeCodepoint, 16)).encode('utf-8')
        elif self.col == "black":
            self.enemyCol = "white"
            self.forwardDir = +1
            self.homeRank = 0
            self.enemyHomeRank = 7
            self.unicodeSymbol = chr(int(whitePieceUnicodeCodepoint, 16) + 6).encode('utf-8')

    def getMoveSet(self, board, pieceLocation):
        return []

    # Useful method for checkmate detection
    def getAttackSet(self, board, pieceLocation):
        return []


class Pawn(Piece):
    def __init__(self, col):
        super(Pawn, self).__init__(col, '2659')
        self.attackSet = []
        self.moveSet = []
        self.type = "p"
        # Pawn's relative column offset to get north east and north west (from white's perspective)
        self.columnAttackOffset = [-1, 1]

    def getMoveSet(self, board, pieceLocation):
        self.moveSet = []
        # Is space directly forward from us free?
        if (pieceAt(board, pieceLocation[0] + self.forwardDir,
                    pieceLocation[1]).type == "_"):
            self.moveSet.append([pieceLocation[0] + self.forwardDir, pieceLocation[1]])
            # If we haven't moved, is the space TWO forward from us free?
            if self.hasNeverMoved and (pieceAt(board, pieceLocation[0] + self.forwardDir * 2, pieceLocation[1]).type == "_"):
                # Append pawn jump move
                self.moveSet.append([pieceLocation[0] + self.forwardDir * 2, pieceLocation[1]])
        self.hasNeverMoved = False
        return self.moveSet

    def getAttackSet(self, board, pieceLocation):
        self.attackSet = []

        for colOffset in self.columnAttackOffset:
            self.i = pieceLocation[0] + self.forwardDir
            self.j = pieceLocation[1] + colOffset
            if not isOffEdge(self.i, self.j) and (pieceAt(board, self.i, self.j).col == self.enemyCol):
                self.attackSet.append([self.i, self.j])
        return self.attackSet


class AdvancedPiece(Piece):
    def __init__(self, col, listOfUnitMoves, movementStyle, whitePieceUnicodeCodepoint):
        super(AdvancedPiece, self).__init__(col, whitePieceUnicodeCodepoint)
        self.myVectorSet = listOfUnitMoves
        # movementStyle either "slider" (ie rook,bishop,queen) or "teleporter" (king,knight) with respect to moveVectors
        self.movementStyle = movementStyle

    def getAttackSet(self, board, pieceLocation):
        self.attackSet = []
        for vector in self.myVectorSet:
            self.i = pieceLocation[0] + vector[0]
            self.j = pieceLocation[1] + vector[1]
            # print 'Checking vector',
            # print vector
            if self.movementStyle == "slider":
                hitEnemyThisDir = False  # Slide until first enemy
                while (not isOffEdge(self.i, self.j) and pieceAt(board, self.i,
                                                                  self.j).col != self.col and hitEnemyThisDir == False):
                    # print 'Adding: ' + str(self.i) + "," + str(self.j)
                    self.attackSet.append([self.i, self.j])
                    if (pieceAt(board, self.i, self.j).col == oppositeCol(self.col)):
                        hitEnemyThisDir = True  # stop sliding this dir if hit enemy
                    self.i += vector[0]
                    self.j += vector[1]

            elif self.movementStyle == "teleporter":
                if (not isOffEdge(self.i, self.j) and pieceAt(board, self.i, self.j).col != self.col):
                    # print 'Adding: ' + str(self.i) + "," + str(self.j)
                    self.attackSet.append([self.i, self.j])

        self.hasNeverMoved = True
        return self.attackSet


class Rook(AdvancedPiece):
    def __init__(self, col):
        self.myVectorSet = [[-1, 0], [1, 0], [0, -1], [0, 1]]
        super(Rook, self).__init__(col, self.myVectorSet, "slider", '2656')
        self.type = "r"


class Bishop(AdvancedPiece):
    def __init__(self, col):
        self.myVectorSet = [[-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(Bishop, self).__init__(col, self.myVectorSet, "slider", '2657')
        self.type = "b"


class Queen(AdvancedPiece):
    def __init__(self, col):  # Both rook AND bishop's movesets
        self.myVectorSet = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(Queen, self).__init__(col, self.myVectorSet, "slider", '2655')
        self.type = "q"


class King(AdvancedPiece):
    def __init__(self, col):  # same as queen in vectorset, but parent class makes moveset smaller
        self.myVectorSet = [[-1, 0], [1, 0], [0, -1], [0, 1], [-1, -1], [-1, +1], [+1, -1], [1, 1]]
        super(King, self).__init__(col, self.myVectorSet, "teleporter", '2654')
        self.type = "k"
        if col == "white":
            self.leftwardsColIndexIncrement = -1
            self.rightwardsColIndexIncrement = 1
        else:
            self.leftwardsColIndexIncrement = 1
            self.rightwardsColIndexIncrement = -1

    def _getCastlingPositions(self):
        self.castlingPositions = [[self.homeRank, "1"], [self.homeRank, "6"]]

    # Override teleporter to get castling
    def getAttackSet(self, board, pieceLocation):
        self.attackSet=super(King,self).getAttackSet(board, pieceLocation)
        self.attackSet += self.getCastlingSet(board, pieceLocation)
        return self.attackSet

    def getCastlingSet(self, board, pieceLocation):
        castlingSet = []
        if self.hasNeverMoved:
            # Ensure the positions to the left of king are empty
            if selectedPiece(board, [self.homeRank, pieceLocation[1] + self.leftwardsColIndexIncrement * 1]).type == "_" \
                    and selectedPiece(board, [self.homeRank, pieceLocation[1] + self.leftwardsColIndexIncrement * 2]).type == "_":
                # And the left rook has never moved
                leftRook = selectedPiece(board, [self.homeRank, pieceLocation[1] + self.leftwardsColIndexIncrement * 3])
                if leftRook.type=="r" and leftRook.hasNeverMoved:
                    castlingSet.append([self.homeRank, pieceLocation[1] + self.leftwardsColIndexIncrement * 2])
            # Ensure the positions to the right of king are empty
            if selectedPiece(board, [self.homeRank, pieceLocation[1] + self.rightwardsColIndexIncrement * 1]).type == "_" \
                    and selectedPiece(board, [self.homeRank, pieceLocation[1] + self.rightwardsColIndexIncrement * 2]).type == "_" \
                    and selectedPiece(board, [self.homeRank, pieceLocation[1] + self.rightwardsColIndexIncrement * 3]).type == "_":
                # And the right rook has never moved
                rightRook = selectedPiece(board, [self.homeRank, pieceLocation[1] + self.rightwardsColIndexIncrement * 4])
                if rightRook.type=="r" and rightRook.hasNeverMoved:
                    castlingSet.append([self.homeRank,  pieceLocation[1] + self.rightwardsColIndexIncrement * 3])
        return castlingSet


class Knight(AdvancedPiece):
    def __init__(self, col):  # similar vector set/moveset relationship as king (see parent class)
        self.myVectorSet = [[-2, -1], [-2, 1], [1, 2], [-1, 2], [2, -1], [2, 1], [-1, -2], [1, -2]]
        super(Knight, self).__init__(col, self.myVectorSet, "teleporter", '2658')
        self.type = "h"  # h for 'horse', as king is taken 'k'
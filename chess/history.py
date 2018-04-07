class MoveHistoryElement:
    """
    The 50-move rule [1] checks if within the last 50 moves, a capture has been made or a pawn has been moved.
    This requires history of the game to check its validity.

    Additionally, the Pawn's en passant [2] move needs to know the prior move to be able to determine validity.

    [1] https://en.wikipedia.org/wiki/Fifty-move_rule
    [2] https://en.wikipedia.org/wiki/En_passant
    """
    def __init__(self, move, piece_moved, capture_piece):
        self.move = move
        self.capture_piece = capture_piece
        self.piece = piece_moved

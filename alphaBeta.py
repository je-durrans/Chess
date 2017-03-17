__author__ = 'John'
from math import copysign


def abGetMoveValue(self, board, color="W", depth=2, alpha=-1e10, beta=1e10, function=max):

    if board.draw:
        return 0
    if depth == 0:
        return self.evaluation.evaluate(board)
    if board.countKings() != 2:
        return copysign(1e7,
                        self.evaluation.evaluate(board,
                                                 color if function == max else
                                                 "W" if color == "B" else "B"
                                                 )
                        )

    nextMoveColor = "W" if color == "B" else "B"
    validMoves = self.enumerateMoves(board, color)
    oppositeFunction = min if function == max else max

    v = oppositeFunction([-1e10, 1-10])
    if function == max:
        for move in validMoves:
            b = board.clone()
            b.move(move[0], move[1], skipValidation=True)
            v = function(v, abGetMoveValue(b, nextMoveColor, depth-1, v, beta, oppositeFunction))
            alpha = max(alpha, v)
            if beta <= alpha:
                break
    else:
        for move in validMoves:
            b = board.clone()
            b.move(move[0], move[1], skipValidation=True)
            v = function(v, abGetMoveValue(b, nextMoveColor, depth-1, alpha, v, oppositeFunction))
            beta = min(beta, v)
            if beta <= alpha:
                break
    return v

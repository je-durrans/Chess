__author__ = 'John'

import math


class Piece:

    def __init__(self, color="W", piece="P"):
        self.color = color
        self.piece = piece
        if piece in ("K", "R"):
            self.moved = False
        self.list = [self.color, self.piece]

    def __str__(self):
        return self.color + self.piece

    def __getitem__(self, index):
        return self.list[index]

    def opCol(self):
        return "B" if self.color == "W" else "W"

    def validateMove(self, x1y1, x2y2, board):  # x refers to rank and y to file ??
        x1, y1 = x1y1
        x2, y2 = x2y2
        dx = x2-x1
        dy = y2-y1
        if dx == 0 and dy == 0:
            return False
        # for i, j in zip()
        if self.piece == "P":
            if self.color == "W" and dy == 0:
                return board[y2][x2].piece is None and \
                       (dx == 1 or dx == 2 and x1 == 1 and board[y2][2].piece is None)
            elif self.color == "B" and dy == 0:
                return board[y2][x2].piece is None and \
                       (dx == -1 or dx == -2 and x1 == 6 and board[y2][5].piece is None)
            elif self.color == "W" and dy**2 == 1:
                return dx == 1 and board[y2][x2].piece is not None and board[y2][x2].piece[0] == "B"  # &ep
            elif self.color == "B" and dy**2 == 1:
                return dx == -1 and board[y2][x2].piece is not None and board[y2][x2].piece[0] == "W"  # &ep
        elif self.piece == "N":
            return dx**2 + dy**2 == 5 and (board[y2][x2].piece is None or board[y2][x2].piece[0] == self.opCol())
        elif self.piece == "K":
            return dx**2 + dy**2 < 3 and (board[y2][x2].piece is None or board[y2][x2].piece[0] == self.opCol())
        elif self.piece == "R":
            lx = list(range(x1, x2, int(math.copysign(1, dx))))[1:]
            ly = list(range(y1, y2, int(math.copysign(1, dy))))[1:]
            b = dx == 0 and dy != 0 or dx != 0 and dy == 0
            if lx:
                b = b and all(board[y1][x].piece is None for x in lx)
            elif ly:
                b = b and all(board[y][x1].piece is None for y in ly)
            b = b and (board[y2][x2].piece is None or board[y2][x2].piece[0] == self.opCol())
            return b
        elif self.piece == "B":
            lx = list(range(x1, x2, int(math.copysign(1, dx))))[1:]
            ly = list(range(y1, y2, int(math.copysign(1, dy))))[1:]
            if lx and ly:
                b = all(board[y][x].piece is None for x, y in zip(lx, ly))
                b = b and (board[y2][x2].piece is None or board[y2][x2].piece[0] == self.opCol())
                return b and dx**2 == dy**2
            else:
                b = board[y2][x2].piece is None or board[y2][x2].piece[0] == self.opCol()
                return b and dx**2 == dy**2
        elif self.piece == "Q":
            if not (dx == 0 and dy != 0 or dx != 0 and dy == 0 or dx**2 == dy**2):
                return False
            lx = list(range(x1, x2, int(math.copysign(1, dx))))[1:]
            ly = list(range(y1, y2, int(math.copysign(1, dy))))[1:]
            b = True
            if lx and ly:
                b = all(board[y][x].piece is None for x, y in zip(lx, ly))
                b = b and (board[y2][x2].piece is None or board[y2][x2].piece[0] == self.opCol())
                return b and dx**2 == dy**2
            if lx:
                b = (dx == 0 and dy != 0 or dx != 0 and dy == 0) and all(board[y1][x].piece is None for x in lx)
            elif ly:
                b = (dx == 0 and dy != 0 or dx != 0 and dy == 0) and all(board[y][x1].piece is None for y in ly)
            b = b and (board[y2][x2].piece is None or board[y2][x2].piece[0] == self.opCol())
            return b

        return False


class Pawn(Piece):

    def __init__(self, color="W"):
        super().__init__(color, "P")


class Rook(Piece):

    def __init__(self, color="W"):
        super().__init__(color, "R")


class Knight(Piece):

    def __init__(self, color="W"):
        super().__init__(color, "N")


class Bishop(Piece):

    def __init__(self, color="W"):
        super().__init__(color, "B")


class Queen(Piece):

    def __init__(self, color="W"):
        super().__init__(color, "Q")


class King(Piece):

    def __init__(self, color="W"):
        super().__init__(color, "K")

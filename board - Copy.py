__author__ = 'John'

from piece import *
from copy import deepcopy

class Board:

    def __init__(self, name=""):
        self.board = tuple(tuple((Square() for i in range(8))) for j in range(8))
        self.positions = {}
        self.draw = False
        self.mainInstance = False
        self.name = name

    def __str__(self):
        resp = ""
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                resp += self.board[j][i].string or "--"
            resp = resp + ","
        resp = resp.replace("None", "--")
        return resp

    def clone(self):
        b = Board()
        b.setup(self.copy())
        b.positions = self.positions.copy()#dict((k,v) for k,v in self.positions.items())
        return b

    def copy(self):
        resp = []
        for j in range(len(self.board)):
            resp.append([])
            for i in range(len(self.board[j])):
                resp[j].append(self.board[j][i].getPiece())
        return resp

    def countPieces(self):
        count = 0
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[j][i].getPiece() is not None:
                    count += 1
        return count

    def countKings(self):
        count = 0
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[j][i].getPiece() is not None and self.board[j][i].getPiece()[1] == "K":
                    count += 1
        return count

    def countPiecesColor(self):
        w = b = 0
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[j][i].getPiece() is not None:
                    if self.board[j][i].getPiece()[0] == "W":
                        w += 1
                    else:
                        b += 1
        return w, b

    def getKingColor(self):
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                if self.board[j][i].getPiece() is not None and self.board[j][i].getPiece()[1] == "K":
                    return self.board[j][i].getPiece()[0]

    def setup(self, board=list()):

        if board:
            for file in range(len(board)):
                for rank in range(len(board[file])):
                    piece = board[file][rank]
                    if piece:
                        self.board[file][rank].setPiece(Piece(piece[0], piece[1]))
        else:
            for color in ("W", "B"):
                rank = 1 if color == "W" else 6
                for file in range(8):
                    self.board[file][rank].setPiece(Pawn(color))

                rank = 0 if color == "W" else 7
                for file in (0, 7):
                    self.board[file][rank].setPiece(Rook(color))
                for file in (1, 6):
                    self.board[file][rank].setPiece(Knight(color))
                for file in 2, 5:
                    self.board[file][rank].setPiece(Bishop(color))
                self.board[3][rank].setPiece(Queen(color))
                self.board[4][rank].setPiece(King(color))
        self.updatePositions(turn="B")
        return self

    def updatePositions(self, turn):
        turn = "White" if turn == "B" else "Black"
        pos = turn+str(self)
        if pos in self.positions:
            self.positions[pos] += 1
        else:
            self.positions[pos] = 1
        #if self.mainInstance:
        #    print("updating")
        if max(self.positions.values()) > 2:
            self.draw = True
            boardConfig = max(self.positions, key=self.positions.get)
            if self.name != "":
                print("Repeated position thrice with", boardConfig[:5], "to move:")
                for i in boardConfig[5:].split(","):
                    print(i)
        #    if self.mainInstance:
        #        print("setting draw")
        if self.countPieces() == 2:
            self.draw = True
            if self.name != "":
                print("Only Kings left")

    def move(self, square1, square2, turn="W", skipValidation=False):
        (rank1, file1) = square1
        piece = self.board[file1][rank1].piece
        if piece is None:
            return False
        if skipValidation or (piece.color == turn and piece.validateMove(square1, square2, self.board)):
            rank2, file2 = square2
            pieceTaken = self.board[file2][rank2].getPiece()
            self.board[file2][rank2].setPiece(self.board[file1][rank1].getPiece())
            self.board[file1][rank1].setPiece(None)
            if piece.piece == "P" and rank2 in (0, 7):
                self.board[file2][rank2].setPiece(Piece(piece.color, "Q"))
            if piece.piece == "P" or pieceTaken is not None:
                self.positions = {}
            self.updatePositions(turn)
            return True
        return False


class Square:
    string = ""

    def __init__(self):
        self.piece = None

    def setPiece(self, piece):
        self.piece = piece
        self.string = str(piece) or ""

    def getPiece(self):
        return self.piece

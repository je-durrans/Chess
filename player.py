__author__ = 'John'

from random import *
from evaluation import *
from gameTree import *
from math import copysign


class Player:

    sigma = 50

    def __init__(self, color="W", values=list(), depth=4):
        self.color = color
        self.evaluation = Evaluation(values)
        self.gameTree = None
        self.maxdepth = depth

    def createOffspring(self, player=None):
        if player is not None:
            split = randrange(373)
            return Player(values=self.evaluation.values[:split]+player.evaluation.values[split:], depth=self.maxdepth).mutate()
        return Player(values=self.evaluation.values, depth=self.maxdepth).mutate()

    def randomise(self):
        array = []
        for i in range(373):
            array.append(randint(0, 1000))
        self.evaluation = Evaluation(array)
        return self

    def mutate(self):
        values = [0] * 373
        for index in range(len(self.evaluation.values)):
            prob = randrange(10)
            if prob >= 3:
                values[index] = round(gauss(self.evaluation.values[index], Player.sigma))
                values[index] = max(values[index], 0)
                values[index] = min(values[index], 1000)
        self.evaluation = Evaluation(values)
        return self

    def makeMove(self, board):

        #pieceCount = board.countPieces()
        #self.maxdepth = 4 if pieceCount <= 12 else 3# if pieceCount <= 12 else 2

        #moveCount = len(self.enumerateMoves(board))
        #depth = 2  # 4 if moveCount <= 15 else 3 if moveCount <= 35 else 2

        wpc, bpc = board.countPiecesColor()
        if self.maxdepth <= 2:
            if wpc <= 5 or bpc <= 5:
                self.maxdepth += 1
        #if wpc + bpc <= 10 and self.maxdepth <=3:
        #    self.maxdepth +=1
        if self.maxdepth <= 2:
            self.gameTree = self.generateGameTree(board, self.color, depth=self.maxdepth)
            self.gameTree.propagate()
            return max(self.gameTree, key=self.gameTree.get)
        else:
            move, value = self.negamax(board, self.color, depth=self.maxdepth, maximising=True)
        return move


        #move, value = self.abGetMoveValue(board, self.color, depth=1)
        #move, value = self.alpha_beta(board, self.color, depth=2, alpha=-10e10, beta=10e10, maximizingPlayer=False)


        #"""



    def opCol(self):
        return "B" if self.color == "W" else "W"

    def enumerateMoves(self, board, color=""):
        color = color or self.color

        validMoves = []

        for startfile in range(8):
            for startrank in range(8):
                if board.board[startfile][startrank].getPiece() and board.board[startfile][startrank].getPiece()[0] == color:
                    for endfile in range(8):
                        for endrank in range(8):
                            if board.board[startfile][startrank].getPiece().validateMove((startrank, startfile), (endrank, endfile), board.board):
                                validMoves.append(((startrank, startfile), (endrank, endfile)))

        return validMoves

    def generateGameTree(self, board, color="", depth=2):

        thisMoveColor = color or self.color
        nextMoveColor = "W" if thisMoveColor == "B" else "B"
        validMoves = self.enumerateMoves(board, thisMoveColor)
        gameTree = GameTree()

        for move in validMoves:
            b = board.clone()
            b.move(move[0], move[1], turn=color, skipValidation=True)
            if b.draw:
                gameTree[move] = 0
            elif depth > 1 and b.countKings() == 2:
                gameTree[move] = self.generateGameTree(b, nextMoveColor, depth-1)
            elif b.countKings() != 2:
                # times depth to capture asap
                gameTree[move] = depth * int(copysign(10000000, self.evaluation.evaluate(b, self.color)))
            else:
                gameTree[move] = self.evaluation.evaluate(b, self.color)

        return gameTree

    def negamax(self, board, moveColor, depth=2, alpha=-10e10, beta=10e10, maximising=True):

        if board.draw:
            return None, 0
        if board.countKings() == 1:
            return None, -10000000 * (depth + 1)
        if depth == 0:
            return None, self.evaluation.evaluate(board, self.color) * maximising

        otherColor = "W" if moveColor == "B" else "B"

        bestValue = -10e10

        if depth > 2 and depth == self.maxdepth:
            tree = self.generateGameTree(board, depth=2)
            tree.propagate()
            validMoves = list(tree.keys())
            validMoves.sort(key=tree.get, reverse=True)
        else:
            validMoves = self.enumerateMoves(board, moveColor)

        for move in validMoves:
            b = board.clone()
            b.move(move[0], move[1], moveColor, skipValidation=True)
            v = -self.negamax(b, otherColor, depth-1, -beta, -alpha, -maximising)[1]
            bestValue = max(bestValue, v)
            if v == bestValue: bestMove = move
            alpha = max(alpha, v)
            if alpha > beta: break
        return bestMove, bestValue


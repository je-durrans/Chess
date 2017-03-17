__author__ = 'John'

from board import *


class GameTree(dict):

    """def evaluate(self, evaluation, board, color):

        for move in self.keys():
            b = board.clone()
            b.move(move[0], move[1], "", True)

            if self[move] is None:
                self[move] = evaluation.evaluate(b, color)
            elif type(self[move]) == GameTree:
                self[move].evaluate(evaluation, b, color)
            elif type(self[move]) != int:
                    print("ERROR!, self[move] is", self[move], "of type" + str(type(self[move])))
"""
    def propagate(self, minimax=max):
        for key, value in self.items():
            if type(value) == GameTree:
                function = max if minimax == min else min
                value.propagate(function)
                self[key] = function(self[key].values())#, key=lambda v: value[v])
        if all(type(value) == int for value in self.values()):
            ended = 1000000 if minimax == max else -1000000  # no pieces left
            try:
                self[key] = minimax(self.values())#, key=lambda x: value[x])
            except ValueError:      # only happens when one player has no pieces left
                self[key] = ended
        self = minimax(self.values())
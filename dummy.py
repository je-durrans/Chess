from random import *
from evaluation import Evaluation

#sigma = 12

class Game:

    def __init__(self, p1, p2, movelimit=0, display=False):
        self.p1 = p1
        self.p2 = p2

    def play(self):
        p1score = self.score(self.p1)#sum(self.p1.values)
        p2score = self.score(self.p2)#sum(self.p2.values)
        if p1score == p2score:
            return "D"
        if p1score > p2score:
            return "W"
        return "B"

    def score(self, player):
        total = 0
        for i in range(373):
            total += 1000 - abs(player.values[i] - i)
        return total

class Player:

    sigma = 2

    def __init__(self, values=list(), depth=0):
        self.values = []
        if values:
            for value in values:
                self.values.append(value)
        else:
            for i in range(373):
                self.values.append(randrange(0, 373))
        self.evaluation = Evaluation(self.values)

    def __str__(self):
        return "p"

    def randomise(self):
        return self

    def createOffspring(self, player2=None):
        if player2 is not None:
            split = randrange(373)
            p = Player(self.evaluation.values[:split]+player2.evaluation.values[split:])
        else:
            p = Player(self.values)
        p.mutate()
        return p

    def mutate(self):
        for index in range(len(self.values)):
            self.values[index] = round(gauss(self.values[index], Player.sigma))
            self.values[index] = max(self.values[index], 0)
            self.values[index] = min(self.values[index], 373)
"""
for i in range(5):
    g = Game(Player(), Player())
    print(g.play())

p = Player()
print(p.values)
print(p.createOffspring().values)
"""

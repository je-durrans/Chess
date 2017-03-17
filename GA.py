__author__ = 'John'

from random import *
"""
from game import *
from player import *
dummyProblem = False
"""
from dummy import *
dummyProblem = True
#"""

populationSize = 20  # even number
moveLimit = 100
numberOfRounds = 10000
numberOfMatchesPerRound = 2  # per player
searchDepth = 2  # starting search depth, is extended as number of pieces decreases, max 4
mutationParameter = 20  # standard deviation

def dummyScore(player):
    total = 0
    for i in range(373):
        #total += player.values[i]
        total += 373 - abs(player.values[i] - i)  # 139129 optimum
    return total

def instantiatePlayers(populationSize):
    players = []
    for i in range(populationSize):
        players.append([Player(depth=searchDepth).randomise().createOffspring(), 0])
    return players

def playRound():
    for playerNumber in range(populationSize):

        #for opponentNumber in range(populationSize):
        #    if opponentNumber == playerNumber: continue
        #

        for match in range(numberOfMatchesPerRound):
            opponentNumber = randrange(populationSize-1)
            if opponentNumber >= playerNumber:
                opponentNumber += 1

            outcome = Game(players[playerNumber][0], players[opponentNumber][0], display=False, movelimit=moveLimit).play()
            players[playerNumber][0].maxdepth = searchDepth
            players[opponentNumber][0].maxdepth = searchDepth
            print("Game Complete", outcome)
            if outcome == "W":
                players[playerNumber][1] += 1
                players[opponentNumber][1] -= 1
            elif outcome == "B":
                players[playerNumber][1] -= 1
                players[opponentNumber][1] += 1
    #for i in range(populationSize):
    #    print(players[i][1])
    print("End of round")
    return players

def playRoundx(roundNumber, players):
    if roundNumber == 0:
        start = 0
    else:
        start = populationSize//2
    for playerNumber in range(start, populationSize):
        players[playerNumber][1] = dummyScore(players[playerNumber][0])
    return players

if __name__ == "__main__":
    Player.sigma = mutationParameter

    #for test in range(100):
    agree = False
    players = instantiatePlayers(populationSize)
    for round in range(numberOfRounds):
        print("commencing round", round+1)
        if dummyProblem:
            Player.sigma = mutationParameter - round//500 + 1  # simulated annealing
            playRoundx(round, players)
        else:
            playRound()
        players = sorted(players, key=lambda x: -x[1])
        print("best score is:", players[0][1])
        #for player in players:
        #    print(player[1])
        # if all(players[0][0].evaluation.values == players[i][0].evaluation.values for i in range(1, populationSize//2)):
        #     print("Top 50% agree at", round+1, "rounds")
        #     agree = True
        #     break
        # print(players)
        # players = players[:int(populationSize/2)]
        # print(players[0][1])
        if round == numberOfRounds-1: break
        for index in range(populationSize // 2):
            # print(players[index][1], end=", ")
            players[index][1] = 0
            index2 = randrange(populationSize//2-1)
            if index2 >= index:
                index2 += 1
            players[index+populationSize//2] = [players[index][0].createOffspring(players[index2 % (populationSize//2)][0]), 0]

    if not agree:
        print("No consensus, optimum:")
    array = players[0][0].evaluation.values



    def pretty(d, depth=0):
        print("    "*(depth-1)+"{")
        for key in d.keys():
            print("    "*depth+str(key), end=": ")
            if type(d[key]) != dict:
                print(d[key])
            else:
                pretty(d[key], depth=depth+1)
        print("    "*(depth)+"}")

    eval = Evaluation(array)

    if dummyProblem:
        file = open("testdummy.txt", "w")
        print(pretty(eval))
    else:
        file = open("test.txt", "w")


    print(eval.values, file=file)
    file.close()
    print("\a")
    input()

__author__ = 'John'

from tkinter import *
from board import *
from time import *

images = {}

def createImageDict():
    global images
    images = {"WP": PhotoImage(file="image/WP.png"),
              "WR": PhotoImage(file="image/WR.png"),
              "WN": PhotoImage(file="image/WN.png"),
              "WB": PhotoImage(file="image/WB.png"),
              "WQ": PhotoImage(file="image/WQ.png"),
              "WK": PhotoImage(file="image/WK.png"),
              "BP": PhotoImage(file="image/BP.png"),
              "BR": PhotoImage(file="image/BR.png"),
              "BN": PhotoImage(file="image/BN.png"),
              "BB": PhotoImage(file="image/BB.png"),
              "BQ": PhotoImage(file="image/BQ.png"),
              "BK": PhotoImage(file="image/BK.png"),
              "":   PhotoImage()}


class SquareButton(Button):

    def __init__(self, master, square, rank, file, game, color=""):
        self.rank = rank
        self.file = file
        self.game = game

        pieces = {"P": "PAWN",
                  "R": "ROOK",
                  "N": "KNIGHT",
                  "B": "BISHOP",
                  "Q": "QUEEN",
                  "K": "KING"}

        if not images:
            createImageDict()

        color = color if color else "gray30" if (rank + file) % 2 == 0 else "gray70"
        string = square.string if square.string == square.string.upper() else ""
        textcolor = "white" if string and string[0] == "W" else "black"
        self.image = images[string] if string else images[""]
        string = pieces[string[1]] if string else ""
        super().__init__(master=master, bg=color,  # text=string, fg=textcolor,
                         image=self.image, width=65, height=65, command=self.command)
        self.grid(row=7-rank, column=file)

    def command(self):
        if self.game.players[self.game.turn] == "human":
            self.game.square(self.rank, self.file)
            self.game.updateGUI()


class Game:

    def __init__(self, player1="", player2="", display=True, board=None,
                 results=list([None]), index=0, timeout=False, movelimit=False):
        self.players = {}
        if type(player1) == str:
            self.players["W"] = "human"
        else:
            player1.color = "W"
            self.players["W"] = player1
        if type(player2) == str:
            self.players["B"] = "human"
        else:
            player2.color = "B"
            self.players["B"] = player2
        self.display = display or "human" in self.players.values()
        self.board = Board("real")
        self.board.mainInstance = True
        self.board.setup(board)
        self.results = results
        self.index = index
        self.timeout = timeout
        self.moveLimit = movelimit
        self.starttime = time()
        self.square1 = None
        self.square2 = None
        self.turn = "W"
        self.winner = None
        self.lastMove = tuple()
        self.moveCount = 0
        if self.display:
            self.root = Tk()
            self.root.grid()
            self.frame = Frame(self.root).grid()
            self.setupGUI()

    def play(self):

        while not self.ended():

            self.updateGUI()

            if self.players[self.turn] == "human":
                while self.square2 is None:
                    self.root.update()
            else:
                self.square1, self.square2 = self.players[self.turn].makeMove(self.board)
                if self.display: sleep(0.2)

            if not self.makeMove():
                self.square1 = self.square2 = None
                continue

            self.moveCount += 1
            if not self.display:
                if self.moveCount % 25 == 0:
                    print("Move number:", self.moveCount)
            self.lastMove = (self.square1, self.square2)
            self.square1 = self.square2 = None

            if self.turn == "W":
                self.turn = "B"
            else:
                self.turn = "W"

        self.updateGUI()

        if self.winner == "W":
            self.results[self.index] = "W"
            return "W"

        elif self.winner == "B":
            self.results[self.index] = "B"
            return "B"

        else:
            self.results[self.index] = "D"
            return "D"

    def ended(self):
        if self.timeout and (time() > self.starttime + self.timeout) or self.moveLimit and self.moveLimit < self.moveCount:
            return "D"
        if self.board.draw:
            self.winner = "D"
        '''for key, value in self.board.positions.items():
            for row in key.split(","):
                print(row)
            print(value)'''
        return self.winner

    def setupGUI(self):
        self.boardrep = []
        for file in range(len(self.board.board)):
            self.boardrep.append([])
            for rank in range(len(self.board.board[file])):
                self.boardrep[file].append(SquareButton(self.frame, self.board.board[file][rank], rank, file, self))

        self.root.update()

    def updateGUI(self):

        if not self.display:
            return

        if self.square1 is not None:
            x, y = self.square1
            self.boardrep[y][x] = SquareButton(self.frame, self.board.board[y][x], x, y, self, "green")
            for file in range(8):
                for rank in range(8):
                    if self.board.board[y][x]:
                        if self.board.board[y][x].getPiece() and self.board.board[y][x].getPiece().validateMove((x, y), (rank, file), self.board.board):
                            self.boardrep[file][rank] = SquareButton(self.frame, self.board.board[file][rank], rank, file, self, "red")

            self.root.update()
            return

        for file in range(len(self.board.board)):
            for rank in range(len(self.board.board[file])):
                self.boardrep[file][rank] = SquareButton(self.frame, self.board.board[file][rank], rank, file, self)

        if self.lastMove:
            (x1, y1), (x2, y2) = self.lastMove
            self.boardrep[y1][x1] = SquareButton(self.frame, self.board.board[y1][x1], x1, y1, self, "yellow")
            self.boardrep[y2][x2] = SquareButton(self.frame, self.board.board[y2][x2], x2, y2, self, "yellow")

        self.root.update()

    def square(self, rank, file):

        if self.square1 is None:
            self.square1 = (rank, file)

        elif self.square2 is None:
            self.square2 = (rank, file)

        else:
            self.square1 = (rank, file)
            self.square2 = None

    def makeMove(self):

        rank, file = self.square2
        takenPiece = self.board.board[file][rank].getPiece()

        moved = self.board.move(self.square1, self.square2, self.turn)

        #if b and rank in (0, 7) and self.board.board[file][rank].piece[1] == "P":
        #    self.promote(self.board.board[file][rank], self.board.board[file][rank].piece[0])

        if moved and takenPiece and takenPiece.piece == "K":
            self.winner = "W" if takenPiece.color == "B" else "B"

        return moved

    def promote(self, square, color):
        # self.PromoteWindow(self)
        #self.type = "Q"  # None
        # while self.type is None:
        #     pass
        #square.setPiece(Piece(color, self.type))
        pass

    # class PromoteWindow(Toplevel):

    #    def __init__(self, game):
    #        self.v = StringVar()
    #        self.v.set("Q")
    #        self.game = game
    #        for text, value in (["Queen", "Q"], ["Rook", "R"], ["Bishop", "B"], ["Knight", "N"]):
    #            b = Radiobutton(self.frame, text=text, value=value, variable=self.v)
    #            b.grid()
    #        b = Button(self.frame, text="Submit", command=self.submit)
    #        b.grid()

    #    def submit(self):
    #        self.game.type = self.v.get()
    #        self.destroy()


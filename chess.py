__author__ = 'John'

from player import *
from game import *
from testBoards import *
from time import *
from random import *
from tkinter import *

if __name__ == "__main__":
    arrays = [[], []]
    p1 = p2 = ""
    display = True
    d = 2

    for array in range(2):
        for i in range(373):
            arrays[array].append(randint(0, 1000))


    def setPlayers(p1v, p2v, displayv):
        global p1, p2, display, root
        root.destroy()
        if p1v == "H":
            p1 = ""
        elif p1v == "CP":
            p1 = Player(depth=d)
        elif p1v == "CR":
            p1 = Player(depth=d, values=arrays[0])
        if p2v == "H":
            p2 = ""
        elif p2v == "CP":
            p2 = Player(depth=d)
        elif p2v == "CR":
            p2 = Player(depth=d, values=arrays[1])
        display = displayv

    root = Tk()
    f1 = Frame(root, bd=3, relief=RIDGE)
    f1.grid(row=0, column=0)
    f2 = Frame(root, bd=3, relief=RIDGE)
    f2.grid(row=0, column=1)
    f3 = Frame(root, bd=3, relief=RIDGE)
    f3.grid(row=1, column=0, columnspan=2)
    Label(f1, text="White Player").grid(row=0, column=0)
    Label(f2, text="Black Player").grid(row=0, column=0)

    p1v = StringVar()
    p2v = StringVar()
    displayv = IntVar()

    p1v.set("H")
    p2v.set("H")
    displayv.set(True)

    for text, mode, row in [("Computer Preset", "CP", 1), ("Computer Random", "CR", 2), ("Human", "H", 3)]:
        b = Radiobutton(f1, text=text, variable=p1v, value=mode)
        b.grid(row=row)
    for text, mode, row in [("Computer Preset", "CP", 1), ("Computer Random", "CR", 2), ("Human", "H", 3)]:
        b = Radiobutton(f2, text=text, variable=p2v, value=mode)
        b.grid(row=row)

    Label(f3, text="Display:").grid(row=0, column=0)

    for text, mode, column in [("On", 1, 0), ("Off", 0, 1)]:
        b = Radiobutton(f3, text=text, variable=displayv, value=mode)
        b.grid(row=1, column=column)
    Button(root, text="Submit", width=20, command=lambda: setPlayers(p1v.get(), p2v.get(), displayv.get())).grid(row=3)

    mainloop()


    game = Game(p1, p2, display=display)  # , board=kingCapture)#, results=results, index=0)#"Me")

    #array = [0] * 373
    #array[25] = 1
    #array[195] = 2
    #array[282] = 3
    #array[286] = 4
    #array[345] = -1
    #game = Game(Player("W", array), Player("B")), board=checkmateTest)#Player("W"), Player("B")

    start = time()
    result = game.play()
    end = time()

    print("Winner:", result)
    print("Running time:", end-start)
    print("Number of moves:", game.moveCount)
    print()
    input("Press enter to close.")

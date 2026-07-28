import random as r
import tkinter as tk
from WordleSolver import getBestWords, findWordsLeft, wordleWord


def playWordle():

    letterIndex = 0

    def updateCurrentWord(event):

        nonlocal letterIndex
        nonlocal letterArray

        if event.char and event.char.isprintable() and letterIndex < 5:

            letterArray[letterIndex].config(text = event.char)

            letterIndex += 1

        elif event.keysym == "Return" and letterIndex == 5:

            for i in range(5):

                letterArray[i].config(text = "_")

            letterIndex = 0

        elif event.keysym == "BackSpace" and letterIndex != 0:

            letterArray[letterIndex - 1].config(text = "_")

            letterIndex -= 1

        print(f"{letterIndex, [letter["text"] for letter in letterArray]}")



    root = tk.Tk()
    root.bind("<Key>", updateCurrentWord)

    root.title("Wordle")

    letterArray = []
    for i in range(5):

        blankLetter = tk.Label(text = "_")
        blankLetter.pack(side = "left")

        letterArray.append(blankLetter)

    print(f"{letterArray}")

    root.mainloop()

def createMenu():

    root = tk.Tk()

    root.title("Main Menu")

    normalWordleButton = tk.Button(root, text = "Play Normal Wordle", command = playWordleWrapper)
    normalWordleButton.pack()
    customWordWordleButton = tk.Button(root, text = "Play Wordle with a custom word", command = playWordleWrapper)
    customWordWordleButton.pack()

    root.mainloop()

if __name__ == "__main__":

    #read the valid word file into a list
    #all possible inputs
    with open("valid-words.csv", "r") as f:
        validWords = f.read().splitlines()

    #read the word bank file into a list
    #finds answer word
    with open("word-bank.csv", "r") as fi:
        targetWordPossiblities = fi.read().splitlines()

    targetWordChoice = r.choice(targetWordPossiblities)

    playWordle()



import random as r
import tkinter as tk
from WordleSolver import getBestWords, findWordsLeft, wordleWord

#read the valid word file into a list
#all possible inputs
with open("valid-words.csv", "r") as f:
    validWords = f.read().splitlines()

currentWordsList = validWords

#read the word bank file into a list
#finds answer word
with open("word-bank.csv", "r") as fi:
    targetWordPossiblities = fi.read().splitlines()

targetWordChoice = r.choice(targetWordPossiblities)

def playWordle():

    letterIndex = 0
    guessNum = 0

    def submitWord(word):

        if word in validWords:

            return wordleWord(word, targetWordChoice)

        else:

            return "Invalid"

    def keyPressed(event):

        nonlocal letterIndex
        nonlocal letterArray
        nonlocal guessNum
        global currentWordsList

        if event.char and event.char.isprintable() and letterIndex < 5:

            letterArray[letterIndex].config(text = event.char)

            letterIndex += 1

        elif event.keysym == "BackSpace" and letterIndex != 0:

            letterArray[letterIndex - 1].config(text = "_")

            letterIndex -= 1

        elif event.keysym == "Return" and letterIndex == 5:

            word = "".join([letter["text"] for letter in letterArray])

            for i in range(5):

                letterArray[i].config(text = "_")

            letterIndex = 0

            print(word)
            
            if submitWord(word) == "Invalid":

                print("Invalid")

            else:

                guessNum += 1

                colourList = submitWord(word)

                currentWordsList = findWordsLeft(word, colourList, currentWordsList)

                for i in range(5):
            
                    colourLetterLabel = tk.Label(text = list(word)[i], font = ("Arial", 50), bg = colourList[i])
                    colourLetterLabel.grid(row = guessNum, column = i)

                    letterArray[i].grid(row = guessNum + 1, column = i)

                if colourList == ["green"] * 5:

                    win()

                elif guessNum == 6:

                    lose()


    root = tk.Tk()
    root.bind("<Key>", keyPressed)

    root.title("Wordle")

    suggestionButton = tk.Button(text = "Click for best guesses", command = lambda: print(getBestWords(currentWordsList, 10, validWords)))
    suggestionButton.grid(row = 0, columnspan = 5)

    letterArray = []
    for i in range(5):

        blankLetter = tk.Label(text = "_", font = ("Arial", 50))
        blankLetter.grid(row = 1, column = i)

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

    playWordle()



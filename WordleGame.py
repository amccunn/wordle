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

#result = true means win false means lose
def endGame(result):

    if result:

        textArray = ["YOU WIN", "Well done you win!!"]

    else:

        textArray = ["YOU LOSE", "You lost, ur bad"]

    winWindow = tk.Tk()

    winWindow.title(textArray[0])

    winLabel = tk.Label(winWindow, text = textArray[1], font = ("Arial", 40))
    winLabel.pack()

    winWindow.mainloop()


#default target word is random, but can be changed to any word in the word bank
def playWordle(targetWord = targetWordChoice):

    letterIndex = 0
    guessNum = 0

    def submitWord(word):

        if word in validWords:

            return wordleWord(word, targetWord)

        else:

            return "Invalid"

    def keyPressed(event):

        nonlocal letterIndex
        nonlocal letterArray
        nonlocal guessNum
        global currentWordsList

        if event.char and event.char.isprintable() and letterIndex < 5:

            letterArray[letterIndex].config(text = event.char.upper())

            letterIndex += 1

        elif event.keysym == "BackSpace" and letterIndex != 0:

            letterArray[letterIndex - 1].config(text = "_")

            letterIndex -= 1

        elif event.keysym == "Return" and letterIndex == 5:

            word = "".join([letter["text"].lower() for letter in letterArray])

            print(word)

            for i in range(5):

                letterArray[i].config(text = "_")

            letterIndex = 0

            if submitWord(word) == "Invalid":

                print("Invalid")

            else:

                guessNum += 1

                colourList = submitWord(word)

                currentWordsList = findWordsLeft(word, colourList, currentWordsList)

                for i in range(5):
            
                    colourLetterLabel = tk.Label(root, text = list(word)[i].upper(), font = ("Arial", 50), bg = colourList[i])
                    colourLetterLabel.grid(row = guessNum, column = i)

                    letterArray[i].grid(row = guessNum + 1, column = i)

                if colourList == ["green"] * 5:

                    endGame(True)

                elif guessNum == 6:

                    endGame(False)


    root = tk.Tk()
    root.bind("<Key>", keyPressed)

    root.title("Wordle")

    suggestionButton = tk.Button(root, text = "Click for best guesses", command = lambda: print(getBestWords(currentWordsList, 10, validWords)))
    suggestionButton.grid(row = 0, columnspan = 5)

    letterArray = []
    for i in range(5):

        blankLetter = tk.Label(root, text = "_", font = ("Arial", 50))
        blankLetter.grid(row = 1, column = i)

        letterArray.append(blankLetter)

    print(f"{letterArray}")

    root.mainloop()

def selectCustomWord(): 

    root = tk.Tk()

    root.title("Select Custom Word")

    wordEntry = tk.Entry(root, text = "Enter a custom word", font = ("Arial", 20))
    wordEntry.pack()

    wordSubmitButton = tk.Button(root, text = "Submit", command = lambda: playWordle(wordEntry.get().lower()) and root.destroy() if wordEntry.get().lower() in validWords else print("Invalid word"))
    wordSubmitButton.pack()

    root.mainloop()

def createMenu():

    root = tk.Tk()

    root.title("Main Menu")

    normalWordleButton = tk.Button(root, text = "Play Normal Wordle", command = lambda: playWordle() and root.destroy())
    normalWordleButton.pack()
    customWordWordleButton = tk.Button(root, text = "Play Wordle with a custom word", command = lambda: selectCustomWord() and root.destroy())
    customWordWordleButton.pack()

    root.mainloop()

if __name__ == "__main__":

    createMenu()



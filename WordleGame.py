import random as r
from WordleSolver import getBestWords, findWordsLeft, wordleWord

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

    print(targetWordChoice)

    #wordle game logic
    guess = ""
    guesses = 0
    wordsLeft = validWords
    while guess != targetWordChoice and guesses < 6:

        print(f"{getBestWords(wordsLeft, 10, validWords)}")

        #ask for valid input
        guess = ""
        while guess not in validWords:

            guess = input("What is your guess: ")

        outputColours = wordleWord(guess, targetWordChoice)

        guesses += 1

        print(outputColours)

        wordsLeft = findWordsLeft(guess, outputColours, wordsLeft)

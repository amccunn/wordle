import random as r

#read the valid word file into a list
with open("valid-words.csv", "r") as f:
    validWords = f.read().splitlines()

#read the word bank file into a list
with open("word-bank.csv", "r") as fi:
    targetWordPossiblities = fi.read().splitlines()

targetWord = r.choice(targetWordPossiblities)

print(targetWord)

#wordle game logic
guess = ""
guesses = 0
while guess != targetWord and guesses < 5:

    #ask for valid input
    guess = ""
    while guess not in validWords:

        guess = input("What is your guess: ")


    wordList = list(guess)
    targetWordList = list(targetWord)

    tempTargetWordList = list(targetWord)
    letterColours = ["grey"] * 5

    for i, letter in enumerate(wordList):

        if letter in tempTargetWordList:

            letterColours[i] = "yellow"

            if letter == tempTargetWordList[i]:

                letterColours[i] = "green"

            for j, targetLetter in enumerate(tempTargetWordList):

                if letter == targetLetter:

                    tempTargetWordList[j] = None

    guesses += 1

    print(letterColours)

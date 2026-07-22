import random as r

#return how many words are left after a guess is made
def findWordsLeft(guessMade, targetWord, currentWordList):

    newWordList = currentWordList

    wordColours = wordleWord(guessMade, targetWord)

    for i, colour in enumerate(wordColours):

        letter = list(guessMade)[i]

        print(colour, letter, i)

        if colour == "grey":

            newWordList = [
                word for word in newWordList
                if letter not in word
            ]

        elif colour == "green":

            newWordList = [
                word for word in newWordList
                if word[i] == letter
            ]


        elif colour == "yellow":

            newWordList = [
                word for word in newWordList 
                if word[i] != letter and letter in (word[:i] + word[i+1:])
            ]

    return newWordList


#return a colour list based off the word input and the target word
def wordleWord(word, targetWord):

    wordList = list(word)
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
                    break

    return letterColours

#read the valid word file into a list
with open("valid-words.csv", "r") as f:
    validWords = f.read().splitlines()

#read the word bank file into a list
with open("word-bank.csv", "r") as fi:
    targetWordPossiblities = fi.read().splitlines()

targetWordChoice = "apply"

print(targetWordChoice)

#wordle game logic
guess = ""
guesses = 0
wordsLeft = validWords
while guess != targetWordChoice and guesses < 6:

    #ask for valid input
    guess = ""
    while guess not in validWords:

        guess = input("What is your guess: ")

    outputColours = wordleWord(guess, targetWordChoice)

    wordsLeft = findWordsLeft(guess, targetWordChoice, wordsLeft)

    print(wordsLeft, len(wordsLeft))

    guesses += 1

    print(outputColours)

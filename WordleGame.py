import random as r

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


if __name__ == "__main__":
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

        guesses += 1

        print(outputColours)

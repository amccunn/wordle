import itertools
import numpy as np
from collections import defaultdict
from WordleGame import wordleWord

colours = ['green', 'yellow', 'grey']

possibleColourCombos = list(itertools.product(colours, repeat=5))

#return how many words are left after a guess is made
def findWordsLeft(guessMade, wordColours, currentWordList):

    newWordList = currentWordList

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


def rankBestWords(wordsLeft):

    wordsDictionary = {}

    length = len(wordsLeft)

    for word in wordsLeft:

        probabilitiesOfPatterns = defaultdict(float)

        for secretWord in wordsLeft:

            colourCombo = tuple(wordleWord(word, secretWord))

            probabilitiesOfPatterns[colourCombo] += 1 / length

        wordsDictionary[word] = dict(probabilitiesOfPatterns)

    wordsInDictionary = wordsDictionary.keys()

    expectedInfo = {}

    for word in wordsInDictionary:

        expectedInfo[word] = sum(list(map(lambda x: float(x * np.log2(1/x)), wordsDictionary[word].values())))

    return expectedInfo


with open("valid-words.csv", "r") as f:
    validWords = f.read().splitlines()

print(f"{rankBestWords(validWords)}")


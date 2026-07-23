import itertools
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

    for word in wordsLeft:

        counts = defaultdict(int)

        for secretWord in wordsLeft:

            colourCombo = tuple(wordleWord(word, secretWord))

            counts[colourCombo] += 1

        wordsDictionary[word] = dict(counts)

    return wordsDictionary

#read the valid word file into a list
with open("valid-words.csv", "r") as f:
    validWords = f.read().splitlines()

print(f"{rankBestWords(validWords)}")


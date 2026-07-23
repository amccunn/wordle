import itertools
import numpy as np
import math  # MODIFIED: Imported builtin math for much faster scalar log operations
import time as t
from heapq import nlargest
from collections import defaultdict

colours = ['green', 'yellow', 'grey']

possibleColourCombos = list(itertools.product(colours, repeat=5))

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


# return how many words are left after a guess is made
def findWordsLeft(guessMade, wordColours, currentWordList):

    newWordList = currentWordList

    for i, colour in enumerate(wordColours):

        letter = guessMade[i]  # MODIFIED: Removed list(guessMade)[i]; strings are already indexable

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

            # MODIFIED: Simplified (word[:i] + word[i+1:]) string creation to `letter in word`
            # Since word[i] != letter is already checked, checking `letter in word` is logically identical and avoids string concatenation
            newWordList = [
                word for word in newWordList 
                if word[i] != letter and letter in word
            ]

    return newWordList


def rankBestWords(wordsLeft, N):

    startTime = t.time()

    wordsDictionary = {}

    length = max(len(wordsLeft),1)
    inv_length = 1.0 / length  # MODIFIED: Precomputed 1 / length to avoid repeated floating-point division

    for word in wordsLeft:

        # MODIFIED: Count pattern occurrences using fast integer arithmetic instead of adding floats in the hot loop
        counts = defaultdict(int)

        for secretWord in wordsLeft:

            colourCombo = tuple(wordleWord(word, secretWord))

            counts[colourCombo] += 1

        # MODIFIED: Normalize integer counts to probabilities once per unique pattern at the end
        wordsDictionary[word] = {combo: count * inv_length for combo, count in counts.items()}

    # finds the expected info of each word by summing its possible colour combos
    expectedInfo = {}
    
    # MODIFIED: Replaced np.log2 with math.log2 and map/lambda with a generator expression.
    # Calling NumPy functions on individual scalar floats adds huge overhead compared to C-native math functions.
    for word, probs in wordsDictionary.items():
        expectedInfo[word] = sum(p * math.log2(1.0 / p) for p in probs.values())

    # returns the top N words and their expected info
    top_n = nlargest(N, expectedInfo.items(), key=lambda item: item[1])

    finishTime = t.time()

    elapsedTime = finishTime - startTime

    print(f"Execution took {elapsedTime} seconds")

    return top_n

if __name__ == "__name__":

    with open("valid-words.csv", "r") as f:
        validWords = f.read().splitlines()

    print(f"{rankBestWords(validWords, 10)}")
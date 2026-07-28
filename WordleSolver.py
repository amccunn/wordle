import itertools
import numpy as np
import math
import time as t
import os
import json
from heapq import nlargest
from collections import defaultdict

colours = ['green', 'yellow', 'grey']

possibleColourCombos = list(itertools.product(colours, repeat=5))

def wordleWord(word, targetWord):
    wordList = list(word)
    targetWordList = list(targetWord)
    letterColours = ["grey"] * 5

    # Pass 1: Check for exact matches (Green)
    for i in range(5):
        if wordList[i] == targetWordList[i]:
            letterColours[i] = "green"
            targetWordList[i] = None  # Consume this letter from target

    # Pass 2: Check for partial matches (Yellow)
    for i in range(5):
        # Skip letters already marked green
        if letterColours[i] == "green":
            continue

        letter = wordList[i]
        if letter in targetWordList:
            letterColours[i] = "yellow"
            # Consume the first matching instance in target
            targetWordList[targetWordList.index(letter)] = None

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

def getBestWords(wordsLeft, N, fullWordList, cache_file="first_guess_scores.json"):

    # Check if this is the first turn (all words are still available)
    if len(wordsLeft) == len(fullWordList):

        if os.path.exists(cache_file):

            with open(cache_file, "r") as f:
                cached_data = json.load(f)
            
            # Return top N from cached dictionary
            return nlargest(N, cached_data.items(), key=lambda item: item[1])
        
        else:
            print("Cache file not found, running full evaluation...")

    # For turn 2 onwards (or if cache doesn't exist), run the original function
    return rankBestWords(wordsLeft, N)


def rankBestWords(wordsLeft, N):

    startTime = t.time()

    wordsDictionary = {}

    length = max(len(wordsLeft),1)
    inv_length = 1.0 / length

    for word in wordsLeft:

        counts = defaultdict(int)

        for secretWord in wordsLeft:

            colourCombo = tuple(wordleWord(word, secretWord))

            counts[colourCombo] += 1

        wordsDictionary[word] = {combo: count * inv_length for combo, count in counts.items()}

    # finds the expected info of each word by summing its possible colour combos
    expectedInfo = {}
    
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
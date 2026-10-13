import itertools
import numpy as np
import math
import time as t
import os
import json
import random as r
from heapq import nlargest
from collections import defaultdict
from wordfreq import zipf_frequency

colours = ['green', 'yellow', 'grey']

possibleColourCombos = list(itertools.product(colours, repeat=5))

with open("valid-words.csv", "r") as f:
    VALID_WORDS = f.read().splitlines()

#sigmoid function to squish the word frequencies into a range of 0-1
def sigmoidShifted(x, shift=3.0, stretch=6.0):
    return 1 / (1 + np.exp(-stretch * (x - shift)))

#finds the frequency of each word in the English language using the wordfreq library
#squishes the frequencies into a range of 0-1 to make them easier to work with
wordFrequencies = {word: sigmoidShifted(zipf_frequency(word, 'en')) for word in VALID_WORDS}
#test word list for testing is a subset of VALID_WORDS of 100 randomly selected words
#evenly spaced by word frequency to ensure a good distribution of common and uncommon words
TEST_WORDS = r.sample(VALID_WORDS, 1000)

#use input word and target word to return a list of colours
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

    target_colours = list(wordColours)

    newWordList = [
        candidate for candidate in currentWordList
        if wordleWord(guessMade, candidate) == target_colours
    ]

    return newWordList

def getBestWords(wordsLeft=VALID_WORDS, N=5, fullWordList=VALID_WORDS, cache_file="first_guess_scores_v2.json"):
    
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

    #startTime = t.time()

    wordsDictionary = {}

    length = max(len(wordsLeft),1)
    inv_length = 1.0 / length

    for word in wordsLeft:

        counts = defaultdict(int)

        for secretWord in wordsLeft:

            colourCombo = tuple(wordleWord(word, secretWord))

            counts[colourCombo] += 1

        wordsDictionary[word] = {combo: count * inv_length for combo, count in counts.items()}

    #finds the expected info of each word by summing its possible colour combos
    #probabilities multiplied by the log2 of the inverse of that probability
    expectedInfo = {}
    
    for word, probs in wordsDictionary.items():
        expectedInfo[word] = sum(p * math.log2(1.0 / p) * wordFrequencies[word] for p in probs.values())

    # returns the top N words and their expected info
    top_n = nlargest(N, expectedInfo.items(), key=lambda item: item[1])

    #finishTime = t.time()

    #elapsedTime = finishTime - startTime

    #print(f"Time elapsed: {elapsedTime:.2f} seconds")

    return top_n

if __name__ == "__main__":

    print(f"{rankBestWords(VALID_WORDS, 10)}")



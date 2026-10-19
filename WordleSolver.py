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

def timer(func):
    def wrapper(*args, **kwargs):
        start = t.time()
        result = func(*args, **kwargs)
        end = t.time()
        print(f"{func.__name__} took {end - start}s")
        return result
    return wrapper

with open("valid-words.csv", "r") as f:
    VALID_WORDS = f.read().splitlines()

with open("word-bank.csv", "r") as fi:
    ANSWERS = fi.read().splitlines()

#sigmoid function to squish the word frequencies into a range of 0-1
def sigmoidShifted(x, shift=3.0, stretch=6.0):
    return 1 / (1 + np.exp(-stretch * (x - shift)))

#takes whole list of vals and squishes them into a range of 0-1 linearly
def linearCompression(val, min_val=0, max_val=7):

    if min_val is None:
        min_val = val
    if max_val is None:
        max_val = val

    squished_val = val / (max_val - min_val) if (max_val - min_val) != 0 else val

    #returns val is failed to squish, otherwise returns squished val
    return squished_val


#finds the frequency of each word in the English language using the wordfreq library
#squishes the frequencies into a range of 0-1 to make them easier to work with
wordFrequencies = {word: sigmoidShifted(zipf_frequency(word, 'en')) for word in VALID_WORDS}



#test word list for testing is a subset of VALID_WORDS of 100 randomly selected words
#evenly spaced by word frequency to ensure a good distribution of common and uncommon words
TEST_WORDS = r.sample(VALID_WORDS, 100)

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

@timer
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

    wordsDictionary = {}

    answersLeft = [ans for ans in wordsLeft
                   if ans in ANSWERS]

    length = max(len(answersLeft),1)
    inv_length = 1.0 / length

    for word in wordsLeft:

        counts = defaultdict(int)

        for secretWord in answersLeft:

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

    return top_n

if __name__ == "__main__":

    print(f"{rankBestWords(VALID_WORDS, 10)}")



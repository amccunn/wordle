from WordleSolver import wordleWord, findWordsLeft, getBestWords, VALID_WORDS

with open("word-bank.csv", "r") as fi:
    targetWordPossiblities = fi.read().splitlines()

wordScores = {}

for word in VALID_WORDS:

    for targetWord in targetWordPossiblities:

        nextGuess = word

        wordAvgGuesses = 0

        for i in range(6):

            #simulate the guess and get the colours for each letter
            wordColourList = wordleWord(nextGuess, targetWord)

            if wordColourList == ["green"] * 5:
                guesses = i + 1
                break

            #find the words left after the guess is made
            wordsLeft = findWordsLeft(nextGuess, wordColourList, VALID_WORDS)

            #calculate the next best guess based on the words left
            nextGuess = getBestWords(wordsLeft=wordsLeft, N=1)[0]

        else:
            guesses = 6

        wordAvgGuesses += guesses

    wordAvgGuesses /= len(targetWordPossiblities)

    wordScores[word] = wordAvgGuesses

algorithmAvgGuesses = sum(wordScores.values()) / len(wordScores)

print(f"Average guesses for algorithm: {algorithmAvgGuesses:.2f}")

        



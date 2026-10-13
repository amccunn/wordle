from WordleSolverOld import wordleWord, findWordsLeft, getBestWords, VALID_WORDS

with open("word-bank.csv", "r") as fi:
    targetWordPossibilities = fi.read().splitlines()

wordAvgGuesses = 0

topTenWords = getBestWords(wordsLeft=VALID_WORDS, N=10)
topTenWordsDict = {}

#test the top 10 best first guesses
for word in topTenWords:

    #test algorithm against all the possible target words
    for targetWord in targetWordPossibilities:

        nextGuess = word[0]

        wordsLeft = targetWordPossibilities.copy()

        for i in range(6):

            #simulate the guess and get the colours for each letter
            wordColourList = wordleWord(nextGuess, targetWord)

            if wordColourList == ["green"] * 5:
                guesses = i + 1
                break

            #find the words left after the guess is made
            wordsLeft = findWordsLeft(nextGuess, wordColourList, wordsLeft)

            #calculate the next best guess based on the words left
            nextGuess = getBestWords(wordsLeft=wordsLeft, N=1)[0][0]

        else:
            guesses = 6

        wordAvgGuesses += guesses

    wordAvgGuesses /= len(targetWordPossibilities)
    topTenWordsDict[word[0]] = wordAvgGuesses

print("\nTop 10 first guesses and their average guesses:")
for word, avg in sorted(topTenWordsDict.items(), key=lambda x: x[1]):
    print(f"{word}: {avg:.3f}")

#average for botWithWordFreqHeuristic: 3.576 - tares first guess since it has the best score
# Top 10 first guesses and their average guesses:
# tales: 3.552
# tears: 3.568
# teras: 3.573
# tares: 3.576
# rates: 3.591
# nares: 3.598
# rales: 3.599
# lares: 3.605
# soare: 3.613
# reais: 3.618
#tales is therefore the best first guess for the bot with the word frequency heuristic
#average for botNoHeuristic: 


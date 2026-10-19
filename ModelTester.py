from WordleSolver import wordleWord, findWordsLeft, getBestWords, VALID_WORDS, timer

@timer
def tester():
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

tester()
#average for botWithWordFreqHeuristic: linearShifted
# Top 10 first guesses and their average guesses:
# least: 3.629
# later: 3.683
# great: 3.698
# since: 3.713
# after: 3.738
# their: 3.740
# means: 3.742
# times: 3.752
# those: 3.759
# years: 3.819
#average for botWithWordFreqHeuristic: sigmoidShifted
# Top 10 first guesses and their average guesses:
# tales: 3.563
# tears: 3.576
# tries: 3.577
# lanes: 3.592
# tires: 3.593
# rates: 3.602
# cares: 3.610
# roles: 3.611
# raise: 3.614
# dares: 3.621
#tales is therefore the best first guess for the bot with the word frequency heuristic
#average for botNoHeuristic: 
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

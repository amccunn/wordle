import random as r

#read the valid word file into a list
with open("valid-words.csv", "r") as f:
    validWords = f.read().splitlines()

#read the word bank file into a list
with open("word-bank.csv", "r") as fi:
    targetWordPossiblities = fi.read().splitlines()

#ask for valid input
guess = ""
while guess not in validWords:

    guess = input("What is your guess: ")

targetWord = r.choice(targetWordPossiblities)

print(targetWord)
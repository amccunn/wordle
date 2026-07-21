#read the wordle word file into a list
with open("valid-words.csv", "r") as r:
    validWords = r.read().splitlines()

#ask for valid input
guess = ""
while guess not in validWords:

    guess = input("What is your guess: ")


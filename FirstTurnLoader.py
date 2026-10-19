import json
from WordleSolver import rankBestWords, timer
from WordleSolverOld import rankBestWords as rankBestWordsOld

@timer
def load():
    with open("valid-words.csv", "r") as f:
        allWordsList = f.read().splitlines()

    # Pre-calculate top N for the starting list and save to disk
    starting_scores = rankBestWords(allWordsList, len(allWordsList))

    # Convert list of tuples to a dictionary for easy saving/loading
    with open("first_guess_scores_v2.json", "w") as f:
        json.dump(dict(starting_scores), f)

    print("First guess scores cached successfully!")

load()
# wordle
Wordle and a bot that can suggest best words

Run WordleGame.py for the normal game with either 
normal wordle or choosing a specific word for 2 player

Whenever changes are made to the rankBestWords func
inside WordleSolver.py you need to run the FirstTurnLoader.py.
It will take a while to run but it offloads the first
turn whenever getBestWords func is called to speed the function
up significantly by storing the results in first_guess_socres.json


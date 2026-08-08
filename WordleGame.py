import random as r
import tkinter as tk
from WordleSolver import getBestWords, findWordsLeft, wordleWord

# read the valid word file into a list
# all possible inputs
with open("valid-words.csv", "r") as f:
    validWords = f.read().splitlines()

currentWordsList = validWords

# read the word bank file into a list
# finds answer word
with open("word-bank.csv", "r") as fi:
    targetWordPossiblities = fi.read().splitlines()

targetWordChoice = r.choice(targetWordPossiblities)

COLORS = {
    "bg": "#f4f4f4",
    "panel": "#ffffff",
    "fg": "#1f1f1f",
    "tile": "#d3d6da",
    "tile_active": "#ffffff",
    "tile_border": "#c9ccd1",
    "green": "#6aaa64",
    "yellow": "#c9b458",
    "gray": "#787c7e",
    "primary": "#0f172a",
    "button": "#1d4ed8",
    "button_text": "#ffffff",
    "secondary": "#e2e8f0",
}

WINDOW_FONT = ("Segoe UI", 24, "bold")
LABEL_FONT = ("Segoe UI", 28, "bold")
BUTTON_FONT = ("Segoe UI", 12, "bold")


def style_button(button):
    button.configure(
        bg=COLORS["button"],
        fg=COLORS["button_text"],
        activebackground="#1e40af",
        activeforeground=COLORS["button_text"],
        relief="flat",
        bd=0,
        padx=18,
        pady=10,
        font=BUTTON_FONT,
    )


# result = true means win false means lose
def endGame(result):
    if result:
        title = "YOU WIN"
        message = "Well done! You cracked the word."
    else:
        title = "YOU LOSE"
        message = "Better luck next time!"

    winWindow = tk.Toplevel()
    winWindow.title(title)
    winWindow.configure(bg=COLORS["bg"])
    winWindow.geometry("360x220")
    winWindow.resizable(False, False)

    titleLabel = tk.Label(
        winWindow,
        text=title,
        font=("Segoe UI", 28, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["primary"],
        pady=20,
    )
    titleLabel.pack()

    messageLabel = tk.Label(
        winWindow,
        text=message,
        font=("Segoe UI", 14),
        bg=COLORS["bg"],
        fg=COLORS["fg"],
    )
    messageLabel.pack(pady=(0, 18))

    playAgainButton = tk.Button(
        winWindow,
        text="Play Again",
        command=winWindow.destroy,
        bg=COLORS["button"],
        fg=COLORS["button_text"],
        activebackground="#1e40af",
        activeforeground=COLORS["button_text"],
        relief="flat",
        bd=0,
        font=BUTTON_FONT,
        padx=20,
        pady=10,
    )
    playAgainButton.pack()

    winWindow.grab_set()
    winWindow.focus_set()


# default target word is random, but can be changed to any word in the word bank
def playWordle(targetWord=targetWordChoice):
    letterIndex = 0
    guessNum = 0

    def submitWord(word):
        if word in validWords:
            return wordleWord(word, targetWord)

        return "Invalid"

    def themeLetterBox(widget, text="_", fill=None, active=False):
        widget.configure(
            text=text,
            width=3,
            height=2,
            font=("Segoe UI", 26, "bold"),
            bg=fill if fill else (COLORS["tile_active"] if active else COLORS["tile"]),
            fg="#ffffff" if fill else COLORS["fg"],
            relief="solid",
            borderwidth=2,
            padx=10,
            pady=8,
        )

    def keyPressed(event):
        nonlocal letterIndex
        nonlocal letterArray
        nonlocal guessNum
        global currentWordsList

        if event.char and event.char.isprintable() and letterIndex < 5:
            letterArray[letterIndex].config(text=event.char.upper())
            letterArray[letterIndex].configure(bg=COLORS["tile_active"], fg=COLORS["fg"])
            letterIndex += 1

        elif event.keysym == "BackSpace" and letterIndex != 0:
            letterIndex -= 1
            themeLetterBox(letterArray[letterIndex], text="_", fill=None, active=False)

        elif event.keysym == "Return" and letterIndex == 5:
            word = "".join([letter.cget("text").lower() for letter in letterArray])
            for i in range(5):
                themeLetterBox(letterArray[i], text="_", fill=None, active=False)
            letterIndex = 0

            if submitWord(word) == "Invalid":
                statusLabel.config(text="Not in word list")
            else:
                guessNum += 1
                colourList = submitWord(word)
                currentWordsList = findWordsLeft(word, colourList, currentWordsList)

                for i in range(5):
                    colourLetterLabel = tk.Label(
                        root,
                        text=list(word)[i].upper(),
                        font=("Segoe UI", 28, "bold"),
                        bg=COLORS[colourList[i]],
                        fg="white",
                        width=3,
                        height=2,
                        padx=10,
                        pady=8,
                        borderwidth=0,
                        relief="flat",
                    )
                    colourLetterLabel.grid(row=guessNum + 2, column=i, padx=4, pady=4)

                    letterArray[i].grid(row=guessNum + 3, column=i, padx=4, pady=4)

                if colourList == ["green"] * 5:
                    endGame(True)
                    root.destroy()
                elif guessNum == 6:
                    endGame(False)
                    root.destroy()

    root = tk.Tk()
    root.bind("<Key>", keyPressed)
    root.title("Wordle")
    root.configure(bg=COLORS["bg"])
    root.geometry("420x620")
    root.resizable(False, False)

    titleLabel = tk.Label(
        root,
        text="WORDLE",
        font=("Segoe UI", 32, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["primary"],
        pady=18,
    )
    titleLabel.grid(row=0, column=0, columnspan=5, sticky="ew")

    statusLabel = tk.Label(
        root,
        text="",
        font=("Segoe UI", 11, "bold"),
        bg=COLORS["bg"],
        fg="#dc2626",
        pady=4,
    )
    statusLabel.grid(row=1, column=0, columnspan=5, sticky="ew")

    suggestionButton = tk.Button(
        root,
        text="Best guesses",
        command=lambda: print(getBestWords(currentWordsList, 10, validWords)),
    )
    style_button(suggestionButton)
    suggestionButton.grid(row=2, column=0, columnspan=5, sticky="ew", padx=18, pady=(0, 10))

    letterArray = []
    for i in range(5):
        blankLetter = tk.Label(
            root,
            text="_",
            font=LABEL_FONT,
            bg=COLORS["tile"],
            fg=COLORS["fg"],
            width=3,
            height=2,
            bd=0,
            relief="solid",
            borderwidth=2,
            padx=10,
            pady=8,
        )
        blankLetter.grid(row=3, column=i, padx=4, pady=4)
        letterArray.append(blankLetter)

    root.mainloop()


def selectCustomWord():
    root = tk.Tk()
    root.title("Select Custom Word")
    root.configure(bg=COLORS["bg"])
    root.geometry("330x180")
    root.resizable(False, False)

    label = tk.Label(
        root,
        text="Enter a custom answer word",
        font=("Segoe UI", 14, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["fg"],
        pady=18,
    )
    label.pack()

    wordEntry = tk.Entry(root, font=("Segoe UI", 20), justify="center", width=12)
    wordEntry.pack(padx=20, pady=(0, 12))

    def submitWord():
        chosenWord = wordEntry.get().lower()
        if chosenWord in validWords:
            root.destroy()
            playWordle(chosenWord)
        else:
            statusLabel.config(text="Please enter a valid word")

    statusLabel = tk.Label(
        root,
        text="",
        font=("Segoe UI", 10, "bold"),
        bg=COLORS["bg"],
        fg="#dc2626",
    )
    statusLabel.pack()

    wordSubmitButton = tk.Button(root, text="Submit", command=submitWord)
    style_button(wordSubmitButton)
    wordSubmitButton.pack(pady=(10, 0))

    root.mainloop()


def createMenu():
    root = tk.Tk()
    root.title("Main Menu")
    root.configure(bg=COLORS["bg"])
    root.geometry("380x260")
    root.resizable(False, False)

    title = tk.Label(
        root,
        text="Wordle",
        font=("Segoe UI", 34, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["primary"],
        pady=20,
    )
    title.pack()

    normalWordleButton = tk.Button(root, text="Play Normal Wordle", command=lambda: (root.destroy(), playWordle()))
    style_button(normalWordleButton)
    normalWordleButton.pack(fill="x", padx=30, pady=(10, 10))

    customWordWordleButton = tk.Button(root, text="Play With Custom Word", command=lambda: (root.destroy(), selectCustomWord()))
    style_button(customWordWordleButton)
    customWordWordleButton.pack(fill="x", padx=30, pady=(0, 10))

    root.mainloop()


if __name__ == "__main__":
    createMenu()


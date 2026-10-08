import time as t
from playwright.sync_api import sync_playwright
from WordleSolver import getBestWords, findWordsLeft, VALID_WORDS

def load_wordle(autoPlay=False):
    # Keep current words local to avoid global state issues across multiple runs
    currentWordsList = VALID_WORDS.copy()

    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=False)
        page = browser.new_page()
        page.goto("https://www.nytimes.com/games/wordle/index.html")

        t.sleep(2)  # Wait for page load
        
        # Dismiss modals
        for name in ["Accept All", "Play", "Continue to Wordle", "Close"]:
            try:
                page.get_by_role("button", name=name).click(timeout=2000)
                t.sleep(5)
            except Exception:
                pass
        
        page.keyboard.press("Escape")

        for attempt in range(6):
            # 1. AUTOPLAY: Choose and type the word ONCE before polling
            if autoPlay:
                best_results = getBestWords(wordsLeft=currentWordsList, N=1)
                if not best_results:
                    print("No candidate words remaining!")
                    break
                
                # Extract clean string if returned as tuple (word, score)
                best_guess = best_results[0][0] if isinstance(best_results[0], (tuple, list)) else best_results[0]
                
                print(f"\nAuto-playing guess #{attempt + 1}: {best_guess}")
                page.keyboard.type(best_guess)
                page.keyboard.press("Enter")
                t.sleep(2)  # Wait for tiles to update
            else:
                print(f"\nWaiting for you to enter guess #{attempt + 1} and press Enter in browser...")
                t.sleep(5)
            # 2. POLLING LOOP: Wait for tiles to turn into final colors
            row_data = None
            valid_states = ["correct", "present", "absent"]
            
            while True:
                row_data = page.evaluate(f"""() => {{
                    const tiles = Array.from(document.querySelectorAll("div[data-state]"));
                    if (tiles.length < 30) return null;
                    
                    const startIndex = {attempt} * 5;
                    const rowTiles = tiles.slice(startIndex, startIndex + 5);
                    
                    return rowTiles.map(tile => ({{
                        state: tile.getAttribute("data-state"),
                        letter: (tile.textContent || "").trim().toLowerCase()
                    }}));
                }}""")

                if row_data and len(row_data) == 5:
                    states = [tile["state"] for tile in row_data]
                    # Check if all 5 tiles have resolved to green/yellow/grey
                    if all(s in valid_states for s in states):
                        break

                t.sleep(0.5)

            # 3. PROCESS RESULT: Extract letters and colors
            guessMade = "".join(tile["letter"] for tile in row_data)
            wordColours = [
                "green" if tile["state"] == "correct" else
                "yellow" if tile["state"] == "present" else "grey"
                for tile in row_data
            ]

            print(f"Guess #{attempt + 1} processed: {guessMade.upper()} -> {wordColours}")

            # Check win condition
            if all(tile["state"] == "correct" for tile in row_data):
                print("🎉 Congratulations! Word guessed correctly!")
                break

            # 4. FILTER DICTIONARY for next attempt
            currentWordsList = findWordsLeft(guessMade, wordColours, currentWordsList)
            
            # Ensure currentWordsList contains only string words (strip scores if present)
            currentWordsList = [w[0] if isinstance(w, (tuple, list)) else w for w in currentWordsList]

            if not autoPlay:
                best_suggestions = getBestWords(wordsLeft=currentWordsList, N=10)
                print(f"Top suggested next words: {best_suggestions}")

        print("\nGame over! Thanks for playing.")
        t.sleep(5)
        browser.close()


if __name__ == "__main__":
    load_wordle(autoPlay=True)
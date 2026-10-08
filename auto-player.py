import time as t
from playwright.sync_api import sync_playwright
from WordleSolver import getBestWords, VALID_WORDS

#initialise current words ready to be edited 
currentWordsList = VALID_WORDS.copy() 

def load_wordle():

    with sync_playwright() as p:
        # Launch browser (set headless=True if you don't need to watch it run)
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Go to the official Wordle game
        page.goto("https://www.nytimes.com/games/wordle/index.html")

        t.sleep(2)  #wait for the page to load completely
        
        # Handle the initial "Play" / privacy modal popup if it appears
        try:
            page.get_by_role("button", name="Accept All").click(timeout=3000)
            t.sleep(1)  # wait for modal to close
        except:
            pass # Modal might not appear if cookies are cached
            
        try:
            page.get_by_role("button", name="Play").click(timeout=3000)
            t.sleep(5)  # wait for the game to start
        except:
            pass

        try:
            page.get_by_role("button", name="Continue to Wordle").click(timeout=3000)
            t.sleep(6)  # wait for ad to close
        except:
            pass

        #close the help modal if it appears
        try:
            page.get_by_role("button", name="Close").click(timeout=3000)
            t.sleep(2)  # wait for modal to close
        except:
            pass

        #wait for user input
        for attempt in range(6):
            print(f"\nWaiting for you to enter guess #{attempt + 1} and press Enter in the browser...")
            
            # Polling loop
            while True:
                row_data = page.evaluate(f"""() => {{
                    // Grab ALL tile divs on the board. (Keyboard keys are <button>s, so this ignores them).
                    const tiles = Array.from(document.querySelectorAll('div[data-state]'));
                    
                    // Wordle has 30 tiles total (6 rows of 5). If they aren't loaded, return null and wait.
                    if (tiles.length < 30) return null;
                    
                    // Slice out the 5 tiles specifically for the current attempt
                    const startIndex = {attempt} * 5;
                    const rowTiles = tiles.slice(startIndex, startIndex + 5);
                    
                    let results = [];
                    rowTiles.forEach(tile => {{
                        const state = tile.getAttribute('data-state'); 
                        const letter = tile.textContent || '';
                        results.push({{ state: state, letter: letter.trim().toLowerCase() }});
                    }});
                    
                    return results;
                }}""")
                
                if row_data and len(row_data) == 5:
                    states = [tile['state'] for tile in row_data]
                    valid_states = ['correct', 'present', 'absent']
                    
                    # If all 5 tiles have finished flipping and have a final color, move on!
                    if all(state in valid_states for state in states):
                        break

                t.sleep(0.5)  # wait a bit before checking again

            print(f"Guess #{attempt + 1} processed: {row_data}")

            getBestWords()



if __name__ == "__main__":
    load_wordle()
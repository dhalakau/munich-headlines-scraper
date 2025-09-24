import requests
from bs4 import BeautifulSoup

URL = "https://www.sueddeutsche.de/"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def fetch_html(url: str) -> str:
    """
    Download the raw HTML text from a given URL.
    Returns it as a string.
    """
    # send an HTTP GET request with our fake browser header
    resp = requests.get(url, headers=HEADERS, timeout=15)

    # raise_for_status() throws an error if HTTP code is 4xx/5xx
    resp.raise_for_status()

    # resp.text contains the HTML of the page
    return resp.text

def extract_titles(html: str) -> list[str]:
    """
    Parse HTML with BeautifulSoup and extract all visible headlines.
    Returns a list of strings.
    """

    # create a BeautifulSoup parser object (using built-in Python parser)
    soup = BeautifulSoup(html, "html.parser")

    # CSS selectors to try — each one targets possible headline formats
    selectors = [
        "h2", "h3",                 # most headlines are in h2/h3 tags
        "article h2", "article h3", # headlines inside <article> blocks
        ".teaser__title", ".headline",  # specific class names used on SZ
        '[data-testid="headline"]', # fallback selector sometimes used
    ]

    # --- storage ---
    titles = []   # list for cleaned, unique headlines
    seen = set()  # set to avoid duplicates (fast lookup)

    # helper: collapse whitespace (" \n " → " ")
    def clean(txt: str) -> str:
        return " ".join(txt.split())

    # loop through each selector
    for sel in selectors:
        # soup.select(sel) returns all elements matching the CSS selector
        for el in soup.select(sel):
            # get the text inside the element, strip leading/trailing spaces
            text = clean(el.get_text(strip=True))

            # filter out very short strings (like nav items "Home", "SZ")
            if len(text) >= 8 and text not in seen:
                seen.add(text)      # mark this headline as seen
                titles.append(text) # add it to our list

    return titles

def main():
    """
    Main program:
    1. fetch the page HTML
    2. extract titles
    3. print them nicely
    """

    # Step 1: download HTML
    html = fetch_html(URL)

    # Step 2: parse and extract all titles
    titles = extract_titles(html)

    # if no titles were found, print a message
    if not titles:
        print("No titles found (the page structure might have changed).")
        return

    # Step 3: print results
    print("Munich headlines:\n")
    for i, t in enumerate(titles, start=1):
        print(f"{i:2}. {t}")

if __name__ == "__main__":
    main()
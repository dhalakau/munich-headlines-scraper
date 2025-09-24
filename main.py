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

    return resp.text

def extract_titles(html: str) -> list[str]:
    """
    Parse HTML with BeautifulSoup and extract all visible headlines.
    Returns a list of strings.
    """

    soup = BeautifulSoup(html, "html.parser")

    selectors = [
        "h2", "h3",                 # most headlines are in h2/h3 tags
        "article h2", "article h3", # headlines inside <article> blocks
        ".teaser__title", ".headline",  # specific class names used on SZ
        '[data-testid="headline"]', # fallback selector sometimes used
    ]

    # storage
    titles = []
    seen = set()  #(fast lookup)

    # helper: collapse whitespace (" \n " → " ")
    def clean(txt: str) -> str:
        return " ".join(txt.split())

    # loop through each selector
    for sel in selectors:
        for el in soup.select(sel):
            text = clean(el.get_text(strip=True))

            if len(text) >= 8 and text not in seen:
                seen.add(text)
                titles.append(text)

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
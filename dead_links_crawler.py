import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor


def get_broken_links(url):
    # Set root domain.
    root_domain = "https://wiki.basgrospoing.fr"

    # Internal function for validating HTTP status code.
    def _validate_url(url):
        r = requests.head(url)
        if r.status_code == 404:
            broken_links.append(url)

    # Make request to URL.
    data = requests.get(url).text

    # Parse HTML from request.
    soup = BeautifulSoup(data, features="html.parser")

    # Create a list containing all links with the root domain.
    
    links = []
    for link in soup.find_all("a"):
        links.append(link.get("href"))
    # links = [link.get("href") for link in soup.find_all("a") if f"//{root_domain}" in link.get("href")]
    # print(links)

    # Initialize list for broken links.
    broken_links = []

    # Loop through links checking for 404 responses, and append to list.
    with ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(_validate_url, links)

    return broken_links


l = get_broken_links("https://wiki.basgrospoing.fr/index.php/Accueil")

print(l)

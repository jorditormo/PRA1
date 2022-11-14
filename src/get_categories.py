from bs4 import BeautifulSoup
import requests


def get_categories(url: str) -> dict:
    """
    Get categories

    PARAMETERS
    ----------
    url: string
        Any string

    Returns
    -------
    dictionary
        key: commodity
        value: category
    """
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
               "Accept-Encoding": "gzip, deflate, sdch, br",
               "Accept-Language": "en-US,en;q=0.8",
               "Cache-Control": "no-cache",
               "dnt": "1",
               "Pragma": "no-cache",
               "Upgrade-Insecure-Requests": "1",
               "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1\
               07.0.0.0 Safari/537.36'}
    page = requests.get(url, headers)
    soup = BeautifulSoup(page.content, 'html.parser')
    menu = soup.findAll('li', {'class': 'panel panel-default dropdown'})
    categories = {}
    for item in menu:
        submenu = item.text.split('\n')
        for i in range(len(submenu)):
            if i == 0:
                cat = submenu[0]
            else:
                categories[submenu[i]] = cat
    return categories

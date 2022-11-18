import pandas as pd
import requests
from bs4 import BeautifulSoup as soup


def scraper(urls: list, cats: dict):
    """
    Get categories

    PARAMETERS
    ----------
    urls: list
        list of url to web scrap
    cats: dict
        dictionary

    Returns
    -------
    DataFrame
        dataset
    """
    df = pd.DataFrame(columns=['commodity', 'description', 'source', 'unit', 'category', 'month', 'price'])
    for url in urls:
        req = requests.get(url)
        pagesoup = soup(req.text, "html.parser")
        source = pagesoup.findAll('a', {"id": "linkSource"})
        source = source[0].text
        desc = pagesoup.findAll('span', {"id": "lblSeriesDescription"})
        desc = desc[0].text
        unit = pagesoup.findAll('span', {'id': 'lblSeriesUnit'})
        unit = unit[0].text
        comm = pagesoup.find('div', {'id': 'nav'})
        comm = list(list(comm)[-2])[0]

        table = pagesoup.find('table', {"class": "tblData"})
        dict_dataset = {'commodity': comm,
                        'description': desc,
                        'source': source,
                        'unit': unit,
                        'category': cats[comm],
                        'month': [],
                        'price': []}
        for row in table.findAll("tr"):
            cells = row.findAll('td')
            if len(cells) != 0:
                month = cells[0].find(text=True)
                price = cells[1].find(text=True)
                dict_dataset['month'].append(month)
                dict_dataset['price'].append(price)

        df1 = pd.DataFrame(dict_dataset)
        df = pd.concat([df, df1], ignore_index=True)
    df = df.replace(',', '_', regex=True)
    df = df.replace(';', '_', regex=True)
    return df

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
import argparse

class IndexMundiScrapper:
    def __init__(self):
        self.url = 'https://www.indexmundi.com/commodities/'
        self.headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                        "Accept-Encoding": "gzip, deflate, sdch, br",
                        "Accept-Language": "en-US,en;q=0.8",
                        "Cache-Control": "no-cache",
                        "dnt": "1",
                        "Pragma": "no-cache",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/1\
                   07.0.0.0 Safari/537.36'}
        logging.info(f"Crawling on {self.url}")

    def get_urls(self, currency: str, years_interval: str) -> list:
        """
        Get url list

        PARAMETERS
        ----------

        url: string
            Any string
        currency: string
            usd, eur
        years_interval: string
            timeframe, in years

        Returns
        -------
        list
            List of urls, by commodity.
        """
        logging.info("Finding the commodities urls")
        urls = []

        page = requests.get(self.url, self.headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        tags = soup.find_all('a', href=True)
        for a in tags:
            if "?commodity" in a['href'] \
                    and "currency" not in a['href'] \
                    and "index" not in a['href']:
                commodity_url = self.url + a['href']
                t0 = time.time()
                subpage = requests.get(commodity_url, self.headers)
                response_delay = time.time() - t0
                # time.sleep(10 * response_delay)
                subsoup = BeautifulSoup(subpage.content, 'html.parser')
                years_id = "l" + years_interval + "y"
                subtags = subsoup.find_all('a', id=years_id, href=True)
                for suba in subtags:
                    curr_soup = subsoup.find_all('select', id="listCurrency")

                    for option in curr_soup:
                        for value in option:
                            if value.get_text() == currency:
                                complete_url = self.url + suba['href'] + "&currency=" + value['value']
                                urls.append(complete_url)
                                logging.info(f"Url saved: {complete_url}")

        return urls

    def get_categories(self) -> dict:
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
        logging.info("Obtaining the commodities categories")
        page = requests.get(self.url, self.headers)
        soup = BeautifulSoup(page.content, 'html.parser')
        menu = soup.findAll('li', {'class': 'panel panel-default dropdown'})
        categories = {}
        for item in menu:
            submenu = [category for category in item.text.split('\n') if category != '' ]
            for i in range(len(submenu)):
                if i == 0:
                    cat = submenu[0]
                else:
                    categories[submenu[i]] = cat
        logging.info("The following categories were found:")
        logging.info(set(categories.values()))
        return categories

    def scrapper(self, urls: list, cats: dict):
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
        logging.info("Start scrapping the commodities urls")
        df = pd.DataFrame(columns=['commodity', 'description', 'source', 'unit', 'category', 'month', 'price'])
        for url in urls:
            t0 = time.time()
            req = requests.get(url, self.headers)
            response_delay = time.time() - t0
            # time.sleep(10 * response_delay)
            pagesoup = BeautifulSoup(req.text, "html.parser")
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
            logging.info(f"Commodity {comm} data saved")

            df1 = pd.DataFrame(dict_dataset)
            df = pd.concat([df, df1], ignore_index=True)
            logging.info(f"Saved data of {len(df)} commodities")

        return df

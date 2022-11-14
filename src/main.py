from get_urls import get_urls
from get_categories import get_categories
from scraper import scraper


url = 'https://www.indexmundi.com/commodities/'
urls = get_urls(url, "US Dollar", "20")
cats = get_categories(url)
df = scraper(urls, cats)
df.to_csv(r'\csv\dataset.csv', index=False)



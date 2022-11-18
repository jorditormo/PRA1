from IndexMundiScrapper import IndexMundiScrapper
import logging
import argparse
import os

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')
YEARS_RANGES = ["5", "10", "15", "20", "25", "30"]
CURRENCIES = ["Algerian Dinar",
              "Argentine Peso",
              "Australian Dollar",
              "Bahraini Dinar",
              "Baht",
              "Bolivar Fuerte",
              "Brazilian Real",
              "Brunei Dollar",
              "Canadian Dollar",
              "Chilean Peso",
              "Colombian Peso",
              "Czech Koruna",
              "Danish Krone",
              "Euro",
              "Forint",
              "Iceland Krona",
              "Indian Rupee",
              "Iranian Rial",
              "Kuwaiti Dinar",
              "Malaysian Ringgit",
              "Mauritius Rupee",
              "Mexican Peso",
              "Nepalese Rupee",
              "New Israeli Sheqel",
              "New Zealand Dollar",
              "Norwegian Krone",
              "Nuevo Sol",
              "Pakistan Rupee",
              "Philippine Peso",
              "Pound Sterling",
              "Pula",
              "Qatari Riyal",
              "Rand",
              "Rial Omani",
              "Rupiah",
              "Russian Ruble",
              "Russian Ruble",
              "Saudi Riyal",
              "Singapore Dollar",
              "Sri Lanka Rupee",
              "Swedish Krona",
              "Swiss Franc",
              "Tenge",
              "Trinidad and Tobago Dollar",
              "Tunisian Dinar",
              "UAE Dirham",
              "Uruguayan Peso",
              "US Dollar",
              "Won",
              "Yen",
              "Yuan Renminbi",
              "Zloty"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--currency", help="Enter the currency", choices=CURRENCIES)
    parser.add_argument("--years_range", help="Enter the years range", choices=YEARS_RANGES)
    args = parser.parse_args()
    logging.info(args)
    scrap = IndexMundiScrapper()
    urls = scrap.get_urls(args.currency, args.years_range)
    cats = scrap.get_categories()
    df = scrap.scrapper(urls, cats)

    df.to_csv(r'..\dataset\dataset.csv', index=False, sep="\t")
    #df.to_csv(os.path.join('..', 'dataset', 'dataset.csv'), index=False)
    logging.info("The data is exported in a csv file")

if __name__ == "__main__":
    main()

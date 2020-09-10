
from bs4 import BeautifulSoup
import ssl
import os
import time
from urllib.request import Request, urlopen
from itertools import chain

from Backend.UPK import obtain_sql_list, obtain_sql_value, modify_for_sql, decimal_places, specific_sql_statement


def update_stock_price(database):
    tic = time.perf_counter()
    # For ignoring SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # obtain filtered list of ticker Symbols --- removes symbols that are not on the NYSE
    filtered_ticker_symbols = ['PRPIX', 'PRTAX', 'PPL', 'EXC', 'F', 'WFC', 'KWR', 'T', 'TLRY', 'ACB', 'ODP', 'KO', 'CGC', 'VFFVX']
    stock_price_dict = {}

    ticker = 'PRPIX'
    url = f'https://finance.yahoo.com/quote/{ticker.upper()}?p={ticker.upper()}&.tsrc=fin-srch'
    req = Request(url, headers={'User-Agent': 'Chrome/84.0.4147.89'})
    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html.parser')

    for span in soup.findAll('span',
                             attrs={'class': 'Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)'
                             }):
        stock_price_dict[ticker] = span.text.strip()
        print(f"{ticker} stock price: {stock_price_dict[ticker]} - for ticker")

    toc = time.perf_counter()
    print(f'Code took {toc - tic:0.4f} seconds')


if __name__ == '__main__':
    tic = time.perf_counter()
    database = os.path.join(os.getcwd(), '..', 'data/account/b8aem6j45m5r36ghs.db')
    update_stock_price(database)
    toc = time.perf_counter()
    print(f'Code took {toc - tic:0.4f} seconds')
    print("Done")

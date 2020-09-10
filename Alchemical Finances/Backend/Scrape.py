
import ssl
import os
import time
import requests
import json
from itertools import chain

from Backend.UPK import obtain_sql_list, obtain_sql_value, modify_for_sql, decimal_places, specific_sql_statement


def update_stock_price(database):
    tic = time.perf_counter()
    # obtain filtered list of ticker Symbols --- removes symbols that are not on the NYSE
    filtered_ticker_symbols = []
    filtered_account_ledgers = []
    stock_price_dict = {}

    equity_tickers, equity_ledgers = obtain_symbols("Equity", database)
    for company in range(0, len(equity_tickers)):
        filtered_ticker_symbols.append(equity_tickers[company])
        filtered_account_ledgers.append(equity_ledgers[company])

    retirement_tickers, retirement_ledgers = obtain_symbols("Retirement", database)
    for company in range(0, len(retirement_tickers)):
        filtered_ticker_symbols.append(retirement_tickers[company])
        filtered_account_ledgers.append(retirement_ledgers[company])

    ticker_ledger_dict = {}

    for ticker in range(0, len(filtered_ticker_symbols)):
        ticker_ledger_dict[filtered_ticker_symbols[ticker]] = filtered_account_ledgers[ticker]

    for ticker in filtered_ticker_symbols:
        market_value = scrape_value(ticker)
        stock_price_dict[ticker] = market_value

    for ticker in filtered_ticker_symbols:
        share_balance_statement = f"SELECT SUM(Purchased - Sold) FROM {ticker_ledger_dict[ticker]}"
        stock_price = decimal_places(float(stock_price_dict[ticker]), 4)
        share_balance_raw = (obtain_sql_value(share_balance_statement, database)[0])
        if share_balance_raw is None:
            share_balance_raw = 0.0
        share_balance = decimal_places(share_balance_raw, 2)
        account_balance = decimal_places((share_balance * stock_price), 2)
        update_balance_statement = f"UPDATE Account_Summary SET Balance='{account_balance}' WHERE Ticker_Symbol='{ticker}'"

        if ticker in equity_tickers:
            update_stock_price_statement = f"UPDATE Equity_Account_Details SET Stock_Price='{stock_price}' WHERE Ticker_Symbol='{ticker}'"
            specific_sql_statement(update_stock_price_statement, database)
        elif ticker in retirement_tickers:
            update_stock_price_statement = f"UPDATE Retirement_Account_Details SET Stock_Price='{stock_price}' WHERE Ticker_Symbol='{ticker}'"
            specific_sql_statement(update_stock_price_statement, database)
        else:
            pass

        specific_sql_statement(update_balance_statement, database)
        # print(f'{ticker}:   {stock_price}:    {account_balance}')
    toc = time.perf_counter()
    print(f'Code took {toc - tic:0.4f} seconds')


def obtain_symbols(parenttype, database):
    statement = f"SELECT Ticker_Symbol, ID FROM Account_Summary WHERE ParentType='{parenttype}'"
    raw_data = obtain_sql_list(statement, database)
    ticker_symbols = [x[0] for x in raw_data]
    account_ledgers = [modify_for_sql(x[1]) for x in raw_data]

    filtered_ticker_symbols = []
    filtered_account_ledgers = []

    for ticker in range(0, len(ticker_symbols)):
        try:
            int(ticker_symbols[ticker])
        except ValueError:
            filtered_ticker_symbols.append(ticker_symbols[ticker])
            filtered_account_ledgers.append(account_ledgers[ticker])
        else:
            pass

    return filtered_ticker_symbols, filtered_account_ledgers


def scrape_value(ticker):
    # For ignoring SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = f'https://api.tiingo.com/tiingo/daily/{ticker}/prices?token=91b842491753e83361bb2a1a58285cfcea87f423'
    headers = {
        'Content-Type': 'application/json'
    }
    req = requests.get(url, headers=headers)
    raw_data = json.loads(req.text)
    ticker_price = raw_data[0]['close']
    return ticker_price


if __name__ == '__main__':
    tic = time.perf_counter()
    database = os.path.join(os.getcwd(), '..', 'data/account/b8aem6j45m5r36ghs.db')
    update_stock_price(database)
    toc = time.perf_counter()
    print(f'Code took {toc - tic:0.4f} seconds')
    print("Done")


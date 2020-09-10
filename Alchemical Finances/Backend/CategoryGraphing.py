import os
import sqlite3

from sqlite3 import Error
from datetime import datetime

from Backend.UPK import obtain_sql_list, cash_format

import numpy as np
import pandas as pd
import matplotlib as plot


def available_years(database, account):
    statement = f"SELECT Transaction_Date, Category, Debit, Credit FROM {account}"
    raw_data = obtain_sql_list(statement, database)

    years = []
    [years.append(tup[0][:4]) for tup in raw_data if tup[0][:4] not in years]

    categories = []
    [categories.append(tup[1]) for tup in raw_data if tup[1] not in categories]

    return years, categories, raw_data


def generate_categories_bgraph(databse, account, year, start_month, end_month, category):
    pass


if __name__ == "__main__":
    database = os.path.join(os.getcwd(), '..', 'data/account/b8aem6j45m5r36ghs.db')
    # User chooses account
    account = input("Which Account would you like to Review (Amazon_Prime_Card): ")

    # Chosen account determines available years
    years, categories, raw_data = available_years(database, account)

    # User Chooses which year
    user_year = input(f"Which year are you interested in: {years}? ")
    while user_year not in years:
        user_year = input(f"Select a provided year: {years} ")

    target_year = user_year

    # User chooses start and end month
    months = [str(x) for x in range(1, 13, 1)]
    start_month = input("What is the starting month of interest: (1 - 12)? ")
    while start_month not in months:
        start_month = input("Try Again, what is the starting month of interest: (1 - 12)? ")

    remaining_months = [str(x) for x in range(int(start_month), 13, 1)]
    end_month = input(f"What is the end month of interest: ({remaining_months[0]} - 12)? ")
    while end_month not in remaining_months:
        end_month = input(f"Please input an integer between {start_month} and 12? ")

    target_months = []
    if start_month == end_month:
        target_months.append(int(start_month))
    else:
        target_months = [x for x in range(int(start_month), int(end_month) + 1, 1)]

    # User Determines all or specific categories based upon account
    target_cats = []
    options = ["All", "Specific"]
    category_choice = input("All Spending Categories or Specific Category? (All/Specific) ")

    while category_choice not in options:
        category_choice = input("'All' or 'Specific': ")

    if category_choice == "All":
        [target_cats.append(x) for x in categories]   

    else: # Specific
        print(categories)
        user_cat = input("From the preceding Categories, which one is of interest? ")

        while user_cat not in categories:
            user_cat = input("Which Category from the previously provided list? ")

        target_cats.append(user_cat)

    # DataFrame construction for All Categories over x-period of time.
    if category_choice == "All":
        cat_transactions = {}
        cat_sum = {}
        cat_count = {}
        for cat in categories:
            cat_transactions[cat] = []
            cat_sum[cat] = 0
            cat_count[cat] = 0

        [cat_transactions[tup[1]].append(tup) for tup in raw_data if tup[0][:4] == target_year and int(tup[0][5:7]) in target_months]

        for cat in cat_transactions:
            for transaction in cat_transactions[cat]:
                debit = transaction[2]
                credit = transaction[3]

                if debit == '':
                    debit = 0
                if credit == '':
                    credit = 0

                cat_sum[cat] += float(credit) - float(debit)
                cat_count[cat] += 1

        category_data = {
            'Total Spent': [cat_sum[x] for x in cat_transactions],
            'Total Transactions': [cat_count[x] for x in cat_transactions],
        }

        category_frame = pd.DataFrame(category_data)
        category_frame.index = [x for x in cat_transactions]

    # DataFrame construction for a Specific period of time.
    else: # Specific
        month_transactions = {}
        month_sum = {}
        month_count = {}
        for month in target_months:
            month_transactions[month] = []
            month_sum[month] = 0
            month_count[month] = 0

        for tup in raw_data:
            if tup[0][:4] == target_year:
                if int(tup[0][5:7]) in target_months and tup[1] in target_cats:
                    month_transactions[int(tup[0][5:7])].append(tup)
                else:  # Other Category
                    pass
            else:  # Wrong year
                pass

        print(month_transactions)

        for month in month_transactions:
            for transaction in month_transactions[month]:
                debit = transaction[2]
                credit = transaction[3]

                if debit == '':
                    debit = 0
                if credit == '':
                    credit = 0

                month_sum[month] += float(credit) - float(debit)
                month_count[month] += 1

        month_data = {
            'Total Spent': [month_sum[x] for x in month_transactions],
            'Total Transactions': [month_count[x] for x in month_transactions]
        }

        month_frame = pd.DataFrame(month_data)
        month_frame.index = [x for x in month_transactions]

    if category_choice == "All":
        print(category_frame)
    else:
        print(month_frame)
    # Program generates graph


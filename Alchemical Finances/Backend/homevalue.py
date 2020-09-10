from bs4 import BeautifulSoup
import ssl
import os
import time
from urllib.request import Request, urlopen
from itertools import chain

# from Backend.UPK import obtain_sql_list, obtain_sql_value, modify_for_sql, decimal_places, specific_sql_statement

# https://www.redfin.com/PA/Ardmore/13-Chatham-Rd-19003/home/38490284


def replace_letter(target):
    modified_target = ""
    for letter in target:
        if letter == " ":
            replaced_letter = "-"
            modified_target += replaced_letter
        else:
            modified_target += letter
    return modified_target


def obtain_address():
    street = input("Address: ")
    modified_street = replace_letter(street)
    county = input("County: ")
    modified_county = replace_letter(county)
    state = input("Two Letter State: ")
    zipcode = input("Zip Code: ")
    redfin_id = input("RedFin ID: ")
    # https://www.redfin.com/PA/Ardmore/13-Chatham-Rd-19003/home/38490284
    url = f"https://www.redfin.com/{state}/{modified_county}/{modified_street}-{zipcode}/home/{redfin_id}/"
    return url


def obtain_homevalue(url):
    redfin_url = url
    req = Request(redfin_url, headers={'User-Agent': 'chrome/83.0.4103.116'})
    webpage = urlopen(req).read()

    soup = BeautifulSoup(webpage, 'html.parser')
    print(soup.findAll('div', attrs={"class": 'value font-size-large'}))
    container = soup.findAll('div', attrs={"class": 'value font-size-large'})
    print(container)
    container = str(container)
    value = container[37:-7]
    updated_value = ""
    for dig in value:
        if dig == ",":
            pass
        else:
            updated_value += dig
    return updated_value


if __name__ == "__main__":
    url = obtain_address()
    print(url)
    estimate = obtain_homevalue(url)
    print(f'{estimate}')

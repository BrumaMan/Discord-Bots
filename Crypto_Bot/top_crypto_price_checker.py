from ast import Try
from bs4 import BeautifulSoup
import requests
from time import sleep
import random

url = "https://coinmarketcap.com/"
result = requests.get(url).text
doc = BeautifulSoup(result, "html.parser")

tbody = doc.tbody
trs = tbody.contents

pages = doc.find(class_="pagination")
page_data = str(pages)
num_of_pages = int(str(page_data).split("<li")[7].split(">")[2][:-3])

market_caps = doc.find(class_="sc-1ow4cwt-1 ieFnWP")
market = str(market_caps).split(">")[1][:-6]
# print(market)


def top_ten_crypto():
    id = 1
    print("---Top crypto from coinmarketcap.com---")
    print()
    for tr in trs[:10]:
        name, price = tr.contents[2:4]
        market_cap = tr.contents[6]
        coin_initial = str(name).split("class")[9].split(">")[1][:-3]
        coin_name = name.p.string
        coin_price = price.span.string
        coin_market_cap = str(market_cap).split(">")[3][:-6]
        print(f"Number: {id}")
        print(f"---{coin_initial}---")
        print(f"Name: {coin_name}")
        print(f"Price: {coin_price}")
        print(f"Market cap: {coin_market_cap}")
        print()
        id += 1


def top_hundred_crypto():
    id = 11
    for tr in trs[10:]:
        name, price = tr.contents[2:4]
        #market_cap = tr.contents[6]
        doc_name = name.a
        doc_price = price.span
        coin_name = str(doc_name).split("span")[3][1:-2]
        symbol = str(doc_name).split("span")[5][23:-2]
        currency = str(doc_price).split(">")[1][0]
        coin_price = str(doc_price).split(">")[2][:4]
        #coin_market_cap = str(market_cap).split(">")[3][:-6]
        print(f"Number: {id}")
        print(f"---{symbol}---")
        print(f"Name: {coin_name}")
        print(f"Price: {currency}{coin_price}")
        #print(f"Market cap: {coin_market_cap}")
        print()
        id += 1


def all_crypto():
    id = 1
    for page in range(1, num_of_pages + 1):
        url = f"https://coinmarketcap.com/?page={page}"
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")
        tbody = doc.tbody
        trs = tbody.contents
        for tr in trs:
            name, price = tr.contents[2:4]
            doc_name = name.a
            doc_price = price.span
            try:
                symbol = str(doc_name).split("span")[5][23:-2]
                coin_name = str(doc_name).split("span")[3][1:-2]
                currency = str(doc_price).split(">")[1][0]
                coin_price = str(doc_price).split(">")[2][:4]
                print(f"Number: {id}")
                print(f"---{symbol}---")
                print(f"Name: {coin_name}")
                print(f"Price: {currency}{coin_price}")
                print()

            except Exception:
                coin_initial = str(name).split("class")[9].split(">")[1][:-3]
                coin_name = name.p.string
                coin_price = price.span.string

                print(f"Number: {id}")
                print(f"---{coin_initial}---")
                print(f"Name: {coin_name}")
                print(f"Price: {coin_price}")
                print()
            id += 1


def random_crypto():
    rand_page = random.randint(1, 91)
    rand_num1 = random.randint(1, 99)
    for page in range(rand_page, num_of_pages + 1):
        url = f"https://coinmarketcap.com/?page={page}"
        result = requests.get(url).text
        doc = BeautifulSoup(result, "html.parser")
        tbody = doc.tbody
        trs = tbody.contents
        for tr in trs[rand_num1:101]:
            name, price = tr.contents[2:4]
            doc_name = name.a
            doc_price = price.span
            try:
                symbol = str(doc_name).split("span")[5][23:-2]
                coin_name = str(doc_name).split("span")[3][1:-2]
                currency = str(doc_price).split(">")[1][0]
                coin_price = str(doc_price).split(">")[2][:4]

                # print(f"---{symbol}---")
                # print(f"Name: {coin_name}")
                # print(f"Price: {currency}{coin_price}")

            except Exception:
                coin_initial = str(name).split("class")[9].split(">")[1][:-3]
                coin_name = name.p.string
                coin_price = price.span.string

                # print(f"---{coin_initial}---")
                # print(f"Name: {coin_name}")
                # print(f"Price: {coin_price}")

            try:
                return f"Name: {coin_name} ({symbol}). Price: {currency}{coin_price}"
            except Exception:
                return f"Name: {coin_name} ({coin_initial}). Price: {coin_price}"


def top_crypto():
    for tr in trs[:10]:
        name, price = tr.contents[2:4]
        market_cap = tr.contents[6]
        coin_initial = str(name).split("class")[9].split(">")[1][:-3]
        coin_name = name.p.string
        coin_price = price.span.string
        coin_market_cap = str(market_cap).split(">")[3][:-6]
        # print(f"---{coin_initial}---")
        # print(f"Name: {coin_name}")
        # print(f"Price: {coin_price}")
        # print(f"Market cap: {coin_market_cap}")
        # print()

        return f"Name: {coin_name} ({coin_initial}). Price: {coin_price}. Market cap: {coin_market_cap}"


# rand = top_crypto()
# print(rand)

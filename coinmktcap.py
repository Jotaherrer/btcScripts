from bs4 import BeautifulSoup
import requests, json, time
import pandas as pd

url_all = 'https://coinmarketcap.com/all/views/all'
url = 'https://coinmarketcap.com'
response = requests.get(url)

cmc = requests.get('https://coinmarketcap.com')
soup = BeautifulSoup(cmc.content, 'html.parser')

soup.title

print(soup.prettify())

data = soup.find('script', id='__NEXT_DATA__', type='application/json')

type(data.contents[0])
len(data.contents[0])
data.contents[0][-10:]

coin_data = json.loads(data.contents[0])
type(coin_data)
len(coin_data)
coin_data.keys()
coin_data['props']
type(coin_data['props'])
coin_data['props'].keys()
coin_data['props']['initialState']

listings = coin_data['props']['initialState']['cryptocurrency']['listingLatest']['data']
type(listings)
len(listings)

coins = {}

for i in listings:
    coins[str(i['id'])] = i['slug']

coins.keys()
coins['1']
coins['1027']
coins['1839']
coins['825']
coins['6636']
coins['2405']

# Historical Data
"""
TEMPLATE:
https://coinmarketcap.com/currencies/[slug]/historical-data/?start=[YYYYMMDD]&end=[YYYYMMDD]
"""
for i in coins:
    page = requests.get('https://coinmarketcap.com/currencies/{coins[i]}/historical-data/?start=[20200101]&end=[20200630]')
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    historical_data = json.loads(data.contents[0])
    quotes = historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical']

    #quotes = historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]['quotes']
    #info = historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical'][i]

type(historical_data)
historical_data.keys()
historical_data['props']['initialState']['cryptocurrency']['ohlcvHistorical']
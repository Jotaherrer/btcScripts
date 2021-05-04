import pandas as pd
import keyboard, math, os, time, datetime as dt
import mplfinance as mpl
import matplotlib.pyplot as plt

from binance.client import Client
from binance.websockets import BinanceSocketManager
from twisted.internet  import reactor

from keys import pkey, skey

"""
https://acodigo.blogspot.com/2021/01/python-binance-api.html
"""

# API KEYS
API_KEY, API_SECRET = pkey, skey

# CREATE INSTANCE
client = Client(API_KEY, API_SECRET)

# GET AND FORMAT PRICES
prices = client.get_all_tickers()
prices_dict = {}
for item in prices:
    coin, price = item.values()
    prices_dict[coin] = float(price)

prices_dict['XLMBTC']

# CREATE DF TO CONSOLIDATE COINS AND PRICES
prices_df = pd.DataFrame(prices_dict.items())
prices_df.rename(columns={0:'Ticker', 1:"Price"}, inplace=True)


tickers = prices_df.Ticker.values
tickers2 = [x[-3:] for x in tickers]
tickers2 = pd.DataFrame(tickers2)
tickers2[0].unique()

# CREATE DFS FOR CERTAIN COINS
btc_prices = prices_df[prices_df['Ticker'].str.contains("BTC")].reset_index(drop=True)
usdt_prices = prices_df[prices_df['Ticker'].str.contains("USDT")].reset_index(drop=True)
usd_prices = prices_df[prices_df['Ticker'].str.contains('USD') & [x[-1] != "T" for x in prices_df['Ticker']]].reset_index(drop=True)
bnb_prices = prices_df[prices_df["Ticker"].str.contains("BNB")].reset_index(drop=True)
eth_prices = prices_df[prices_df["Ticker"].str.contains("ETH")].reset_index(drop=True)

usdt_tickers = usdt_prices['Ticker'].values
usdt_tickers = [x[:-4] for x in usdt_tickers]
usdt_values = usdt_prices['Price'].values
usdt_modified = pd.DataFrame({'Ticker':usdt_tickers, "Price USDT":usdt_values})
usd_tickers = usd_prices['Ticker'].values
usd_tickers = [x[:-4] for x in usd_tickers]
usd_values = usd_prices['Price'].values
usd_modified = pd.DataFrame({"Ticker":usd_tickers, "Price USD": usd_values})
merged_usd = usd_modified.merge(usdt_modified, on='Ticker')

"""
merged_usd['Spread'] = merged_usd['Price USD'] / merged_usd['Price USDT'] - 1.
merged_usd_mod = merged_usd[(merged_usd['Spread'] < 0.2) & (merged_usd['Spread'] > -0.2)]
merged_usd2 = merged_usd[~(merged_usd['Spread'] < 0.2) & (merged_usd['Spread'] > -0.2)]
"""

## 4 HOUR CHART
klines_btc = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_4HOUR, "15 day ago UTC")
type(klines_btc)
klines_btc[0]

chart_df = pd.DataFrame(klines_btc, columns=["Date", 'Open', 'High', 'Low', "Close", "Volume",
                                             "Close Time", "Quote Asset Volume", "N. Trades",
                                             "Taker buy base asset volume", "Taker buy quote asset volume",
                                             'Ignore'])
chart_df = chart_df.drop(chart_df.columns[[6,7,8,9,10,11]],axis=1)
chart_df["Date"] = pd.to_datetime(chart_df['Date'], unit='ms')
chart_df.set_index('Date', inplace=True, drop=True)

chart_df['Open'] = chart_df['Open'].astype(float)
chart_df['High'] = chart_df['High'].astype(float)
chart_df['Low'] = chart_df['Low'].astype(float)
chart_df['Close'] = chart_df['Close'].astype(float)
chart_df['Volume'] = chart_df['Volume'].astype(float)

mpl.plot(chart_df, type='candle', style='binance', volume=True)

chart_df['Spread 4HR'] = chart_df['High']/chart_df['Low']-1
fig, ax = plt.subplots()
ax.plot(chart_df['Close'], color='orange', marker='o', label='Price')
ax.set_ylabel('BTC Price')
ax2 = ax.twinx()
ax2.plot(chart_df['Spread 4HR'], color='blue', marker='*', label='Spread')
ax2.set_ylabel('BTC Spread')
plt.legend()
plt.show()

chart_df['var'] =


# 1 MINUTE CHART
klines_btc2 = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1MINUTE, "15 day ago UTC")
chart_df2 = pd.DataFrame(klines_btc2, columns=["Date", 'Open', 'High', 'Low', "Close", "Volume",
                                              "Close Time", "Quote Asset Volume", "N. Trades",
                                              "Taker buy base asset volume", "Taker buy quote asset volume",
                                              'Ignore'])
chart_df2 = chart_df2.drop(chart_df2.columns[[6,7,8,9,10,11]],axis=1)
chart_df2["Date"] = pd.to_datetime(chart_df2['Date'], unit='ms')
chart_df2.set_index('Date', inplace=True, drop=True)

chart_df2['Open'] = chart_df2['Open'].astype(float)
chart_df2['High'] = chart_df2['High'].astype(float)
chart_df2['Low'] = chart_df2['Low'].astype(float)
chart_df2['Close'] = chart_df2['Close'].astype(float)
chart_df2['Volume'] = chart_df2['Volume'].astype(float)

chart_df2['Spread'] = chart_df2['High']/chart_df2['Close']-1

fig2, ax3 = plt.subplots()
ax3.plot(chart_df2['Close'], color='orange', marker='o', label='Price')
ax3.set_ylabel('BTC Price')
ax4 = ax3.twinx()
ax4.plot(chart_df2['Spread'], color='blue', marker='*', label='Spread')
ax4.set_ylabel('BTC Spread')
plt.legend()
plt.show()


## HISTORICAL DATA - DAILY
btc_daily = client.get_historical_klines('BTCUSDT', Client.KLINE_INTERVAL_1DAY, "5 years ago UTC")
len(btc_daily)
btc_daily[0]
btc_daily_df = pd.DataFrame(btc_daily, columns=["Date", "Open", "High", "Low", "Close", "Volume",
                                                "Close Time", "Quote Asset Volume", "Num. Trades",
                                                "T1", "T2", "Ignore"])
btc_daily_df = btc_daily_df.drop(btc_daily_df.columns[[7,9,10,11]], axis=1)
btc_daily_df['Date'] = pd.to_datetime(btc_daily_df['Date'], unit='ms')
btc_daily_df['Close Time'] = pd.to_datetime(btc_daily_df['Close Time'], unit='ms')
btc_daily_df.set_index('Date', inplace=True, drop=True)


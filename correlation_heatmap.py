import pandas as pd
import pandas_datareader.data as pdr
import seaborn as sns
import datetime as dt
import numpy as np

## SETTING DATES
today = dt.datetime.today()
end = today.strftime('%Y-%m-%d')
start = dt.datetime.strptime('2019-01-01', '%Y-%m-%d')
start = start.strftime('%Y-%m-%d')

btc = pdr.DataReader('BTC-USD','yahoo',start=start, end=end)
bnb_btc = pdr.DataReader('BNB-BTC','yahoo',start=start, end=end)
xlm_btc = pdr.DataReader('XLM-BTC','yahoo',start=start, end=end)
eth_btc = pdr.DataReader('ETH-BTC','yahoo',start=start, end=end)
neo_btc = pdr.DataReader('NEO-BTC','yahoo',start=start, end=end)

ret_bnb = bnb_btc.loc[:,'Adj Close'].pct_change().dropna()
df_bnb = pd.DataFrame(ret_bnb)
ret_xlm = xlm_btc.loc[:,'Adj Close'].pct_change().dropna()
df_xlm = pd.DataFrame(ret_xlm)
ret_eth = eth_btc.loc[:,'Adj Close'].pct_change().dropna()
df_eth = pd.DataFrame(ret_eth)
ret_neo = neo_btc.loc[:,'Adj Close'].pct_change().dropna()
df_neo = pd.DataFrame(ret_neo)

### MOVING AVERAGES
ma_days = [10,20,50,200]
for ma in ma_days:
    col_name = "MA %s days" % (str(ma))
    btc[col_name] = btc['Adj Close'].rolling(window=ma, center=False).mean()

btc.loc[:,['Adj Close','MA 10 days','MA 20 days','MA 50 days','MA 200 days' ]].plot(legend=True)

### CRYPTO CORRS - HEATMAP
corr = ret_bnb.rolling('10D', min_periods=10).corr(ret_eth).plot()
corrs = np.corrcoef([ret_bnb,ret_eth,ret_neo,ret_xlm])
sns.heatmap(corrs,xticklabels=['BNB/BTC', 'ETH/BTC', 'NEO/BTC', 'XLM/BTC'],yticklabels=['BNB/BTC', 'ETH/BTC', 'NEO/BTC', 'XLM/BTC'],annot=True,cmap='Blues')

### BTC CORR - HEATMAP
ret_btc = btc.loc[:,'Adj Close'].pct_change().dropna()
corr_btc = np.corrcoef([ret_btc,ret_bnb,ret_eth,ret_neo,ret_xlm]) 
sns.heatmap(corr_btc,xticklabels=['BTC/USD','BNB/BTC', 'ETH/BTC', 'NEO/BTC', 'XLM/BTC'],yticklabels=['BTC/USD','BNB/BTC', 'ETH/BTC', 'NEO/BTC', 'XLM/BTC'],annot=True,cmap='Reds')

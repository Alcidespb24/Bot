import cbpro
import pandas as pd
from pathlib import Path
import time 
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import pytz
import itertools

client = cbpro.PublicClient()
client.get_product_trades(product_id='ETH-USD')

get_trades = client.get_product_trades(product_id='ETH-USD')

df = list(itertools.islice(get_trades, 100000))

df = pd.DataFrame(df[:-1])

df['price'] = pd.to_numeric(df['price'])
df['size'] = pd.to_numeric(df['size'])

df['trade_dollar_size'] = df['price'] * df['size']
df ['change_in_price'] = df['price'].diff()

df[['price', 'size','trade_dollar_size','change_in_price']].describe()

df['time']=pd.to_datetime(df['time'].astype(str))

df.drop(['trade_id'], axis=1)

first = True

#while True:
    #df
    #print(df)
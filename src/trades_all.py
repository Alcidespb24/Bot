import cbpro
import pandas as pd
from pathlib import Path
import time 
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
import pytz
import itertools
from tkinter import *
from tkinter import ttk
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')


client = cbpro.PublicClient()
client.get_product_trades(product_id='ETH-USD')


symbol = 'ETH-USD'

def trades (symbol):
    get_trades = client.get_product_trades(product_id=f'{symbol}')
    df = list(itertools.islice(get_trades, 1000))
    
    df = pd.DataFrame(df)
    df = pd.DataFrame(df[:-1])
    
    df['price'] = pd.to_numeric(df['price'])
    df['size'] = pd.to_numeric(df['size'])

    df['trade_dollar_size'] = df['price'] * df['size']
    df ['change_in_price'] = df['price'].diff()

    df ['change_in_size'] = df['size'].diff()

    df['trade_dollar_size'] = pd.to_numeric(df['price'])
    df['change_in_price'] = pd.to_numeric(df['size'])
    df['change_in_size'] = pd.to_numeric(df['price'])

    df[['price', 'size','trade_dollar_size','change_in_price']].describe()

    df.drop(['trade_id'], axis=1)
    
    df.loc[df['side'] == 'buy', 'size'] = df['size'] * -1
    df.loc[df['side'] == 'sell', 'size'] = df['size'] * 1
    
    df.to_csv(r"D:\Trading\Bot\Docs/ETHUSD Trades.csv",index=False)
    
    return(df)
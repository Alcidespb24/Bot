import pandas as pd
from pathlib import Path
import time
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import statistics
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import Dash, html, dcc
from sklearn.linear_model import LinearRegression
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

def trades_5m():
    df = pd.read_csv("D:\Trading\Bot\Docs/ETHUSD Trades.csv")
    
    df['time'] = df['time'].values.astype('datetime64[s]')
    
    df_5m = df.resample('5min', on='time').agg({'price':'mean', 'size':'sum','side':'count'}).rename(columns={'price':'average price','size': 'sum of size','side':'volume'})

    df_5m['change_in_price'] = df_5m['average price'].diff()
    df_5m['change_in_size'] = df_5m['sum of size'].diff()
    df_5m['change_in_volume'] = df_5m['volume'].diff()

    df_5m.to_csv(r"D:\Trading\Bot\Docs/ETHUSD Trades_5m.csv",index=True)
    
    return(df_5m)
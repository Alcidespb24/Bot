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

df = pd.read_csv("D:\Trading\Bot\Docs/ETHUSD Trades.csv")

df['time'] = df['time'].values.astype('datetime64[s]')

df_5m = df.resample('5min', on='time').agg({'price': 'mean', 'size': 'sum', 'side': 'count'}).rename(
    columns={'price': 'average price', 'size': 'sum of size', 'side': 'volume'})

df_5m['change_in_price'] = df_5m['average price'].diff()
df_5m['change_in_size'] = df_5m['sum of size'].diff()
df_5m['change_in_volume'] = df_5m['volume'].diff()

df_5m.to_csv(r"D:\Trading\Bot\Docs/ETHUSD Trades_5m.csv", index=True)

df_5m = pd.read_csv('D:\Trading\Bot\Docs/ETHUSD Trades_5m.csv')

fig_ps = px.scatter(df_5m, x='sum of size', y='average price',
                 size='volume', color='time', title='Average Price v Size')
fig_ps.update_layout(autosize=True)
fig_ps.show()

fig_pv = px.scatter(df_5m, x='volume', y='average price', color='time',
                 size='volume', title='Volume Distribution & Average Price')
fig_pv.update_layout(autosize=True)
fig_pv.show()

fig_vt = px.bar(df_5m, x='time', y='volume', color='average price',
             text='average price', title='Time & Volume Distribution Bars')
fig_vt.update_layout(autosize=True)
fig_vt.show()

fig_ch_ps = px.scatter(df_5m, x='change_in_size', y='change_in_price',
                 size='volume', color='time', title='Change in Price & Change in Size')
fig_ch_ps.update_layout(autosize=True)
fig_ch_ps.show()

df_5m = df_5m.round(2)

fig_wf = go.Figure(go.Waterfall(x=df_5m['time'],
                             y=df_5m['change_in_price'],
                             orientation='v',
                             textposition='outside',
                             text=df_5m['sum of size'],
                             hovertext=['x', 'y'],
                             decreasing={"marker": {
                                 "line": {"color": "red", "width": 2}}},
                             increasing={"marker": {"color": "Green"}},
                             ))
fig_wf.update_layout(autosize=True)
fig_wf.show()

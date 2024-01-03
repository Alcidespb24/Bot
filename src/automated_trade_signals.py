import pandas as pd
from main import *
from trades_eth import *

trades = trades_eth(20)

def automatic_trades():
    if(trades.df_eth['probability_up'] > 0.80):
        open_position("ETH-USD", "Buy", 100)
    elif(trades.df_eth['probability_down'] > 0.80):
        open_position("ETH-USD", "Sell", 100)

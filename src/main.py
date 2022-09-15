import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from pylab import mpl, plt
import pandas_ta as ta
from sklearn import datasets, linear_model
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from gather_data_function import *
from mt5_init_function import *

init()

def open_position(
    Symbol, order_type, size, tp_distance=None, stop_distance=None, comment=""
):
    symbol_info = mt5.symbol_info(Symbol)
    if symbol_info is None:
        print(Symbol, "not found")
        return

    if not symbol_info.visible:
        print(Symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(Symbol, True):
            print("symbol_select({}}) failed, exit", Symbol)
            return
    print(Symbol, "found!")

    if order_type == "Buy":
        order = mt5.ORDER_TYPE_BUY
        if stop_distance:
            sl = stop_distance
        if tp_distance:
            tp = tp_distance

    if order_type == "Sell":
        order = mt5.ORDER_TYPE_SELL
        if stop_distance:
            sl = stop_distance
        if tp_distance:
            tp = tp_distance

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Symbol,
        "volume": float(size),
        "type": order,
        "sl": sl,
        "tp": tp,
        "magic": 10,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print("Failed to send order :")
    else:
        print("Order successfully placed!")
    if mt5.positions_total == 0:
        result = mt5.order_send(request)

def get_states(df, symbols):
    df = gather_data(f'{symbol}',start_from)
    states = {}
    if (df['entry_type'].iloc[-1] == 'LONG'):
        states = 'Buy'
        print(states)
    elif(df['entry_type'].iloc[-1] == 'SHORT') :
        states = 'Sell'
    elif df['entry_type'].iloc[-1] == 'No Entry':
        states = 'No Entry'
    else:
        states = 'Nothing'
    return states

def reading_state ():
    first = True
    
    while True:
        if mt5.positions_total() == 0:
            if (datetime.now().second % 2 == 0) or first:
                if datetime.now().second % 1 == 0 or first:
                    # Refresh Data
                    first = False
                    df = gather_data(f'{symbol}',start_from)
                    states = get_states(df, f"{symbol}")
                    if states == "Buy":
                        print("Order Type: " + states)
                        open_position(f"{symbol}", "Buy", lots, df.tp.iloc[-1], df.sl.iloc[-1], "Buy_Order")
                    elif states == "Sell":
                        print('Order Type: ' + states)
                        open_position(f"{symbol}", "Sell", lots, df.tp.iloc[-1], df.sl.iloc[-1],"Sell_Order")
reading_state()
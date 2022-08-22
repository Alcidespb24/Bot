#!/usr/bin/env python
# coding: utf-8

from http.client import OK
from turtle import position
import pandas as pd
import numpy as np
import pandas_ta as ta
import matplotlib.pyplot as plt
import MetaTrader5 as mt5
from datetime import datetime, timedelta
import time
import pytz

# Init and loggin in MT5
mt5.initialize()

login = 1051262325
password = "V9YJDBR7KE"
server = "FTMO-Demo"

mt5.login(login, password, server)


# In[3]:


if mt5.login(login, password, server):
    account_info_dict = mt5.account_info()._asdict()
    for prop in account_info_dict:
        print("  {}={}".format(prop, account_info_dict[prop]))
else:
    print(
        "failed to connect at account #{}, error code: {}".format(
            account, mt5.last_error()
        )
    )

# In[4]:


def sma(data, window):
    return data.rolling(window=window).mean()


# In[5]:


symbols = ["ETHUSD"]
lots = 60.0
lots_ = 25.0
h_value_long = 0.7
h_value_short = -0.7
h_nrange = -0.03
h_range = 0.03
rsi_mline = 50
rsi_uline = 70
rsi_lline = 30
start_n_minutes_ago = 1440
start_pos = 0
start_from = datetime.now() - timedelta(minutes=start_n_minutes_ago)

mt5.initialize()


def gather_data(symbol, start_from):
    for symbol in symbols:
        rates = mt5.copy_rates_from_pos(
            symbol, mt5.TIMEFRAME_M5, start_pos, start_n_minutes_ago
        )
        df = pd.DataFrame(rates)
        df["time"] = pd.to_datetime(df["time"], unit="s")

        df[f"{symbol}-MA20"] = sma(df["close"], 20)
        df[f"{symbol}-MA13"] = sma(df["close"], 13)
        df[f"{symbol}-EMA100"] = df["close"].ewm(span=100, adjust=False).mean()

        df[f"{symbol}-RSI"] = ta.rsi(df["close"], length=14)

        # Calc the short term EMA
        short_ema = df["close"].ewm(span=12, adjust=False).mean()
        # Calc the long term EMA
        long_ema = df["close"].ewm(span=26, adjust=False).mean()
        # Calc the MACD line
        macd_line = short_ema - long_ema
        # Calc the signal line
        signal = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal
        df[f"{symbol}-MACD"] = macd_line
        df[f"{symbol}-Signal"] = signal
        df[f"{symbol}-Histogram"] = histogram

        df[f"{symbol}-ATR"] = ta.atr(
            high=df["high"], low=df["low"], close=df["close"], length=14
        )

        df.dropna(inplace=True)
    return df


def get_states(df, symbols):
    states = {}
    df = gather_data(f"{symbols}", start_from)
    for symbol in symbols:
        ask_price = mt5.symbol_info_tick("ETHUSD").ask
        bid_price = mt5.symbol_info_tick("ETHUSD").bid

        if (
            df["ETHUSD-MACD"].iloc[-1] > df["ETHUSD-Signal"].iloc[-1]
            and df["ETHUSD-MACD"].iloc[-1] > 0
            # and df["ETHUSD-Signal"].iloc[-1] > 0
            and df["ETHUSD-Histogram"].iloc[-1] >= h_value_long
            and df["ETHUSD-MA20"].iloc[-1] < ask_price
            and df["ETHUSD-MA13"].iloc[-1] < ask_price
            and rsi_uline > df["ETHUSD-RSI"].iloc[-1] > rsi_mline
            # and df["ETHUSD-EMA100"].iloc[-1] < ask_price
        ):
            states = "Buy"
        elif (
            df["ETHUSD-MACD"].iloc[-1] < df["ETHUSD-Signal"].iloc[-1]
            and df["ETHUSD-MACD"].iloc[-1] < 0
            # and df["ETHUSD-Signal"].iloc[-1] < 0
            and df["ETHUSD-Histogram"].iloc[-1] <= h_value_short
            and df["ETHUSD-MA20"].iloc[-1] > bid_price
            and df["ETHUSD-MA13"].iloc[-1] > bid_price
            and rsi_lline < df["ETHUSD-RSI"].iloc[-1] < rsi_mline
            # and df["ETHUSD-EMA100"].iloc[-1] > bid_price
        ):
            states = "Sell"
        elif h_nrange < df["ETHUSD-Histogram"].iloc[-1] < h_range:
            states = "The lines have crossed"
        else:
            states = "Nothing is happening"
        return states


# In[6]:


get_states(gather_data(f"{symbols}", start_from), f"{symbols}")
gather_data(f"{symbols}", start_from)

# In[7]:


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
        price = mt5.symbol_info_tick(Symbol).ask
        if stop_distance:
            sl = price - (stop_distance)
        if tp_distance:
            tp = price + (tp_distance)

    if order_type == "Sell":
        order = mt5.ORDER_TYPE_SELL
        price = mt5.symbol_info_tick(Symbol).bid
        if stop_distance:
            sl = price + (stop_distance)
        if tp_distance:
            tp = price - (tp_distance)

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Symbol,
        "volume": float(size),
        "type": order,
        "price": price,
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

    result = mt5.order_send(request)


orders = mt5.orders_get()


def loop():
    first = True

    while True:
        if mt5.positions_total() == 0:
            if (datetime.now().second % 2 == 0) or first:
                if datetime.now().second % 1 == 0 or first:
                    # Refresh Data
                    first = False
                    df = gather_data(f"{symbols}", start_from)
                    states = get_states(df, f"{symbols}")
                    if states == "Buy":
                        print("Order Type: " + states)
                        open_position("ETHUSD", "Buy", lots,
                                      10, 6, "First Strategy")
                        print(orders)
                        other_loop()
                        break
                    elif states == "Sell":
                        print("Order Type: " + states)
                        open_position("ETHUSD", "Sell", lots,
                                      10, 6, "First Strategy")
                        print(orders)
                        other_loop()
                        break


def other_loop():
    first = True

    while True:
        if mt5.positions_total() == 0:
            if (datetime.now().second % 2 == 0) or first:
                if datetime.now().second % 1 == 0 or first:
                    # Refresh Data
                    first = False
                    df = gather_data(f"{symbols}", start_from)
                    states = get_states(df, f"{symbols}")
                    if states == "The lines have crossed":
                        print("State: ", states)
                        loop()
                        break


other_loop()

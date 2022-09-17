import pandas as pd
from mt5_init_function import *
from datetime import datetime, timedelta
import pytz

symbol = ('ETHUSD')
lots = 50.0
timezone = pytz.timezone("Etc/UTC")
start_n_minutes_ago = 1440
start_from = datetime.now() - timedelta(minutes=start_n_minutes_ago)
start_pos = 0
until_now = datetime.now()

def gather_data(symbol, start_from):
    rates = mt5.copy_rates_from_pos(
                symbol, mt5.TIMEFRAME_M5, start_pos, start_n_minutes_ago
            )
    df = pd.DataFrame(rates)
    df["time"] = pd.to_datetime(df["time"], unit="s")

    df.ta.sma(close=df['close'], length=20, append=True)
    df.ta.ema(close=df['close'], length=100, append=True)
    df.ta.ema(close=df['close'], length=10, append=True)

    g_candle = df.open < df.close
    df['green_candle'] = g_candle

    df['range_price'] = df.close-df.open
    df['range_price_movement'] = df.range_price.shift(1)

    df['Above_SMA20'] = df.close > df.SMA_20
    df['Above_EMA100'] = df.close > df.EMA_100
    df['Above_EMA10'] = df.close > df.EMA_10

    df['median_price'] = (df.high+df.low)/2

    momentum_up='Ascending'
    momentum_down='Descending'
    def conditions (df):
        if(df['range_price'] > 1) & (df['range_price_movement'] > 1):
            return momentum_up
        elif(df['range_price'] < -1) & (df['range_price_movement'] < -1):
            return momentum_down

    df['momentum'] = df.apply(conditions, axis=1)
    df.loc[df['range_price'] > 5, 'candle_clasification' ] = 'Significant G Candle'
    df.loc[df['range_price'] < -5, 'candle_clasification' ] = 'Significant R Candle'

    df['rel_volume'] = df.tick_volume > 625

    long = 'LONG'
    short = 'SHORT'
    none = 'No Entry'
    def checking (df):
        if(df['rel_volume']) & (df['momentum'] == 'Ascending') & (df['candle_clasification'] == 'Significant G Candle'):
            return long
        elif(df['rel_volume']) & (df['momentum'] == 'Descending') & (df['candle_clasification'] == 'Significant R Candle'):
            return short
        else:
            return none
    df['entry_type'] = df.apply(checking, axis=1)

    df['mean'] = df.close.mean()
    df['range_price_mean'] = df.range_price.mean()
    df['std'] = df.range_price.std()

    df.loc[df['entry_type'] == 'LONG', 'entry_price' ] = df.close
    df.loc[df['entry_type'] == 'SHORT', 'entry_price' ] = df.close

    df.loc[df['entry_type'] == 'LONG', 'sl' ] = df.open
    df.loc[df['entry_type'] == 'SHORT', 'sl' ] = df.open

    df.loc[df['entry_type'] == 'LONG', 'tp' ] = df.close + 10
    df.loc[df['entry_type'] == 'SHORT', 'tp' ] = df.close - 10
    
    return df
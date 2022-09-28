import pandas as pd
from mt5_init_function import *
from datetime import datetime, timedelta
import pytz
import numpy as np

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

    df['ha_open'] = (df.close.shift(1) + df.close.shift(2))/2
    df['ha_close'] = (df.open+df.low+df.close+df.high)/4

    g_candle = df.open < df.close
    df['green_candle'] = g_candle

    df['range_price'] = df.close-df.open
    df['range_price_movement'] = df.range_price.shift(1)

    df['ha_range_price'] = df.ha_close-df.ha_open
    df['ha_range_price_movement'] = df.ha_range_price.shift(1)

    df['median_price'] = (df.high+df.low)/2

    momentum_up = 'Ascending'
    momentum_down = 'Descending'

    def conditions(df):
        if (df['range_price'] > 1) & (df['range_price_movement'] > 1):
            return momentum_up
        elif (df['range_price'] < -1) & (df['range_price_movement'] < -1):
            return momentum_down

    df['momentum'] = df.apply(conditions, axis=1)
    df.loc[df['range_price'] >= 5,
           'candle_clasification'] = 'Significant G Candle'
    df.loc[df['range_price'] <= -5,
           'candle_clasification'] = 'Significant R Candle'

    df['rel_volume'] = df.tick_volume > 400

    median_move_up = 'Increasing'
    median_move_down = 'Decreasing'
    df['median_price_trend'] = df.median_price.shift(5)

    def median_move(df):
        if (df['median_price'] > df['median_price_trend']):
            return median_move_up
        elif (df['median_price'] < df['median_price_trend']):
            return median_move_down
    df['median_price_move'] = df.apply(median_move, axis=1)

    df.loc[df['range_price'] >= 7, 'abnormal_candle'] = 'Abnormal G Candle'
    df.loc[df['range_price'] <= -7, 'abnormal_candle'] = 'Abnormal R Candle'

    long = 'LONG'
    short = 'SHORT'
    none = 'No Entry'

    def checking(df):
        if (df['rel_volume']) & (df['momentum'] == 'Ascending') & (df['candle_clasification'] == 'Significant G Candle'):
            return long
        elif (df['rel_volume']) & (df['momentum'] == 'Descending') & (df['candle_clasification'] == 'Significant R Candle'):
            return short
        elif (df['abnormal_candle'] == 'Abnormal G Candle'):
            return long
        elif (df['abnormal_candle'] == 'Abnormal R Candle'):
            return short
        else:
            return none
    df['entry_type'] = df.apply(checking, axis=1)

    df['mean'] = df.close.mean()
    df['ha_range_price_movement'] = df.ha_range_price.mean()
    df['std'] = df.ha_range_price.std()

    df.loc[df['entry_type'] == 'LONG', 'entry_price'] = df.ha_close
    df.loc[df['entry_type'] == 'SHORT', 'entry_price'] = df.ha_close

    df.loc[df['entry_type'] == 'LONG', 'sl'] = df.ha_open
    df.loc[df['entry_type'] == 'SHORT', 'sl'] = df.ha_open

    df.loc[df['entry_type'] == 'LONG', 'tp'] = df.ha_close + 10
    df.loc[df['entry_type'] == 'SHORT', 'tp'] = df.ha_close - 10

    df['returns'] = (np.log(df.ha_close/df.ha_close.shift(-1)))

    df['max_value'] = df.median_price.max()
    df['min_value'] = df.median_price.min()

    return df

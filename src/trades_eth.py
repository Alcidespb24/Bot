from datetime import datetime, timedelta
import time
import cbpro
import pandas as pd
import numpy as np
import statistics
from scipy.stats import norm
client = cbpro.PublicClient()
symbol = 'ETH-USD'
_full_list = []

def convert_iso_format_to_datetime(iso_format_time: str) -> datetime:
    return datetime.strptime(iso_format_time, '%Y-%m-%dT%H:%M:%S.%f%z')


def get_posix_time(datetime_obj: datetime) -> time:
    return time.mktime(datetime_obj.timetuple())

def get_trades_in_last_xmins(mins: int) -> list:
    client
    current_date = datetime.now().utcnow()
    date_five_mins_ago = current_date - timedelta(minutes=mins)
    date_five_mins_ago_posix = get_posix_time(date_five_mins_ago)
    get_trades_latest = client.get_product_trades(product_id=f'{symbol}')
    current_element = get_trades_latest.__next__()
    buffer = []

    while get_posix_time(convert_iso_format_to_datetime(current_element['time'])) > date_five_mins_ago_posix:
        client
        buffer.append(current_element)
        current_element = get_trades_latest.__next__()

    return buffer

def calculate_probability_of_price_change(df):
    # Calculate daily price change percentage
    df['percentage_change'] = df['average price'].pct_change() * 100
    
    # Calculate mean and standard deviation of daily price change
    mean_change = df['percentage_change'].mean()
    std_dev_change = df['percentage_change'].std()
    
    # Use cumulative distribution function (CDF) to calculate the probability of positive and negative changes
    df['probability_up'] = norm.cdf(0, loc=mean_change, scale=std_dev_change)
    df['probability_down'] = 1 - df['probability_up']
    
    return df


def trades_eth(minutes):
    
    global _full_list

    get_trades = get_trades_in_last_xmins(minutes)

    _full_list += get_trades

    df = pd.DataFrame(_full_list)

    df = df.drop_duplicates(subset='trade_id')

    df['price'] = pd.to_numeric(df['price'])
    df['size'] = pd.to_numeric(df['size'])

    df['trade_dollar_size'] = df['price'] * df['size']
    df['change_in_price'] = df['price'].diff()

    df['change_in_size'] = df['size'].diff()

    df['trade_dollar_size'] = pd.to_numeric(df['price'])
    df['change_in_price'] = pd.to_numeric(df['size'])
    df['change_in_size'] = pd.to_numeric(df['price'])

    df[['price', 'size', 'trade_dollar_size', 'change_in_price']].describe()

    df.loc[df['side'] == 'buy', 'size'] = df['size'] * -1
    df.loc[df['side'] == 'sell', 'size'] = df['size'] * 1

    df['time'] = df['time'].values.astype('datetime64[s]')

    df_eth = df.resample('5min', on='time').agg({'price': 'mean', 'size': 'sum', 'trade_id': 'count'}).rename(
        columns={'price': 'average price', 'size': 'sum of size', 'trade_id': 'volume'})

    df_eth.reset_index(inplace=True)

    df_eth['time'] = df_eth['time'].astype(str)

    df_eth['change_in_price'] = df_eth['average price'].diff()
    df_eth['change_in_size'] = df_eth['sum of size'].diff()
    df_eth['change_in_volume'] = df_eth['volume'].diff()

    df_eth['std dev'] = statistics.pstdev(df_eth['average price'])

    df_eth = calculate_probability_of_price_change(df_eth)

    df_eth = df_eth.round(2)

    return df_eth

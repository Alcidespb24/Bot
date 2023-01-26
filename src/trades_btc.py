from datetime import datetime, timedelta
import time
import cbpro
import pandas as pd

client = cbpro.PublicClient()
symbol = 'BTC-USD'
_full_list = []

def convert_iso_format_to_datetime(iso_format_time: str) -> datetime:
    return datetime.strptime(iso_format_time,'%Y-%m-%dT%H:%M:%S.%f%z')


def get_posix_time(datetime_obj: datetime) -> time:
    return time.mktime(datetime_obj.timetuple()) 

def get_trades_in_last_xmins (mins: int) -> list: 
    current_date = datetime.now().utcnow()
    date_five_mins_ago = current_date - timedelta(minutes = mins)
    date_five_mins_ago_posix = get_posix_time(date_five_mins_ago)

    get_trades_latest = client.get_product_trades(product_id=f'{symbol}')    
    current_element = get_trades_latest.__next__()
    buffer = []

    while get_posix_time(convert_iso_format_to_datetime(current_element['time'])) > date_five_mins_ago_posix:
        buffer.append(current_element)
        current_element = get_trades_latest.__next__()


    return buffer


def trades_btc(minutes):

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

    df_btc = df.resample('5min', on='time').agg({'price': 'mean', 'size': 'sum', 'side': 'count'}).rename(
        columns={'price': 'average price', 'size': 'sum of size', 'side': 'volume'})

    df_btc.reset_index(inplace=True)
    
    df_btc['time'] = df_btc['time'].astype(str)

    df_btc['change_in_price'] = df_btc['average price'].diff()
    df_btc['change_in_size'] = df_btc['sum of size'].diff()
    df_btc['change_in_volume'] = df_btc['volume'].diff()

    return df_btc
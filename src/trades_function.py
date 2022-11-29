import cbpro
import pandas as pd
import itertools
from datetime import datetime, timedelta
import time



def convert_iso_format_to_datetime(iso_format_time: str) -> datetime:
    return datetime.strptime(iso_format_time,'%Y-%m-%dT%H:%M:%S.%f%z')


def get_posix_time(datetime_obj: datetime) -> time:
    return time.mktime(datetime_obj.timetuple()) 

def get_trades_in_last_5mins () -> list:    
    client = cbpro.PublicClient()
    client.get_product_trades(product_id='ETH-USD')

    symbol = 'ETH-USD'
    current_date = datetime.now().utcnow()
    date_five_mins_ago = current_date - timedelta(minutes=2)
    date_five_mins_ago_posix = get_posix_time(date_five_mins_ago)
    
    get_trades_latest = client.get_product_trades(product_id=f'{symbol}')    
    current_element = get_trades_latest.__next__()
    buffer = []
    
    while get_posix_time(convert_iso_format_to_datetime(current_element['time'])) > date_five_mins_ago_posix:
        current_element = get_trades_latest.__next__()
        buffer.append(current_element)

    return buffer

_full_list = []
def trades():
    global _full_list 
    _full_list += get_trades_in_last_5mins()
    print(len(_full_list))

    df = pd.DataFrame(_full_list)

    df['price'] = pd.to_numeric(df['price'])
    df['size'] = pd.to_numeric(df['size'])

    df['trade_dollar_size'] = df['price'] * df['size']
    df['change_in_price'] = df['price'].diff()

    df['change_in_size'] = df['size'].diff()

    df['trade_dollar_size'] = pd.to_numeric(df['price'])
    df['change_in_price'] = pd.to_numeric(df['size'])
    df['change_in_size'] = pd.to_numeric(df['price'])

    df[['price', 'size', 'trade_dollar_size', 'change_in_price']].describe()

    df.drop(['trade_id'], axis=1)

    df.loc[df['side'] == 'buy', 'size'] = df['size'] * -1
    df.loc[df['side'] == 'sell', 'size'] = df['size'] * 1

    df['time'] = df['time'].values.astype('datetime64[s]')

    df_5m = df.resample('5min', on='time').agg({'price': 'mean', 'size': 'sum', 'side': 'count'}).rename(
        columns={'price': 'average price', 'size': 'sum of size', 'side': 'volume'})

    df_5m['change_in_price'] = df_5m['average price'].diff()
    df_5m['change_in_size'] = df_5m['sum of size'].diff()
    df_5m['change_in_volume'] = df_5m['volume'].diff()

    # df_5m.to_csv(r"./ETHUSD_Trades_5m.csv", index=True)

    # df_5m = pd.read_csv(r"./ETHUSD_Trades_5m.csv")

    return (df_5m)

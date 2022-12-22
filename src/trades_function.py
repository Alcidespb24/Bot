from datetime import datetime, timedelta
import time
import cbpro
import pandas as pd
import threading

def convert_iso_format_to_datetime(iso_format_time: str) -> datetime:
        return datetime.strptime(iso_format_time, '%Y-%m-%dT%H:%M:%S.%f%z')

def get_posix_time(datetime_obj: datetime) -> time:
        return time.mktime(datetime_obj.timetuple())
class TradeManager:
    _list_of_all_trades: list
    _symbol = 'ETH-USD'
    _interval_rate_secs: int

    def __init__(self, update_rate_secs = 1):
        self._list_of_all_trades = []
        self._interval_rate_secs = update_rate_secs

    def start_periodic_polling(self):
        thrd = threading.Timer(self._interval_rate_secs, self.start_periodic_polling)
        thrd.start()
        self.update_full_list_of_trades()

    def get_trades_in_last_xsecs (self,time_secs: int) -> list:
        client = cbpro.PublicClient()  
        current_date = datetime.now().utcnow()
        date_x_secs_ago = current_date - timedelta(seconds=time_secs)
        date_x_secs_ago_posix = get_posix_time(date_x_secs_ago)

        get_trades_latest = client.get_product_trades(product_id=f'{self._symbol}')    
        current_element = get_trades_latest.__next__()
        buffer = []

        while get_posix_time(convert_iso_format_to_datetime(current_element['time'])) > date_x_secs_ago_posix:
            buffer.append(current_element)
            current_element = get_trades_latest.__next__()

        return buffer

    def update_full_list_of_trades(self):
        self._list_of_all_trades += self.get_trades_in_last_xsecs(self._interval_rate_secs)
        return


    def get_trades_in_5m_intervals(self):    
        df = pd.DataFrame(self._list_of_all_trades)
        
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

        df_5m = df.resample('1min', on='time').agg({'price': 'mean', 'size': 'sum', 'side': 'count'}).rename(
            columns={'price': 'average price', 'size': 'sum of size', 'side': 'volume'})

        df_5m.round(4)
        df_5m.reset_index(inplace=True)
        
        df_5m['time'] = df_5m['time'].astype(str)

        df_5m['change_in_price'] = df_5m['average price'].diff()
        df_5m['change_in_size'] = df_5m['sum of size'].diff()
        df_5m['change_in_volume'] = df_5m['volume'].diff()

        return (df_5m)

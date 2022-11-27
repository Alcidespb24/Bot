import cbpro
import pandas as pd
import itertools


def trades():

    client = cbpro.PublicClient()
    client.get_product_trades(product_id='ETH-USD')

    symbol = 'ETH-USD'

    get_trades = client.get_product_trades(product_id=f'{symbol}')

    df = list(itertools.islice(get_trades, 25000))

    df = pd.DataFrame(df[:-1])

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

    df_5m.to_csv(r"D:\Trading\Bot\Docs/ETHUSD Trades_5m.csv", index=True)

    df_5m = pd.read_csv(r"D:\Trading\Bot\Docs/ETHUSD Trades_5m.csv")

    return (df_5m)

import cbpro
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import MutableMapping

client = cbpro.PublicClient()
client.get_product_trades(product_id='ETH-USD')

get_trades = client.get_product_trades(product_id='ETH-USD')

next(get_trades)
all_trades = list(get_trades)
all_trades
df_trades = pd.DataFrame(all_trades[:-1])
df_trades
df_trades['price'] = pd.to_numeric(df_trades['price'])
df_trades['size'] = pd.to_numeric(df_trades['size'])
df_trades['trade_dollar_size'] = df_trades['price'] * df_trades['size']
df_trades ['change_in_price'] = df_trades['price'].diff().abs()
df_trades[['price', 'size','trade_dollar_size','change_in_price']].describe()
df_trades['time'] = pd.to_datetime(df_trades.time, format='%Y-%m-%d %H:%M:%S')

df_trades['time'] = df_trades['time'].dt.strftime("%Y-%m-%d %H:%M:%S")

df_trades.head()
df_trades.drop(['trade_id'], axis=1)

df_trades.to_csv(r"C:\Users\sheyl\Desktop\Alcides\Bot\Docs/ETHUSD Trades.csv",index=False)

fig, ax = plt.subplots(figsize = (15, 5))

sns.scatterplot(x=df_trades["price"], y=df_trades["size"], hue="side", data=df_trades, ax=ax)

ax.set_xlabel("Price")
ax.set_ylabel("Quantity")

plt.show()


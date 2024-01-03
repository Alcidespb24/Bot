import cbpro
import pandas as pd
from datetime import datetime, timedelta

# Initialize the Coinbase Pro client
public_client = cbpro.PublicClient()

# Calculate the time range: two weeks ago and today
end_time = datetime.now()
start_time = end_time - timedelta(weeks=4)

# Get product trades within the specified time range
trades_generator = public_client.get_product_trades(product_id='BTC-USD', before=start_time)

# Convert the generator to a list of trades
trades_list = list(trades_generator)

# Convert trades list to a DataFrame
trades_nested = pd.json_normalize(trades_list)
df = pd.DataFrame(trades_nested)

# Convert columns to appropriate data types
df['time'] = pd.to_datetime(df['time'])
df['price'] = pd.to_numeric(df['price'])
df['size'] = pd.to_numeric(df['size'])

df['time'] = df['time'].dt.tz_convert('US/Eastern')

df = df.dropna()

# Resample the data and calculate aggregated values
df_resampled = df.resample('5min', on='time').agg({
    'price': 'mean',
    'size': 'sum',
    'trade_id': 'count'
}).rename(columns={
    'price': 'average price',
    'size': 'sum of size',
    'trade_id': 'volume'
})

df_resampled['change_in_price'] = df_resampled['average price'].diff()
df_resampled['change_in_volume'] = df_resampled['volume'].diff()

# Save the resampled DataFrame to a CSV file
df_resampled.to_csv('Tuesday_September_18th.csv')
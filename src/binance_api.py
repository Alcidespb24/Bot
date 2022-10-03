from binance import Client
import pandas as pd

api_key = 'Iq8W1329NSUufpFoPMliUlbKi6AONciPGBpPPl065r7hBYUADFWbYHKZZu3qLxKT'
api_secret = 'UKd62vHIGuwZPjPgOhPlfeA2uyFE4634PuCyNvLqNceOx9N6VgWVIgjtfmooE9Sg'

client = Client(api_key, api_secret)

order_book = client.get_order_book(symbol = 'ETHUSDT')
df = pd.DataFrame(order_book)
df.head()


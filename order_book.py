import cbpro
import pandas as pd

def ob():
    
    client = cbpro.PublicClient()

    # order_book = cbp.get_product_order_book('ETH-USD')

    order_book = cbpro.OrderBook(product_id='ETH-USD')
    order_book.start()

    data = client.get_product_order_book('ETH-USD', level=2)
    data

    # df = pd.DataFrame(data['bids'])
    # df
    bids = pd.DataFrame(data['bids'])
    asks = pd.DataFrame(data['asks'])
    # df = pd.DataFrame(data)

    df = pd.merge(bids, asks, left_index=True, right_index=True)
    df = df.rename({"0_x":"Bid Price","1_x":"Bid Size", "2_x":"Bid Amount",
                    "0_y":"Ask Price","1_y":"Ask Size", "2_y":"Ask Amount"}, axis='columns')

    df['Bid Price'] = pd.to_numeric(df['Bid Price'])
    df['Ask Price'] = pd.to_numeric(df['Ask Price'])
    df['Bid Amount'] = pd.to_numeric(df['Bid Amount'])
    df['Ask Amount'] = pd.to_numeric(df['Ask Amount'])
    
    return (df)

df = ob()
df.head(50)
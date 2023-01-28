import http.client
import json
import pandas as pd
import warnings
from dash import Dash, html, dcc, dash_table, ctx
from dash.dependencies import Input, Output
from dash import dcc, html
import dash
import plotly.express as px
import plotly.io as pio
pio.templates
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')


def trades():
    conn = http.client.HTTPSConnection("api.exchange.coinbase.com")
    payload = ''
    headers = {
        'User-Agent': 'something'

    }
    conn.request("GET", "/products/ETH-USD/trades", payload, headers)
    res = conn.getresponse()
    # json = res.json()
    data = res.read()
    data_string = data.decode('utf-8')

    df = pd.DataFrame.from_records(json.loads(data_string))

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

    df_eth = df.resample('5min', on='time').agg({'price': 'mean', 'size': 'sum', 'side': 'count'}).rename(
        columns={'price': 'average price', 'size': 'sum of size', 'side': 'volume'})

    df_eth.reset_index(inplace=True)

    df_eth['time'] = df_eth['time'].astype(str)

    df_eth['change_in_price'] = df_eth['average price'].diff()
    df_eth['change_in_size'] = df_eth['sum of size'].diff()
    df_eth['change_in_volume'] = df_eth['volume'].diff()
    df_eth = df_eth.round(2)
    return df_eth


df = trades()
df
app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    html.Div([
        html.Div([
            dcc.Graph(id='volume_average_price_figure',
                      animate=True,
                      responsive=True,
                      )
        ],),
           html.Div([
            dash_table.DataTable(id='df_live_update')
        ]),
        dcc.Interval(
            id='live_update_interval',
            interval=1*1000,  # in milliseconds
            n_intervals=0
        ),
    ]
    )
)


@app.callback(Output('volume_average_price_figure', 'figure'),
              Input('live_update_interval', 'n_intervals'))
def volume_average_price_figure_callback(n):
    df=trades()
    volume_average_price_figure = px.scatter(
        df,
        x='time',
        y='average price',
        text='change_in_price',
        color='time',
        template="plotly_dark",
        size='volume',
        title='Volume Distribution & Average Price',
        hover_name="time",
    )

    volume_average_price_figure['layout']['yaxis'].update(autorange=True)
    volume_average_price_figure['layout']['xaxis'].update(autorange=True)
    volume_average_price_figure.update_layout(
        plot_bgcolor='#040303', paper_bgcolor='#040303')
    volume_average_price_figure.update_traces(textposition="bottom right")
    volume_average_price_figure.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='#2C3639')
    volume_average_price_figure.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='#2C3639')

    return volume_average_price_figure


@app.callback(Output('df_live_update', 'data'),
              Input('live_update_interval', 'n_intervals'))
def data_table_update(n):
    df=trades()
    df_5m_lvalues = df.tail(5)
    return df_5m_lvalues.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True)
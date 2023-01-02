import warnings
from dash import Dash, html, dcc, dash_table, ctx
from dash.dependencies import Input, Output
from dash import dcc, html
import dash
from trades_function import trades
from style import *
from mt5_init_function import *
from main import open_position
import plotly.express as px
import plotly.io as pio
pio.templates
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

df_5m = trades(minutes=15)

def get_all_trades():
    global df_5m
    df_5m = trades(minutes=5)
    df_5m.dropna()
    df_5m = df_5m.round(2)


app = dash.Dash(__name__)

app.layout = html.Div(
    html.Div([
        html.Div([
            html.Div([
                dcc.Graph(id='volume_average_price_figure',
                          animate=True,
                          responsive=True,
                          config=graph_config)
            ], style=graph_style
            ),
            html.Div([
                dcc.Graph(id='time_average_price_figure',
                          animate=True,
                          responsive=True,
                          config=graph_config)
            ], style=graph_style
            )
        ], style=graph_div_style),

        html.Div([
            dash_table.DataTable(id='df_live_update', style_cell=style_cell, editable=True,
                                 style_table=style_table,
                                 style_data_conditional=style_data_conditional)
        ], style=data_table_div),
        html.Div([
            html.Div([html.Button('BUY', id='buy_button', n_clicks=0,
                     style=button_buy_style)],),
            html.Div([html.Button('SELL', id='sell_button', n_clicks=0,
                     style=button_sell_style)],),
            html.Div(id='container-button-timestamp')
        ], style=button_div_style),
        dcc.Interval(
            id='live_update_interval',
            interval=1*1000,  # in milliseconds
            n_intervals=0
        ),
    ], style=container_style)
)


@app.callback(Output('volume_average_price_figure', 'figure'),
              Input('live_update_interval', 'n_intervals'))
def volume_average_price_figure_callback(n):
    global df_5m
    volume_average_price_figure = px.scatter(
        df_5m,
        x='volume',
        y='average price',
        text='change_in_price',
        color='time',
        template="plotly_dark",
        size='volume',
        title='Volume Distribution & Average Price',
        hover_name="time",
    )

    # volume_average_price_figure['layout']['yaxis'].update(autorange=True)
    # volume_average_price_figure['layout']['xaxis'].update(autorange=True)
    volume_average_price_figure.update_layout(
        plot_bgcolor='#040303', paper_bgcolor='#040303')
    volume_average_price_figure.update_traces(textposition="bottom right")
    volume_average_price_figure.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='#2C3639')
    volume_average_price_figure.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='#2C3639')

    return volume_average_price_figure


@app.callback(Output('time_average_price_figure', 'figure'),
              Input('live_update_interval', 'n_intervals'))
def time_average_price_figure_callback(n):
    global df_5m

    time_average_price_figure = px.scatter(
        df_5m,
        x='time',
        y='average price',
        text='sum of size',
        size='volume',
        color='time',
        template="plotly_dark",
        title='Price v Change Time',
        hover_name="volume",
    )

    time_average_price_figure['layout']['yaxis'].update(autorange=True)
    time_average_price_figure['layout']['xaxis'].update(autorange=True)
    time_average_price_figure.update_layout(
        plot_bgcolor='#040303', paper_bgcolor='#040303')
    time_average_price_figure.update_traces(textposition="bottom right")
    time_average_price_figure.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='#2C3639')
    time_average_price_figure.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='#2C3639')

    return time_average_price_figure


# @app.callback(Output('live_update_volume', 'children'),
#               Input('live_update_interval', 'n_intervals'))
# def live_text_update_callback(n):
#     get_all_trades()
#     global df_5m

#     return (
#         [
#             html.Span('Volume: ' + df_5m['volume'].map(str).iloc[-1],
#                       style=live_update_text_style),
#             html.Span('Change: ' + df_5m['change_in_price'].map(str).iloc[-1],
#                       style=live_update_text_style),
#             html.Span('Price: ' + df_5m['average price'].map(str).iloc[-1],
#                       style=live_update_text_style),
#             html.Span('Size: ' + df_5m['sum of size'].map(str).iloc[-1],
#                       style=live_update_text_style)
#         ]
#     )


@app.callback(Output('df_live_update', 'data'),
              Input('live_update_interval', 'n_intervals'))
def data_table_update(n):
    get_all_trades()
    global df_5m
    df_5m_lvalues = df_5m.dropna().tail(5)
    return df_5m_lvalues.to_dict('records')


@app.callback(
    Output('container-button-timestamp', 'children'),
    Input('buy_button', 'n_clicks'),
    Input('sell_button', 'n_clicks'),
)
def displayClick(bb, sb):

    if "buy_button" == ctx.triggered_id:
        trade = open_position(Symbol='ETHUSD', order_type='Buy', size=20,
                              tp_distance=1300, stop_distance=1200, comment='it worked')
        print('I am trying to buy')
    elif "sell_button" == ctx.triggered_id:
        trade = open_position(Symbol='ETHUSD', order_type='Sell', size=20,
                              tp_distance=1200, stop_distance=1300, comment='it worked')
        print('I am trying to sell')
    else:
        'Something went wrong'
    return trade


if __name__ == '__main__':
    app.run_server(debug=True)

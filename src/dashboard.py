import warnings
import winsound
from dash import Dash, html, dcc, dash_table, ctx
from dash.dependencies import Input, Output
from dash import dcc, html
import dash
from trades_eth import trades_eth
from style import *
import plotly.express as px
import plotly.io as pio
pio.templates
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

df_eth = trades_eth(minutes=20)

def get_all_trades():
    global df_eth
    df_eth = trades_eth(minutes=20)
    df_eth = df_eth.round(2)
    df_eth.dropna()

    if df_eth.volume.iloc[0] >= 2500 and df_eth.change_in_price.iloc[0] >= 3 and df_eth.change_in_size.iloc[0] >= 100:
        winsound.PlaySound("beep.wav", winsound.SND_FILENAME)
    elif df_eth.volume.iloc[0] >= 2500 and df_eth.change_in_price.iloc[0] <= -3 and df_eth.change_in_size.iloc[0] <= -100:
        winsound.PlaySound("SystemExclamation.wav", winsound.SND_FILENAME)

app = dash.Dash(__name__)

server = app.server

app.layout = html.Div(
    html.Div([
        html.H1('ETH-USD', style={'color': '#91D8E4',
                              'text-align': 'left', 'margin': '50px 0px 0px 65px'}),
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

        dcc.Interval(
            id='live_update_interval',
            interval=1*5000,  # in milliseconds
            n_intervals=0
        ),
    ], style=container_style)
)


@app.callback(Output('volume_average_price_figure', 'figure'),
              Input('live_update_interval', 'n_intervals'))
def volume_average_price_figure_callback(n):
    global df_eth
    volume_average_price_figure = px.scatter(
        df_eth,
        x='volume',
        y='average price',
        text='sum of size',
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


@app.callback(Output('time_average_price_figure', 'figure'),
              Input('live_update_interval', 'n_intervals'))
def time_average_price_figure_callback(n):
    global df_eth

    time_average_price_figure = px.scatter(
        df_eth,
        x='time',
        y='average price',
        text='change_in_price',
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


@app.callback(Output('df_live_update', 'data'),
              Input('live_update_interval', 'n_intervals'))
def data_table_update(n):
    get_all_trades()
    global df_eth
    df_5m_lvalues = df_eth.tail(5)
    
    return df_5m_lvalues.to_dict('records')

if __name__ == '__main__':
    app.run_server(debug=True)
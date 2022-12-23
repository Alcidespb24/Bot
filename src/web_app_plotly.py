from trades_function import TradeManager
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import Dash, html, dcc
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')


df_5m = trades()

def get_all_trades():
    global df_5m
    df_5m = trades()
    df_5m.dropna()
    df_5m = df_5m.round(4)

app = dash.Dash(__name__)

live_update_text_style = {
         'color': 'white',
         'font-size': '20px',
         'background-color': 'black',
         'borderRadius': '45px',
         'margin': '0px 10px 0px 10px',
         'padding': '10px',
         }

app.layout = html.Div(
    html.Div([
        html.Div(id='live_update_volume', style={'margin': '50px 0px 40px 0px'}),

        html.Div([
            dcc.Graph(id='volume_average_price_figure',
                    animate=True,
                    responsive=True,
                    config={'editable': True,
                            'scrollZoom': True,
                            'staticPlot': False,
                            'doubleClick': 'reset',
                            'displayModeBar': False,
                            }),

            html.Hr(),

            dcc.Graph(id='time_average_price_figure',
                    animate=True,
                    responsive=True,
                    config={'editable': True,
                            'scrollZoom': True,
                            'staticPlot': False,
                            'doubleClick': 'reset',
                            'displayModeBar': False,
                            }),
        ]),
        dcc.Interval(
            id='live_update_interval',
            interval=1*5000,  # in milliseconds
            n_intervals=0
        ),
    ],)
)

@app.callback(Output('volume_average_price_figure', 'figure'),
              Input('live_update_interval', 'n_intervals'))
def volume_average_price_figure_callback(n):
    df_5m = trade_mgr.get_trades_in_5m_intervals()
    volume_average_price_figure = px.scatter(
                       df_5m, 
                       x='volume',
                       y='average price',
                       trendline='ols',
                       trendline_scope="overall",
                       trendline_color_override='white',
                       text='change_in_price',
                       color='time',
                       template="plotly_dark",
                       size='volume',
                       title='Volume Distribution & Average Price',
                       hover_name="time",
                       )

    volume_average_price_figure['layout']['yaxis'].update(autorange=True)
    volume_average_price_figure['layout']['xaxis'].update(autorange=True)
    volume_average_price_figure.update_layout(plot_bgcolor='#212121', paper_bgcolor='#212121')
    volume_average_price_figure.update_traces(textposition="bottom right")
    volume_average_price_figure.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Gray')
    volume_average_price_figure.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Gray')

    return volume_average_price_figure

@app.callback(Output('time_average_price_figure', 'figure'),
              Input('live_update_interval', 'n_intervals'))
def time_average_price_figure_callback(n):
    df_5m = trade_mgr.get_trades_in_5m_intervals()

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
    time_average_price_figure.update_layout(plot_bgcolor='#212121', paper_bgcolor='#212121')
    time_average_price_figure.update_traces(textposition="bottom right")
    time_average_price_figure.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Gray')
    time_average_price_figure.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Gray')

    return time_average_price_figure

@app.callback(Output('live_update_volume', 'children'),
              Input('live_update_interval', 'n_intervals'))
def live_text_update_callback(n):
    df_5m = trade_mgr.get_trades_in_5m_intervals()

    return (
            [
                html.Span('Volume: ' + df_5m['volume'].map(str).iloc[-1],
                            style=live_update_text_style),
                html.Span('Change In Price: ' + df_5m['change_in_price'].map(str).iloc[-1],
                            style=live_update_text_style)
            ]
        )

if __name__ == '__main__':
    trade_mgr.start_periodic_polling()
    app.run_server(debug=True)

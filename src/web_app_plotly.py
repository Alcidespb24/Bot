from trades_function import trades
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import Dash, html, dcc
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

df_5m = trades()
df_5m.dropna()

app = dash.Dash(__name__)

volume_txt_style = {'border': '40px',
         'color': 'white',
         'font-size': '20px',
         'background-color': 'black',
         'borderRadius': '45px',
         'overflow': 'hidden',
         'padding': '20px',
         'margin': '0px 0px 50px 0px',
         'display':'inline-block',
         'float':'left'
         }
chp_txt_style = {'border': '40px',
         'color': 'white',
         'font-size': '20px',
         'background-color': 'black',
         'borderRadius': '45px',
         'overflow': 'hidden',
         'padding': '20px',
         'margin': '0px 0px 50px 20px',
         'display':'inline-block',
         }

color = '#F3ECB0',

app.layout = html.Div(
    [html.Div([
        html.H1('Live'),
        html.Div(html.Span('Volume: ' + df_5m['volume'].map(str).iloc[-1],
                           id='live_update_volume',
                           style=volume_txt_style)),
        html.Div(html.Span('Change In Price: ' + df_5m['change_in_price'].map(str).iloc[-1],
                           id='live_update_pricech',
                           style=chp_txt_style)),
        dcc.Graph(id='fig_v',
                  animate=True,
                  responsive=True,
                  config={'editable': True,
                          'scrollZoom': True,
                          'staticPlot': False,
                          'doubleClick': 'reset',
                          'displayModeBar': False,
                          'watermark': True
                          }),
        dcc.Interval(
            id='fig_1_update',
            interval=1*5000,  # in milliseconds
            n_intervals=0
        )
    ]),

        html.Div([
            html.Div(id='live-update-text'),
            dcc.Graph(id='fig_p',
                      animate=True,
                      responsive=True,
                      config={'editable': True,
                              'scrollZoom': True,
                              'staticPlot': False,
                              'doubleClick': 'reset',
                              'displayModeBar': False,
                              'watermark': True
                              }),
            dcc.Interval(
                id='fig_2_update',
                interval=1*5000,  # in milliseconds
                n_intervals=0
            )
        ])]
)


@app.callback(Output('fig_v', 'figure'),
              Output('fig_p', 'figure'),
              Input('fig_1_update', 'n_intervals'),
              Input('fig_2_update', 'n_intervals'))
def update_graph_live(n, figure):

    df_5m = trades()
    df_5m = df_5m.round(1)

    fig_v = px.scatter(df_5m, x='volume',
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

    fig_p = px.scatter(df_5m, x='time',
                       y='average price',
                       text='sum of size',
                       size='volume',
                       color='time',
                       template="plotly_dark",
                       title='Price v Change Time',
                       hover_name="volume",
                       )
    fig_v['layout']['yaxis'].update(autorange=True)
    fig_v['layout']['xaxis'].update(autorange=True)
    fig_v.update_layout(plot_bgcolor='#212121', paper_bgcolor='#212121')
    fig_v.update_traces(textposition="bottom right")
    fig_v.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Gray')
    fig_v.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Gray')

    fig_p['layout']['yaxis'].update(autorange=True)
    fig_p['layout']['xaxis'].update(autorange=True)
    fig_p.update_layout(plot_bgcolor='#212121', paper_bgcolor='#212121')
    fig_p.update_traces(textposition="bottom right")
    fig_p.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Gray')
    fig_p.update_xaxes(showgrid=True, gridwidth=1, gridcolor='Gray')

    return (fig_v, fig_p)


if __name__ == '__main__':
    app.run_server(debug=True)

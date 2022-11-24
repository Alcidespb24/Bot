from trades_function import trades
import datetime as datetime
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

df_5m = trades()
df_5m

app = dash.Dash(__name__)

color = '#F3ECB0',

app.layout = html.Div(
    [html.Div([
        html.H1('Live Update'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='fig_v',
                  responsive=True),
        dcc.Interval(
            id='fig_1_update',
            interval=1*5000,  # in milliseconds
            n_intervals=0
        )
    ]),

        html.Div([
            html.Div(id='live-update-text'),
            dcc.Graph(id='fig_p',
                      responsive=True),
            dcc.Interval(
                id='fig_2_update',
                interval=1*5000,  # in milliseconds
                n_intervals=0
            )
        ])]
)


@app.callback(Output('fig_v', 'figure'),
              Output('fig_p', 'figure'),
              Input('fig_1_update', 'n_intervals'))
def update_graph_live(n):

    df_5m = trades()
    df_5m = df_5m.round(2)

#     fig = px.scatter(df_5m, x='sum of size',
#                      y='average price',
#                      text='change_in_price',
#                      size='volume',color='time',
#                      template="plotly_dark",
#                      title='Size v Price')
#     fig.update_layout(autosize=True)
#     fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='Gray')

    fig_v = px.scatter(df_5m, x='volume', y='average price',
                        trendline="ols", text='change_in_price',
                        color='time',
                        template="plotly_dark",
                        size='volume',
                        title='Volume Distribution & Average Price',
                        hover_name="time",
                        )

    fig_p = px.scatter(df_5m, x='time',
                       y='average price',
                       trendline="ols",
                       text='sum of size',
                       size='volume',
                       color='time',
                       template="plotly_dark",
                       title='Price v Change Time',
                       hover_name="time",
                       )
    fig_v.update_layout(plot_bgcolor='#212121', paper_bgcolor='#212121')
    fig_v.update_yaxes(showgrid=False)
    fig_v.update_xaxes(showgrid=False)

    fig_p.update_layout(plot_bgcolor='#212121', paper_bgcolor='#212121')
    fig_p.update_yaxes(showgrid=False)
    fig_p.update_xaxes(showgrid=False)

#     fig = go.Figure(go.Waterfall(x=df_5m['time'],
#                              y=df_5m['change_in_price'],
#                              orientation = 'v',
#                              textposition = 'outside',
#                              text = df_5m['sum of size'],
#                              hovertext = ['x','y'],
#                              decreasing = {"marker":{"line":{"color":"red", "width":2}}},
#                              increasing = {"marker":{"color":"Green"}},
#                          ))
#     fig.update_layout(autosize=True)

#     fig.add_trace(go.Bar(x=df_5m['time'], y=df_5m['volume']))

#     fig.append_trace({
#         'x': df_5m['time'],
#         'y': df_5m['change_in_price'],
#         'name': 'Volume',
#         'mode': 'lines+markers',
#         'type': 'scatter'
#     }, 1, 1)

    return (fig_v, fig_p)

if __name__ == '__main__':
    app.run_server(debug=True)

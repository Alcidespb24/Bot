# import warnings
# import os
# from dash import Dash, html, dcc, dash_table, ctx
# from dash.dependencies import Input, Output
# from dash import dcc, html
# import dash
# from trades_function import trades
# from style import *
# import plotly.express as px
# import plotly.io as pio
# pio.templates
# warnings.filterwarnings('ignore')
# warnings.simplefilter('ignore')
# df_5m = trades(minutes=5)


# def get_all_trades():
#     global df_5m
#     df_5m = trades(minutes=5)
#     df_5m.dropna()
#     df_5m = df_5m.round(2)


# app = dash.Dash(__name__)

# server = app.server

# app.layout = html.Div(
#     html.Div([
#         html.H1('ETH', style={'color': '#91D8E4',
#                               'text-align': 'left', 'margin': '50px 0px 0px 65px'}),
#         html.Div([
#             html.Div([
#                 dcc.Graph(id='volume_average_price_figure',
#                           animate=True,
#                           responsive=True,
#                           config=graph_config)
#             ], style=graph_style
#             ),
#             html.Div([
#                 dcc.Graph(id='time_average_price_figure',
#                           animate=True,
#                           responsive=True,
#                           config=graph_config)
#             ], style=graph_style
#             )
#         ], style=graph_div_style),

#         html.Div([
#             dash_table.DataTable(id='df_live_update', style_cell=style_cell, editable=True,
#                                  style_table=style_table,
#                                  style_data_conditional=style_data_conditional)
#         ], style=data_table_div),

#         dcc.Interval(
#             id='live_update_interval',
#             interval=1*5000,  # in milliseconds
#             n_intervals=0
#         ),
#     ], style=container_style)
# )


# @app.callback(Output('volume_average_price_figure', 'figure'),
#               Input('live_update_interval', 'n_intervals'))
# def volume_average_price_figure_callback(n):
#     global df_5m
#     volume_average_price_figure = px.scatter(
#         df_5m,
#         x='volume',
#         y='average price',
#         text='change_in_price',
#         color='time',
#         template="plotly_dark",
#         size='volume',
#         title='Volume Distribution & Average Price',
#         hover_name="time",
#     )

#     volume_average_price_figure['layout']['yaxis'].update(autorange=True)
#     volume_average_price_figure['layout']['xaxis'].update(autorange=True)
#     volume_average_price_figure.update_layout(
#         plot_bgcolor='#040303', paper_bgcolor='#040303')
#     volume_average_price_figure.update_traces(textposition="bottom right")
#     volume_average_price_figure.update_yaxes(
#         showgrid=True, gridwidth=1, gridcolor='#2C3639')
#     volume_average_price_figure.update_xaxes(
#         showgrid=True, gridwidth=1, gridcolor='#2C3639')

#     return volume_average_price_figure


# @app.callback(Output('time_average_price_figure', 'figure'),
#               Input('live_update_interval', 'n_intervals'))
# def time_average_price_figure_callback(n):
#     global df_5m

#     time_average_price_figure = px.scatter(
#         df_5m,
#         x='time',
#         y='average price',
#         text='sum of size',
#         size='volume',
#         color='time',
#         template="plotly_dark",
#         title='Price v Change Time',
#         hover_name="volume",
#     )

#     time_average_price_figure['layout']['yaxis'].update(autorange=True)
#     time_average_price_figure['layout']['xaxis'].update(autorange=True)
#     time_average_price_figure.update_layout(
#         plot_bgcolor='#040303', paper_bgcolor='#040303')
#     time_average_price_figure.update_traces(textposition="bottom right")
#     time_average_price_figure.update_yaxes(
#         showgrid=True, gridwidth=1, gridcolor='#2C3639')
#     time_average_price_figure.update_xaxes(
#         showgrid=True, gridwidth=1, gridcolor='#2C3639')

#     return time_average_price_figure


# @app.callback(Output('df_live_update', 'data'),
#               Input('live_update_interval', 'n_intervals'))
# def data_table_update(n):
#     get_all_trades()
#     global df_5m
#     df_5m_lvalues = df_5m.dropna().tail(5)
#     return df_5m_lvalues.to_dict('records')


# if __name__ == '__main__':
#     app.run_server(debug=True)

import datetime

import dash
from dash import dcc, html
import plotly
from dash.dependencies import Input, Output

# pip install pyorbital
from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div(
    html.Div([
        html.H4('TERRA Satellite Live Feed'),
        html.Div(id='live-update-text'),
        dcc.Graph(id='live-update-graph'),
        dcc.Interval(
            id='interval-component',
            interval=1*1000, # in milliseconds
            n_intervals=0
        )
    ])
)


@app.callback(Output('live-update-text', 'children'),
              Input('interval-component', 'n_intervals'))
def update_metrics(n):
    lon, lat, alt = satellite.get_lonlatalt(datetime.datetime.now())
    style = {'padding': '5px', 'fontSize': '16px'}
    return [
        html.Span('Longitude: {0:.2f}'.format(lon), style=style),
        html.Span('Latitude: {0:.2f}'.format(lat), style=style),
        html.Span('Altitude: {0:0.2f}'.format(alt), style=style)
    ]


# Multiple components can update everytime interval gets fired.
@app.callback(Output('live-update-graph', 'figure'),
              Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    satellite = Orbital('TERRA')
    data = {
        'time': [],
        'Latitude': [],
        'Longitude': [],
        'Altitude': []
    }

    # Collect some data
    for i in range(180):
        time = datetime.datetime.now() - datetime.timedelta(seconds=i*20)
        lon, lat, alt = satellite.get_lonlatalt(
            time
        )
        data['Longitude'].append(lon)
        data['Latitude'].append(lat)
        data['Altitude'].append(alt)
        data['time'].append(time)

    # Create the graph with subplots
    fig = plotly.tools.make_subplots(rows=2, cols=1, vertical_spacing=0.2)
    fig['layout']['margin'] = {
        'l': 30, 'r': 10, 'b': 30, 't': 10
    }
    fig['layout']['legend'] = {'x': 0, 'y': 1, 'xanchor': 'left'}

    fig.append_trace({
        'x': data['time'],
        'y': data['Altitude'],
        'name': 'Altitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 1, 1)
    fig.append_trace({
        'x': data['Longitude'],
        'y': data['Latitude'],
        'text': data['time'],
        'name': 'Longitude vs Latitude',
        'mode': 'lines+markers',
        'type': 'scatter'
    }, 2, 1)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
import warnings
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
from dash import dcc, html
import dash
from trades_function import trades
import plotly.express as px
import plotly.io as pio
pio.templates
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')


df_5m = trades()


def get_all_trades():
    global df_5m
    df_5m = trades()
    df_5m.dropna()
    df_5m = df_5m.round(2)


app = dash.Dash(__name__)

live_update_text_style = {
    'color': 'white',
    'font-size': '15px',
    'background-color': '#2A0944',
    'border-radius': '50%',
    'display': 'inline-block',
    'box-shadow': 'rgba(14, 30, 37, 0.12) 0px 2px 4px 0px, rgba(14, 30, 37, 0.32) 0px 2px 16px 0px',
    'margin': '20px',
    'padding': '25px',
    'width': '50px',
    'height': '50px',
    'text-align': 'center',
    'align-items': 'center'
}

style_cell = style_cell = {
    'color': 'white',
    'backgroundColor': '#212121',
    'textAlign': 'center'
}

style_data_conditional = [
    {
        'if': {
            'filter_query': '{volume} > 2500',
            'column_id': 'volume'
        },
        'backgroundColor': '#B3FFAE',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{volume} < 2000',
            'column_id': 'volume'
        },
        'backgroundColor': '#EC7272',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{volume} > 3000',
            'column_id': 'volume'
        },
        'backgroundColor': '#4E9F3D',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{volume} > 5000',
            'column_id': 'volume'
        },
        'backgroundColor': '#82CD47',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_price} > 1',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#B6E2A1',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_price} > 5',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#519872',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_price} > 10',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#4E9F3D',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_price} < -1',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#FF6464',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_price} < -5',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#519872',
        'color': 'red',

    },
    {
        'if': {
            'filter_query': '{change_in_price} < -10',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#4E9F3D',
        'color': 'red',
    },
    {
        'if': {
            'filter_query': '{sum of size} < 0',
            'column_id': 'sum of size'
        },
        'backgroundColor': '#FF0000',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{sum of size} > 0',
            'column_id': 'sum of size'
        },
        'backgroundColor': '#4E9F3D',
        'color': 'white',
    },
]

app.layout = html.Div(
    html.Div([
        html.Div(
            dcc.Graph(id='volume_average_price_figure',
                      animate=True,
                      responsive=True,
                      style={
                          'width': '50%',
                          'float': 'left',
                          'margin': '50px 0px 20px 0px'
                      },
                      config={'editable': True,
                              'scrollZoom': True,
                              'staticPlot': False,
                              'doubleClick': 'reset',
                              'displayModeBar': False,
                              })),

        dcc.Graph(id='time_average_price_figure',
                  animate=True,
                  responsive=True,
                  style={
                      'width': '50%',
                      'float': 'right',
                      'margin': '50px 0px 20px 0px',
                  },
                  config={'editable': True,
                          'scrollZoom': True,
                          'staticPlot': False,
                          'doubleClick': 'reset',
                          'displayModeBar': False,
                          }),
        html.Div(id='df_live_update'),
        # html.Div([
        #      html.Div(id='live_update_volume', style={
        #          'padding': '20px',
        #          'text-align': 'center',
        #          'background-color': '#212121'}),
        #      ]),
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

    volume_average_price_figure['layout']['yaxis'].update(autorange=True)
    volume_average_price_figure['layout']['xaxis'].update(autorange=True)
    volume_average_price_figure.update_layout(
        plot_bgcolor='#212121', paper_bgcolor='#212121')
    volume_average_price_figure.update_traces(textposition="bottom right")
    volume_average_price_figure.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='Gray')
    volume_average_price_figure.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='Gray')

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
        plot_bgcolor='#212121', paper_bgcolor='#212121')
    time_average_price_figure.update_traces(textposition="bottom right")
    time_average_price_figure.update_yaxes(
        showgrid=True, gridwidth=1, gridcolor='Gray')
    time_average_price_figure.update_xaxes(
        showgrid=True, gridwidth=1, gridcolor='Gray')

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


@app.callback(Output('df_live_update', 'children'),
              Input('live_update_interval', 'n_intervals'))
def data_table_update(n):
    get_all_trades()
    global df_5m

    df_5m_lvalues = df_5m.tail(3)

    return (
        dash_table.DataTable(df_5m_lvalues.to_dict('records'), style_cell=style_cell, editable=True,
                             style_data_conditional=style_data_conditional),
    )


if __name__ == '__main__':
    app.run_server(debug=True)
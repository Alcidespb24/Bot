from trades_5m import *
import dash
from dash import Dash, html, dcc


app = Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Waterfall Graph'),

    html.Div(children='''
        A guide graph
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig_wf
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)

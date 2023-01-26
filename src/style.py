container_style = {'background-color': 'black',
                   'height': '100%',
                   'width': '100%',
                   'position': 'absolute',
                   'left': '0',
                   'right': '0',
                   'bottom': '0'
                   }

graph_config = {'editable': True,
                'scrollZoom': True,
                'staticPlot': False,
                'doubleClick': 'reset',
                'displayModeBar': False, }

graph_style = {'display': 'inline-block',
               'width': '45%',
               'margin-left': '65px'
               }
graph_div_style = {'display': 'inline-block',
                   'width': '100%',
                   'margin': '50px 0px 0px 0px',
                   }
style_table = {
    'margin-left': '65px',
    'margin-right': '35px'
}
data_table_div = {'display': 'block',
                  'width': '93.5%',
                  'margin-top': '50px',
                  }
style_cell = {
    'color': 'white',
    'backgroundColor': '#040303',
    'textAlign': 'center',
}

style_data_conditional = [
    {
        'if': {
            'filter_query': '{volume} > 2500',
            'column_id': 'volume'
        },
        'backgroundColor': '#FFD369',
        'color': 'black',
    },
    {
        'if': {
            'filter_query': '{volume} < 2500',
            'column_id': 'volume'
        },
        'backgroundColor': '#3F4E4F',
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
        'backgroundColor': '#03C988',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_price} > 1',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#FFD369',
        'color': 'black',
    },
    {
        'if': {
            'filter_query': '{change_in_price} > 5',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#4E9F3D',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_price} > 10',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#03C988',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_price} < -1',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#FFD369',
        'color': 'black',
    },
    {
        'if': {
            'filter_query': '{change_in_price} < -5',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#519872',
        'color': 'white',

    },
    {
        'if': {
            'filter_query': '{change_in_price} < -10',
            'column_id': 'change_in_price'
        },
        'backgroundColor': '#4E9F3D',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{sum of size} < 1',
            'column_id': 'sum of size'
        },
        'backgroundColor': '#FF0000',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{sum of size} > 1',
            'column_id': 'sum of size'
        },
        'backgroundColor': '#4E9F3D',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_size} < 1',
            'column_id': 'change_in_size'
        },
        'backgroundColor': '#FF0000',
        'color': 'white',
    },
    {
        'if': {
            'filter_query': '{change_in_size} > 1',
            'column_id': 'change_in_size'
        },
        'backgroundColor': '#519872',
        'color': 'white',
    }
]

button_buy_style = {'background-color': 'green',
                    'display': 'inline-block',
                    'width': '25%',
                    'margin-top': '10px'}

button_sell_style = {'background-color': 'red',
                     'display': 'inline-block',
                     'width': '25%',
                     'margin-top': '10px'}
button_div_style = {'margin': '25px 50px 0px 50px',
                    'text-align': 'center',
                    'align-items': 'center'}

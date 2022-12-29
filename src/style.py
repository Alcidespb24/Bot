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

style_cell = {
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

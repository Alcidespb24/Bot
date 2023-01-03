##BUTTONS LAYOUT AND CALLBACK FUNCTION##

# html.Div([
        #     html.Div([html.Button('BUY', id='buy_button', n_clicks=0,
        #              style=button_buy_style)],),
        #     html.Div([html.Button('SELL', id='sell_button', n_clicks=0,
        #              style=button_sell_style)],),
        #     html.Div(id='container-button-timestamp')
        # ], style=button_div_style),


# @app.callback(
#     Output('container-button-timestamp', 'children'),
#     Input('buy_button', 'n_clicks'),
#     Input('sell_button', 'n_clicks'),
# )
# def displayClick(bb, sb):

#     if "buy_button" == ctx.triggered_id:
#         trade = open_position(Symbol='ETHUSD', order_type='Buy', size=20,
#                               tp_distance=1300, stop_distance=1200, comment='it worked')
#         print('I am trying to buy')
#     elif "sell_button" == ctx.triggered_id:
#         trade = open_position(Symbol='ETHUSD', order_type='Sell', size=20,
#                               tp_distance=1200, stop_distance=1300, comment='it worked')
#         print('I am trying to sell')
#     else:
#         'Something went wrong'
#     return trade


##TEXT DISPLAYING RELEVANT INFORMATION##

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


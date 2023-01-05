from mt5_init_function import *

init()

def open_position(
    Symbol, order_type, size, tp_distance=None, stop_distance=None, comment=""
):
    symbol_info = mt5.symbol_info(Symbol)
    if symbol_info is None:
        print(Symbol, "not found")
        return

    if not symbol_info.visible:
        print(Symbol, "is not visible, trying to switch on")
        if not mt5.symbol_select(Symbol, True):
            print("symbol_select({}}) failed, exit", Symbol)
            return
    print(Symbol, "found!")

    if order_type == "Buy":
        order = mt5.ORDER_TYPE_BUY
        if stop_distance:
            sl = stop_distance
        if tp_distance:
            tp = tp_distance

    if order_type == "Sell":
        order = mt5.ORDER_TYPE_SELL
        if stop_distance:
            sl = stop_distance
        if tp_distance:
            tp = tp_distance

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": Symbol,
        "volume": float(size),
        "type": order,
        "sl": sl,
        "tp": tp,
        "magic": 10,
        "comment": comment,
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)
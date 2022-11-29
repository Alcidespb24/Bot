import pandas as pd
import cbpro
import datetime as datetime
from datetime import datetime, timedelta
import time
import numpy as np
import itertools
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
from dash import Dash, html, dcc
import schedule as sched
# from trades_all import trades

symbol = 'ETH-USD'
client = cbpro.PublicClient()   


def convert_iso_format_to_datetime(iso_format_time: str) -> datetime:
    return datetime.strptime(iso_format_time,'%Y-%m-%dT%H:%M:%S.%f%z')


def get_posix_time(datetime_obj: datetime) -> time:
    return time.mktime(datetime_obj.timetuple()) 




def get_trades_in_last_5mins ():    
    current_date = datetime.now().utcnow()
    date_five_mins_ago = current_date - timedelta(minutes=5)
    date_five_mins_ago_posix = get_posix_time(date_five_mins_ago)
    
    get_trades_latest = client.get_product_trades(product_id=f'{symbol}')    
    current_element = get_trades_latest.__next__()
    buffer = []
    
    while get_posix_time(convert_iso_format_to_datetime(current_element['time'])) > date_five_mins_ago_posix:
        current_element = next(get_trades_latest)
        buffer.append(current_element)

    return buffer

elements_list = []
def update_list_of_trades() -> None:
    elements_list = elements_list.append(get_trades_in_last_5mins())
    print(len(elements_list))


if __name__ == '__main__':
    sched.every(3).seconds.do(update_list_of_trades)

    while True:
        sched.run_pending()
        time.sleep(1)
    
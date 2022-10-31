from operator import eq
from time import sleep
import os

if os.name == 'nt':
    import MetaTrader5 as mt5
    
else:
    from mt5linux import MetaTrader5
    mt5 = MetaTrader5()



def init():    
    mt5.initialize()

    if mt5.terminal_info() == None:
        quit()
        
    login = 1051286908
    password = "G6NEWUYDL5"
    server = "FTMO-Demo"

    mt5.login(login, password, server)

    if mt5.login(login, password, server):
        account_info_dict = mt5.account_info()._asdict()
        for prop in account_info_dict:
            print("  {}={}".format(prop, account_info_dict[prop]))
    else:
        print(
            "failed to connect at account #"
        )
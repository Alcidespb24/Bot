import MetaTrader5 as mt5

def init():
    mt5.initialize()

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
            "failed to connect at account #{}, error code: {}".format(
                account, mt5.last_error()
            )
        )
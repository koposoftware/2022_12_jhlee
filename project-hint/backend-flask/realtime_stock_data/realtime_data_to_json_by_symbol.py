import json
import numpy as np
from pandas._libs.tslibs.offsets import relativedelta
from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import time
# from apscheduler.schedulers.blocking import BlockingScheduler
# sched = BlockingScheduler()
# from apscheduler.schedulers.background import BackgroundScheduler
# sched = BackgroundScheduler()


def get_ohlcv_by_symbol(symbol, today):
    symbol = symbol
    # symbol_with_ks = symbol + '.KS'

    now = str(datetime.now())
    df_today = now[:19]

    yesterday = '20220902'
    now = str(datetime.now())
    df_today = now[11:19]

    df_stock_by_ticker = stock.get_market_ohlcv_by_ticker(date=today, market="ALL")
    df_stock_by_ticker = df_stock_by_ticker.reset_index()
    df_stock_by_ticker['날짜'] = df_today

    df_stock_name = pd.DataFrame({'티커': stock.get_market_ticker_list(market="ALL")})
    df_stock_name['종목명'] = df_stock_by_ticker['티커'].map(lambda x: stock.get_market_ticker_name(x))
    df_stock = pd.merge(df_stock_name, df_stock_by_ticker, left_on='티커', right_on='티커', how='outer')
    df_stock.columns = ['symbol', 'name', 'open', 'high', 'low', 'close', 'volume', 'amount', 'rate', 'date']
    # df_stock.columns = ['symbol', 'stockName', 'now', 'high', 'low', 'close', 'volume', 'transacAmount', 'dayRate', 'date']

    # df_stock = df_stock.sort_values(by='code')
    # df_stock = df_stock.reset_index()
    # df_stock.drop(["index"], axis=1)
    df_stock.set_index('symbol', inplace=True)

    df_stock_by_symbol = df_stock[df_stock.index == symbol]
    df_stock_by_symbol = df_stock_by_symbol.drop(['open', 'high', 'low', 'volume', 'amount'], axis=1)

    df_stock_by_symbol.to_json('/Users/hwaner/Documents/workspace/project-hint/backend-flask/static/data/stock_real_data_by_symbol.json',
                               orient='index', force_ascii=False)

    # df_stock_by_symbol.to_json('/Users/hwaner/Documents/workspace/project-hint/frontend-react/public/stock_real_data_by_symbol.json',
    #                            orient='index', force_ascii=False)

    print(df_stock_by_symbol)


class RealtimeController:

    def main(self, symbol):
        symbol = symbol
        now = str(datetime.now())
        today = now[:4] + now[5:7] + now[8:10]
        hour = int(now[11:13])

        get_ohlcv_by_symbol(symbol, today)

        while (9 <= hour <= 22):
            now = str(datetime.now())
            hour = int(now[11:13])
            minute = int(now[14:16])
            print(hour, minute)
            if hour == 15 and minute == 30:
                break

            get_ohlcv_by_symbol(symbol, today)
            time.sleep(3)


# if __name__ == '__main__':
#     symbol = '000120'
#     tmp = RealtimeController()
#     tmp.main(symbol=symbol)

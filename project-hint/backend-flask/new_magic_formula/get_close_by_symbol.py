import json
from pykrx import stock
from datetime import datetime, timedelta
import pandas as pd
import time


def get_ohlcv(today):

    # yesterday = today - timedelta(1)
    now = str(datetime.now())
    df_today = now[:19]

    df_stock_by_ticker = stock.get_market_ohlcv_by_ticker(date=today, market="ALL")
    df_stock_by_ticker = df_stock_by_ticker.reset_index()
    df_stock_by_ticker['날짜'] = df_today

    df_stock_name = pd.DataFrame({'티커': stock.get_market_ticker_list(market="ALL")})
    df_stock_name['종목명'] = df_stock_by_ticker['티커'].map(lambda x: stock.get_market_ticker_name(x))
    df_stock = pd.merge(df_stock_name, df_stock_by_ticker, left_on='티커', right_on='티커', how='outer')
    df_stock.columns = ['code', 'name', 'open', 'high', 'low', 'close', 'volume', 'amount', 'rate', 'date']

    df_stock.to_csv(
        '/Users/hwaner/Documents/workspace/project-hint/backend-spring/src/main/resources/static/realtime_stocks.csv',
        sep=',', na_rep='NaN')
    print(df_stock)


def fmain():
    now = str(datetime.now())
    today = now[:4] + now[5:7] + now[8:10]
    hour = int(now[11:13])
    minute = int(now[14:16])

    while (9 <= hour <= 21):
        now = str(datetime.now())
        hour = int(now[11:13])
        minute = int(now[14:16])
        print(hour, minute)
        if hour == 15 and minute == 30:
            break
        get_ohlcv(today)
        time.sleep(5)


# fmain()

if __name__ == '__main__':
    fmain()

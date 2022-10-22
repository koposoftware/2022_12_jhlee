from datetime import datetime, timedelta
from pykrx import stock


class get_change_ratio:

    def get_up(self):

        today = str(datetime.now())
        df_today = today[:10]

        df_p = stock.get_market_price_change_by_ticker(df_today, df_today).sort_values(by='등락률', ascending=False)
        df_p_top5 = df_p.iloc[:5].copy()
        df_p_top5 = df_p_top5.reset_index()

        # df_p = df_p.drop(['시가', '종가', '변동폭', '거래량', '거래대금'], axis=1)

        result = df_p_top5[['종목명', '종가', '등락률']]

        return result

    def get_down(self):

        today = str(datetime.now())
        df_today = today[:10]
        print(df_today)

        df_p = stock.get_market_price_change_by_ticker(df_today, df_today).sort_values(by='등락률')
        df_p_top5 = df_p.iloc[:5].copy()
        df_p_top5 = df_p_top5.reset_index()

        # df_p = df_p.drop(['시가', '종가', '변동폭', '거래량', '거래대금'], axis=1)

        result = df_p_top5[['종목명', '종가', '등락률']]

        return result

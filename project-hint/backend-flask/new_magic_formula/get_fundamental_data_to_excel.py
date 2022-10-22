from urllib.request import urlopen, Request

import datetime
import time
import requests
import io
import pandas as pd
from pandas import DataFrame
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine
import MySQLdb
import pandas.io.sql as pdsql

conn = MySQLdb.connect(host='129.154.206.233', port=3306, db='fundamental_data', user='hint', passwd='hint',
                       charset='utf8mb4')
cursor = conn.cursor()
df_stock_list = pdsql.read_sql_query('select 종목코드 from 상장회사_목록', con=conn)

ticker_list = df_stock_list['종목코드'].tolist()


def get_html_fnguide(ticker):
    # def get_html_fnguide(ticker, gb):

    """
    :param ticker: 종목코드
    :param gb: 데이터 종류(0: 재무제표, 1: 재무비율, 2: 투자지표, 3: 컨센서스)
    """

    #     url = []
    #     url.append("http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A" + ticker + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701")
    #     url.append("http://comp.fnguide.com/SVO2/ASP/SVD_FinanceRatio.asp?pGB=1&gicode=A" + ticker + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=104&stkGb=701")
    #     url.append("http://comp.fnguide.com/SVO2/ASP/SVD_Invest.asp?pGB=1&gicode=A" + ticker + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=105&stkGb=701")
    #     url.append("http://comp.fnguide.com/SVO2/ASP/SVD_Consensus.asp?pGB=1&gicode=A" + ticker + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=108&stkGb=701")

    #     if gb > 3 :
    #         return None

    #     url = url[gb]

    url = "http://comp.fnguide.com/SVO2/ASP/SVD_Finance.asp?pGB=1&gicode=A" + ticker + "&cID=&MenuYn=Y&ReportGB=&NewMenuID=103&stkGb=701"
    try:
        # req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36'})
        html_text = urlopen(req).read()

    except AttributeError as e:
        return None

    return html_text


def bulid_fundamental_data_to_excel_in_fnguide():
    data = []
    for code in ticker_list:
        rowIncomeStatement = [2]
        rowFinancialStatement = [8, 0, 4]
        print(code)
        listTicker = [code]

        # 포괄손익계산서 테이블
        try:
            dfIncomeStatement = pd.read_html(get_html_fnguide(code))[0]
            listIncomeStatement = dfIncomeStatement.iloc[rowIncomeStatement, 1].tolist()
        except:
            listIncomeStatement = [0]

        # 재무제표 테이블
        try:
            dfFinancialStatement = pd.read_html(get_html_fnguide(code))[2]
            listFinancialStatement = dfFinancialStatement.iloc[rowFinancialStatement, 1].tolist()
        except:
            listFinancialStatement = [0, 0, 0]

        listFinance = listTicker + listIncomeStatement + listFinancialStatement
        data.append(listFinance)
        listTicker = []

    df = DataFrame(data, columns=['종목코드', '2019 매출총이익', '2019 자본총계', '2019 자산총계', '2019 부채총계'])

    df.to_excel('../static/data/res_finace2019.xlsx')


if __name__ == "__main__":

    start = datetime.datetime.now()
    bulid_fundamental_data_to_excel_in_fnguide()

    print('operation time: ', datetime.datetime.now() - start)

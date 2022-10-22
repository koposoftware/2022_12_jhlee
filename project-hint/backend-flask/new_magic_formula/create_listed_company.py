import requests
import pandas as pd
import io
import mysql.connector
import sqlalchemy
from sqlalchemy import create_engine

engine = create_engine('mysql+mysqlconnector://hint:hint@129.154.206.233:3306/fundamental_data', echo=False)


def get_krx_stock_master():
    # Generate OTP
    gen_otp_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    gen_otp_data = {
        'locale': 'ko_KR',
        'mktTpCd': '0',
        'tboxisuSrtCd_finder_listisu0_6': '전체',
        'isuSrtCd': 'ALL',
        'isuSrtCd2': 'ALL',
        'codeNmisuSrtCd_finder_listisu0_6': '',
        'param1isuSrtCd_finder_listisu0_6': '',
        'sortType': 'A',
        'stdIndCd': 'ALL',
        'sectTpCd': 'ALL',
        'parval': 'ALL',
        'mktcap': 'ALL',
        'acntclsMm': 'ALL',
        'tboxmktpartcNo_finder_designadvser0_6':'',
        'mktpartcNo': '',
        'mktpartcNo2': '',
        'codeNmmktpartcNo_finder_designadvser0_6': '',
        'param1mktpartcNo_finder_designadvser0_6': '',
        'condListShrs': '1',
        'listshrs': '',
        'listshrs2': '',
        'condCap': '1',
        'cap': '',
        'cap2': '',
        'share': '1',
        'money': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT03402',
    }

    r = requests.post(gen_otp_url, gen_otp_data)
    code = r.content

    # download
    down_url = 'http://data.krx.co.kr/comm/fileDn/download_excel/download.cmd'
    down_data = {
        'code': code,
    }

    #io를 사용하여 다운로드 파일을 받지않고 file type으로 만들어준다
    r = requests.post(down_url, down_data)
    f = io.BytesIO(r.content)

    usecols = ['종목코드', '종목명', '업종코드', '업종명']
    df = pd.read_excel(f, converters={'종목코드': str, '업종코드': str}, usecols=usecols)
    df.columns = ['종목코드', '종목명', '업종코드', '업종명']
    return df


# 상장회사 목록을 listed_company table명으로 만든다.
if __name__ == "__main__":

    df = get_krx_stock_master()
    df.to_sql(name='상장회사_목록', con=engine, if_exists='replace', index=False)
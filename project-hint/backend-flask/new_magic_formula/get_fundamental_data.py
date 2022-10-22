import datetime
import time
import MySQLdb
import pandas.io.sql as pdsql
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame


def get_company_fundamental_fnguide(code):
    url = "http://asp01.fnguide.com/SVO2/ASP/SVD_Main.asp?pGB=1&gicode=A%s&NewMenuID=11&cID=50&MenuYn=N" % (code)
    respstr = requests.get(url).text
    soup = BeautifulSoup(respstr, "lxml")

    # <!--IFRS 별도/연간 -->
    target_table = soup.find("div", class_="um_table", id="highlight_D_A")
    # print(target_table)

    result = []
    # target_table.find_all('tr')
    for tr in target_table.find_all('tr'):
        #     print("[%s]" % tr)
        for th in tr.find_all('th'):
            value = "%s" % th.text.replace('(P) : Provisional', '').replace('(E) : Estimate', '').replace('잠정실적', '').replace(
                '컨센서스, 추정치', '').replace('(E)', '').replace('(P)', '').replace('/', '-').strip()
            if ('-04' in value) or ('-06' in value) or ('-09' in value) or ('-11' in value):
                value = value + '-30'
            elif ('-01' in value) or ('-03' in value) or ('-05' in value) or ('-07' in value) or ('-08' in value) or (
                    '-10' in value) or ('-12' in value):
                value = value + '-31'
            elif ('-02' in value):
                value = value + '-28'

            result.append(value)
            #     print(value)
        #         print("[%s]" % th.text.replace('(E) : Estimate','').replace('컨센서스, 추정치','').strip())
        for td in tr.find_all('td'):
            value = td.text.strip().replace(',', '')
            try:
                value = float(value)
            except Exception as e:
                value = 0
            result.append(value)
    #         print(td.text.strip())

    del result[0]
    del result[1]
    # result

    dfdata = []
    for x in range(0, len(result), 9):
        dfdata.append(result[x:x + 9])
    # print(dfdata[:5])

    df = DataFrame(data=dfdata, columns=[str(x) for x in range(1, 10)]).T
    df.columns = ['날짜', '매출액', '영업이익', '영업이익(발표기준)', '당기순이익', '-지배주주순이익', '-비지배주주순이익', '자산총계', '부채총계', '자본총계',
                  '-지배주주지분', '-비지배주주지분', '자본금', '부채비율', '유보율', '영업이익률', '순이익률', 'ROA', 'ROE', 'EPS', 'BPS', 'DPS',
                  'PER', 'PBR', '발행주식수', '배당수익률']
    # df[:5]
    df.drop(df.index[[0]], inplace=True)
    df = df[['날짜', '매출액', '영업이익', '당기순이익', '자산총계', '부채총계', '자본총계', '자본금', '부채비율', '유보율', '영업이익률', '순이익률', 'ROA', 'ROE',
             'EPS', 'BPS', 'DPS', 'PER', 'PBR', '발행주식수', '배당수익률']]
    # df

    df_year = df[:4]
    df_qtr = df[4:]

    return (df_year, df_qtr)


def build_fundamenta_data():
    conn = MySQLdb.connect(host='129.154.206.233', port=13366, db='fundamental_data', user='hint', passwd='nothint0115', charset='utf8mb4')
    cursor = conn.cursor()

    replace_sqlite = (
        "replace into 상장회사_재무정보( 날짜, 종목코드, 기간구분, 매출액, 영업이익, 당기순이익, 자산총계, 부채총계, 자본총계, 자본금, 부채비율, 유보율, 영업이익률, 순이익률, ROA, ROE, EPS, BPS, DPS, PER, PBR, 발행주식수, 배당수익률 ) "
        "values(%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s) "
    )

    df = pdsql.read_sql_query('select 종목코드, 종목명 from 상장회사_목록', con=conn)

    CODES = list(df.values)
    for code, name in CODES:
        time.sleep(1)
        try:
            (df_year, df_qtr) = get_company_fundamental_fnguide(code)
        except Exception as e:
            continue
        print('FnGuide - %s %s' % (code, name))

        if len(df_year.index) > 0 or len(df_qtr.index) > 0:
            if len(df_year.index) > 0:
                기간구분 = '년간'
                for idx, row in df_year.iterrows():
                    날짜, 매출액, 영업이익, 당기순이익, 자산총계, 부채총계, 자본총계, 자본금, 부채비율, 유보율, 영업이익률, 순이익률, ROA, ROE, EPS, BPS, DPS, PER, PBR, 발행주식수, 배당수익률 = row
                    종목코드 = code
                    d = (
                        날짜, 종목코드, 기간구분, 매출액, 영업이익, 당기순이익, 자산총계, 부채총계, 자본총계, 자본금, 부채비율, 유보율, 영업이익률, 순이익률, ROA, ROE, EPS, BPS,
                        DPS, PER, PBR, 발행주식수, 배당수익률)
                    cursor.execute(replace_sqlite, d)
                    conn.commit()

            if len(df_qtr.index) > 0:
                기간구분 = '분기'
                for idx, row in df_qtr.iterrows():
                    날짜, 매출액, 영업이익, 당기순이익, 자산총계, 부채총계, 자본총계, 자본금, 부채비율, 유보율, 영업이익률, 순이익률, ROA, ROE, EPS, BPS, DPS, PER, PBR, 발행주식수, 배당수익률 = row
                    종목코드 = code
                    d = (
                        날짜, 종목코드, 기간구분, 매출액, 영업이익, 당기순이익, 자산총계, 부채총계, 자본총계, 자본금, 부채비율, 유보율, 영업이익률, 순이익률, ROA, ROE, EPS, BPS,
                        DPS, PER, PBR, 발행주식수, 배당수익률)
                    cursor.execute(replace_sqlite, d)
                    conn.commit()


# if __name__ == "__main__":
#     # 재무정보가져오기 - 분기에 한번 실행하면 됨 operation time:  0:55:17.424615
#     start = datetime.datetime.now()
#     build_fundamenta_data()
#
#     print('operation time: ', datetime.datetime.now() - start)

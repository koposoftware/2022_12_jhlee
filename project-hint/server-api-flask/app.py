from flask import Flask, request, abort, jsonify, Response, make_response
import json
from time import time
from time import localtime
from pytz import timezone
import FinanceDataReader as fdr
from pykrx import stock
from datetime import date, timedelta, datetime
import logging
from flask_cors import CORS

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
cors = CORS(app, resources={r"/**": {"origins": "*"}})


# Health Check
@app.route('/ping')
def ping():
    return 'ping은 돌아오는거야'


allowed_stock_type = ['KRX', 'NASDAQ', 'NYSE']


# 상장중인 종목 정보를 불러오는 API (국내 주식, 해외 주식)
@app.route('/api/stock/codes')
def getListedStockCodes():
    type = request.args.get('type')
    if type not in allowed_stock_type:
        abort(400, 'Bad Type')

    if type == 'KRX':
        return jsonify(getKrxCodes())

    df = fdr.StockListing(type)[['Symbol', 'Name']]
    return Response(df.to_json(orient='records'), mimetype='application/json')


def getKrxCodes():
    krx_stock_codes = []
    for ticker in stock.get_market_ticker_list(market='ALL'):
        name = stock.get_market_ticker_name(ticker)
        krx_stock_codes.append({
            "Symbol": ticker,
            "Name": name
        })
    return krx_stock_codes


# 해당하는 주식들의 현재가를 조회하는 API
@app.route('/api/stock/price')
def getCurrentStockPrice():
    codes = request.args.get('codes')
    result = []
    last_day = date.today() - timedelta(days=14)
    for code in distinctAndSplit(codes):
        current_price = fetchCurrentStockPrice(code, last_day)
        if current_price:
            result.append(current_price)
    return jsonify(result)


@app.route('/api/stock/int-price')
def getCurrentStockPriceToInt():
    codes = request.args.get('codes')
    last_day = date.today() - timedelta(days=14)
    for code in distinctAndSplit(codes):
        current_price = fetchCurrentStockPriceToInt(code, last_day)
        if current_price:
            response = make_response(json.dumps(current_price))
            response.content_type = 'application/json'
    return response


def distinctAndSplit(codes):
    return list(set(codes.split(",")))


def fetchCurrentStockPrice(code, day):
    try:
        return {
            "code": code,
            "price": str(fdr.DataReader(code, day)[['Close']].iloc[-1][0])
        }
    except Exception as e:
        logging.error("주식 현재가를 불러오는 중 에러가 발생하였습니다 code: {0} error: {1}".format(code, e))


def fetchCurrentStockPriceToInt(code, day):
    try:
        data = [time() * 1000, int(str(fdr.DataReader(code, day)[['Close']].iloc[-1][0]))]
        return data
    except Exception as e:
        logging.error("주식 현재가를 불러오는 중 에러가 발생하였습니다 code: {0} error: {1}".format(code, e))


@app.route('/api/stock/change-ratio/descending', methods=['GET'])
def change_ratio_descending():
    get_ratio = get_descending()
    return get_ratio.to_json(orient='index', force_ascii=False)


@app.route('/api/stock/change-ratio/ascending', methods=['GET'])
def change_ratio_ascending():
    get_ratio = get_ascending()
    return get_ratio.to_json(orient='index', force_ascii=False)


def get_descending():
    today = datetime.now()
    # df_today = today[:10]

    df_p = stock.get_market_price_change_by_ticker(today, today).sort_values(by='등락률', ascending=False)
    df_p_top5 = df_p.iloc[:5].copy()
    df_p_top5 = df_p_top5.reset_index()
    print(df_p_top5)

    # df_p = df_p.drop(['시가', '종가', '변동폭', '거래량', '거래대금'], axis=1)

    result = df_p_top5[['종목명', '종가', '등락률']]
    result['등락률'] = result['등락률'] / 100

    return result


def get_ascending():
    today = datetime.now()
    # df_today = today[:10]

    df_p = stock.get_market_price_change_by_ticker(today, today).sort_values(by='등락률')
    # df_p = stock.get_market_price_change_by_ticker('20220929', '20220930').sort_values(by='등락률')
    df_p_top5 = df_p.iloc[:5].copy()
    df_p_top5 = df_p_top5.reset_index()
    print(df_p_top5)

    # df_p = df_p.drop(['시가', '종가', '변동폭', '거래량', '거래대금'], axis=1)

    result = df_p_top5[['종목명', '종가', '등락률']]
    result['등락률'] = result['등락률'] / 100

    return result


CORS(app)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)

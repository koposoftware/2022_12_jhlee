from flask import Flask, render_template, make_response

import json
from candle.candle_crawling import CandleController
from flask_cors import CORS

from change_ratio.get_change_ratio import get_change_ratio
from news.read_csv import ReadCsvCreateForWordcloud
from new_magic_formula.model import Recommendation_Stock_Model
from realtime_stock_data.realtime_data_to_json_by_symbol import RealtimeController
from datetime import datetime, timedelta
import time
from time import time
from random import random

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
CORS(app, resources={r'/**': {"origins": "*"}})
CORS(app, supports_credentials=True)
CORS_ALLOW_ORIGIN = "*,*"
CORS_EXPOSE_HEADERS = "*,*"
CORS_ALLOW_HEADERS = "content-type,*"
cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(","),
            expose_headers=CORS_EXPOSE_HEADERS.split(","), supports_credentials=True)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


# @app.route('/')
# def hello_world():
#     return render_template('index.html')


@app.route('/recommendation/<period>/<propensity>', methods=['GET'])
def recommend_stock(period, propensity):
    period = period
    propensity = propensity
    print(period, propensity)
    recommend_stock_model = Recommendation_Stock_Model()
    return json.dumps(recommend_stock_model.recommendation_listing(period=period, propensity=propensity))


@app.route('/change-ratio/up', methods=['GET'])
def change_ratio_up():
    get_ratio = get_change_ratio()
    return get_ratio.get_up().to_json(orient='index', force_ascii=False)


@app.route('/change-ratio/down', methods=['GET'])
def change_ratio_down():
    get_ratio = get_change_ratio()
    return get_ratio.get_down().to_json(orient='index', force_ascii=False)


@app.route('/wordcloud', methods=['GET'])
def create_wordcloud_using_csv():
    c = ReadCsvCreateForWordcloud()
    result = c.read()
    print(result)
    return result


@app.route('/stocks/candle/<symbol>', methods=['GET'])
def get_candle(symbol):
    symbol = symbol
    tmp = CandleController()
    app_result = tmp.candle_crawling(symbol=symbol)
    return json.dumps(app_result)


@app.route('/stocks/realdata/<symbol>', methods=['GET'])
def get_realdata_by_symbol(symbol):
    # symbol = symbol
    # tmp = RealtimeController()
    # tmp.main(symbol=symbol)

    # now = str(datetime.now())
    # today = now[:4] + now[5:7] + now[8:10]
    # hour = int(now[11:13])
    #
    # while (0 <= hour <= 5):
    #     now = str(datetime.now())
    #     hour = int(now[11:13])
    #     minute = int(now[14:16])
    #     print(hour, minute)
    #     if hour == 15 and minute == 30:
    #         break
    #
    #     with open(
    #             '/Users/hwaner/Documents/workspace/project-hint/backend-flask/static/data/stock_real_data_by_symbol.json',
    #             "r", encoding='UTF8') as f:
    #         json_data = json.load(f)
    #
    #     res = json.dumps(json_data, indent="\t", sort_keys=True, ensure_ascii=False)
    #     time.sleep(3)
    #     return res

    now = str(datetime.now())
    today = now[:4] + now[5:7] + now[8:10]
    hour = int(now[11:13])

    while (0 <= hour <= 5):
        now = str(datetime.now())
        hour = int(now[11:13])
        minute = int(now[14:16])
        print(hour, minute)
        if hour == 15 and minute == 30:
            break

        symbol = symbol
        tmp = RealtimeController()
        tmp.main(symbol=symbol)

        with open(
                '/Users/hwaner/Documents/workspace/project-hint/backend-flask/static/data/stock_real_data_by_symbol.json',
                "r", encoding='UTF8') as f:
            json_data = json.load(f)

        res = json.dumps(json_data, indent="\t", sort_keys=True, ensure_ascii=False)
        time.sleep(3)
        return res


@app.route('/live-data', methods=['GET'])
def live_data():
    # Create a PHP array and echo it as JSON
    data = [time() * 1000, random() * 100]
    print(data)
    response = make_response(json.dumps(data))
    response.content_type = 'application/json'
    return response


CORS(app)
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', threaded=True)

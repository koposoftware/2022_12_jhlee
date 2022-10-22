from flask import Flask, render_template, request, Response, url_for, redirect, make_response, jsonify, request
from flask_cors import CORS
from datetime import datetime, date, timedelta
import flask
import math
import json
import re
import io
import time
import os
import warnings

from pykrx import stock
import FinanceDataReader as fdr

import numpy as np
import pandas as pd
import yfinance as yf
import seaborn as sns
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
from matplotlib import font_manager, rc

from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly
from fbprophet.plot import add_changepoints_to_plot
from mplfinance.original_flavor import candlestick_ohlc

import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.subplots as ms
from plotly.subplots import make_subplots

from ta.trend import MACD
from ta.momentum import StochasticOscillator
from ta.momentum import RSIIndicator

import chart_studio.tools as tls
# import chart_studio
# import chart_studio.plotly as py

from code_cr import *
import pattern as pt

# %matplotlib inline
# warnings.filterwarnings('ignore')

print ('설정파일 위치: ', matplotlib.matplotlib_fname())
print(matplotlib.get_cachedir())

# rc('font', family='AppleGothic')
rc('font', family='Noto Sans KR')
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans KR']

matplotlib.use('Agg')

# ======================================================================== 데이터 가져오기

# com_df = pd.read_csv('com_df_botong.csv',
#                      dtype={'stock_code': 'str', '표준코드': 'str', '단축코드': 'str', 'stock_code_ori': 'str'},
#                      parse_dates=['listed_date', '상장일'])

com_df = pd.read_csv('com_df_botong.csv',
                     dtype={'stock_code': 'str', '표준코드': 'str', '단축코드': 'str'},
                     parse_dates=['listed_date', '상장일'])


# ======================================================================== router

app = Flask(__name__, template_folder="templates", static_folder="static")
# app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
# CORS_ALLOW_ORIGIN = "*,*"
# CORS_EXPOSE_HEADERS = "*,*"
# CORS_ALLOW_HEADERS = "content-type,*"
# cors = CORS(app, origins=CORS_ALLOW_ORIGIN.split(","), allow_headers=CORS_ALLOW_HEADERS.split(","),
#             expose_headers=CORS_EXPOSE_HEADERS.split(","), supports_credentials=True)


@app.route('/')
def index():
    return render_template("index.html")

# ======================================================================== 자동완성(실시간 비동기 처리)

@app.route('/com_search_ajax', methods=['post'])
def com_search_ajax():
    str = request.form.get('search_input')
    print(str + "검색")

    # 웹에서 입력한 검색어와 관련된 업체만 가져오기
    # com_df_rm >>> 금융/보험 데이터 제거한 데이터 가져오기
#     com_df_srch = com_df = pd.read_csv('com_df_rm_botong.csv',
#                                        dtype={'stock_code': 'str', '표준코드': 'str', '단축코드': 'str', 'stock_code_ori': 'str'},
#                                        parse_dates=['listed_date', '상장일'])
    
    com_df_srch = com_df = pd.read_csv('com_df_rm_botong.csv',
                                       dtype={'stock_code': 'str', '표준코드': 'str', '단축코드': 'str'},
                                       parse_dates=['listed_date', '상장일'])

    temp = com_df_srch[(com_df_srch['한글 종목약명'].str.contains(str)) | (com_df_srch['한글 종목약명'].str.contains(str.upper()))][
        ['yh_code', '한글 종목약명']].head(10)
    
    print(temp.values.tolist())
    
    return json.dumps(temp.values.tolist())


# ======================================================================== 전송 후 페이지 처리

@app.route('/form_submit_get', methods=["get"])
def form_submit_get():

    # 전송된 데이터 받기
    hidden_stock_code = request.args.get("hidden_stock_code")
    hidden_corp_name = request.args.get("hidden_corp_name")
#     p_hidden_corp_name = hidden_corp_name[:-3]

    # 우선주 종목코드 >>> 보통주 종목코드
#     origin_code = ori_code(hidden_stock_code)
    origin_code = hidden_stock_code[:-3]

    # yfinance 종목코드 >>> pykrx 종목코드
    stock_code = hidden_stock_code[:-3]

    # 재무 정보 시각화
    radar_label, radar_dict, weather_list, foreign, giguan = relate_radar_weather_data(stock_code=stock_code)
    
    bar_label, bar_mch_list, bar_dg_list = mch_dg(stock_code=stock_code)
    
    icons = icon_selection(weather_list)
    print(icons)
    icons2 = foreign_giguan([foreign, giguan])

    if math.isnan(giguan):
        giguan = 0.01
    if math.isnan(foreign):
        foreign = 0.01

    giguan = format(int(giguan), ',')
    foreign = format(int(foreign), ',')

    # 뉴스 크롤링
    df = news_crawl(origin_code)  # 우선주 >>> 보통주
    json_str = df.to_json(orient="values")
    json_obj = json.loads(json_str)
    code = invest_opinion(origin_code)  # 우선주 >>> 보통주

    # 재무제표 크롤링
    ifrs = crawl_ifrs(origin_code)  # 우선주 >>> 보통주

    # 경제지수, 기업 주가
    chart_res = chart_data(hidden_stock_code)
    f_info = finance_data(hidden_stock_code)

    return render_template("res.html", ifrs=ifrs,
                           res_obj=chart_res,
                           hidden_corp_name=hidden_corp_name,
                           stock_code=stock_code,
                           f_info=f_info,
                           RD_LABEL_LIST=radar_label, RD_DATA_DICT=radar_dict,
                           BAR_LABEL_LIST=bar_label,
                           BAR_DATA_LIST_MCH=bar_mch_list,
                           BAR_DATA_LIST_DG=bar_dg_list, MY_NEWS=json_obj, MY_CODE=code,
                           # MY_HIGH=high_stock, MY_LOW=low_stock, MY_CLOSE=close_stock,
                           # MY_MAE=mae_mean,
                           # 날씨
                           WEATHER_DATA_LIST=weather_list,
                           ICONS=icons,
                           FOREIGN=foreign,  # 외인 매수
                           GIGUAN=giguan,  # 기관 매수
                           ICONS2=icons2  # 외인, 기관 매수
                           )


# ======================================================================== 날짜선택에 따른 주가정보

# 날짜지정을 하지 않을경우 >>> 1년 주가정보
def chart_data(ent, select_date=None):
    ent = ent.split(".")[0]
    if (select_date != None):
        ent_df = stock.get_market_ohlcv_by_date(fromdate=select_date[0], todate=select_date[1], ticker=ent)

    else:
        e_date = datetime.now()
        s_date = e_date - timedelta(days=30)
        print(f"s_date .................: {s_date}")
        ent_df = stock.get_market_ohlcv_by_date(fromdate=s_date, todate=e_date, ticker=ent)

    ent_df = ent_df.reset_index()
    ent_df = ent_df.drop(['시가', '고가', '저가', '거래량'], axis=1)
    ent_df.columns = ['Date', 'Close']
    ent_df['Date'] = ent_df['Date'].astype('str')
    ent_dict = ent_df.to_dict()

    dfcp = ent_df.tail(2)
    rate_color = dfcp['Close'].values.tolist()
    ent_dict['eve'] = rate_color[0]
    ent_dict['today'] = rate_color[1]
    if (rate_color[1] - rate_color[0] < 0):
        ent_dict['rate'] = "fa fa-sort-desc"
        ent_dict['color'] = 'blue'
    else:
        ent_dict['rate'] = "fa fa-sort-asc"
        ent_dict['color'] = 'red'

    res = {'ent': ent, 'ent_dict': ent_dict}
    return res


# ======================================================================== 비동기로 선택한 날짜를 yfinance의 날짜로 가공

@app.route('/calendar_ajax_handle', methods=["post"])
def calendar_ajax_handle():
    data = request.form.get("prm")
    ent_name = request.form.get("ent")
    splt_data = data.split(":")
    se_list = []
    for my_day in splt_data:
        se_list.append(str(datetime.strptime(my_day, "%m/%d/%Y").date()))
    print(f'ent_name............. : {ent_name}')
    res = chart_data(ent_name, se_list)
    return res


# ======================================================================== 주요지표 크롤링

# 전일대비 html에 뿌려줄 data >>> [rate, color]
def finance_data(stock_code):
    stock_list = ['^KS11', '^KQ11', '^IXIC', '^GSPC', '^DJI']
    res_list = {}
    for stock in stock_list:
        yf_df = yf.download(stock, start='2022-01-01')
        se_list = round(yf_df.tail(2).reset_index()['Close'].astype('float'), 2)
        if (se_list[1] - se_list[0] < 0):
            se_list['rate'] = "fa fa-sort-desc"
            se_list['color'] = 'blue'
        else:
            se_list['rate'] = "fa fa-sort-asc"
            se_list['color'] = 'red'
        res_list[stock] = se_list
    return res_list

# ======================================================================== 예측 카드

@app.route('/prediction', methods=['GET', 'POST'])
def index_inner():

    if request.method == 'GET':
        stock_code = request.args.get("stock_code")
        return render_template('index_inner.html', stock_code=stock_code)
    
    else:
        code = request.form['code']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        period = request.form['period']

        if request.form['action'] == '프랙탈 기반 예측':
            return redirect(url_for('pattern', startdate=startdate, enddate=enddate, code=code, period=period))
        
        if request.form['action'] == 'Prophet 모델 기반 예측':
            return redirect(url_for('prophet', startdate=startdate, enddate=enddate, code=code, period=period)) 
     

@app.route('/com_search_code', methods=['POST'])
def com_search_code():
    str = request.form.get('search_input')
    print(str + "검색")

    com_df_srch = com_df = pd.read_csv('com_df_rm_botong.csv',
                                       dtype={'stock_code': 'str', '표준코드': 'str', '단축코드': 'str'},
                                       parse_dates=['listed_date', '상장일'])

    temp = com_df_srch[(com_df_srch['한글 종목약명'].str.contains(str)) | (com_df_srch['한글 종목약명'].str.contains(str.upper()))][
        ['stock_code', '한글 종목약명']].head(3)
    
    print(temp.values.tolist())
    
    return json.dumps(temp.values.tolist())
    
    
@app.route('/plot.png', methods=['GET'])
def plot_png():
    code = request.args.get('code', None)
    startdate = request.args.get('startdate', None)
    enddate = request.args.get('enddate', None)
    period = int(request.args.get('period', None))
    print(startdate)
    
    p = pt.PatternFinder()
    p.set_stock(code, enddate)
    result = p.search(startdate, enddate, period)
    print(result)
    if len(result) > 0:
        fig = p.plot_pattern(list(result.keys())[0], period)
        output = io.BytesIO()
        FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.route('/plotchart.png', methods=['GET'])
def plot_chart():
    code = request.args.get('code', None)
    startdate = request.args.get('startdate', None)
    enddate = request.args.get('enddate', None)
    
    period = int(request.args.get('period', None))
    enddate_tmp = request.args.get('enddate', None)
    
    format = '%Y-%m-%d'
    tomorrow = datetime.strptime(enddate_tmp,format) + timedelta(1)
    after_period = tomorrow + timedelta(period - 1)
    print(tomorrow)
    print(after_period)
    
    fig = plt.figure(figsize=(6.9, 4.9), tight_layout=True)
    fig.set_facecolor('w')
#     gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1])
    axes = []
    axes.append(plt.subplot())
#     axes.append(plt.subplot(gs[1], sharex=axes[0]))
    axes[0].get_xaxis().set_visible(True)

    print(code)
    data = fdr.DataReader(code)
    data_ = data[startdate:enddate]
    print(code, startdate, enddate)

    x = np.arange(len(data_.index))
    ohlc = data_[['Open', 'High', 'Low', 'Close']].values
    dohlc = np.hstack((np.reshape(x, (-1, 1)), ohlc))
    
    day_list = []
    name_list = []
    for i, day in enumerate(data_.index):
        if day.dayofweek == 0:
            day_list.append(i)
            name_list.append(day.strftime('%m-%d') + '(Mon)')
    
    # 봉차트
    axes[0].set_xticks(range(len(x)))
    axes[0].get_xaxis().set_major_locator(ticker.FixedLocator(day_list))
    axes[0].get_xaxis().set_major_formatter(ticker.FixedFormatter(name_list))
    axes[0].set_xticklabels(list(name_list), rotation=30)
    candlestick_ohlc(axes[0], dohlc, width=0.5, colorup='r', colordown='b', alpha=0.5)
    
    axes[0].set_facecolor('#F9F9F9')
    axes[0].spines['bottom'].set_color('#F9F9F9')
    axes[0].spines['top'].set_color('#F9F9F9')
    axes[0].spines['left'].set_color('#F9F9F9')
    axes[0].spines['right'].set_color('#F9F9F9')

    # 거래량 차트
#     axes[1].bar(x, data_['Volume'], color='grey', width=0.6, align='center')
#     axes[1].set_xticks(range(len(x)))
#     axes[1].get_xaxis().set_major_locator(ticker.FixedLocator(day_list))
#     axes[1].get_xaxis().set_major_formatter(ticker.FixedFormatter(name_list))
#     axes[1].set_xticklabels(list(name_list), rotation=45)
#     axes[1].get_xaxis().set_major_locator(ticker.MaxNLocator(10))
#     axes[1].set_xticklabels(list(data_.index.strftime('%Y-%m-%d')), rotation=45)
#     axes[1].set_xticklabels(list(data_.index.strftime('%m/%d')), rotation=60)
#     axes[1].get_xaxis().set_visible(True)
#     axes[1].get_yaxis().set_visible(False)

    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = "AppleGothic"
    plt.rcParams['font.family'] = "sans-serif"
    
    plt.grid(visible=True, color='w', axis='x')
    plt.tight_layout()

    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


@app.errorhandler(403)
@app.errorhandler(404)
@app.errorhandler(410)
@app.errorhandler(500)
def page_not_found(e):
    return render_template('error.html')


@app.route('/pattern', methods=['GET', 'POST'])
def pattern():
    
    if request.method == 'POST':
        code = request.form['code']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        period = int(request.form['period'])
        
        startdate_tmp = request.form['startdate']
        enddate_tmp = request.form['enddate']
        
    else:
        code = request.args.get('code', None)
        startdate = request.args.get('startdate', None)
        enddate = request.args.get('enddate', None)
        period = int(request.args.get('period', None))
        
        startdate_tmp = request.args.get('startdate', None)
        enddate_tmp = request.args.get('enddate', None)
        
    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = "AppleGothic"
    plt.rcParams['font.family'] = "sans-serif"
    
    p = pt.PatternFinder()
    p.set_stock(code, enddate)
    result = p.search(startdate, enddate, period)
    preds = p.stat_prediction(result, period)
    
    format = '%Y-%m-%d'
    chart_start_date = datetime.strptime(startdate_tmp, format) - timedelta(30)
#     chart_end_date = datetime.strptime(enddate_tmp, format) + timedelta(period + 5)

    print(chart_start_date)
#     print(chart_end_date)

    df = fdr.DataReader(code, chart_start_date)

#     df = df.dropna()
    df = df.drop(['Change'], axis=1)
    
    dt_all = pd.date_range(start=df.index[0],end=df.index[-1])
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
    
    fig = go.Figure()
    fig = make_subplots(specs = [[{"secondary_y": True}]])

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color = 'red',
            decreasing_line_color = 'blue',
    #         showlegend=False,
            name='캔들'),
    #     secondary_y=True
    )
    
    ## 거래량
    colors = ['red' if row['Open'] - row['Close'] >= 0 else 'blue' for index, row in df.iterrows()]
    fig.add_trace(
        go.Bar(
            x=df.index, 
            y=df['Volume'],
            marker_color=colors,
            name='거래량',
            opacity=0.35,
            showlegend=False
        ),
    #     row=2, col=1,
        secondary_y=True
    )

    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=df['Close'], 
            opacity=0.8, 
            line=dict(color='green', width=1.5), 
            name='종가'),
    #     secondary_y=True
    )
    
    fig.update_yaxes(
        secondary_y=False,
        range=[df.Close.min()*0.9, df.Close.max()*1.1],
        showticklabels=True
    )

    fig.update_yaxes(
        secondary_y=True,
        range=[0, df.Volume.max()*3],
        showticklabels=False,
        ticklabelposition="inside top"
    )
    
    fig.update_yaxes(tickformat=',') 

    fig.update_layout({
#         'title': dict(
#             # <br> 태크와 <sup>태그 사용해서 서브 타이틀을 작성할 수 있음
#             text='캔들 + 거래량',
#             x=0.493,
#             y=0.977,
#             font=dict(
#                 size=14,
#                 color="#73879C"
#             )
#         ),
    #     'template': 'plotly_white',
        'width': 720,
        'height': 445,
    #     'plot_bgcolor': 'rgba(228,236,246,0.5)',
        'plot_bgcolor': 'rgba(247,247,247,0.8)',
    #     'paper_bgcolor': 'rgba(0,0,0,0)',
        'legend': dict(
            yanchor = "top", y = 0.98,
            xanchor = "left", x = 0.01,
            bordercolor="#EDEDED",
            borderwidth=2,
            itemsizing='constant',
        ),
        'autosize': False,
        'margin': dict(
            l=20,
            r=5,
            t=30,
            b=20
        ),
        'hovermode': 'x',
        'xaxis_rangeslider_visible': False,
        'xaxis_rangebreaks': [dict(values=dt_breaks)],
    })
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    if len(preds) > 0:
        avg_ = preds.mean() * 100
        min_ = preds.min() * 100
        max_ = preds.max() * 100
        size_ = len(preds)
        print(avg_, min_, max_, size_)
        return render_template('res_inner.html', code=code, startdate=startdate, enddate=enddate, period=period,
                               graphJSON=graphJSON, avg=round(avg_, 2), min=round(min_, 2), max=round(max_, 2), size=size_)
    else:
        return render_template('res_inner.html', code=code, startdate=startdate, enddate=enddate, period=period, noresult=1)


@app.route('/prophet', methods=['GET', 'POST'])
def prophet():
    
    if request.method == 'POST':
        code = request.form['code']
        startdate = request.form['startdate']
        enddate = request.form['enddate']
        period = int(request.form['period'])
    else:
        code = request.args.get('code', None)
        startdate = request.args.get('startdate', None)
        enddate = request.args.get('enddate', None)
        period = int(request.args.get('period', None))
        
    stock = fdr.DataReader(code, startdate, enddate)
    stock['y'] = stock['Close']
    stock['ds'] = stock.index
    
    stock_real = fdr.DataReader(code, startdate)

    m = Prophet(daily_seasonality=True, seasonality_prior_scale= 0.01, changepoint_prior_scale=1.0)
    m.fit(stock)

    future = m.make_future_dataframe(periods=period)

    forecast = m.predict(future)

    rc('font', family='AppleGothic')
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = "AppleGothic"
    plt.rcParams['font.family'] = "sans-serif"

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x = forecast['ds'].dt.to_pydatetime(), 
            y = forecast['yhat'], 
        opacity=1, 
#         line=dict(color='#0072B2', width=3),
        line=dict(color='#007BFF', width=2.5),
        name='예측 종가'),
#         secondary_y=True
    )

    fig.add_trace(
        go.Scatter(
            x = stock_real.index, 
            y = stock_real['Close'], 
            opacity = 1, 
            line = dict(color = 'red', width = 2), 
            name = '실제 종가'),
#             secondary_y=True
    )
    
    fig.add_trace(
        go.Scatter(
        x = stock_real.index, 
        y = stock_real['Close'],
        opacity = 0.8,
        mode = 'markers',
        marker=dict(size=4.5, color='black'),
        name = '실제 종가(산점도)',
        visible='legendonly'
        )
    )

    fig.add_trace(
        go.Scatter(
            x = forecast['ds'].dt.to_pydatetime(),
            y = forecast['yhat_upper'],
            line = dict(color='rgba(0,0,0,0)'),
            name='80% 신뢰구간',
            legendgroup='80% 신뢰구간',
            showlegend=False
        )
    )

    fig.add_trace(
        go.Scatter(
            x = forecast['ds'].dt.to_pydatetime(),
            y = forecast['yhat_lower'],
            line = dict(color='rgba(0,0,0,0)'),
            fill='tonexty',
            fillcolor = 'rgba(66, 135, 245, 0.2)',
            name='80% 신뢰구간',
            legendgroup='80% 신뢰구간'
        )
    )

    fig.update_yaxes(tickformat=',')
    
    fig.update_layout({
        'xaxis_title': "",
        'yaxis_title': "",
        'width': 1440,
        'height': 550,
        'plot_bgcolor': 'rgba(247,247,247,0.8)',
        'legend': dict(
            yanchor = "top", y = 0.98,
            xanchor = "left", x = 0.01,
            bordercolor="#EDEDED",
            borderwidth=2,
            itemsizing='constant',
            tracegroupgap=2
        ),
        'margin': dict(
            l=20,
            r=5,
            t=30,
            b=20
        ),
        'hovermode': 'x',
    #     'hovermode': 'y',
        'xaxis_rangeslider_visible': False
    })

#     m = Prophet()
#     m.fit(stock)

#     future = m.make_future_dataframe(periods=period)

#     forecast = m.predict(future)

#     fig = plot_plotly(m, forecast)
#     fig2 = plot_components_plotly(m, forecast)
    
#     fig.update_layout({
#         'xaxis_title': "",
#         'yaxis_title': "",
#         'width': 1000,
#         'height': 550,
# #         'plot_bgcolor': 'rgba(228,236,246,0.4)',
#         'plot_bgcolor': 'rgba(247,247,247,0.8)',        
# #         'paper_bgcolor': 'rgba(0,0,0,0)',
#         'margin': dict(
#             l=20,
#             r=5,
#             t=30,
#             b=20
#         ),
#         'xaxis_rangeslider_visible': False
#     })
    
#     fig2.update_layout({
# #         'xaxis_title': "",
# #         'yaxis_title': "",
#         'width': 430,
#         'height': 525,
# #         'plot_bgcolor': 'rgba(228,236,246,0.4)',
#         'plot_bgcolor': 'rgba(247,247,247,0.8)',
# #         'paper_bgcolor': 'rgba(0,0,0,0)',
#         'margin': dict(
#             l=20,
#             r=0,
#             t=30,
#             b=20
#         ),
#         'hovermode': 'x'
#     })
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
#     graphJSON2 = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('prophet.html', graphJSON=graphJSON, code=code, startdate=startdate, enddate=enddate, period=period)

# ======================================================================== 차트 카드

@app.route('/chart', methods=['GET', 'POST'])
def index_inner_chart():

    if request.method == 'GET':
        stock_code = request.args.get("stock_code")
        return render_template('chart.html', stock_code=stock_code)
    
    else:
        code = request.form['code']
        startdate = request.form['startdate']
        enddate = request.form['enddate']

        if request.form['action'] == '차트 보기':
            return redirect(url_for('chart_render', code=code, startdate=startdate, enddate=enddate))


@app.route('/chart_render', methods=['GET', 'POST'])
def chart_render():
    
    if request.method == 'POST':
        code = request.form['code']
        startdate = request.form['startdate']
        enddate = request.form['enddate']

    else:
        code = request.args.get('code', None)
        startdate = request.args.get('startdate', None)
        enddate = request.args.get('enddate', None)

    today = date.today()
    yesterday = date.today() - timedelta(1)

    df = fdr.DataReader(code, start=startdate, end=enddate)
#     df = df[df.Open != 0]

    df['ma_5'] = df['Close'].rolling(window=5).mean()
    df['ma_20'] = df['Close'].rolling(window=20).mean()
    df['ma_60'] = df['Close'].rolling(window=60).mean()
    df['ma_120'] = df['Close'].rolling(window=120).mean()
    df['std'] = df['Close'].rolling(window=20).std(ddof = 0)

    # MACD
    macd = MACD(
        close=df['Close'], 
        window_slow=26,
        window_fast=12, 
        window_sign=9
    )

    # stochastic
    # stoch = StochasticOscillator(
    #     high=df['High'],
    #     close=df['Close'],
    #     low=df['Low'],
    #     window=14,
    #     smooth_window=3
    # )

    # RSI
    rsi = RSIIndicator(
        close = df['Close'],
        window = 14
    )

#     df = df.dropna()
    df = df.drop(['Change'], axis=1)
    print(df)

    dt_all = pd.date_range(start=df.index[0],end=df.index[-1])
    dt_obs = [d.strftime("%Y-%m-%d") for d in pd.to_datetime(df.index)]
    dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]

    fig = go.Figure()

    fig = make_subplots(
        rows=3,
        cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.6,0.2,0.2],
        specs = [[{"secondary_y": True}], [{"secondary_y": False}], [{"secondary_y": False}]]
    )

    fig.add_trace(
        go.Candlestick(
            x=df.index,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            increasing_line_color = 'red',
            decreasing_line_color = 'blue',
    #         showlegend=False,
            name='캔들'),
        secondary_y=False,
        row=1, col=1,
    )

    # 거래량 ----------------------------------------------------------------
    colors = ['blue' if row['Open'] - row['Close'] >= 0 else 'red' for index, row in df.iterrows()]
    fig.add_trace(
        go.Bar(
            x=df.index, 
            y=df['Volume'],
            marker_color=colors,
            name='거래량',
            opacity=0.35,
            showlegend=False
        ),
        secondary_y=True,
        row=1, col=1
    )
    
    ## stoch
    # fig.add_trace(
    #     go.Scatter(
    #         x=df.index,
    #         y=stoch.stoch(),
    #         line=dict(color='black', width=2),
    #         showlegend=False),
    #     row=4, col=1
    # )

    # fig.add_trace(
    #     go.Scatter(
    #         x=df.index,
    #         y=stoch.stoch_signal(),
    #         line=dict(color='blue', width=1),
    #         showlegend=False),
    #     row=4, col=1
    # )    

    # 이평선 ----------------------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=df['ma_5'], 
            opacity=0.8, 
            line=dict(color='green', width=2), 
            name='5일'),
#         secondary_y=True
    )

    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=df['ma_20'], 
            opacity=0.8, 
            line=dict(color='gold', width=2), 
            name='20일'),
#         secondary_y=True
    )

    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=df['ma_60'], 
            opacity=0.8, 
            line=dict(color='darkblue', width=2), 
            name='60일'),
#         secondary_y=True
    )

    fig.add_trace(
        go.Scatter(
            x=df.index, 
            y=df['ma_120'], 
            opacity=0.8, 
            line=dict(color='grey', width=2), 
            name='120일'),
#         secondary_y=True
    )

    # 볼린저밴드(상단)
    fig.add_trace(
        go.Scatter(
            x = df.index,
            y = df['ma_20'] + (df['std'] * 2),
            line_color = 'rgba(44, 160, 44, 0.3)',
#             line = {'dash': 'dash'},
            name = '볼린저밴드',
            legendgroup='볼린저밴드',
            visible='legendonly'),
        row = 1, col = 1
    )

    # 볼린저밴드(하단)
    fig.add_trace(
        go.Scatter(
            x = df.index,
            y = df['ma_20'] - (df['std'] * 2),
            line_color = 'rgba(44, 160, 44, 0.3)',
#             line = {'dash': 'dash'},
            fill = 'tonexty',
            fillcolor = 'rgba(44, 160, 44, 0.15)',
            name = '볼린저밴드',
            legendgroup='볼린저밴드',
            showlegend=False,
            visible='legendonly'),
        row = 1, col = 1
    )

    # 지지저항선 ----------------------------------------------------------------
    def is_support(df,i):
        cond1 = df['Low'][i] < df['Low'][i-1]   
        cond2 = df['Low'][i] < df['Low'][i+1]   
        cond3 = df['Low'][i+1] < df['Low'][i+2]   
        cond4 = df['Low'][i-1] < df['Low'][i-2]  
        return (cond1 and cond2 and cond3 and cond4) 

    def is_resistance(df,i):  
        cond1 = df['High'][i] > df['High'][i-1]   
        cond2 = df['High'][i] > df['High'][i+1]   
        cond3 = df['High'][i+1] > df['High'][i+2]   
        cond4 = df['High'][i-1] > df['High'][i-2]  
        return (cond1 and cond2 and cond3 and cond4)

    def is_far_from_level(value, levels, df):    
        ave =  np.mean(df['High'] - df['Low'])    
        return np.sum([abs(value-level)<ave for _,level in levels])==0

    levels = []
    for i in range(2, df.shape[0] - 2):  
        if is_support(df, i):    
            low = df['Low'][i]    
            if is_far_from_level(low, levels, df):      
                levels.append((i, low))  
        elif is_resistance(df, i):    
            high = df['High'][i]    
            if is_far_from_level(high, levels, df):      
                levels.append((i, high))
                
    fig.add_trace(
         go.Scatter(
            x = [df.index[levels[0][0]], max(df.index)],
            y = [levels[0][1], levels[0][1]],
            mode = "lines",
            line = dict(shape = 'linear', color = 'coral', width = 1.2),
            opacity = 0.5,
            name='지지/저항선',
            legendgroup='지지/저항선',
            visible='legendonly'),
        row=1, col=1
    )
    
    for level in levels[1:]:
        fig.add_trace(
            go.Scatter(
                x = [df.index[level[0]], max(df.index)],
                y = [level[1], level[1]],
                mode = "lines",
                line = dict(shape = 'linear', color = 'coral', width = 1.2),
                opacity = 0.5,
                name='지지/저항선',
                legendgroup='지지/저항선',
                showlegend=False,
                visible='legendonly'),
            row=1, col=1
        )

    # RSI ----------------------------------------------------------------
    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=rsi.rsi(),
            line=dict(color='darkblue', width=1.5),
            showlegend=False,
            name='rsi 14'),
        row=2, col=1,
        secondary_y=False
    )
    
    fig.add_hline(y=70, line_dash="dot", row=2, col=1, line_color="red", line_width=2,
                  annotation_text= '과매수', annotation_font_color='red', annotation_position='top left')
    fig.add_hline(y=30, line_dash="dot", row=2, col=1, line_color="blue", line_width=2,
                  annotation_text= '과매도', annotation_font_color='blue', annotation_position='bottom left')
    fig.add_hrect(y0=30, y1=70, line_width=0, fillcolor="green", opacity=0.1)

    # MACD ----------------------------------------------------------------
    colors = ['red' if val >= 0 else 'blue' for val in macd.macd_diff()]
    fig.add_trace(
        go.Bar(
            x=df.index, 
            y=macd.macd_diff(),
            marker_color=colors,
            showlegend=False,
            name='diff'),
        row=3, col=1,
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=macd.macd(),
            line=dict(color='gold', width=2),
            showlegend=False,
            name='macd'),
        row=3, col=1,
        secondary_y=False
    )

    fig.add_trace(
        go.Scatter(
            x=df.index,
            y=macd.macd_signal(),
            line=dict(color='darkblue', width=1),
            showlegend=False,
            name='signal'),
        row=3, col=1,
        secondary_y=False
    )

    # 설정 --------------------------------------------------------------
    fig.update_yaxes(
        secondary_y=False,
        range=[df.Close.min()*0.9, df.Close.max()*1.1],
        showticklabels=True,
        row=1, col=1
    )
    
    fig.update_yaxes(
        secondary_y=True,
        range=[0, df.Volume.max()*3],
        showticklabels=False,
        showgrid=False,
        row=1, col=1
    )

    fig.update_xaxes(title_text='RSI 14', row=1, col=1)
    fig.update_xaxes(title_standoff=6, title_font=dict(size=12, color="#73879C"))

    fig.update_yaxes(showgrid=False, row=2, col=1)
    fig.update_xaxes(title_text='MACD', row=2, col=1)
    fig.update_xaxes(title_standoff=6, title_font=dict(size=12, color="#73879C"))
    
    fig.update_yaxes(tickformat=',') 

    fig.update_layout({
        'title': dict(
            text='캔들 + 이평선 + 거래량 + 볼린저밴드 + 지지/저항선',
            x=0.492,
            y=0.977,
            font=dict(
                size=14,
                color="#73879C"
            )
        ),
    #     'template': 'plotly_white',
        'width': 1510,
        'height': 650,
#         'plot_bgcolor': 'rgba(228,236,246,0.5)',
        'plot_bgcolor': 'rgba(247,247,247,0.8)',
    #     'paper_bgcolor': 'rgba(0,0,0,0)',
        'legend': dict(
            yanchor = "top", y = 0.98,
            xanchor = "left", x = 0.01,
            bordercolor="#EDEDED",
            borderwidth=2,
            itemsizing='constant',
            tracegroupgap=2
        ),
        'margin': dict(
            l=20,
            r=5,
            t=30,
            b=20
        ),
        'hovermode': 'x',
        'xaxis_rangeslider_visible': False,
        'xaxis_rangebreaks': [dict(values=dt_breaks)]
    })
    
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('chart_render.html', graphJSON=graphJSON, code=code, startdate=startdate, enddate=enddate)

# ======================================================================== 메인 동작

CORS(app)
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5050, threaded=True)

import FinanceDataReader as fdr
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.figure import Figure
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt
import matplotlib

rc('font', family='Noto Sans KR')
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Noto Sans KR']

class PatternFinder():
    
#     def __init__(self, period=period):
#         self.period = period
    
    def set_stock(self, code: str, enddate):
        self.code = code
        self.data = fdr.DataReader(code, start=None, end=enddate)
        self.close = self.data['Close']
        self.change = self.data['Change']
        return self.data
        
    def search(self, start_date, end_date, period, threshold=0.98):
        base = self.close[start_date:end_date]
        self.base_norm = (base - base.min()) / (base.max() - base.min())
        self.base = base

        window_size = len(base)
        moving_cnt = len(self.data) - window_size - period - 1
        cos_sims = self.__cosine_sims(moving_cnt, window_size)
        
        self.window_size = window_size
        cos_sims = cos_sims[cos_sims > threshold]
        return cos_sims
    
    
    def __cosine_sims(self, moving_cnt, window_size):
        
        def cosine_similarity(x, y):
            return np.dot(x, y) / (np.sqrt(np.dot(x, x)) * np.sqrt(np.dot(y, y)))
        
        # 유사도 저장 딕셔너리
        sim_list = []

        for i in range(moving_cnt):
            target = self.close[i:i+window_size]

            # 정규화
            target_norm = (target - target.min()) / (target.max() - target.min())

            # 코사인 유사도 저장
            cos_similarity = cosine_similarity(self.base_norm, target_norm)

            # 코사인 유사도 <- i(인덱스), 시계열데이터 함께 저장
            sim_list.append(cos_similarity)
            
        return pd.Series(sim_list).sort_values(ascending=False)

    
    def plot_pattern(self, idx, period):
#         if period != self.period:
#             self.period = period

        top = self.close[idx:idx+self.window_size+period]
        top_norm = (top - top.min()) / (top.max() - top.min())
        fig = Figure(figsize=(7.2, 4.3), tight_layout=True)
        fig.set_facecolor('w')

        axis = fig.add_subplot(1, 1, 1)
        axis.plot(self.base_norm.values, label='기준', color='darkblue', alpha=0.6)
        axis.plot(top_norm.values, label='예측', color='red', linestyle='dashed')
        axis.plot(top_norm.values[:len(self.base_norm.values)], label='프랙탈', color='red', linestyle='solid')
        axis.axvline(x=len(self.base_norm)-1, c='tomato', linestyle='dotted')
        axis.axvspan(len(self.base_norm.values)-1, len(top_norm.values)-1, facecolor='yellow', alpha=0.2)
        axis.legend()
        axis.get_yaxis().set_visible(False)
        axis.get_xaxis().set_visible(False)
        axis.set_facecolor('#F9F9F9')
        axis.spines['bottom'].set_color('#F9F9F9')
        axis.spines['top'].set_color('#F9F9F9')
        axis.spines['left'].set_color('#F9F9F9')
        axis.spines['right'].set_color('#F9F9F9')
                
        preds = self.change[idx+self.window_size: idx+self.window_size+period]
        print(f'pred: {preds.mean()*100} % ')
        return fig

    def stat_prediction(self, results, period):
        idx_list = list(results.keys())
        mean_list = []

        for idx in idx_list:
            pred = self.change[idx+self.window_size: idx+self.window_size+period]
            mean_list.append(pred.mean())
        return np.array(mean_list)
    
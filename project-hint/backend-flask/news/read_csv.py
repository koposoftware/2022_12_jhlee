import csv
import json


class ReadCsvCreateForWordcloud:
    def read(self):
        # with open('data/30_news_threeDays_mining.csv', 'r', encoding='utf-8') as f:
        with open('/Users/hwaner/Documents/workspace/project-hint/backend-flask/static/data/news_threeDays_mining.csv',
                  'r', encoding='utf-8') as f:
            data = csv.reader(f)
            t = list()
            for x, y in data:
                aa = dict(text=x, value=y)
                t.append(aa)
            p = json.dumps(t)
        return p


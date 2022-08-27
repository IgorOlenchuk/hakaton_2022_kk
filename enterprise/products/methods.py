import pandas as pd
from pathlib import Path

from datetime import datetime

from darts import TimeSeries
from darts.models import ExponentialSmoothing, NaiveSeasonal


import matplotlib.pyplot as plt

import time
from tqdm import tqdm

directory = '/content/upload'
pathlist = Path(directory).glob('*.xlsx')
filename = []

def do_work():
    #files = []
    
    for file in tqdm(pathlist):
      #files.append(file)
      print('Обрабатываем файл: {file}'.format(file=file))

      file_time(file)
      time.sleep(1)
        
    #return files

def file_time(file):
    data = pd.ExcelFile(file)
    for sheet in data.sheet_names:
        if sheet == 'Monthly':
            #data_monthly = pd.read_excel(file, sheet_name=sheet, index_col=False, engine='openpyxl')
            #return data_monthly
            print('Найден лист Месяцы')
            a = []
            data = pd.read_excel(file, sheet_name=sheet, index_col=False, engine='openpyxl')
            for i in data.columns:
              a.append(i)
            print(a)
        elif sheet == 'Quarterly':
            #data_quarterly = pd.read_excel(file, sheet_name=sheet, index_col=False, engine='openpyxl')
            #return data_quarterly
            print('Найден лист Кварталы')
        else:
            print('Отсутствуют листы')

do_work()

custom_datetime = lambda x: datetime.strptime(x, '%Ym%m')

data = pd.read_excel('/content/Train.xlsx', 
                     sheet_name='Monthly', 
                     skiprows=[1],
                     index_col=False, #[0], 
                     engine='openpyxl', 
                     parse_dates=[0], 
                     date_parser=custom_datetime)

data.head()

data.shape

data.info()

data.isna().sum().sort_values().tail(5)

from statsmodels.tsa.seasonal import seasonal_decompose
decompose_data = seasonal_decompose(data['Реальная пенсия'], model='additive', period=int(len(data)/10))
decompose_data.plot();

seasonality=decompose_data.seasonal
seasonality.plot(color='green')

data.index

series = TimeSeries.from_dataframe(data, 'Unnamed: 0', 'Безработицв')
# Разделить данные на тестовые и валидационные выборки
train, valid = series[:-24], series[-24:]
model = ExponentialSmoothing()
model.fit(train)
prediction = model.predict(len(valid), num_samples=1000)

seasonal_model = NaiveSeasonal(K=12)
seasonal_model.fit(train)
seasonal_forecast = seasonal_model.predict(len(valid))

from darts.utils.statistics import plot_acf, check_seasonality

plot_acf(train, m=12, alpha=0.05)
plt.figure(figsize=(12, 10))
series.plot()
prediction.plot(label='forecast', low_quantile=0.05, high_quantile=0.95)
seasonal_forecast.plot(label='seasonal', low_quantile=0.05, high_quantile=0.95)
plt.legend()

from darts.metrics import mape

print("Средняя абсолютная ошибка в процентах + seasonal: {:.2f}%.".format(mape(series, combined_forecast)))
print("Средняя абсолютная ошибка в процентах + seasonal: {:.2f}%.".format(mape(series, combined_forecast)))

from darts.models import NaiveDrift

drift_model = NaiveDrift()
drift_model.fit(train)
drift_forecast = drift_model.predict(36)

combined_forecast = drift_forecast + seasonal_forecast - train.last_value()

series.plot()
combined_forecast.plot(label="combined")
drift_forecast.plot(label="drift")


import pandas as pandas
import requests
import json
import matplotlib.pyplot as plt
from pyti.smoothed_moving_average import smoothed_moving_average as sma


def collect_data(symbol, time):
    base = 'https://api.binance.com'
    endpoint = '/api/v1/klines'
    params = '?&symbol='+symbol+'&interval=' + time
    data = requests.get(base + endpoint + params)
    dictionary = json.loads(data.text)

    dataframe = pandas.DataFrame.from_dict(dictionary)
    dataframe = dataframe.drop(range(6, 12), axis=1)

    dataframe.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    for col in dataframe.columns:
        dataframe[col] = dataframe[col].astype(float)

    dataframe['fast_sma'] = sma(dataframe['close'].tolist(), 10)
    dataframe['slow_sma'] = sma(dataframe['close'].tolist(), 30)

    dataframe.plot(x ='time', y='fast_sma', kind = 'line', title = 'fast sma in the last 10 hours')
    dataframe.plot(x ='time', y='slow_sma', kind = 'line', title = 'slow sma in the last 30 hours')
    plt.show()


collect_data('BTCUSDT', '1h')
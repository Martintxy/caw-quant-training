# test any new functions or libraries
import requests
import datetime
import numpy as np
import pandas as pd
import math
limit = 10
tsym = "USDT"
# req = requests.get(
#             'https://min-api.cryptocompare.com/data/top/mktcapfull?limit=10&tsym=USDT')
# df = pd.DataFrame.from_dict(req.json(), orient = 'index')
# df_data = df.loc["Data",0]
# print(df_data)
fsym = "BTC"
tsym = "USDT"
e = "binance"
start_time = "2017-04-01 00:00:00"
end_time = "2020-04-01 00:00:00"
url = 'https://min-api.cryptocompare.com/data'
start_time_unix = pd.Timestamp(start_time).value // 10**9
end_time_unix = pd.Timestamp(end_time).value // 10**9
# request from cryptocompare
histohour_url_first = '/v2/histohour?fsym={}&tsym={}&e={}&limit=2000&toTs={}'.format(fsym, tsym, e, end_time_unix)
print(url + histohour_url_first)



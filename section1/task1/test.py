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

req = requests.get('https://min-api.cryptocompare.com/data/top/pairs?fsym=BTC&limit=10')
# convert the json type object into a dataframe
df = pd.DataFrame.from_dict(req.json(), orient = 'index')
df_table = pd.DataFrame(df.loc["Data", 0])
print(df_table)


# create a request variable
import requests
import datetime
import numpy as np
import pandas as pd
import math


class CryptoCompareAPI():
    # constuctor
    def __init__(self):
        self.url = 'https://min-api.cryptocompare.com/data'

    def get_histohour_data(self, fsym, tsym, e, start_time, end_time):
        # convert datetime to unix epoch time
        start_time_unix = pd.Timestamp(start_time).value // 10**9
        end_time_unix = pd.Timestamp(end_time).value // 10**9
        # request from cryptocompare
        req = requests.get(
            'https://min-api.cryptocompare.com/data/v2/histohour?fsym={}&tsym={}&e={}&limit=2000&toTs={}'.format(fsym, tsym, e, end_time_unix))
        # convert the json type object into a dataframe
        df = pd.DataFrame(req.json())
        # get the data table for one request
        df_table = pd.DataFrame(df.loc["Data", "Data"])
        # get the timestamp for the subsequent request
        df_timestamploop = df.loc["TimeFrom", "Data"]

        # write for loop to request data repeatedly
        hours = int((end_time_unix - start_time_unix) / 3600)
        time_of_request = int(hours // 2000)
        limit = int(hours % 2000)
        # no need to +1 because it is do-while
        for i in range(1, time_of_request):
            # request according to the last timestamp
            req_loop = requests.get(
                'https://min-api.cryptocompare.com/data/v2/histohour?fsym={}&tsym={}&e={}&limit=2000&toTs={}'.format(fsym, tsym, e, df_timestamploop))
            df_loop = pd.DataFrame(req_loop.json())
            # extract the table and convert to a dataframe
            df_tableloop = pd.DataFrame(df_loop.loc["Data", "Data"])
            # extract the timestamp to be used for the next loop
            df_timestamploop = df_loop.loc["TimeFrom", "Data"]
            # append tables
            df_table = pd.concat([df_tableloop, df_table]).drop_duplicates()

        # get last request < 2000 hour
        req_loop = requests.get(
            'https://min-api.cryptocompare.com/data/v2/histohour?fsym={}&tsym={}&e={}&limit={}&toTs={}'.format(fsym, tsym, e, limit, df_timestamploop))
        df_loop = pd.DataFrame(req_loop.json())
        df_tableloop = pd.DataFrame(df_loop.loc["Data", "Data"])
        df_timestamploop = df_loop.loc["TimeFrom", "Data"]
        # append
        df_table = pd.concat([df_tableloop, df_table]).drop_duplicates()

        # formatting
        df_table = df_table.drop(
            columns=['conversionType', 'conversionSymbol'])
        df_table = df_table.reindex(
            columns=['close', 'high', 'low', 'open', 'volumefrom', 'volumeto', 'time'])
        df_table = df_table.rename(
            columns={'volumefrom': 'volume', 'volumeto': 'baseVolume', 'time': 'datetime'})
        df_table['datetime'] = pd.to_datetime(df_table['datetime'], unit='s')
        return(df_table)

    # optional
    def get_toplist_trading_pairs(self, fsym, limit):
        req = requests.get(
            'https://min-api.cryptocompare.com/data/top/pairs?fsym={}&limit={}'.format(fsym, limit))
        # convert the json type object into a dataframe
        df = pd.DataFrame.from_dict(req.json(), orient = 'index')
        df_table = pd.DataFrame(df.loc["Data", 0])
        return(df_table)

# test
fsym = "BTC"
tsym = "USDT"
e = "binance"
start_time = "2017-04-01 00:00:00"
end_time = "2020-04-01 00:00:00"
candle_data = CryptoCompareAPI()
print(candle_data.get_histohour_data(fsym, tsym, e, start_time, end_time))

# optional
limit = 10
print(candle_data.get_toplist_trading_pairs(fsym, limit))

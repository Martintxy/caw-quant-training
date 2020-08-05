# create a request variable
import requests
import datetime
import numpy as np
import pandas as pd
import math

def data_formatting(df_table):
    # formatting
    df_table = df_table.drop(
        columns=['conversionType', 'conversionSymbol'])
    df_table = df_table.reindex(
        columns=['close', 'high', 'low', 'open', 'volumefrom', 'volumeto', 'time'])
    df_table = df_table.rename(
        columns={'volumefrom': 'volume', 'volumeto': 'baseVolume', 'time': 'datetime'})
    df_table['datetime'] = pd.to_datetime(df_table['datetime'], unit='s')
    return(df_table)

class CryptoCompareAPI():
    def __init__(self):
        self.url = 'https://min-api.cryptocompare.com/data'

    def get_histohour_data(self, fsym, tsym, e, start_time, end_time):
        # convert datetime to unix
        start_time_unix = pd.Timestamp(start_time).value // 10**9
        end_time_unix = pd.Timestamp(end_time).value // 10**9
        # request from cryptocompare
        histohour_url_first = '/v2/histohour?fsym={}&tsym={}&e={}&limit=2000&toTs={}'.format(fsym, tsym, e, end_time_unix)
        req = requests.get(self.url + histohour_url_first)
        # convert into a dataframe
        df = pd.DataFrame(req.json())
        # get data for one request
        df_table = pd.DataFrame(df.loc["Data", "Data"])
        # get the timestamp for the subsequent request
        df_timestamploop = df.loc["TimeFrom", "Data"]

        # for loop to request data
        hours = int((end_time_unix - start_time_unix) / 3600)
        time_of_request = int(hours // 2000)
        limit = int(hours % 2000)
        for i in range(1, time_of_request):
            # request according to the last timestamp
            histohour_url_loop = '/v2/histohour?fsym={}&tsym={}&e={}&limit=2000&toTs={}'.format(fsym, tsym, e, df_timestamploop)
            req_loop = requests.get(self.url + histohour_url_loop)
            df_loop = pd.DataFrame(req_loop.json())
            # extract the table and convert to a dataframe
            df_tableloop = pd.DataFrame(df_loop.loc["Data", "Data"])
            # extract the timestamp to be used for the next loop
            df_timestamploop = df_loop.loc["TimeFrom", "Data"]
            # append tables
            df_table = pd.concat([df_tableloop, df_table]).drop_duplicates()

        # get last request < 2000 hour
        histohour_url_final = '/v2/histohour?fsym={}&tsym={}&e={}&limit={}&toTs={}'.format(fsym, tsym, e, limit, df_timestamploop)
        req_loop = requests.get(self.url + histohour_url_final)
        df_loop = pd.DataFrame(req_loop.json())
        df_tableloop = pd.DataFrame(df_loop.loc["Data", "Data"])
        df_timestamploop = df_loop.loc["TimeFrom", "Data"]
        # append
        df_table = pd.concat([df_tableloop, df_table]).drop_duplicates()

        # formatting
        df_table = data_formatting(df_table)
        return(df_table)

    # optional
    def get_toplist_trading_pairs(self, fsym, limit):
        toplist_url = '/top/pairs?fsym={}&limit={}'.format(fsym, limit)
        req = requests.get(self.url + toplist_url)
        # convert the json type object into a dataframe
        df = pd.DataFrame.from_dict(req.json(), orient='index')
        df_table = pd.DataFrame(df.loc["Data", 0])
        return(df_table)

# get data
fsym = "BTC"
tsym = "USDT"
e = "binance"
start_time = "2020-01-01 00:00:00"
end_time = "2020-04-01 00:00:00"
candle_data = CryptoCompareAPI()
histohour_datatable = candle_data.get_histohour_data(
    fsym, tsym, e, start_time, end_time)
print(histohour_datatable)
# export to .csv file and remove the row index
histohour_datatable.to_csv('section2/data/BTC_USDT_1h.csv', index=False)

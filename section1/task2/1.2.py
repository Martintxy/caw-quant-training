from binance.client import Client
import requests
import datetime
import numpy as np
import pandas as pd
from binance.enums import *

api_key = 'DYpf4c2nFdjIL8xIe2D4KckfRDEJJ9WD0N6bOJZBEvCD5IjhHGo6d1BCwXAR2bBV'
api_secret = 'jUhYqtfcJABTj3mXX3VbhwCCpdgXcLbcGyoGrnOYSQZMMiYIJhSUudivydubucx1'
client = Client(api_key, api_secret)

# get candle data
candles = client.get_klines(
    symbol='BNBBTC', interval=Client.KLINE_INTERVAL_30MINUTE)
df_candles = pd.DataFrame(candles)
df_candles[0] = pd.to_datetime(df_candles[0], unit='ms')
df_candles.columns = ['Open_time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close_time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignored']
print('Candle data:')
print(df_candles)
df_candles.to_csv('section1/task2/candle.csv', index=False)

# get trades
recent_trades = client.get_recent_trades(symbol='BNBBTC')
df_recent = pd.DataFrame(recent_trades)
print('Recent trades:')
print(df_recent)
df_recent.to_csv('section1/task2/recent trades.csv', index=False)

# aggregate trades
agg_trades = client.get_aggregate_trades(symbol='BNBBTC')
df_agg = pd.DataFrame(agg_trades)
# format
df_agg.columns = ['Aggregated trade id', 'Price', 'Quantity', 'First breakdown trade id','Last breakdown trade id', 'Trade time', 'Maker', 'Ignored']
print('Aggregate trades')
print(df_agg)
df_agg.to_csv('section1/task2/aggregate trades.csv', index=False)

# get market depth
depth = client.get_order_book(symbol='BNBBTC')
df_depth = pd.DataFrame(depth)
print("Market depth:")
print(df_depth)
df_depth.to_csv('section1/task2/market depth.csv', index=False)

# optional
order = client.create_test_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.001')
print(order)

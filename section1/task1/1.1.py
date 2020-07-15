# create a request variable
# start time = 1491004800 (2017-4-1), end time = 1585699200 (2020-4-1)
import requests
import datetime
import numpy as np
import pandas as pd
import math
StartTime = 1491004800
EndTime = 1585699200
# request from cryptocompare that contains 2000 pieces of data
req = requests.get('https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USDT&e=binance&limit=2000&toTs={}'.format(EndTime))
# convert the json type object into a pandas dataframe
Df = pd.DataFrame(req.json())
# get the data table for one request
DfTable = pd.DataFrame(Df.loc["Data","Data"])
# get the timestamp for the subsequent request
DfTimeStampLoop = Df.loc["TimeFrom", "Data"]

# write for loop to request data repeatedly
hours = int((EndTime - StartTime) / 3600)
TimeOfRequest = int(hours // 2000)
limit = int(hours % 2000)
# no need to +1 because it is do-while
for i in range(1,TimeOfRequest):
    # request according to the last timestamp
    ReqLoop = requests.get('https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USDT&e=binance&limit=2000&toTs={}'.format(DfTimeStampLoop))
    DfLoop = pd.DataFrame(ReqLoop.json())
    # extract the table and convert to a dataframe
    DfTableLoop = pd.DataFrame(DfLoop.loc["Data","Data"])
    # extract the timestamp to be used for the next loop
    DfTimeStampLoop = DfLoop.loc["TimeFrom", "Data"]
    # append tables
    DfTable = pd.concat([DfTableLoop,DfTable]).drop_duplicates()

# get last request < 2000 hour
ReqLoop = requests.get('https://min-api.cryptocompare.com/data/v2/histohour?fsym=BTC&tsym=USDT&e=binance&limit={}&toTs={}'.format(limit, DfTimeStampLoop))
DfLoop = pd.DataFrame(ReqLoop.json())
DfTableLoop = pd.DataFrame(DfLoop.loc["Data","Data"])
DfTimeStampLoop = DfLoop.loc["TimeFrom", "Data"]
# append
DfTable = pd.concat([DfTableLoop,DfTable]).drop_duplicates()

# formatting
DfTable = DfTable.drop(columns = ['conversionType', 'conversionSymbol'])
DfTable = DfTable.reindex(columns = ['close','high','low','open','volumefrom','volumeto','time'])
DfTable = DfTable.rename(columns = {'volumefrom':'volume', 'volumeto':'baseVolume','time':'datetime'})
DfTable['datetime'] = pd.to_datetime(DfTable['datetime'], unit='s')
print(DfTable)
# export to .csv file and remove the row index
DfTable.to_csv('1.1.csv', index = False)



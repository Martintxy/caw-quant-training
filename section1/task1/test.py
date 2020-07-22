# test any new functions or libraries
import requests
import datetime
import numpy as np
import pandas as pd
import math
import time
from binance.client import Client
from binance.enums import *

api_key = 'DYpf4c2nFdjIL8xIe2D4KckfRDEJJ9WD0N6bOJZBEvCD5IjhHGo6d1BCwXAR2bBV'
api_secret = 'jUhYqtfcJABTj3mXX3VbhwCCpdgXcLbcGyoGrnOYSQZMMiYIJhSUudivydubucx1'
client = Client(api_key, api_secret)

order = client.create_test_order(
    symbol='BNBBTC',
    side=SIDE_BUY,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=100,
    price='0.001')
print(order)

import requests
import datetime
import numpy as np
import pandas as pd
import json
from crypto_news_api import CryptoControlAPI

# optional 1
''' 
Unitest:
1. It is easy to modulize and good for maintainance.
2. It is written in a class in the form of class xx_Test(unittest.TestCase), in which multiple functions are tested with the self.assertEqual function.
Two arguments are passed into the function: the expected output and the output returned by the function. Then the unittest module will return 1 out of 3 outputs:
OK, ERROR or FAIL to show the end state.
3. Just import unittest library.
'''

# optional 2
# Connect to the CryptoControl API
with open('section1/task3/api_key.json', mode='r') as key_file:
    key2 = json.loads(key_file.read())['key2']

api = CryptoControlAPI(key2)

# Connect to a self-hosted proxy server (to improve performance) that points to cryptocontrol.io
proxyApi = CryptoControlAPI(key2, "http://cryptocontrol_proxy/api/v1/public")

# Get top news
print(pd.DataFrame(api.getTopNews()))\
# returned dataframe can be viewed fully in the csv file, same for the other dataframes
pd.DataFrame(api.getTopNews()).to_csv('section1/task3/topnews.csv', index=False)

# get latest russian news
print(pd.DataFrame(api.getLatestNews("ru")))

# # get top bitcoin news
print(pd.DataFrame(api.getTopNewsByCoin("bitcoin")))

# get top EOS tweets
print(pd.DataFrame(api.getTopTweetsByCoin("eos")))

# get top Ripple reddit posts
print(pd.DataFrame(api.getLatestRedditPostsByCoin("ripple")))

# get reddit/tweets/articles in a single combined feed for NEO
feed = pd.DataFrame(api.getTopFeedByCoin("neo"))
print(feed)

# get latest reddit/tweets/articles (seperated) for Litecoin
print(pd.DataFrame(api.getLatestItemsByCoin("litecoin")))

# get details (subreddits, twitter handles, description, links) for ethereum
links = api.getCoinDetails("ethereum")['links']
print(pd.DataFrame(links))
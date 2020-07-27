# test any new functions or libraries
import requests
import datetime
import numpy as np
import pandas as pd
import math
import json
import unittest
from etherscan.tokens import Tokens
from crypto_news_api import CryptoControlAPI

import requests
import datetime
import numpy as np
import pandas as pd
import json
from crypto_news_api import CryptoControlAPI
# optional 2
# Connect to the CryptoControl API
with open('section1/task3/api_key.json', mode='r') as key_file:
    key2 = json.loads(key_file.read())['key2']

api = CryptoControlAPI(key2)

# Connect to a self-hosted proxy server (to improve performance) that points to cryptocontrol.io
proxyApi = CryptoControlAPI(key2, "http://cryptocontrol_proxy/api/v1/public")


# get news articles grouped by category
print(pd.DataFrame(api.getTopNewsByCategory()))


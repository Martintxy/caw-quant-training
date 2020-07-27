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

with open('section1/task3/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

ELCOIN_TOKEN_SUPPLY = '21265524714464'
ELCOIN_TOKEN_BALANCE = "135499"
CONTRACT_ADDRESS = '0x57d90b64a1a57749b0f932f1a3395792e12e7055'
ADDRESS = '0xe04f27eb70e025b78871a2ad7eabe85e61212761'
API_KEY = key


class TokensTestCase(unittest.TestCase):

    def test_get_token_supply(self):
        api = Tokens(contract_address=CONTRACT_ADDRESS, api_key=(API_KEY))
        self.assertEqual(api.get_total_supply(), ELCOIN_TOKEN_SUPPLY)

    def test_get_token_balance(self):
        api = Tokens(contract_address=CONTRACT_ADDRESS, api_key=API_KEY)
        self.assertEqual(api.get_token_balance(ADDRESS), ELCOIN_TOKEN_BALANCE)

# main function
if __name__ == '__main__':
    unittest.main()






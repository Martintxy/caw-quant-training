import requests
import datetime
import numpy as np
import pandas as pd
from etherscan.accounts import Account
#from etherscan.blocks import Blocks - cannot find etherscan.blocks
from etherscan.contracts import Contract
from etherscan.proxies import Proxies
from etherscan.stats import Stats
from etherscan.tokens import Tokens
# from etherscan.transactions import Transactions - cannot find transactions
import json

# Account
with open('section1/task3/api_key.json', mode='r') as key_file:
    key = json.loads(key_file.read())['key']

address = '0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a'

api = Account(address=address, api_key=key)
transactions = api.get_transaction_page(page=1, offset=10000, sort='des')
trans_table = pd.DataFrame(transactions)
print('Transactions:')
print(trans_table)

balance = api.get_balance()
print(balance)

# Contract
address = '0xfb6916095ca1df60bb79ce92ce3ea74c37c5d359'

api = Contract(address=address, api_key=key)
abi = api.get_abi()
print('\nContract:')
print(abi)

# Proxies
api = Proxies(api_key=key)
block = api.get_block_by_number(5747732)
print('\nProxies:')
print(block['number'])

block = api.get_most_recent_block()
print(int(block, 16))

# Stats
api = Stats(api_key=key)
last_price = api.get_ether_last_price()
last_price_table = pd.DataFrame(last_price,index = [0])
print('\nLast ether price')
print(last_price_table)

# call with default address, The DAO
api = Stats(api_key=key)
supply = api.get_total_ether_supply()
print('Total ether supply:')
print(supply)

# Tokens
address = '0xe04f27eb70e025b78871a2ad7eabe85e61212761'
api = Tokens(contract_address='0x57d90b64a1a57749b0f932f1a3395792e12e7055', api_key=key)
balance = api.get_token_balance(address=address)
print('\nTokens:')
print('Balance:', balance)



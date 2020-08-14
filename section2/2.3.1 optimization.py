# libraries
import os
import datetime
import sys

import backtrader as bt
import pandas as pd
import matplotlib.pyplot as plt

# environment params/ global variables
datadir = 'section2/data'  # data path
logdir = 'section2/log'  # log path
reportdir = 'section2/report'  # report path
datafile = 'BTC_USDT_1h.csv'  # data file
from_datetime = '2020-01-01 00:00:00'  # start time
to_datetime = '2020-04-01 00:00:00'  # end time

# define strategy class
class SMACross(bt.Strategy):
    params = (
        ('pfast', 10),
        ('pslow', 20),
        ('printlog', True)
    )
    
    def __init__(self):
        aver_fast = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.p.pfast) 
        aver_slow = bt.indicators.SimpleMovingAverage(self.datas[0], period=self.p.pslow) 
        self.crossover = bt.indicators.CrossOver(aver_fast, aver_slow)
    
    def next(self):
        # if not in the mkt
        if not self.position:  
            # buy if fast is above slow
            if self.crossover > 0:  
                self.order = self.buy()

        # sell if in the mkt and fast is below slow
        elif self.crossover < 0:
            self.order = self.sell()

    def log(self, txt, dt=None, doprint=False):
        ''' Logging function fot this strategy'''
        if self.params.printlog or doprint:
            dt = dt or self.datas[0].datetime.date(0)
            print('%s, %s' % (dt.isoformat(), txt))

    def stop(self):
        self.log('(fastma period %2d, slowma period %2d) Ending Value %.2f' %
                 (self.params.pfast, self.params.pslow, self.broker.getvalue()))


# initiate cerebro instance
cerebro = bt.Cerebro()

# create a Data Feed
data = pd.read_csv(
    os.path.join(datadir, datafile), index_col='datetime', parse_dates=True)
data = data.loc[
    (data.index >= pd.to_datetime(from_datetime)) &
    (data.index <= pd.to_datetime(to_datetime))]
datafeed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(datafeed)

# feed optimized strategy
cerebro.optstrategy(SMACross, pfast = range(5,25,5), pslow = range(20,100,20))

# additional backtest setting
cerebro.addsizer(bt.sizers.PercentSizer, percents=99)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

# run
cerebro.run(maxcpus = 1)

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

# additional backtest setting
cerebro.addsizer(bt.sizers.PercentSizer, percents=99)
cerebro.broker.set_cash(10000)
cerebro.broker.setcommission(commission=0.001)

if __name__ == "__main__":
    # feed strategy
    cerebro.addstrategy(SMACross)

    # add logger
    logfile = '_'.join([datafile[0:-4], str(cerebro.strats[0][0][0])[-10:-2], str(cerebro.strats[0][0][0].params.__dict__['pfast']),
                        str(cerebro.strats[0][0][0].params.__dict__['pslow']), from_datetime[:10], to_datetime[:10]])+'.csv'
    cerebro.addwriter(
        bt.WriterFile,
        out=os.path.join(logdir, logfile),
        csv=True)

    # run
    cerebro.run()

    # save report
    figfile = '_'.join([datafile[0:-4], str(cerebro.strats[0][0][0])[-10:-2], str(cerebro.strats[0][0][0].params.__dict__['pfast']),
                        str(cerebro.strats[0][0][0].params.__dict__['pslow']), from_datetime[:10], to_datetime[:10]])+'.png'
    plt.rcParams['figure.figsize'] = [13.8, 10]
    fig = cerebro.plot(style='candlestick', barup='green', bardown='red')
    fig[0][0].savefig(
        os.path.join(reportdir, figfile),
        dpi=480)

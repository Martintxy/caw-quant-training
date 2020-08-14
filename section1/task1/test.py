import datetime

import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats

cerebro = bt.Cerebro()

# data
dataname = 'section2/data/2005-2006-day-001.txt'
data = btfeeds.BacktraderCSVData(dataname=dataname)

cerebro.adddata(data)

# strategy
cerebro.addstrategy(btstrats.SMA_CrossOver)

# Analyzer
#cerebro.addanalyzer(btanalyzers.SharpeRatio, _name='mysharpe')

thestrats = cerebro.run()
thestrat = thestrats[0]

#print('Sharpe Ratio:', thestrat.analyzers.mysharpe.get_analysis()['sharperatio'])
print(thestrat.analyzers.)
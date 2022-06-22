from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import backtrader.feeds as btfeeds
import backtrader.strategies as btstrats
import pandas as pd
import quantstats
from strategies import *
import os

def saveplots(cerebro, numfigs=1, iplot=True, start=None, end=None,
             width=16, height=9, dpi=300, tight=True, use=None, file_path = '', **kwargs):

        from backtrader import plot
        if cerebro.p.oldsync:
            plotter = plot.Plot_OldSync(**kwargs)
        else:
            plotter = plot.Plot(**kwargs)

        figs = []
        for stratlist in cerebro.runstrats:
            for si, strat in enumerate(stratlist):
                rfig = plotter.plot(strat, figid=si * 100,
                                    numfigs=numfigs, iplot=iplot,
                                    start=start, end=end, use=use)
                figs.append(rfig)

        for fig in figs:
            for f in fig:
                f.savefig(file_path, bbox_inches='tight')
        return figs


def backtest_start(tf):
    data = bt.feeds.GenericCSVData(
        dataname = 'Data/' + tf + '.csv',

        fromdate=datetime.datetime(2020, 1, 1),
        todate=datetime.datetime(2021, 12, 30),

        nullvalue=0.0,
        timeframe=bt.TimeFrame.Minutes,
        dtformat=('%Y.%m.%d'),
        tmformat=('%H:%M'),
        datetime=0,
        time=1,
        open=2,
        high=3,
        low=4,
        close=5,
        volume=6,
        openinterest=-1
        )
    cerebro = bt.Cerebro()
    cerebro.broker.setcash(10000.0)


    cerebro.addstrategy(stop_loss)
    cerebro.broker.set_checksubmit(checksubmit=False)
    cerebro.adddata(data)
    cerebro.addwriter(bt.WriterFile, csv=True, out='log.csv')

    cerebro.broker.setcommission(commission=28, margin=2000, mult=78.0)
    cerebro.addanalyzer(btanalyzers.PyFolio, _name='pyfolio')
    strats = cerebro.run()
    strat0 = strats[0]
    pyfoliozer = strat0.analyzers.getbyname('pyfolio')
    returns, positions, transactions, gross_lev = pyfoliozer.get_pf_items()
    returns.index = returns.index.tz_convert(None)
    quantstats.reports.html(returns, output='test.html', title=stratey_name+'_'+tf)
    saveplots(cerebro, file_path = 'plot.png', style='candlestick') 
    os.rename('quantstats-tearsheet.html', folder_name+stratey_name+'/'+tf+'.html')
    os.rename('log.csv', folder_name+stratey_name+'/'+tf+'.csv')
    os.rename('plot.png', folder_name+stratey_name+'/'+tf+'.png')

if __name__ == '__main__':
    folder_name = 'indicators/'
    stratey_name ='test'
    try:
        os.makedirs(folder_name+stratey_name)
        
    except:
        pass
    timeframes_toBeTest = ['30mins']
    for timeframe_ongoing in timeframes_toBeTest:
        backtest_start(timeframe_ongoing)
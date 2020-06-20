import backtrader as bt
import datetime
import random
from strategies import TestStrategy, MacdStrategy
from backtrader.feeds import GenericCSVData

# Author: Malay Agarwal

######################################################
# This is a backtester connected to the geneticAlgo.py
# This returns the end value of portfolio 
# unless it is over leveraged it returns 0
######################################################

# global variable for ease of GA file to change
signalValues = [0,0,0,0]
startdate = datetime.datetime(2018,1,1)
enddate = datetime.datetime(2018,4,1)

def main():
    class GenericCSV_PE(GenericCSVData):
        lines = ('macd','macd_pcent',)
        params = (('macd',8),('macd_pcent', 9),)
    
    # Initiate cerbero(backtester)
    cerebro = bt.Cerebro()
    # Set portfolio cash value
    cerebro.broker.set_cash(1000000)

    global startdate
    global enddate

    data = GenericCSV_PE(
        dataname='SNAPdata.csv',
        # backtrader only handles minutes or days
        timeframe=bt.TimeFrame.Minutes,
        compression=60,

        fromdate=startdate,
        todate=enddate,
        

        dtformat=('%Y-%m-%d'),
        tmformat=('%H:%M'),

        datetime=0,
        time=1,
        open=2,
        high=3,
        low=4,
        close=5,
        volume=6,
        openinterest=-1,
        # adjclose=6,
        macd=7,
        macd_pcent = 8
    )

    cerebro.adddata(data)

    global signalValues

    # adds strategy for backtrader to use, and sets the values for the values to execute trades at for MACD percentage of price
    cerebro.addstrategy(MacdStrategy, testnumbers = signalValues)
    # sets the share size of each trade
    cerebro.addsizer(bt.sizers.FixedSize, stake = 20000)

    # can uncomment out the print lines and comment the if else and cerebro.plot() to get a plot and start/end val

    # print ('Start Portfolio Value: %.2f' % cerebro.broker.getvalue())
    cerebro.run()
    # print ('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    # if there is too much risk, set to 1.4x total port value, return 0
    # makes sure there is not a short position larger than 1.4x portfolio value
    if (cerebro.broker.get_cash() > (1.4 * cerebro.broker.getvalue())):
        return 0
    else:
        return (cerebro.broker.getvalue())

    # cerebro.plot()

if __name__ == "__main__":
    main()
# main()
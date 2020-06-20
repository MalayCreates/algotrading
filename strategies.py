# Import the backtrader platform
import backtrader as bt

# Author: Malay Agarwal

###################################################################
# This is the execution of buy/sells
# Will take values fed from backtest.py which the GA comes up with
# testnumbers is a list that signals when to buy/sell
# takes MACD as a percentage of price
###################################################################

# Create a Stratey
class MacdStrategy(bt.Strategy):
    def log(self, txt, dt=None):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)

    def __init__(self,testnumbers):
        self.dataclose = self.datas[0].close
        self.macd_pcent = self.datas[0].macd_pcent
        self.order = None
        self.testnumbers = testnumbers
        self.qty = 0
    
    # define what to print if different orders are buys/sells
    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            return
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log('BUY EXECUTED AT {}'.format(order.executed.price))
            elif order.issell():
                self.log('SELL EXECUTED AT {}'.format(order.executed.price))
            self.bar_executed = len(self)
        self.order = None

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])
    
        if self.order:
            return
        
        # if there are no open positions
        if not self.position:
            # GA handles finding optimal number to find optimal MACD % of price
            # Buys the dip
            if self.macd_pcent <= self.testnumbers[0]:
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # allows a max loss of 7%, but will take profit if it ever has 7% drop
                self.order = self.buy(exectype=bt.Order.StopTrail, trailpercent=0.07)
            elif self.macd_pcent > self.testnumbers[1]:
                # Short sells at a high point for the MACD
                self.log('SELL CREATE, %.2f' % self.dataclose[0])
                # allows max loss of 7%
                self.order = self.sell(exectype=bt.Order.StopTrail, trailpercent=0.07)
        # if it already has a position open
        else:
            # Close all open positions
            if self.macd_pcent > self.testnumbers[2]:
                self.log('SELL TO CLOSE CREATED {}'.format(self.dataclose[0]))
                # close all long orders
                self.order = self.close()
            elif self.macd_pcent < self.testnumbers[3]:
                self.log('BUY TO CLOSE CREATED {}'.format(self.dataclose[0]))
                # close all short orders
                self.order = self.close()
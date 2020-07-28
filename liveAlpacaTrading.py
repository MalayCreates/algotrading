import pandas as pd
import alpaca_trade_api as tradeapi
import time
from datetime import datetime
import pandas_datareader.data as web

# Author: Malay Agarwal

######################################################################
# This is an example of a ticker I have trading live
# This trades Intel at most once a day
# at 9:00 am it will make a trade based off the previous day close MACD
#######################################################################

# alpha vantage key
avKey = 'ALPHA VANTAGE KEY'
# Cannot give out my API key or Secret Key
APIkey = 'API KEY'
SecretKey = 'SECRET KEY'
# paper trades
BaseURL = 'https://paper-api.alpaca.markets'
# initiate the REST api for Alpaca
api = tradeapi.REST(APIkey,SecretKey,BaseURL)
# collect current date
currentDay = datetime.now().day
currentMonth = datetime.now().month
currentYear = datetime.now().year


g= open("INTCdata.csv","w+")
# from the beginning for 2020 collect the daily adjusted close and write to file
df = web.DataReader("INTC", "av-daily-adjusted", start=datetime(2020, 1, 1), 
     end=datetime(currentYear, currentMonth, currentDay), api_key=(avKey))
df.to_csv('INTCdata.csv')

# read the same file as a dataframe
# Calculates the MACD by subtracting 12 day EMA from 26 EMA
df2 = pd.read_csv('INTCdata.csv', parse_dates=True, index_col = 0)
close_df = pd.DataFrame()
close_df['Adj Close'] = df2['adjusted close']
macd_df = close_df
macd_df['EMA 12'] = close_df['Adj Close'].ewm(
    span=12, adjust=False, ignore_na=False).mean()
macd_df['EMA 26'] = close_df['Adj Close'].ewm(
    span=26, adjust=False, ignore_na=False).mean()
macd_df['MACD'] = macd_df['EMA 12'] - macd_df['EMA 26']

# collect the last value as the currentMACD
# in my backtesting I found MACD as a percentage of price
# however here, I use actual price MACD rather than percent
currentMACD = ((macd_df.tail(1)['MACD']).values[0])

# find if there is open position
current_position = ((api.get_position('INTC')).qty)

class AlpacaClass:
    def __init__(self):
        self.macd = currentMACD
        self.closeSignal = 0
        self.openSignal = 0

        if self.macd > 1:
            self.closeSignal = 2
        elif self.macd < -0.1:
            self.closeSignal = 1

        if self.macd <= 1:
            self.openSignal = 1
        elif self.macd > 2:
            self.openSignal = 2

    def alpacaExecute(self):
        self.position = 0

        # want it to collect the current position
        try:
            self.position = int(current_position)
        except:
            print ('No current positions')
            pass
        
        # If portfolio is short
        if self.position < 0:
            # is there a buy to close signal
            if self.closeSignal == 1:
                api.submit_order(
                symbol = 'INTC',
                qty = 10000,
                side = 'buy',
                type = 'market',
                time_in_force = 'day'
            )
                return ('Market Order BUY TO CLOSE Submitted')
            # is there still a sell to open signal
            # keep shorting
            elif self.openSignal == 2:
                api.submit_order(
                symbol = 'INTC',
                qty = 10000,
                side = 'sell',
                type = 'market',
                time_in_force = 'day'
            )
                print ('Market Order SELL TO OPEN Submitted')

        # If portfolio is long
        elif self.position> 0:
            # is there a sell to close signal
            if self.closeSignal == 2:
                api.submit_order(
                symbol = 'INTC',
                qty = 10000,
                side = 'sell',
                type = 'market',
                time_in_force = 'day'
            )
                print ('Market Order SELL TO CLOSE Submitted')
            # is there still a buy to open signal
            # buy more
            elif self.openSignal == 1:
                api.submit_order(
                symbol = 'INTC',
                qty = 10000,
                side = 'buy',
                type = 'market',
                time_in_force = 'day'
            )
                print ('Market Order BUY TO OPEN Submitted')
        
        # If we are not in a positon at all
        else:
            # check if there is buy to open signal
            if self.openSignal == 1:
                api.submit_order(
                symbol = 'INTC',
                qty = 10000,
                side = 'buy',
                type = 'market',
                time_in_force = 'day'
            )
                print ('Market Order BUY TO OPEN Submitted')
            # check if there is sell to open signal
            elif self.openSignal() == 2:
                api.submit_order(
                symbol = 'INTC',
                qty = 10000,
                side = 'sell',
                type = 'market',
                time_in_force = 'day'
            )
                print ('Market Order SELL TO OPEN Submitted')
            
# Run it back
def main():
    
    INTC = AlpacaClass()
    INTC.alpacaExecute()

if __name__ == "__main__":
    main()

import alpaca_trade_api as tradeapi
import pandas as pd
import datetime

APIkey = 'API KEY'
SecretKey = 'SECRET KEY'
BaseURL = 'https://api.alpaca.markets'

api = tradeapi.REST(APIkey,SecretKey,BaseURL)

tickerList = ['SNAP','INTC']

# This is for data collection
# Had to finesse polygon api because they only let me grab
# a few hours of a window so I iteratively have to go back
# was a major pain but the only way for polygon to work
numDone = 1
for ticker in tickerList:
    fromdate = (datetime.date(2017,1,1))
    enddate = (datetime.date(2017,1,1))
    x = str(fromdate)
    y = str(enddate)
    currentdate = (datetime.date(2020,6,25))
    delta = datetime.timedelta(1)

    stockdf = api.polygon.historic_agg_v2(ticker, 1,  'hour', _from=(x), to=(y)).df

    i=0
    opentime = datetime.time(9)
    endtime = datetime.time(16)
    while (enddate <= currentdate):
        fromdate += delta
        enddate += delta
        tempdf = api.polygon.historic_agg_v2(ticker, 1,  'hour', _from=(str(fromdate)), to=(str(enddate))).df
        if not tempdf.empty:
            stockdf = stockdf.append(tempdf)
    stockdf = stockdf.between_time('09:00','16:00')
    stockdf.to_csv('%s.csv'%ticker)
    print (numDone)
    numDone += 1

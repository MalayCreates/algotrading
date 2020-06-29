import pandas as pd
import pandas_datareader.data as web
import numpy as np
import datetime
import matplotlib.pyplot as plt
from matplotlib import style
from alpha_vantage.timeseries import TimeSeries


df = pd.read_csv('SNAP.csv', parse_dates=True, index_col = 0)
close_df = pd.DataFrame()
close_df['close'] = df['close']
macd_df = close_df
macd_df['EMA 12'] = close_df['close'].ewm(
    span=12, adjust=False, ignore_na=False).mean()
macd_df['EMA 26'] = close_df['close'].ewm(
    span=26, adjust=False, ignore_na=False).mean()
macd_df['MACD'] = macd_df['EMA 12'] - macd_df['EMA 26']
macd_df['MACD_PCENT'] = macd_df['MACD'] / macd_df['close']
macd_df['MACD_PCENT'] = macd_df['MACD_PCENT'].apply(lambda x: x*100))

df['MACD'] = macd_df['MACD']
df['MACD_PCENT'] = macd_df ['MACD_PCENT']
df.to_csv('SNAP.csv')

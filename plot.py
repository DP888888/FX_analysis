#!/usr/bin/env python
import test
import platform
import os, sys
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
from datetime import datetime
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates



def work (typeName):
    price = test.PriceRecord (typeName)
    # price.printM1()
    # # exit()
    # price.CheckData()
    # exit()
    df = price.plotGivenDate('2020.03.24', '2020.03.24', 60)

    df['DATE'] = df['DATE'] + ' ' + df['TIME']

    df = df[['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE']]
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['HIGH'] = df['HIGH'].astype(float)
    df['LOW'] = df['LOW'].astype(float)
    df['CLOSE'] = df['CLOSE'].astype(float)
    df['OPEN'] = df['OPEN'].astype(float)
    # df['DATE'] = df['DATE'].apply(mdates.date2num)

    date_tickers = df.DATE.values
    weekday_quotes = [tuple([i] + list(quote[1:])) for i, quote in enumerate(df.values)]

    for i in range (len (weekday_quotes)):
        print (i, date_tickers[i],  '      ====   ',  weekday_quotes[i])

    fig, ax = plt.subplots()
    dpi = 300
    fig.set_dpi(dpi)

    def format_date(x, pos=None):
        if x < 0 or x > len(date_tickers) - 1:
            return ''
        ret = date_tickers[int(x)]
        t = str (ret)
        l = t.find ('-')
        r = t.rfind (':')
        t = t[l + 1:r]
        pp = t.find ('T')
        t = t[:pp] + ' ' + t[pp + 1: ]
        # print (t)
        return t


    # plotting the data
    # candlestick_ohlc(ax, df.values, width=0.015, colorup='green', colordown='red')
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

    candlestick_ohlc(ax, weekday_quotes, width=0.015 * 30, colorup='green', colordown='red', alpha=0.8)


    # ax.xaxis_date()
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M'))
    # ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    if typeName == 'GBPJPY':
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    else:
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))

    plt.grid()
    # plt.xticks(rotation=45)
    fig.set_size_inches(1920 / dpi, 1980 / dpi)
    plt.axhline(1.0805)
    plt.axvline(5.5)
    plt.show()


df = work ('EURUSD')
# df = work ('GBPJPY')

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
    # value = input("Please enter a string:\n")
    # value = '2020.03.24'
    # End = '2020.03.25'
    value = '2021.12.16'
    End = '2021.12.17'
    BarMin = 5
    df = price.plot_5_GivenDate(value, value, 5)
    if df.empty :
        print ('error, no price data!')
        return

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
        # t = t[:pp] + ' ' + t[pp + 1: ]  #print day & time
        t = t[pp + 1: ]  #only print time
        return t


    # plotting the data
    # candlestick_ohlc(ax, df.values, width=0.015, colorup='green', colordown='red')
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

    candlestick_ohlc(ax, weekday_quotes, width=0.015 * 30 * 1.5, colorup='red', colordown='green', alpha=0.8)


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
    # fig.set_size_inches(1920 / dpi, 1980 / dpi)

    if BarMin == 5:
        # plt.axhline(1.0805)
        plt.axvline(12)
        plt.axvline(60)
        for i in range (1, len (price.TradeSignal)):
            # print(' ===   ', price.TradeSignal.loc[i])
            if price.TradeSignal.loc[i]['type'] == typeName and  price.TradeSignal.loc[i]['date'] == value.replace ('.', '/'):
                # print ( price.TradeSignal.loc[i])
                entry = price.TradeSignal.loc[i]['entry']
                cut = price.TradeSignal.loc[i]['cut']
                First = price.TradeSignal.loc[i]['First']
                Second = price.TradeSignal.loc[i]['Second']
                plt.axhline(entry, color = 'y')
                plt.axhline(cut)
                plt.axhline(First)
                plt.axhline(Second, color = 'b')
            # if price.TradeSignal.loc[i]['type'] == typeName and price.TradeSignal.loc[i]['DATE'] == value:

        plt.show()


# df = work ('EURUSD')
df = work ('GBPJPY')

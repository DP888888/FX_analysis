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


def work (typeName, value, End, BarMin):
    price = test.PriceRecord (typeName)
    if BarMin == 5:
        df = price.plot_5_GivenDate(value, value, 5)
    elif BarMin == 60:
        df = price.plot_60_GivenDate(value, value, 60)
    else:
        sys.exit("Can only plot 5min or 60min!")

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

    def format_date(x, pos=None):
        if x < 0 or x > len(date_tickers) - 1:
            return ''
        ret = date_tickers[int(x)]
        t = str(ret)
        l = t.find('-')
        r = t.rfind(':')
        t = t[l + 1:r]
        pp = t.find('T')
        t = t[:pp] + ' ' + t[pp + 1:]  # print day & time
        # t = t[pp + 1: ]  #only print time
        return t

    Vline_l = -1
    Vline_r = -1
    for i in range (len (weekday_quotes)):
        # print (i, date_tickers[i],  '      ====   ',  weekday_quotes[i])
        StrT = str (date_tickers[i]).replace('T', ' ')
        StrT = StrT.split ('.')[0]
        if test.StrToDateTime(StrT) < test.StrToDateTime(value + ' 07:00:00'):
            Vline_l = i
        if Vline_r == -1 and test.StrToDateTime(StrT) > test.StrToDateTime(value + ' 11:00:00'):
            Vline_r = i
    # print (Vline_l, Vline_r)

    fig, ax = plt.subplots()
    dpi = 300
    fig.set_dpi(dpi)

    # plotting the data
    # candlestick_ohlc(ax, df.values, width=0.015, colorup='green', colordown='red')
    # ax.xaxis.set_major_locator(ticker.MultipleLocator(10))
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))

    candlestick_ohlc(ax, weekday_quotes, width=0.015 * 30 * 1.5, colorup='red', colordown='green', alpha=0.8)


    if typeName == 'GBPJPY':
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    else:
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))

    plt.grid()
    plt.xticks(rotation=15)
    # fig.set_size_inches(1920 / dpi, 1980 / dpi)

    plt.axvline(Vline_l - 0.5)
    plt.axvline(Vline_r + 0.5)


    for i in range (1, len (price.TradeSignal)):
        if price.TradeSignal.loc[i]['type'] == typeName and  price.TradeSignal.loc[i]['date'] == value.replace ('.', '/'):
            entry = price.TradeSignal.loc[i]['entry']
            cut = price.TradeSignal.loc[i]['cut']
            First = price.TradeSignal.loc[i]['First']
            Second = price.TradeSignal.loc[i]['Second']
            plt.axhline(entry, color = 'brown')
            plt.axhline(cut, color = 'purple')
            plt.axhline(First, color = 'purple')
            plt.axhline(Second, color = 'yellow')

    plt.show()


Type = input("Please enter type number (1 for EURUSD, 2 for GBPUSD, 3 for GBPJPY)\n")
Type = int (Type)
if Type == 1:
    TypeName = 'EURUSD'
elif Type == 2:
    TypeName = 'GBPUSD'
elif Type == 3:
    TypeName = 'GBPJPY'
else:
    sys.exit ("Type number should be 1, 2 or 3.")

Date = input ("Please enter plot date (like 2020.01.03)\n")
BarMin = input ("enter the minutes of each bar (5 or 60)\n")
BarMin = int(BarMin)

print (TypeName, Date, BarMin)
df = work (TypeName, Date, Date, BarMin)

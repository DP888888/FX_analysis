import test
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc

def plot_c(df, ax=None, fmt="%Y-%m-%d"):
    if ax is None:
        fig, ax = plt.subplots()

    # dat[df.index.name] = dat[df.index.name].map(mdates.date2num)
    dat = df
    print (type (dat))
    print ('==== ', dat.values)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    plt.xticks(rotation=45)
    _ = candlestick_ohlc(ax, dat.values, width=.6, colorup='g', alpha =1)

    # ax.set_xlabel(idx_name)
    # ax.set_ylabel("OHLC")
    return ax


def work (typeName):
    price = test.PriceRecord (typeName)
    # price.printM1()
    # print ('===')
    df = price.plotGivenDate('2020.10.01')
    print (df)
    return df
    # ax = plot_c(df)


df = work ('EURUSD')
print (df.index)

import pandas as pd
from pandas.compat import StringIO

import matplotlib.pyplot as plt
# from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates

def plot_candlestick(df, ax=None, fmt="%Y-%m-%d"):
    if ax is None:
        fig, ax = plt.subplots()
    idx_name = df.index.name
    # print (df.index)
    # print ('idx name', idx_name)
    dat = df.reset_index()[[idx_name, "OPEN", "HIGH", "LOW", "CLOSE"]]
    # dat = df
    # print ('222222   ', dat)
    dat[df.index.name] = dat[df.index.name].map(mdates.date2num)
    print ('23453453422222   ', dat)
    # print (type (dat))
    # print ('==== ', dat.values)
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter(fmt))
    plt.xticks(rotation=45)
    _ = candlestick_ohlc(ax, dat.values, width=.6, colorup='g', alpha =1)

    # ax.set_xlabel(idx_name)
    # ax.set_ylabel("OHLC")
    return ax

data="""DATE,Stock,OPEN,HIGH,LOW,CLOSE,Volume
2016-09-29,KESM,7.92,7.98,7.92,7.97,149400
2016-09-30,KESM,7.96,7.97,7.84,7.9,29900"""

# data="""DATE,Stock,OPEN,HIGH,LOW,CLOSE,Volume
# 2016-09-29,KESM,7.92,7.98,7.92,7.97,149400
# 2016-09-30,KESM,7.96,7.97,7.84,7.9,29900
# 2016-10-04,KESM,7.8,7.94,7.8,7.93,99900
# 2016-10-05,KESM,7.93,7.95,7.89,7.93,77500
# 2016-10-06,KESM,7.93,7.93,7.89,7.92,130600
# 2016-10-07,KESM,7.91,7.94,7.91,7.92,103000"""

# df = pd.read_csv(StringIO(data), index_col='DATE', parse_dates=True)
df = df.set_index ('DATE')
print (df)

print ("'''''''")
print (df)

ax = plot_candlestick(df)

print(ax)

plt.tight_layout()
#plt.savefig("candle.png")
plt.show()
import test
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

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
# print (' ====', df.value)
df['DATE'] = df['DATE'] + ' ' + df['TIME']

df = df[['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE']]
print (df)
df['DATE'] = pd.to_datetime(df['DATE'])
df['HIGH'] = df['HIGH'].astype(float)
df['LOW'] = df['LOW'].astype(float)
df['CLOSE'] = df['CLOSE'].astype(float)
df['OPEN'] = df['OPEN'].astype(float)

print ('=== ', df)

df['DATE'] = df['DATE'].apply (mdates.date2num)
fig, ax = plt.subplots()

# plotting the data
# candlestick_ohlc(ax, df.values, width=0.6, colorup='green', colordown='red', alpha=0.8)
candlestick_ohlc(ax, df.values, width=0.00015, colorup='green', colordown='red')
ax.xaxis_date()
# ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))

plt.xticks(rotation=45)
plt.show ()


exit ()
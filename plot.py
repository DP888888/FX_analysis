import test
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
import pandas as pd
import matplotlib.pyplot as plt
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates

def work (typeName):
    price = test.PriceRecord (typeName)
    df = price.plotGivenDate('2020.10.01', 60)
    print (df)

    df['DATE'] = df['DATE'] + ' ' + df['TIME']

    df = df[['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE']]
    print(df)
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['HIGH'] = df['HIGH'].astype(float)
    df['LOW'] = df['LOW'].astype(float)
    df['CLOSE'] = df['CLOSE'].astype(float)
    df['OPEN'] = df['OPEN'].astype(float)

    print('=== ', df)

    df['DATE'] = df['DATE'].apply(mdates.date2num)
    fig, ax = plt.subplots()

    # plotting the data
    # candlestick_ohlc(ax, df.values, width=0.015, colorup='green', colordown='red')
    candlestick_ohlc(ax, df.values, width=0.015, colorup='green', colordown='red', alpha=0.8)
    ax.xaxis_date()
    ax.xaxis.set_major_locator(ticker.MultipleLocator(0.5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%y-%m-%d %H:%M:%S'))
    if typeName == 'GBPJPY':
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.2f'))
    else:
        ax.yaxis.set_major_formatter(FormatStrFormatter('%.4f'))

    plt.grid()
    # plt.xticks(rotation=45)
    plt.show()
    # return df


# df = work ('EURUSD')
df = work ('GBPJPY')

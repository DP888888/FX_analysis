import test
import pandas as pd
import signal

# eur = test.PriceRecord('EURUSD') #调用test文件里面的方法和类，前面必须要先加上那个文件名
# eur.printM1()
# exit()

column = ['date', 'week', 'type', 'direction', 'entry', 'cut', 'first', 'second']
TradeSignal = pd.read_csv('data/TradeSignal(1).csv', names = column)
TradeSignal = signal.changeDataFormate (TradeSignal)
# print( TradeSignal)


def work (typeName):
    price = test.PriceRecord (typeName)
    price.printM1()

    for i in range (1, 5):
    # for i in range (1, len (TradeSignal)):
        # str =TradeSignal.loc[i]['type']
        # print (str)
        if TradeSignal.loc[i]['type'] == typeName:
            print (i)
            print(TradeSignal.loc[i])
            TodayPriceRecord = price.findPriceGivenDate (TradeSignal.loc[i]['date'] )
            print (TodayPriceRecord)



work ('EURUSD')

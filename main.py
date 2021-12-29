import test
import pandas as pd
import signal

# eur = test.PriceRecord('EURUSD') #调用test文件里面的方法和类，前面必须要先加上那个文件名
# eur.printM1()
# exit()

column = ['date', 'week', 'type', 'direction', 'entry', 'cut', 'First', 'Second']
TradeSignal = pd.read_csv('data/TradeSignal(1).csv', names = column)
TradeSignal = signal.changeDataFormate (TradeSignal)
# print( TradeSignal)

def FindPos (nowPrice, SignalArray, long):
    BeginPrice = float (nowPrice.OPEN)
    if long:
        # Long, from top to down
        if BeginPrice > list (SignalArray.values())[0]:
            return -1
    else:

        Keys = list (SignalArray.keys ())
        Values = list (SignalArray.values ())
        for i in (len (SignalArray) - 1, 0, -1):
            if BeginPrice >= Values[i]:
                return Keys[i]
        assert  (0)

    return -1


def FindTraceFromPriceAndSignal(TodayPriceRecord, SignalArray, long):
    print (long)
    curPos = FindPos (TodayPriceRecord.iloc[0], SignalArray, long)
    print ('curPos  ', curPos)
    i = 0
    # for index, row in TodayPriceRecord.iterrows():
    #     if curPos == -1:
    #         curPos = FindPos(TodayPriceRecord)
    return []


def work (typeName):
    price = test.PriceRecord (typeName)
    price.printM1()

    for i in range (1, 2):
    # for i in range (1, len (TradeSignal)):
        # str =TradeSignal.loc[i]['type']
        # print (str)
        if TradeSignal.loc[i]['type'] == typeName:
            print (i)
            TodayPriceRecord = price.findPriceGivenDate (TradeSignal.loc[i]['date'] )
            print (TodayPriceRecord)
            print(TradeSignal.loc[i])
            SignalArray = {}
            SignalArray[0] = float (TradeSignal.loc[i].Second)
            SignalArray[1] = float (TradeSignal.loc[i].First)
            SignalArray[2] = float (TradeSignal.loc[i].entry)
            SignalArray[3] = float (TradeSignal.loc[i].cut)
            print (SignalArray)
            trace = FindTraceFromPriceAndSignal (TodayPriceRecord, SignalArray, TradeSignal.loc[i].direction == 'short')
            print (trace)



work ('EURUSD')

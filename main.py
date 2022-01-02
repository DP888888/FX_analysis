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

def Between (strCurPrice, CandleRecord):
    CurPrice = float ( strCurPrice)
    Min = min (float (CandleRecord.OPEN), float (CandleRecord.CLOSE))
    Max = max (float (CandleRecord.OPEN), float (CandleRecord.CLOSE))
    return CurPrice >= Min and CurPrice <= Max


def FindPos (CandleRecord, SignalArray, long):
    Keys = list(SignalArray.keys())
    Values = list(SignalArray.values())

    if long:
        if CandleRecord.OPEN <= CandleRecord.CLOSE:
            #up candle
            # find the highest match position, find from high to low
            for i in range(len(Values)):
                if Between (Values[i], CandleRecord):
                    return Keys[i]
        else:
            # down candle
            # find the lowest match position, find from low to high
            for i in range(len(Values) - 1, 0, -1):
                if Between (Values[i], CandleRecord):
                    return Keys[i]
    else:
        # short
        if CandleRecord.OPEN <= CandleRecord.CLOSE:
            #up candle
            # find the highest match position, find from high to low
            for i in range(len(Values) - 1, 0, -1):
                if Between (Values[i], CandleRecord):
                    return Keys[i]
        else:
            # down candle
            # find the lowest match position, find from low to high
            for i in range(len(Values)):
                if Between (Values[i], CandleRecord):
                    return Keys[i]
    return -1




def FindTraceFromPriceAndSignal(TodayPriceRecord, SignalArray, long):
    # print (long)
    curPos = -1
    i = 0
    ret = []
    for index, row in TodayPriceRecord.iterrows():
        nextPos = FindPos(row, SignalArray, long)
        if nextPos != -1 and nextPos != curPos:
            curPos = nextPos
            ret.append (curPos)
    # print (SignalArray)
    return ret


def work (typeName):
    price = test.PriceRecord (typeName)
    # price.printM1()

    for i in range (1, 20):
        if TradeSignal.loc[i]['type'] == typeName :
            print ('=========== ', i)
            TodayPriceRecord = price.findPriceGivenDate (TradeSignal.loc[i]['date'] )
            # print (TodayPriceRecord)
            # print(TradeSignal.loc[i])
            SignalArray = {}
            SignalArray[0] = float (TradeSignal.loc[i].Second)
            SignalArray[1] = float (TradeSignal.loc[i].First)
            SignalArray[2] = float (TradeSignal.loc[i].entry)
            SignalArray[3] = float (TradeSignal.loc[i].cut)
            # print (SignalArray)
            trace = FindTraceFromPriceAndSignal (TodayPriceRecord, SignalArray, TradeSignal.loc[i].direction == 'long')
            print (trace)
            # break



work ('EURUSD')

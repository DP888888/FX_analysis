import test
from collections import OrderedDict
import operator
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

    ret = []
    if long:
        if CandleRecord.OPEN <= CandleRecord.CLOSE:
            #up candle
            # find the highest match position, find from high to low
            for i in range(len(Values)):
                if Between (Values[i], CandleRecord):
                    ret.append(Keys[i])
                    # return Keys[i]
        else:
            # down candle
            # find the lowest match position, find from low to high
            for i in range(len(Values) - 1, 0, -1):
                if Between (Values[i], CandleRecord):
                    ret.append(Keys[i])
                    # return Keys[i]
    else:
        # short
        if CandleRecord.OPEN <= CandleRecord.CLOSE:
            #up candle
            # find the highest match position, find from high to low
            for i in range(len(Values) - 1, 0, -1):
                if Between (Values[i], CandleRecord):
                    ret.append(Keys[i])
                    # return Keys[i]
        else:
            # down candle
            # find the lowest match position, find from low to high
            for i in range(len(Values)):
                if Between (Values[i], CandleRecord):
                    ret.append(Keys[i])
                    # return Keys[i]
    return ret




def FindTraceFromPriceAndSignal(TodayPriceRecord, SignalArray, long):
    # print (long)
    curPos = -1
    i = 0
    ret = []
    for index, row in TodayPriceRecord.iterrows():
        nextPos = FindPos(row, SignalArray, long)
        # print( '====   ', nextPos)
        ret = ret + nextPos
        # if nextPos != -1 and nextPos != curPos:
        #     curPos = nextPos
        #     ret.append (curPos)
    # print (SignalArray)
    return ret

def MakeUnique (trace):
    ret = []
    st = set()
    for each in trace:
        if each not in st:
            # if each == 5: #when we meet cut line (3), clear all records and re-count the set
            #     st.clear ()
            st.add (each)
            ret.append (each)
    return ret


def work (typeName):
    price = test.PriceRecord (typeName)
    # price.printM1()

    countUniqueTrace = {}
    Count = 0
    for i in range (1, len (TradeSignal)):
        if TradeSignal.loc[i]['type'] == typeName :
            Count = Count + 1
            # print ('=========== ', i)
            TodayPriceRecord = price.findPriceGivenDate (TradeSignal.loc[i]['date'] )
            # print (TodayPriceRecord)
            # print(TradeSignal.loc[i])
            SignalArray = signal.SetSignalArray(TradeSignal, i)

            # print (SignalArray)
            trace = FindTraceFromPriceAndSignal (TodayPriceRecord, SignalArray, TradeSignal.loc[i].direction == 'long')
            # print (trace)
            UniqueTrace = tuple (MakeUnique (trace))
            # print ('======   ', UniqueTrace)
            if UniqueTrace in countUniqueTrace.keys ():
                countUniqueTrace[UniqueTrace] = countUniqueTrace[UniqueTrace] + 1
            else:
                countUniqueTrace[UniqueTrace] = 1
    print (Count)
    # print (countUniqueTrace)
    # countUniqueTrace = sorted(countUniqueTrace.items(), key=lambda kv: kv[1])
    # print (countUniqueTrace)
    # for each in countUniqueTrace:
    #     print (each)
    # for each in countUniqueTrace:
    #     print (each, countUniqueTrace[each])
    # OrderedDict(sorted(countUniqueTrace.items(), key=itemgetter(1)))
    countUniqueTrace = OrderedDict(sorted(countUniqueTrace.items(), key=lambda x: x[1]))
    # sorted(countUniqueTrace.iteritems(), key=operator.itemgetter(1))
    # print (countUniqueTrace)
    # print ('====')
    for each in reversed (countUniqueTrace):
        print (each, countUniqueTrace[each])




work ('EURUSD')

import test
from collections import OrderedDict
import numpy
import operator
import pandas as pd
import signal

# eur = test.PriceRecord('EURUSD') #调用test文件里面的方法和类，前面必须要先加上那个文件名
# eur.printM1()
# exit()



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
            # find the lowest match position, find from low to high
            for i in range(len(Values) - 1, 0, -1):
                if Between (Values[i], CandleRecord):
                    ret.append(Keys[i])
                    # return Keys[i]
        else:
            # down candle
            # find the highest match position, find from high to low
            for i in range(len(Values)):
                if Between (Values[i], CandleRecord):
                    ret.append(Keys[i])
                    # return Keys[i]
    else:
        # short
        if CandleRecord.OPEN <= CandleRecord.CLOSE:
            #up candle
            for i in range(len(Values)):
                if Between (Values[i], CandleRecord):
                    ret.append(Keys[i])
                    # return Keys[i]
        else:
            # down candle
            for i in range(len(Values) - 1, 0, -1):
                if Between (Values[i], CandleRecord):
                    ret.append(Keys[i])
                    # return Keys[i]
    for i in range (len (ret)):
        if (ret[i] == 0):
            return ret[0:i + 1]
    return ret




def FindTraceFromPriceAndSignal(TodayPriceRecord, SignalArray, long):
    # print (long)
    curPos = -1
    i = 0
    ret = []
    for index, row in TodayPriceRecord.iterrows():
        nextPos = FindPos(row, SignalArray, long)
        # if (len (nextPos) > 0):
        #     print( '====   ', nextPos)
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
            # if each >= 5: #when we meet cut line (3), clear all records and re-count the set
            #     st.clear ()
            st.add (each)
            ret.append (each)
    return ret


def work (typeName):
    print ('  ^^^^^^ ********** ++++ ======  ', typeName)
    price = test.PriceRecord (typeName)
    print (price.TradeSignal)
    exit()

    test.FullTraceOfEachDate = {}
    test.countUniqueTrace = {}
    test.IndexSetOfEachTrace = {} #record the index in TradeSignal of each trace
    Count = 0
    test.TotalSignalNum = 0
    for i in range (1, len (TradeSignal)):
        if TradeSignal.loc[i]['type'] == typeName :
            TodayPriceRecord = price.findPriceGivenDate (TradeSignal.loc[i]['date'] )
            if TodayPriceRecord.size == 0:
                # print (i, TradeSignal.loc[i]['date'] )
                continue
            Count = Count + 1
            SignalArray = signal.SetSignalArray(TradeSignal, i)

            trace = FindTraceFromPriceAndSignal (TodayPriceRecord, SignalArray, TradeSignal.loc[i].direction == 'long')
            UniqueTrace = tuple (MakeUnique (trace))
            # print (i, TradeSignal.loc[i]['date'], trace, UniqueTrace)
            signal.IncDict(test.countUniqueTrace, UniqueTrace, 1)
            if tuple (UniqueTrace) in test.IndexSetOfEachTrace.keys ():
                test.IndexSetOfEachTrace[UniqueTrace].append (i)
            else:
                test.IndexSetOfEachTrace[UniqueTrace] = [i]

            date = TradeSignal.loc[i]['date']
            test.FullTraceOfEachDate [date] = trace


    print ('Total count: ', Count)
    # print ('empty  ', Empty)
    test.TotalSignalNum = Count
    signal.AnalysisTrace(test.countUniqueTrace, Count, TradeSignal, test.IndexSetOfEachTrace, test)





work ('EURUSD')
# work ('GBPUSD')
# work ('GBPJPY')

import pandas as pd
from collections import OrderedDict

def changeDataFormate (TradeSignal):
    TradeSignal = TradeSignal.drop(labels=0)
    return TradeSignal

def SetSignalArray (TradeSignal, i):
    SignalArray = {}
    index = 0
    if TradeSignal.loc[i].Second == '/':
        SignalArray[index] = 1000000.0
        index = index + 1
        SignalArray[index] = 1000000.0
    else:
        SignalArray[index] = float(TradeSignal.loc[i].Second)
        index = index + 1
        SignalArray[index] = (float(TradeSignal.loc[i].Second) + float(TradeSignal.loc[i].First)) / 2

    index = index + 1

    SignalArray[index] = float(TradeSignal.loc[i].First)
    index = index + 1

    SignalArray[index] = (float(TradeSignal.loc[i].entry) + float(TradeSignal.loc[i].First)) / 2
    index = index + 1

    SignalArray[index] = float(TradeSignal.loc[i].entry)
    index = index + 1

    SignalArray[index] = (float(TradeSignal.loc[i].cut) + float(TradeSignal.loc[i].entry)) / 2
    index = index + 1

    SignalArray[index] = float(TradeSignal.loc[i].cut)
    index = index + 1

    if TradeSignal.loc[i].direction == 'long':
        SignalArray[index] = float(TradeSignal.loc[i].cut) - 0.0010
        index = index + 1
        SignalArray[index] = float(TradeSignal.loc[i].cut) - 0.0020
    else:
        SignalArray[index] = float(TradeSignal.loc[i].cut) + 0.0010
        index = index + 1
        SignalArray[index] = float(TradeSignal.loc[i].cut) + 0.0020
    index = index + 1

    return SignalArray

def CountReachPosNum (countUniqueTrace, posIndex):
    count = 0
    ret = []
    for each in countUniqueTrace:
        for eachPos in each:
            if posIndex == eachPos:
                count = count + countUniqueTrace[each]
                ret.append (each)
                break
    print ('The number of traces ever reach position ', posIndex, '  : ', count)
    for each in ret:
        print ('       ', each, countUniqueTrace[each])

def IncDict (dict, List, curCount):
    if List in dict.keys ():
        dict[List] = dict[List] + curCount
    else:
        dict[List] = 1

def AnalyseBeginPos (countUniqueTrace, TotCount):
    begin = {}
    for each in countUniqueTrace:
        IncDict (begin, each[0:1], countUniqueTrace[each])
        IncDict (begin, each[0:2], countUniqueTrace[each])
    begin = OrderedDict (sorted(begin.items(), key = lambda x: x[0]))
    print ('Count the beginning of each trace')
    for each in begin:
        print (each, begin[each], '                ',  str ( round (begin[each] / TotCount * 100.0, 3)) + '%')

def AnalysisTrace (countUniqueTrace, TotCount):
    countUniqueTrace = OrderedDict(sorted(countUniqueTrace.items(), key=lambda x: x[0]))
    for each in countUniqueTrace:
        print(each, countUniqueTrace[each])
    print (' ====================== ')
    countUniqueTrace = OrderedDict(sorted(countUniqueTrace.items(), key=lambda x: x[1]))
    for each in reversed(countUniqueTrace):
        print(each, countUniqueTrace[each])

    AnalyseBeginPos (countUniqueTrace, TotCount)

    CountReachPosNum (countUniqueTrace, 0)
    CountReachPosNum(countUniqueTrace, 7) # cut - 10

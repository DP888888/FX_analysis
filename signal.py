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

def RemoveContinousEqual (trace):
    ret = []
    for i in range (len (trace)):
        if i == 0 or trace[i] != trace[i - 1]:
            ret.append (trace[i])
    return  ret


def MakeUniqueForMidPosOpenPosition (trace):
    ret = []
    st = set()
    midPosReach = 0
    for each in trace:
        if each not in st:
            if each == 5 and midPosReach == 0:
                midPosReach = 1
                st.clear ()
            st.add (each)
            ret.append (each)
    return ret

def CountReachPosNum (countUniqueTrace, posIndex, TradeSignal, IndexSetOfEachTrace, test):
    count = 0
    ret = []
    for each in countUniqueTrace:
        for eachPos in each:
            if posIndex == eachPos:
                count = count + countUniqueTrace[each]
                ret.append (each)
                break
    print ('The number of traces ever reach position ', posIndex, '  : ', count, Percentage(count, test.TotalSignalNum))

    for each in ret:
        print ('       ', each, countUniqueTrace[each])

        if posIndex == 5:
            # print ('            ', IndexSetOfEachTrace[each])
            for i in range (len (IndexSetOfEachTrace[each])):
                cur = IndexSetOfEachTrace[each][i]
                # date = TradeSignal['date'].values[cur] #this is wrong !!
                date = TradeSignal.loc[cur]['date']
                # print ('     ========= ', cur, date)
                print ('                ******    ', MakeUniqueForMidPosOpenPosition(test.FullTraceOfEachDate[date]))
        print ()

def IncDict (dict, List, curCount):
    if List in dict.keys ():
        dict[List] = dict[List] + curCount
    else:
        dict[List] = curCount

def Percentage (a, b):
    return str ( round (a / b * 100.0, 3)) + '%'

def AnalyseBeginPos (countUniqueTrace, TotCount):
    begin = {}
    for each in countUniqueTrace:
        IncDict (begin, each[0:1], countUniqueTrace[each])
        IncDict (begin, each[0:2], countUniqueTrace[each])
    begin = OrderedDict (sorted(begin.items(), key = lambda x: x[0]))
    print ('Count the beginning of each trace')
    for each in begin:
        print (each, begin[each], '                ', Percentage(begin[each], TotCount))

def AnalysisTrace (countUniqueTrace, TotCount, TradeSignal, IndexSetOfEachTrace, test):
    countUniqueTrace = OrderedDict(sorted(countUniqueTrace.items(), key=lambda x: x[0]))
    for each in countUniqueTrace:
        print(each, countUniqueTrace[each])
        # print ('         ', IndexSetOfEachTrace[tuple (each)])
    # return


    print (' ====================== ')
    countUniqueTrace = OrderedDict(sorted(countUniqueTrace.items(), key=lambda x: x[1]))
    for each in reversed(countUniqueTrace):
        print(each, countUniqueTrace[each])

    countUniqueTrace = OrderedDict(sorted(countUniqueTrace.items(), key=lambda x: x[0]))
    AnalyseBeginPos (countUniqueTrace, TotCount)

    CountReachPosNum (countUniqueTrace, 0, TradeSignal, IndexSetOfEachTrace, test)
    CountReachPosNum(countUniqueTrace, 5, TradeSignal, IndexSetOfEachTrace, test)
    CountReachPosNum(countUniqueTrace, 6, TradeSignal, IndexSetOfEachTrace, test)
    CountReachPosNum(countUniqueTrace, 7, TradeSignal, IndexSetOfEachTrace, test) # cut - 10
    CountReachPosNum(countUniqueTrace, 8, TradeSignal, IndexSetOfEachTrace, test) # cut - 20

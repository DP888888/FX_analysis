import pandas as pd

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
import pandas as pd

def changeDataFormate (TradeSignal):
    TradeSignal = TradeSignal.drop(labels=0)
    return TradeSignal

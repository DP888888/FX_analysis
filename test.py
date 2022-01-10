import io

import pandas as pd
import datetime

def changeDataFormate (TradeSignal):
    return TradeSignal

def StrToDateTime(input):
    # print (input)
    str = input['SignalDate'] + ' ' + input['TIME']
    dateFormatter = "%Y.%m.%d %H:%M:%S"
    t = datetime.datetime.strptime(str, dateFormatter)
    # print(t)
    return t


def FindPosGivenDateTime(priceDate, SignalDate):
    # priceDate = pd.DataFrame.as_matrix (df_priceDate)
    # print (priceDate[1000:2000])
    # print (priceDate)
    # print ('begin find !', SignalDate)
    # print (priceDate.loc[4])
    l = 1
    r = len (priceDate)
    ans = -1
    while (l <= r):
        mid = (l + r) // 2
        # print (priceDate.loc[mid])

        if SignalDate == StrToDateTime (priceDate.loc[mid]):
            ans = mid
            break
        if SignalDate < StrToDateTime (priceDate.loc[mid]):
            r = mid - 1
        if SignalDate > StrToDateTime (priceDate.loc[mid]):
            l = mid + 1

    # print ('finish find ', ans)
    assert (ans != -1) #must find price record
    # print (SignalDate, priceDate.loc[ans])
    return ans


class PriceRecord:
    def __init__(self, name):
        self.name = name
        column = ['SignalDate', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICKVOL', 'VOL', 'SPREAD']
        file_name = 'data/' + name + '_M1.csv'
        # print(file_name)
        self.M1price = pd.read_csv (file_name, sep= '\t', names = column)
        self.FullTraceOfEachDate = {}
        self.countUniqueTrace = {}
        self.IndexSetOfEachTrace = {} #record the index in TradeSignal of each trace
        self.TotalSignalNum = 0

    def printM1 (self):
        print (self.M1price)

    def findPriceGivenDate (self, SignalDate):
        NewDate = ''
        num = 0
        # print (SignalDate, 'begin find ..')

        dateFormatter = "%Y/%m/%d"
        signalDate = datetime.datetime.strptime(SignalDate, dateFormatter)


        # print(self.M1price)
        find = 0
        out = []

        BeginPos = FindPosGivenDateTime (self.M1price, signalDate + datetime.timedelta(hours=7))
        EndPos = FindPosGivenDateTime (self.M1price, signalDate + datetime.timedelta(hours=11))
        # print ('finish ')
        return self.M1price[BeginPos: EndPos]
import io

import pandas as pd
import datetime

def changeDataFormate (TradeSignal):
    return TradeSignal

def StrToDateTime(input):
    # print (input)
    str = input['DATE'] + ' ' + input['TIME']
    dateFormatter = "%Y.%m.%d %H:%M:%S"
    t = datetime.datetime.strptime(str, dateFormatter)
    # print(t)
    return t


def FindPosGivenDateTime(priceDate, DATE):
    # priceDate = pd.DataFrame.as_matrix (df_priceDate)
    # print (priceDate[1000:2000])
    # print (priceDate)
    # print ('begin find !', DATE)
    # print (priceDate.loc[4])
    l = 1
    r = len (priceDate)
    ans = -1
    while (l <= r):
        mid = (l + r) // 2
        # print (priceDate.loc[mid])

        if DATE == StrToDateTime (priceDate.loc[mid]):
            ans = mid
            break
        if DATE < StrToDateTime (priceDate.loc[mid]):
            r = mid - 1
        if DATE > StrToDateTime (priceDate.loc[mid]):
            l = mid + 1

    # print ('finish find ', ans)
    assert (ans != -1) #must find price record
    # print (DATE, priceDate.loc[ans])
    return ans


class PriceRecord:
    def __init__(self, name):
        self.name = name
        column = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICKVOL', 'VOL', 'SPREAD']
        file_name = 'data/' + name + '_M1.csv'
        # print(file_name)
        self.M1price = pd.read_csv (file_name, sep= '\t', names = column)
        self.FullTraceOfEachDate = {}
        self.countUniqueTrace = {}
        self.IndexSetOfEachTrace = {} #record the index in TradeSignal of each trace
        self.TotalSignalNum = 0

    def printM1 (self):
        print (self.M1price)

    def findPriceGivenDate (self, DATE):
        NewDate = ''
        num = 0
        # print (DATE, 'begin find ..')

        dateFormatter = "%Y/%m/%d"
        DATE = datetime.datetime.strptime(DATE, dateFormatter)


        # print(self.M1price)
        find = 0
        out = []

        BeginPos = FindPosGivenDateTime (self.M1price, DATE + datetime.timedelta(hours=7))
        EndPos = FindPosGivenDateTime (self.M1price, DATE + datetime.timedelta(hours=11))
        # print ('finish ')
        return self.M1price[BeginPos: EndPos]

    def SumArrayToOneBar (self, input):
        ret = input[0]
        ret[5] = input[-1][5] #close
        for each in input:
            if float (each[3]) > float (ret[3]): #high
                ret[3] = each[3]
            if float (each[4]) < float (ret[4]): #low
                ret[4] = each[4]
        return  ret

    def plotGivenDate (self, date, MinutePerBar = 1):
        find = 0
        l = -1
        r = -1
        ret = []
        for index, row in self.M1price.iterrows():
            if row['DATE'] == date:
                if l == -1:
                    l = index
                    find = 1
            else:
                if find == 1:
                    r = index
                    break
        tmp = []
        for i in range (l, r):
            if len (tmp) == MinutePerBar or i == r - 1:
                ret.append (self.SumArrayToOneBar (tmp))
                tmp.clear()
            tmp.append (self.M1price.loc[i])
        return pd.DataFrame (ret)

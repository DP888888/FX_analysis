import io

import pandas as pd
import datetime
from pytz import timezone

def changeDataFormate (TradeSignal):
    return TradeSignal

def DtRowToDateTime(input):
    str = input['DATE'] + ' ' + input['TIME']
    dateFormatter = "%Y.%m.%d %H:%M:%S"
    t = datetime.datetime.strptime(str, dateFormatter)
    return t

def StrToDateTime(input):
    dateFormatter = "%Y.%m.%d %H:%M:%S"
    t = datetime.datetime.strptime(str (input), dateFormatter)
    return t

def StrToDayTime(str):
    dateFormatter = "%Y.%m.%d"
    t = datetime.datetime.strptime(str, dateFormatter)
    return t

def CheckDateBetween(date, BeginDate, EncDate):
    input = StrToDayTime(date)
    begin = StrToDayTime(BeginDate)
    end = StrToDayTime(EncDate)
    return input >= begin and input <= end




def FindPosGivenDateTime(priceDate, DATE):
    l = 1
    r = len (priceDate)-1

    if DATE < DtRowToDateTime (priceDate.loc[l]) or  DATE > DtRowToDateTime (priceDate.loc[r]):
        return -1

    ans = -1
    while (l <= r):
        mid = (l + r) // 2

        if DATE == DtRowToDateTime (priceDate.loc[mid]):
            ans = mid
            break
        if DATE < DtRowToDateTime (priceDate.loc[mid]):
            r = mid - 1
        if DATE > DtRowToDateTime (priceDate.loc[mid]):
            l = mid + 1

    assert (ans != -1) #must find price record
    return ans


class PriceRecord:
    def changeTimeFromUTCtoMT4 (self):
        tz_chicago = timezone('America/Chicago')
        for index, row in self.M1price.iterrows ():
            now = DtRowToDateTime(self.M1price.loc[index])
            after = now + datetime.timedelta(hours=9)
            p = now.replace(tzinfo=datetime.timezone.utc).astimezone(tz_chicago) + datetime.timedelta(hours=8)
            # self.M1price.loc[index, 'DATE'] =
            NewDate = str (p.date()).replace ('-', '.')
            # self.M1price.loc[index, 'TIME'] =
            NewTime = str (p.time())
            print (NewDate + ', ' + NewTime + ', ', end = '')
            print("{:.5f}".format(row['OPEN']), end = ', ' )
            print("{:.5f}".format(row['HIGH']), end = ', ' )
            print("{:.5f}".format(row['LOW']), end = ', ' )
            print("{:.5f}".format(row['CLOSE']), end = ', ' )
            print("{:.5f}".format(row['TICKVOL']) )


    def __init__(self, name):
        self.name = name
        # column = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICKVOL', 'VOL', 'SPREAD']
        column = ['DATE', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICKVOL']
        # file_name = 'data/small_' + name + '_M1.csv'
        # file_name = 'data/new_' + name + '_M1.csv'
        file_name = 'data/mt4_' + name + '_M1.csv'
        self.M1price = pd.read_csv (file_name, sep= ',', names = column)
        self.FullTraceOfEachDate = {}
        self.countUniqueTrace = {}
        self.IndexSetOfEachTrace = {} #record the index in TradeSignal of each trace
        self.TotalSignalNum = 0
        new_file_name = file_name.replace ('small', 'MT4')

        column = ['date', 'week', 'type', 'direction', 'entry', 'cut', 'First', 'Second']
        self.TradeSignal = pd.read_csv('data/TradeSignal(4).csv', names=column)
        self.TradeSignal = changeDataFormate(self.TradeSignal)
        self.TradeSignal['direction'] = self.TradeSignal['direction'].astype(str)
        for index, each in self.TradeSignal.iterrows():
            if float(each['entry']) < float(each['cut']):
                dir = 'short'
            else:
                dir = 'long'
            self.TradeSignal.at[index, 'direction'] = dir

    def printM1 (self):
        print (self.M1price)

    def findPriceGivenDate (self, DATE):
        NewDate = ''
        num = 0

        dateFormatter = "%Y/%m/%d"
        DATE = datetime.datetime.strptime(DATE, dateFormatter)


        find = 0
        out = []

        BeginPos = FindPosGivenDateTime (self.M1price, DATE + datetime.timedelta(hours=7))
        EndPos = FindPosGivenDateTime (self.M1price, DATE + datetime.timedelta(hours=11))
        # print ('finish ')
        if BeginPos == -1 or EndPos == -1:
            return pd.DataFrame()
            # retrun -1
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

    def CheckData (self):
        count = -1
        last = self.M1price.loc[1]['DATE']
        for index, each in self.M1price.iterrows():
            # print (index, each)
            if index == 0:
                continue
            if each['DATE'] != last:
                # if count != 1440:
                #     print (last, count-1440)
                print(last, count - 1440)
                last = each['DATE']
                count = 1
            else:
                count = count + 1
        print(last, count - 1440)

    def plot_60_GivenDate (self, BeginDate, EndDate, MinutePerBar = 1):
        find = 0
        l = -1
        r = -1
        ret = []

        l = FindPosGivenDateTime (self.M1price, StrToDayTime(BeginDate))
        r = FindPosGivenDateTime (self.M1price, StrToDateTime(BeginDate + ' 23:59:00'))

        while l - 1 >= 1 and CheckDateBetween(self.M1price.loc[l - 1]['DATE'], BeginDate, EndDate):
            l = l - 1
        Max = len (self.M1price)
        while r + 1 < Max and CheckDateBetween(self.M1price.loc[r + 1]['DATE'], BeginDate, EndDate):
            r = r + 1

        tmp = []
        for i in range (l, r):
            if len (tmp) == MinutePerBar or i == r - 1:
                ret.append (self.SumArrayToOneBar (tmp))
                tmp.clear()
            tmp.append (self.M1price.loc[i])
        return pd.DataFrame (ret)

    def plot_5_GivenDate (self, BeginDate, EndDate, MinutePerBar = 1):
        find = 0
        l = -1
        r = -1
        ret = []

        l = FindPosGivenDateTime (self.M1price, StrToDateTime(BeginDate + ' 06:00:00'))
        r = FindPosGivenDateTime (self.M1price, StrToDateTime(BeginDate + ' 11:30:00'))

        tmp = []
        for i in range (l, r):
            if len (tmp) == MinutePerBar or i == r - 1:
                ret.append (self.SumArrayToOneBar (tmp))
                tmp.clear()
            tmp.append (self.M1price.loc[i])
        return pd.DataFrame (ret)

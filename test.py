import io

import pandas as pd

def changeDataFormate (TradeSignal):
    return TradeSignal


def FindPosGivenDateTime(priceDate, Date, time):
    # priceDate = pd.DataFrame.as_matrix (df_priceDate)
    # print (priceDate)
    print ('begin find !')
    # print (priceDate.loc[4])
    l = 1
    r = len (priceDate)
    while (l < r):
        mid = (l + r) // 2
        print (mid, priceDate.loc [mid])
        break


class PriceRecord:
    def __init__(self, name):
        self.name = name
        column = ['date', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICKVOL', 'VOL', 'SPREAD']
        file_name = 'data/' + name + '_M1.csv'
        # print(file_name)
        self.M1price = pd.read_csv (file_name, sep= '\t', names = column)

    def printM1 (self):
        print (self.M1price)

    def findDate (self, date):
        # print (date)
        NewDate = ''
        num = 0
        for index, each in enumerate (date):
            if each == '/':
                NewDate = NewDate + '.'
                num = num + 1
                if num == 2 and len (date) - index <= 2: #change 2020/10/1 to 2020.10.01
                    NewDate = NewDate + '0'
            else:
                NewDate = NewDate + each
        print (NewDate, 'begin find ..')
        # print(self.M1price)
        find = 0
        out = []
        # for index, row in self.M1price.iterrows ():
        #     if (row['date'] == NewDate):
        #         # print ('find !!!', index)
        #         # print (row)
        #         find = 1
        #         out.append (index)
        #         # break
        #     else :
        #         if find == 1:
        #             break
        BeginPos = FindPosGivenDateTime (self.M1price, NewDate, '00:00:00')
        EndPos = FindPosGivenDateTime (self.M1price, NewDate, '01:00:00')
        print ('finish ')
        # print (out)
        return out
        # print (type (self.M1price))
        # for each in self.M1price:
        #     print (type (each))
        #     break
        #     # if each.date == NewDate:
        #     #     print (each)
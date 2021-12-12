import io

import pandas as pd

def changeDataFormate (TradeSignal):
    return TradeSignal

class PriceRecord:
    def __init__(self, name):
        self.name = name
        column = ['date', 'TIME', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'TICKVOL', 'VOL', 'SPREAD']
        file_name = 'data/' + name + '_M1_small.csv'
        # print(file_name)
        M1price = pd.read_csv (file_name, sep= '\t', names = column)

    # def print1(self):
    #     print("我的名字是%s,我的年龄是%d" % (self.name, self.age))
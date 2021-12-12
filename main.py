import test
import pandas as pd
import signal

eur = test.PriceRecord('EURUSD') #调用test文件里面的方法和类，前面必须要先加上那个文件名

column = ['date', 'week', 'type', 'direction', 'entry', 'cut', 'first', 'second']
TradeSignal = pd.read_csv('data/TradeSignal(1).csv', names = column)
TradeSignal = signal.changeDataFormate (TradeSignal)
print( TradeSignal)

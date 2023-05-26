import pandas as pd
import numpy as np
import math

class calData():
   def __init__(self, RgTT):
       self.lenHr = len(pd.date_range(RgTT[0], RgTT[1], freq='1H'))

   def mainCal(self, BDf, CDf):
       df = pd.Series(index=BDf.columns)
       for st in BDf.columns:
           absdata = abs((BDf[st] - CDf[st])/(BDf[st] + CDf[st]))
           df[st] = 2*sum(absdata)/len(absdata)
       df.loc['Max'] = df.max()
       df = df.apply(lambda x: str(round(x*100, 2))+'%')
       return df

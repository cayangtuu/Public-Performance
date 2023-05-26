import pandas as pd
import numpy as np
import math

class calData():
   def __init__(self, RgTT):
      self.Days = pd.date_range(RgTT[0], RgTT[1], freq='1D')

   def mainCal(self, inDf, calType):
      outDf = pd.DataFrame()
      for DD in self.Days.strftime('%Y-%m-%d'):
          edData = inDf.loc[DD, :]                    #各測站每日小時
          dayDf = eval('self.'+calType+'(edData)')    #各測站模擬期程內每日小時最大值/8小時最大值/日平均值
          outDf = pd.concat([outDf, dayDf], axis=1)
      outDf = outDf.T
      outDf.index = self.Days
      return outDf

   ### 每日小時最大值/8小時最大值/日平均值 計算
   def HourMax(self, df):
       dfOut = pd.Series(index=df.columns)
       for st in df.columns:
          if (df[st].count() >= 16):
             dfOut[st] = df[st].max(axis=0, skipna=True) 
          else:
             dfOut[st] = np.nan
       return dfOut

   def ETHourMax(self, df):
       dfOut = pd.Series(index=df.columns)
       for st in df.columns:
          dataRoll = []
          for i in range(0, 24-8):
             wdw = df[st][i:(i+8)]
             if (wdw.count() >= 5):
                avgwdw = wdw.mean(skipna=True)
                dataRoll.append(avgwdw)
          try:
            dfOut[st] = max(dataRoll)
          except ValueError:
            dfOut[st] = np.nan  
       return dfOut

   def DayMean(self, df):
       dfOut = pd.Series(index=df.columns)
       for st in df.columns:
          if (df[st].count() >= 16):
             dfOut[st] = df[st].mean(axis=0, skipna=True) 
          else:
             dfOut[st] = np.nan
       return df.mean(axis=0, skipna=True)



   ###計算DVb, CMb, CMf, RRF, DVf數值 
   def calDVb(self, df, calType): 
       if (calType=='ETHourMax'):
          Nm = math.ceil(len(self.Days)*0.93)-1
       else:
          Nm = math.ceil(len(self.Days)*0.98)-1

       DVb = pd.Series(index=df.columns)
       for st in DVb.index:
         DVb[st] = df[st].sort_values(na_position='first').iloc[Nm]
       return DVb

   def calRRF(self, BDdf, CDdf):
       Nm = 10
       CMb, CMf = pd.Series(index=BDdf.columns), pd.Series(index=CDdf.columns)
       for st in CMb.index:
          TopMaxVl = BDdf[st].nlargest(Nm, keep='all')
          CMb[st] = TopMaxVl.mean()
          CMf[st] = CDdf[st].loc[TopMaxVl.index].mean()
       
       RRF = round(CMf/CMb, 4)
       return CMb, CMf, RRF

   def calDVf(self, DVb, RRF):
       DVf = round(DVb*RRF, 4)
       return DVf

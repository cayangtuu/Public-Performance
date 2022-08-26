import pandas as pd
import numpy as np
import math

class CalData():
   def __init__(self, Data, var, RgTT):
      self.var = var
      self.Data = Data
      self.Days = pd.date_range(RgTT[0], RgTT[1], freq='1D')
      self.Nm = math.ceil(len(self.Days)*0.98)-1



   ###最大小時平均值增量
   def HourMax(self):
      def sTime(DD):
         if (self.var=='O3'):
            time = slice(DD+'-11', DD+'-18')                 ###若物種為O3時，以每日11時至18時計算
         else:
            time = slice(DD, DD+'-23')
         return time

      EveryDf = []
      for DD in self.Days.strftime('%Y-%m-%d'):
         DailyDf = self.Data.sel(time=sTime(DD))             #各網格點每日資料(共有24*x*y)
         DailyMax = DailyDf.max(axis=0)                      #各網格點每日最大值(x*y)
         EveryDf.append(DailyMax)
      SortDf = np.sort(EveryDf, axis=0)                      #各網格點該月數值由小到大排列
      DF = SortDf[self.Nm]

      return DF



   ###最大8小時平均值增量
   def ETHourMax(self):
      def Rolling8(Data):                                    ###8小時移動平均
         Rolls = []
         for i in range(0, 24-8):
            wdw = Data[i:(i+8)]
            Avgwdw = wdw.mean(axis=0)
            Rolls.append(Avgwdw)
         return Rolls

      EveryDf = []
      for DD in self.Days.strftime('%Y-%m-%d'):
         DailyDf = self.Data.sel(time=slice(DD, DD+'-23'))   #各網格點每日資料(共有24*x*y)
         RollingDf = Rolling8(DailyDf)                       #各網格點每日8小時移動平均值(共有17*x*y)
         DailyMax = np.max(RollingDf, axis=0)                #各網格點每日8小時移動平均最大值(x*y)
         EveryDf.append(DailyMax)
      SortDf = np.sort(EveryDf, axis=0)                      #各網格點該月數值由小到大排列
      DF = SortDf[math.ceil(len(self.Days)*0.93)-1]

      return DF



   ###日平均值增量
   def DayMean(self):
      EveryDf = []
      for DD in self.Days.strftime('%Y-%m-%d'):
         DailyDf = self.Data.sel(time=slice(DD, DD+'-23'))   #各網格點每日資料(共有24*x*y)
         DailyMean = DailyDf.mean(axis=0)                    #各網格點每日平均值(x*y)
         EveryDf.append(DailyMean)
      exit()
      SortDf = np.sort(EveryDf, axis=0)                      #各網格點該月數值由小到大排列
      DF = SortDf[self.Nm]

      return DF


   
   ###年平均值增量
   def YearMean(self):
      DF = self.Data.mean(axis=0).values                     #各網格點該月所有小時平均值(x*y)

      return DF


import pandas as pd
import numpy as np
import math

class CalData():
   def __init__(self, Bdf, Cdf, var, RgTT):
      self.Bdf = Bdf
      self.Cdf = Cdf
      self.var = var
      self.Days = pd.date_range(RgTT[0], RgTT[1], freq='1D')
      self.Nm = math.ceil(len(self.Days)*0.98)-1


   ###網格點於該月中self.Nm所在的日期所對應的數值
   def IndexVl(self, SIdx, Data):
      OutData = np.array([[float(Data[SIdx[ii][jj]][ii][jj]) \
                  for jj in range(SIdx.shape[1])]
                  for ii in range(SIdx.shape[0])])
      return OutData


   ###最大小時平均值增量
   def HourMax(self):
      def sTime(DD):
         if (self.var=='O3'):
            time = slice(DD+'-11', DD+'-18')            ###若物種為O3時，以每日11時至18時計算
         else:
            time = slice(DD, DD+'-23')
         return time

      IncDf, BDf, CDf = [], [], []
      for DD in self.Days.strftime('%Y-%m-%d'):
         BDD = self.Bdf.sel(time=sTime(DD)).values      #Before各網格點每日資料(共有24*x*y)
         CDD = self.Cdf.sel(time=sTime(DD)).values      #After 各網格點每日資料(共有24*x*y)

         IncDD = CDD - BDD                              #各網格點增量值(24*x*y)
         MaxIdx = np.argmax(IncDD, axis=0)              #尋找每日中最大值所在的小時 
         IncMax = self.IndexVl(MaxIdx, IncDD)           #各網格點每日最大值增量(x*y)

         IncDf.append(IncMax)
         BDf.append(self.IndexVl(MaxIdx, BDD))
         CDf.append(self.IndexVl(MaxIdx, CDD))

      SIdx = np.argsort(IncDf, axis=0)[self.Nm]         #尋找該月中self.Nm所在的日期
      IncData = self.IndexVl(SIdx, IncDf)
      BData = np.around(self.IndexVl(SIdx, BDf), 2)
      CData = np.around(self.IndexVl(SIdx, CDf), 2)

      return {'Inc':IncData, 'Before':BData, 'After':CData}



   ###最大8小時平均值增量
   def ETHourMax(self):
      def Rolling8(BDD, CDD):                           ###8小時移動平均
         IncRoll, BRoll, CRoll = [], [], []
         for i in range(0, 24-8):
            Bwdw = BDD[i:(i+8)]
            BAvgwdw = Bwdw.mean(axis=0)
            Cwdw = CDD[i:(i+8)]
            CAvgwdw = Cwdw.mean(axis=0)

            BRoll.append(BAvgwdw)
            CRoll.append(CAvgwdw)
            IncRoll.append(CAvgwdw - BAvgwdw)
         return IncRoll, BRoll, CRoll

      IncDf, BDf, CDf = [], [], []
      for DD in self.Days.strftime('%Y-%m-%d'):
         BDD = self.Bdf.sel(time=slice(DD, DD+'-23'))   #Before各網格點每日資料(共有24*x*y)
         CDD = self.Cdf.sel(time=slice(DD, DD+'-23'))   #After 各網格點每日資料(共有24*x*y)

         IncRoll, BRoll, CRoll = Rolling8(BDD, CDD)     #8小時平均值(17*x*y)
         MaxIdx = np.argmax(IncRoll, axis=0)            #尋找每日中最大值所在的8小時平均值位置
         IncMax = self.IndexVl(MaxIdx, IncRoll)         #各網格點每日8小時移動平均最大值(x*y)

         IncDf.append(IncMax)
         BDf.append(self.IndexVl(MaxIdx, BRoll))
         CDf.append(self.IndexVl(MaxIdx, CRoll))

      Nm = math.ceil(len(self.Days)*0.93)-1
      SIdx = np.argsort(IncDf, axis=0)[Nm]              #尋找該月中Nm所在的日期
      IncData = self.IndexVl(SIdx, IncDf)
      BData = np.around(self.IndexVl(SIdx, BDf), 2)
      CData = np.around(self.IndexVl(SIdx, CDf), 2)

      return {'Inc':IncData, 'Before':BData, 'After':CData}



   ###日平均值增量
   def DayMean(self):
      IncDf, BDf, CDf = [], [], []
      for DD in self.Days.strftime('%Y-%m-%d'):
         BDD = self.Bdf.sel(time=slice(DD, DD+'-23'))   #Before各網格點每日資料(共有24*x*y)
         CDD = self.Cdf.sel(time=slice(DD, DD+'-23'))   #After 各網格點每日資料(共有24*x*y)
         BMean = BDD.mean(axis=0)                       #Before各網格點每日平均值(x*y)
         CMean = CDD.mean(axis=0)                       #After 各網格點每日平均值(x*y)

         IncDD = CMean - BMean                          #各網格點每日平均值增量(x*y)
         IncDf.append(IncDD)                            #該月每日各網格點增量(24*x*y)
         BDf.append(BMean)
         CDf.append(CMean)

      SIdx = np.argsort(IncDf, axis=0)[self.Nm]         #尋找該月中self.Nm所在的日期
      IncData = self.IndexVl(SIdx, IncDf)
      BData = np.around(self.IndexVl(SIdx, BDf), 2)
      CData = np.around(self.IndexVl(SIdx, CDf), 2)

      return {'Inc':IncData, 'Before':BData, 'After':CData}


   
   ###年平均值增量
   def YearMean(self):
      BData = self.Bdf.mean(axis=0).values              #Before各網格點該月所有小時平均值(x*y)
      CData = self.Cdf.mean(axis=0).values              #After 各網格點該月所有小時平均值(x*y)
      IncData = CData - BData                           #各網格點該月平均值增量

      BData = np.around(BData, 2)
      CData = np.around(CData, 2)

      return {'Inc':IncData, 'Before':BData, 'After':CData}


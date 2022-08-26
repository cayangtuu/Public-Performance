import pandas as pd
import numpy as np
import os, calendar
from Lib import getData, calData, plot2D

###時間格式設定
try:
#   keyTime = input("請輸入性能評估月份，ex:2019-01 : ")
    keyTime = '2019-01'
    YY, MM = keyTime.split('-')
    LM = calendar.monthrange(int(YY), int(MM))[1]
    start = keyTime + '-01-00'
    end   = keyTime + '-' + str(LM) + '-23'
    RgTT = [start, end]
except ValueError:
    print('！！！ 請確認輸入格式 ！！！')
    sys.exit()
if (YY != '2019'):
    print("！！！模擬年份請輸入'2019'！！！")
    sys.exit()

nowTT = pd.Timestamp.now().strftime('%Y-%m-%d-%H-%M-%S')


###資料夾與檔案名稱設定
SimDir = os.path.join(os.getcwd(), 'Data', 'Sim')
BaseFil = os.path.join(SimDir, 'Base', 'v1.2019-01.conc.nc')
CaseFil = os.path.join(SimDir, 'Case', 'c-v1.2019-01.conc.nc')
gridFil = os.path.join(SimDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')

OutDir = os.path.join(os.getcwd(), 'Data', 'Evaluate', nowTT)
plotDir = os.path.join(OutDir, 'plot2D')
try:
   os.makedirs(OutDir)
   os.makedirs(plotDir)
except FileExistsError:
   pass

###物種設定
Vars = ['PM10', 'PM25', 'SO2', 'NO2', 'O3']

###經緯度範圍設定
latlon = [119.3, 122.1, 21.82, 25.43]

###副程式
##由Grd轉為每個網格點經緯度資料
def Grd2LL(DF, Lat, Lon, PFCN):
   sLat = Lat.values.reshape(-1)
   sLon = Lon.values.reshape(-1)
   sDF  = DF.reshape(-1)

   LLData = pd.DataFrame.from_dict({'Lat':sLat, 
                                    'Lon':sLon, 
                                    PFCN:sDF})
   return LLData


###主程式
Data = getData.getData(BaseFil, CaseFil, gridFil, RgTT)
Lat, Lon = Data.LatLon()
for var in Vars:
   Indf = Data.EvyLLVl(var)

   CalData = calData.CalData(Indf, var, RgTT)
   PlotData = plot2D.PLOT(var, latlon, keyTime, gridFil, plotDir)

   ##進行不同物種之增量計算設定
   if (var == 'O3'):
      PerForm = ['HourMax', 'ETHourMax']
      PerForCN = ['最大小時平均值增量', '八小時平均值增量']
   elif (var == 'PM25') or (var == 'PM10'):
      PerForm = ['DayMean', 'YearMean']
      PerForCN = ['日平均值增量', '年平均值增量']
   else:
      PerForm = ['HourMax', 'YearMean']
      PerForCN = ['最大小時平均值增量', '年平均值增量']


   for PF in range(len(PerForm)):
      #增量計算
      DF = eval('CalData.' + PerForm[PF] + '()')

      #輸出檔案
      OutData = Grd2LL(DF, Lat, Lon, PerForCN[PF])
      OutFil = os.path.join(OutDir, keyTime+'_'+var+PerForCN[PF]+'.csv')
      OutData.to_csv(OutFil, encoding='utf-8-sig', index = False)

      #繪製等濃度圖
      Plot = PlotData.plot2D(DF, Lat, Lon, PerForCN[PF])


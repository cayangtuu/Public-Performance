import pandas as pd
import numpy as np
import os, sys, calendar
from Lib import getData, calData, CountyDict, plot2D

###時間格式設定
try:
    keyTime = input("請輸入'計算增量前後模擬濃度差值'月份，ex:2019-01 : ")
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
gridFil = os.path.join(SimDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')
CountyFil = os.path.join(SimDir, 'CountyDict', 'CountyDict.csv') #網格所屬縣市檔案名稱
stFil = os.path.join(SimDir, 'st.csv')                           #測站經緯度檔案名稱(有再加入)


###使用者自行輸入Before及After 檔案名稱
def FileExists(Fil):
   if os.path.isfile(Fil):
     pass
   else:
     print("檔案不存在，請確認輸入檔案名稱是否正確 ! ! !")
     sys.exit()
   return
BaseFilNm = input("請輸入Base之增量前模擬檔案名稱，ex:v1.2019-01.conc.nc : ")
BaseFil = os.path.join(SimDir, 'Base', BaseFilNm)       #Before檔案名稱
FileExists(BaseFil)
CaseFilNm = input("請輸入Case之增量後模擬檔案名稱，ex:c-v1.2019-01.conc.nc : ")
CaseFil = os.path.join(SimDir, 'Case', CaseFilNm)       #After 檔案名稱
FileExists(CaseFil)


###創建輸出檔案之資料夾
OutDir = os.path.join(os.getcwd(), 'Data', 'Evaluate', nowTT+'_For'+keyTime)
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

#########################################################################################################
#########################################################################################################

###副程式
##由Grd轉為每個網格點經緯度資料
def Grd2LL(DF, Lat, Lon, PFCN, Unit):
   LLData = pd.DataFrame.from_dict({\
            '經度':Lon.values.reshape(-1),\
            '緯度':Lat.values.reshape(-1),\
            PFCN+Unit:DF['Inc'].reshape(-1),\
            '背景模擬濃度'+Unit:DF['Before'].reshape(-1),\
            '增量後模擬濃度'+Unit:DF['After'].reshape(-1)})
   return LLData

##由List轉為每個網格點經緯度資料
def List2LL(CtyDF, PFCN, Unit):
   columns = ['縣市', '經度', '緯度', PFCN+Unit, \
              '背景模擬濃度'+Unit, '增量後模擬濃度'+Unit]
   LLData = pd.DataFrame(CtyDF, \
                         columns = columns, \
                         dtype = np.object)
   return LLData

def VarUnit(var):
   if var in ['PM25', 'PM10']:
     unit = '(ug/m3)'
   elif var in ['NO2', 'SO2', 'O3']:
     unit = r'(ppb)' 
   return unit

###主程式
Data = getData.getData(BaseFil, CaseFil, gridFil, RgTT)           #取得模擬資料前基本資訊輸入
Lat, Lon = Data.LatLon()                                          #取得經緯度資料
#CtyDict = CountyDict.CtyDict([Lat,Lon], SimDir)                  #輸出網格所屬縣市資料(若檔案存在則不跑)
CtyDict = np.loadtxt(CountyFil, delimiter=',', \
              encoding='utf-8-sig', dtype=np.object)[:,:92]       #讀入網格所屬縣市資料(與上行擇一開啟)

for var in Vars:
   Bdf, Cdf = Data.EvyLLVl(var)                                   #取得Before及After之模擬資料

   CalData = calData.CalData(Bdf, Cdf, var, RgTT)                 #計算各物種模擬濃度增量統計前基本資訊輸入
   PlotData = plot2D.PLOT(var, latlon, keyTime, gridFil, plotDir)      #繪製等濃度圖前基本資訊輸入

   ##進行不同物種之增量計算設定
   if (var == 'O3'):
      PerForm = ['HourMax', 'ETHourMax']
      PerForCN = ['最大小時平均值差值', '八小時平均值差值']
      PerForEN = ['MaxHourlyAvg', '8HourAvg']
   elif (var == 'PM25') or (var == 'PM10'):
      PerForm = ['DayMean', 'YearMean']
      PerForCN = ['日平均值差值', '年平均值差值']
      PerForEN = ['DailyAvg', 'AnnualMean']
   else:
      PerForm = ['HourMax', 'YearMean']
      PerForCN = ['最大小時平均值差值', '年平均值差值']
      PerForEN = ['MaxHourlyAvg', 'AnnualMean']


   for PF in range(len(PerForm)):
      #print(f'var={var}, 統計類型={PerForm[PF]}')
      #增量計算及檔案輸出
      CalDF = eval('CalData.' + PerForm[PF] + '()') 

      CalOut = Grd2LL(CalDF, Lat, Lon, PerForCN[PF], VarUnit(var))
      CalFil = os.path.join(OutDir, keyTime+'__GRIDS__'+var+'_'+PerForEN[PF]+'.csv')
      CalOut.to_csv(CalFil, encoding='utf-8-sig', index = False)


      #縣市最大模擬增量值及檔案輸出
      CtyDF = CountyDict.CtyData(gridFil, stFil, CtyDict, CalDF)

      CtyOut = List2LL(CtyDF, PerForCN[PF], VarUnit(var))
      CtyFil = os.path.join(OutDir, keyTime+'__COUNTIESMAX__'+var+'_'+PerForEN[PF]+'.csv')
      CtyOut.to_csv(CtyFil, encoding='utf-8-sig', index = False)


      #繪製等濃度圖
      Plot = PlotData.plot2D(CalDF['Inc'], Lat, Lon, [PerForCN[PF], PerForEN[PF]])

print('finish')

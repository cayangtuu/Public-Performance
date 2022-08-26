import datetime as dt
import time, calendar
import os, sys
import warnings
import pandas as pd
from Lib import plot2D
from numpy import nan


def main():
    global now, tt_list, latlon, cmaqFil
    now = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

    ######### 產生繪圖時間間距
    try:
       keyTime = input("請輸入繪圖的【月份】，ex:2019-01: ")
       YY, MM = keyTime.split('-')
       monthCountDay = calendar.monthrange(int(YY), int(MM))[1]
       start = dt.datetime(int(YY), int(MM), 1, 0)
       end = dt.datetime(int(YY), int(MM), monthCountDay, 23)
    except ValueError:
       print('！！！ 請確認輸入格式 ！！！')
       sys.exit()

    if (YY != '2019'):
       print("！！！模擬年份請輸入'2019'！！！")
       sys.exit()

    tt_list = [start, end]

    
    ######### 產生繪圖經緯度範圍 [lat: 119.3~122.1(E), lon: 21.82~25.43(N)]
    latlon_limit = [119.3, 122.1, 21.82, 25.43]
    latlon = [119.3, 122.1, 21.82, 25.43]
#   try:
#      Lon = input("請輸入繪圖的【經度】範圍，ex:119.3-122.1 : ")
#      LLon, RLon = Lon.split('-')
#      Lat = input("請輸入繪圖的【緯度】範圍，ex:21.82-25.43 : ")
#      SLat, NLat = Lat.split('-')
#      latlon = [float(LLon), float(RLon), float(SLat), float(NLat)]
#   except ValueError:
#      print('！！！ 請確認輸入格式 ！！！')
#      sys.exit()

#   if (latlon[0] < latlon_limit[0]) or (latlon[2] < latlon_limit[2]) or \
#      (latlon[1] > latlon_limit[1]) or (latlon[3] > latlon_limit[3]):
#      print('請檢查輸入之經緯度範圍，已超出可繪圖的範圖 \n' +
#            '（經度: 東經119.3~122.1, 緯度: 北緯21.82~25.43）')
#      sys.exit()


    ######Sim 先將CMAQ資料讀進來
    cmaqDir = os.path.join(os.getcwd(), 'Data', 'Sim', 'cctm')
    cmaqFil = os.path.join(cmaqDir, 'v4.' + keyTime + '.conc.nc')


    ##畫圖選擇
#   MainPlot2D('hour')
#   MainPlot2D('day')
    MainPlot2D('month')

    print('finish')


def MainCMAQData(func):
    from Lib import getCMAQ
    def wrap(*args, **kwargs):
        CMAQData = getCMAQ.getCMAQ(cmaqFil)
        if 'VOC' in CMAQData.CMAQData:
            CMAQData.CMAQData = CMAQData.CMAQData.rename({'VOC': 'NMHC'})  ##更改物種名稱
        if 'PM25_TOT' in CMAQData.CMAQData:
            CMAQData.CMAQData = CMAQData.CMAQData.rename({'PM25_TOT': 'PM25'})  ##更改物種名稱
        func(CMAQData, *args, **kwargs)
    return wrap



@MainCMAQData
def MainPlot2D(CMAQData, Ttype):
    '''平面圖繪製'''
    CCtempt = CMAQData.CMAQData.sel(time=slice(tt_list[0] - dt.timedelta(hours=8),
                                               tt_list[1] - dt.timedelta(hours=8))) #只取整個月份的資料
    CCtempt['time']= CCtempt.time + pd.Timedelta(hours=8) # UTC -> LT

    if Ttype == 'hour':
       CCData = CCtempt
       pp2DspcList = ['O3', 'NO2', 'NMHC']
    elif Ttype == 'day':
       warnings.filterwarnings("ignore", category=FutureWarning)
       CCData =  CCtempt.resample(time = '1D').mean()
       pp2DspcList = ['PM10', 'PM25', 'NO2', 'SO2']
    elif Ttype == 'month':
       warnings.filterwarnings("ignore", category=FutureWarning)
       CCData =  CCtempt.resample(time = '1M').mean()
       pp2DspcList = ['O3', 'NO2', 'NMHC', 'PM10', 'PM25', 'SO2']

    
    pp2D = plot2D.plot2D(CCData, latlon)
    tmpT_list = CCData.time.values
    pp2DTimeList = [i for i in range(len(tmpT_list))]
    for spc in pp2DspcList:
        print('Start to plot 2D : ' + spc)
        for tt in pp2DTimeList:
            pp2D.plot2D(spc, tt, type=Ttype)

if __name__ == '__main__':
    main()

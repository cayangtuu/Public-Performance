import datetime as dt
import time, calendar
import os, sys
import warnings
import pandas as pd
import numpy as np
from Lib import plot2D


def main():
    global nowTT, tt_list, latlon, cmaqFil, gridFil

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
    nowTT = pd.Timestamp.now().strftime("%Y-%m-%d-%H-%M-%S")
    
    ######### 產生繪圖經緯度範圍 [lat: 119.3~122.1(E), lon: 21.82~25.43(N)]
    latlon_limit = [119.3, 122.1, 21.82, 25.43]
    latlon = [119.3, 122.1, 21.82, 25.43]


    ######Sim 先將CMAQ資料讀進來
    cmaqDir = os.path.join(os.getcwd(), 'Data', 'Sim')
    gridFil = os.path.join(cmaqDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')
    cmaqFilNm = input("請輸入欲計算性能評估之模擬檔案名稱，ex:v1.2019-01.conc.nc : ")
    cmaqFil = os.path.join(cmaqDir, 'cctm', cmaqFilNm)
    if os.path.isfile(cmaqFil):
      pass
    else:
      print("檔案不存在，請確認輸入檔案名稱是否正確 ! ! !")
      sys.exit()


    ##畫圖選擇
    MainPlot2D('hour')
    MainPlot2D('day')
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
    '''用MCIP換掉原先內部的lat,lon'''
    CMAQData.updateLL(gridFil)

    '''平面圖繪製'''
    CCtempt = CMAQData.CMAQData.sel(time=slice(tt_list[0] - dt.timedelta(hours=8),
                                               tt_list[1] - dt.timedelta(hours=8))) #只取整個月份的資料
    CCtempt['time']= CCtempt.time + pd.Timedelta(hours=8) # UTC -> LT

    if Ttype == 'hour':
       CCData = CCtempt.isel(time=CCtempt.time.dt.hour.isin(np.arange(12,17+1))) #只畫12-17時段
       pp2DspcList = ['O3', 'NO2', 'NMHC']
    elif Ttype == 'day':
       warnings.filterwarnings("ignore", category=FutureWarning)
       CCData =  CCtempt.resample(time = '1D').mean()
       pp2DspcList = ['PM10', 'PM25', 'NO2', 'SO2']
    elif Ttype == 'month':
       warnings.filterwarnings("ignore", category=FutureWarning)
       CCData =  CCtempt.resample(time = '1M').mean()
       pp2DspcList = ['NO2', 'PM10', 'PM25', 'SO2']

    
    pp2D = plot2D.plot2D(CCData, latlon, nowTT)
    tmpT_list = CCData.time.values
    pp2DTimeList = [i for i in range(len(tmpT_list))]
    for spc in pp2DspcList:
        print('Start to plot 2D : ' + spc)
        for tt in pp2DTimeList:
            pp2D.plot2D(spc, tt, type=Ttype)

if __name__ == '__main__':
    main()

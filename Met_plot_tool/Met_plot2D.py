import datetime as dt
import os, sys, calendar
import warnings
import numpy as np
import pandas as pd
from Lib import plot2D, getStData


def main():
    global nowTT, tt_list, latlon, wrfDir, stWind, stInfo

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

    
    ######### 產生繪圖經緯度範圍 [lat: 117.68915~124.49884(E), lon: 20.89283~27.013783(N)]
    latlon = [117.68915, 124.49884, 20.89283, 27.013783]
#   latlon_limit = [117.68915, 124.49884, 20.89283, 27.013783]
#   try:
#      Lon = input("請輸入繪圖的【經度】範圍，ex:117.68915-124.49884 : ")
#      LLon, RLon = Lon.split('-')
#      Lat = input("請輸入繪圖的【緯度】範圍，ex:20.89283-27.013783 : ")
#      SLat, NLat = Lat.split('-')
#      latlon = [float(LLon), float(RLon), float(SLat), float(NLat)]
#   except ValueError:
#      print('！！！ 請確認輸入格式 ！！！')
#      sys.exit()

#   if (latlon[0] < latlon_limit[0]) or (latlon[2] < latlon_limit[2]) or \
#      (latlon[1] > latlon_limit[1]) or (latlon[3] > latlon_limit[3]):
#      print('請檢查輸入之經緯度範圍，已超出可繪圖的範圖 \n' +
#            '（經度: 東經117.68915~124.49884, 緯度: 北緯20.89283~27.013783）')
#      sys.exit()


    ######先將WRF原始資料, 測站風場資料, 測站資訊 讀進來
    wrfDir = os.path.join(os.getcwd(), 'Data', 'Sim', 'Raw_Data', keyTime)
    SimDir = os.path.join(os.getcwd(), 'Data', 'Sim')
    stFil  = os.path.join(os.getcwd(), 'Data', 'Sim', 'st.csv')

    stWind, stInfo = getStData.getWind(stFil, SimDir, tt_list)


    ##畫圖選擇
    MainPlot2D('hour')
    MainPlot2D('month')

    print('finish')


def MainPlot2D(Ttype):
    '''平面圖繪製'''
    WRF = plot2D.plot2D(wrfDir, latlon, stInfo, stWind, nowTT)

    if (Ttype == 'hour'):
       tmpT_list = WRF._open_dataset(wrfDir)[1].Time.values
       pp2DTimeList = [i for i in range(0, len(tmpT_list), 6)   #只畫02,08,14,20 LT時間
            if (pd.to_datetime(tmpT_list[i]) >= (tt_list[0]+pd.Timedelta(hours=2))) & \
               (pd.to_datetime(tmpT_list[i]) <= (tt_list[1]))]

    elif (Ttype == 'month'):
       tmpT_list = WRF._month_data()[1].Time.values
       pp2DTimeList = [i for i in range(len(tmpT_list))         #只畫1個月的圖
                       if (pd.to_datetime(tmpT_list[i]) >= tt_list[0]) & \
                          (pd.to_datetime(tmpT_list[i]) <= tt_list[1])]


    for tt in pp2DTimeList:
        LstTime = tmpT_list[tt]
        WRF.plot2D(tt, LstTime, type=Ttype)



if __name__ == '__main__':
    main()

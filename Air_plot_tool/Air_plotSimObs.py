import datetime as dt
import os, sys, calendar
import pandas as pd
from Lib import plotSimObs
from numpy import nan


def main():
    global nowTT, AirQ_Area, tt_list, cmaqFil, gridFil, stFil, ObsDir
    AirQ_Area = {'North':   ['基隆', '汐止', '萬里', '新店', '土城', '板橋', '新莊', '菜寮',
                             '林口', '淡水', '士林', '中山', '萬華', '古亭', '松山', '桃園',
                             '大園', '觀音', '平鎮', '龍潭', '湖口', '竹東', '新竹', '頭份', 
                             '苗栗', '三義', '豐原', '陽明', '宜蘭', '冬山', '富貴角'],
                 'Central': ['竹東', '新竹', '頭份', '苗栗', '三義', '豐原', '沙鹿', '大里',
                             '忠明', '西屯', '彰化', '線西', '二林', '南投', '斗六', '崙背',
                             '新港', '朴子', '台西', '嘉義', '竹山', '埔里'],
                 'YunChia': ['彰化', '線西', '二林', '南投', '斗六', '崙背', '新港', '朴子',
                             '台西', '嘉義', '新營', '善化', '安南', '台南', '美濃', '竹山',
                             '埔里', '麥寮'],
                 'South':   ['朴子', '嘉義', '新營', '善化', '安南', '台南', '美濃', '橋頭',
                             '仁武', '大寮', '林園', '楠梓', '左營', '前金', '前鎮', '小港',
                             '屏東', '潮州', '恆春'],
                 'East':    ['台東', '花蓮', '埔里', '關山']}


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
    
    ######Sim 先將CMAQ資料讀進來
    cmaqDir = os.path.join(os.getcwd(), 'Data', 'Sim')
    gridFil = os.path.join(cmaqDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')
    stFil   = os.path.join(cmaqDir, 'st.csv')

    cmaqFilNm = input("請輸入欲計算性能評估之模擬檔案名稱，ex:v1.2019-01.conc.nc : ")
    cmaqFil = os.path.join(cmaqDir, 'cctm', cmaqFilNm)
    if os.path.isfile(cmaqFil):
      pass
    else:
      print("檔案不存在，請確認輸入檔案名稱是否正確 ! ! !")
      sys.exit()

    ###### Obs 先將觀測資料讀進來
    ObsDir = os.path.join(os.getcwd(), 'Data', 'Obs')

    ##畫圖選擇
    print('scatter')
    MainPlotTimeSeries('scatter')
    print('timeseries')
    MainPlotTimeSeries('timeseries')

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


def TransData(data, Tvars):

    Trans_data = pd.DataFrame()
    for var in Tvars:
       if (var == 'O3') or (var == 'NMHC'):
          varSer = data[var]
       elif (var == 'NO2_hr'):
          varSer = data['NO2']
       elif (var == 'NO2_day'):
          varSer = data['NO2'].resample('D').mean()
       else:
          varSer = data[var].resample('D').mean()

       mask = (varSer.index >= tt_list[0]) & (varSer.index <= tt_list[-1])
       varSer = varSer.loc[mask]  ###去除掉跑到下個月的時間
       Trans_data =  pd.concat([Trans_data, varSer], axis=1, sort=False)

    Trans_data.columns = Tvars
    return Trans_data


@MainCMAQData
def MainPlotTimeSeries(CMAQData, type):
    from Lib import getEPA
    '''用MCIP換掉原先內部的lat,lon'''
    CMAQData.updateLL(gridFil)

    '''一邊讀入觀測及模擬值並畫圖(折線圖)'''
    for area in AirQ_Area:
        print('目前進度:', area)
        for st in AirQ_Area[area]:
            #####讀入觀測資訊
            vars = ['PM10', 'PM25', 'SO2', 'NO2', 'O3', 'NMHC']
            obsSt = getEPA.getEPA(st, tt_list, vars, ObsDir)

            #####讀入CMAQ資訊
            stInfo = CMAQData.stInfo(stFil, st)
            stInfo.update({'area': area})
            cmaqSt = CMAQData.getCMAQst(lat=stInfo['lat'], lon=stInfo['lon'], vars=vars)

            for_O3PM = ['for_O3','for_PM']
            for O3PM in for_O3PM:
                if O3PM == 'for_O3':
                   if all(pd.isnull(obsSt['NMHC'])) == True:
                      Tvars = ['O3', 'NO2_hr']
                   else:
                      Tvars = ['O3', 'NO2_hr', 'NMHC']
                elif O3PM == 'for_PM':
                   Tvars = ['PM10', 'PM25', 'SO2', 'NO2_day']

                pp = plotSimObs.plotSimObs(nowTT, stInfo, TransData(obsSt, Tvars), TransData(cmaqSt, Tvars))
                pp.plot(Tvars, tt_list, O3PM, type=type)


if __name__ == '__main__':
    main()

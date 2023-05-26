import datetime as dt
import time, calendar
import os, sys
import pandas as pd
from Lib import plotSimObs
from numpy import nan


def main():
    global AirQ_Area, nowTT, tt_list, ObsDir, SimDir, stFil

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


    ######### 給定測站
    AirQ_Area = {'North':   ['鞍部', '淡水'  , '竹子湖', '基隆'  , 
                             '台北', '新屋'  , '板橋'  , '新竹'  , 
                             '宜蘭', '蘇澳' ],
                 'Central': ['梧棲', '台中'  , '日月潭', '阿里山',
                             '嘉義', '玉山' ],
                 'South':   ['嘉義', '玉山'  , '永康'  , '台南'  , 
                             '高雄', '大武'  , '恆春' ],
                 'YunChia': ['台中', '日月潭', '阿里山', '嘉義'  , 
                             '玉山', '永康'  , '台南' ],
                 'East':    ['台中', '花蓮'  , '日月潭', '阿里山', 
                             '玉山', '成功'  , '台東'  , '大武' ]}

    
    ######先將Sim及Obs及St資料讀進來
    pwdPath = os.getcwd()
    SimDir  = os.path.join(pwdPath, 'Data', 'Sim')
    ObsDir  = os.path.join(pwdPath, 'Data', 'Obs')
    stFil   = os.path.join(pwdPath, 'Data', 'Sim', 'st.csv')

    ##畫圖選擇
    MainPlotSimObs()
    print('finish')


def MainPlotSimObs():
    from Lib import getStData

    '''一邊讀入觀測及模擬值並畫圖'''
    for area in AirQ_Area:
        print('目前進度:', area)
        for st in AirQ_Area[area]:
            vars = ['T2', 'WS', 'WD']
            #####讀入觀測及模擬資訊
            StData = getStData.getStData(st, tt_list, vars)
            obsSt = StData.getData(ObsDir, 'obs')
            simSt = StData.getData(SimDir, 'sim')
            obsSt.index = pd.date_range(tt_list[0], tt_list[1], freq='1h')
            simSt.index = pd.date_range(tt_list[0], tt_list[1], freq='1h')

            #####讀入測站資訊
            stInfo = StData.stInfo(stFil)
            stInfo.update({'area': area})

            pp = plotSimObs.plot_SimObs(stInfo, obsSt, simSt, tt_list, nowTT)
            for var in vars:
               pp.plot(var)


if __name__ == '__main__':
    main()

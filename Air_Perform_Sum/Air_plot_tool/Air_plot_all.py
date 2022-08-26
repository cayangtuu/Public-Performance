import pandas as pd
import os, sys, calendar
from Lib.Evaluate import Evaluate
from Lib.simobs_hr2day import simobs_hr2day
from Lib.simobs_readhr import sim_readhr, obs_readhr
from Lib.plotSimObs import plot


##輸入欲模擬的月份
start = '2019-01'
end = '2019-12'
Month = pd.date_range(start, end, freq='1MS').strftime('%Y-%m')


##資料夾配置
workDir = os.path.join(os.getcwd(), 'Data', 'Evaluate')
ObsDir  = os.path.join(os.getcwd(), 'Data', 'Obs')
SimDir  = os.path.join(os.getcwd(), 'Data', 'Sim')
cmaqDir = os.path.join(SimDir, 'cctm')
gridFil = os.path.join(SimDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')
stFil   = os.path.join(SimDir, 'st.csv')


AirQ_Area = {'北部': ['基隆', '汐止', '萬里', '新店', '土城', '板橋', '新莊', 
                      '菜寮', '林口', '淡水', '士林', '中山', '萬華', '古亭', 
                      '松山', '桃園', '大園', '觀音', '平鎮', '龍潭', '湖口',
                      '竹東', '新竹', '頭份', '苗栗', '三義', '豐原', '陽明', 
                      '宜蘭', '冬山', '富貴角'],
             '中部': ['竹東', '新竹', '頭份', '苗栗', '三義', '豐原', '沙鹿',
                      '大里', '忠明', '西屯', '彰化', '線西', '二林', '南投', 
                      '斗六', '崙背', '新港', '朴子', '台西', '嘉義', '竹山', '埔里'],
             '雲嘉': ['彰化', '線西', '二林', '南投', '斗六', '崙背', '新港', 
                      '朴子', '台西', '嘉義', '新營', '善化', '安南', '台南', 
                      '美濃', '竹山', '埔里', '麥寮'],
             '南部': ['朴子', '嘉義', '新營', '善化', '安南', '台南', '美濃', 
                      '橋頭', '仁武', '大寮', '林園', '楠梓', '左營', '前金',
                      '前鎮', '小港', '屏東', '潮州', '恆春'],
             '東部': ['台東', '花蓮', '埔里', '關山']}

allVar = {'O3': ['O3','NO2','NMHC'],
          'PM': ['PM10','PM25','NO2','SO2']}

Criteria = {'O3':{'O3':  {'MB': [-0.1,0.1],
                          'MNB':[-0.15, 0.15], 'MNE':[0.0, 0.35], 'R':0.45 },
                  'NO2': {'MNB':[-0.4, 0.5],   'MNE':[0.0, 0.80], 'R':0.35},
                  'NMHC':{'MNB':[-0.4, 0.5],   'MNE':[0.0, 0.80], 'R':0.35 }},
            'PM':{'PM10':{'MFB':[-0.35, 0.35], 'MFE':[0, 0.55],   'R':0.50 },
                  'PM25':{'MFB':[-0.35, 0.35], 'MFE':[0, 0.55],   'R':0.50 },
                  'SO2' :{'MFB':[-0.65, 0.65], 'MFE':[0.0, 0.85], 'R':0.45 },
                  'NO2' :{'MFB':[-0.65, 0.65], 'MFE':[0.0, 0.85], 'R':0.45 }}}


Data = { cats:{ var:{ iid:{ area:[] for area in AirQ_Area } 
                     for iid in Criteria[cats][var] } 
               for var in allVar[cats] } 
         for cats in allVar}
for MM in Month:
    LD = calendar.monthrange(int(MM.split('-')[0]), int(MM.split('-')[1]))[1]
    RgTT = [MM+'-01-00', MM+'-'+str(LD)+'-23']
    cmaqFil = os.path.join(cmaqDir, 'v1.'+MM+'.conc.nc')


    for area in AirQ_Area:
        stons = AirQ_Area[area]

        for cats in allVar:
            Vars = allVar[cats]

            for var in Vars:

                obs_PH = obs_readhr(ObsDir, RgTT, stons, var)
                sim_PH = sim_readhr(cmaqFil, gridFil, stFil, stons, var, RgTT)

                if (var == 'NMHC'):
                   ND = 50.
                elif (var == 'O3'):
                   ND = 40.
                elif (var == 'NO2') or (var == 'SO2'):
                   ND = 0.5
                elif (var == 'PM25') or (var == 'PM10'):
                   ND = 5.
                obs_PH = obs_PH.where(obs_PH >= ND, -999.)
                sim_PH = sim_PH.where(obs_PH >= ND, -999.)

                obs_DA, sim_DA = simobs_hr2day(obs_PH, sim_PH, RgTT)
             
                data_dict = Evaluate(obs_PH, sim_PH, obs_DA, sim_DA, stons, cats, var)

                for id in list(data_dict.keys()):
                    Data[cats][var][id][area].append(data_dict[id]['overal'])

plot(Data, AirQ_Area, allVar, Criteria, workDir)

print('finish')

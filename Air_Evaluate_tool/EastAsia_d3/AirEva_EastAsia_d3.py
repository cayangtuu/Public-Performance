import pandas as pd
import os, sys
import datetime, calendar
from Lib.Evaluate import Evaluate
from Lib.simobs_hr2day import simobs_hr2day
from Lib.simobs_readhr import sim_readhr, obs_readhr


try:
    keyTime = input("請輸入性能評估月份，ex:2019-01 : ")
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

nowTT = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

##資料夾配置
workDir = os.path.join(os.getcwd(), 'Data', 'Evaluate', nowTT+ '_For' +keyTime)
ObsDir  = os.path.join(os.getcwd(), 'Data', 'Obs')
SimDir  = os.path.join(os.getcwd(), 'Data', 'Sim')
cmaqFil = os.path.join(SimDir, 'cctm', 'v4.d3.'+keyTime+'.conc.nc')
gridFil = os.path.join(SimDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')
stFil   = os.path.join(SimDir, 'st.csv')

AirQ_Area = {'EastAsia': ['濟州', '沖繩', '上海', '福州', '廈門']}

allVar = {'O3': ['O3','NO2','NMHC'],
          'PM': ['PM10','PM25','NO2','SO2']}


for area in AirQ_Area:
    stons = AirQ_Area[area]

    for cats in allVar:
        Vars = allVar[cats]

        for var in Vars:
            print('Processing  '+area+'  '+var)

            obs_PH = obs_readhr(ObsDir, RgTT, stons, var)
            sim_PH = sim_readhr(cmaqFil, gridFil, stFil, stons, var, RgTT)

            if (var == 'O3'):
               ND = 40.
               sim_PH_o3MB = sim_PH
            else:
               ND = 10.e-10
#           elif (var == 'NMHC'):
#              ND = 50.
#           elif (var == 'NO2') or (var == 'SO2'):
#              ND = 0.5
#           elif (var == 'PM25') or (var == 'PM10'):
#              ND = 5.
            obs_PH = obs_PH.where(obs_PH >= ND, -999.)
            sim_PH = sim_PH.where(obs_PH >= ND, -999.)

            obs_DA, sim_DA = simobs_hr2day(obs_PH, sim_PH, RgTT)


            data_dict = Evaluate(obs_PH, sim_PH, obs_DA, sim_DA, sim_PH_o3MB, stons, cats, var)


            outputfile = os.path.join(workDir, area, cats)
            try:
               os.makedirs(outputfile)
            except FileExistsError:
               pass

            csvfile = os.path.join(outputfile, YY + MM + '_' + var + '.csv')
            pd.DataFrame.from_dict(data=data_dict).to_csv(csvfile, encoding ='utf-8-sig')

print('finish')

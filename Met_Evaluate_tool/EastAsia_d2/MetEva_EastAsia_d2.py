import pandas as pd
import os, sys
import datetime, calendar
from Lib.simobs_readhr import sim_readhr, obs_readhr
from Lib.Evaluate import evaluate


try:
    keyTime = input("請輸入性能評估月份，ex:2019-01 : ")
    keyTime = datetime.datetime.strptime(keyTime,'%Y-%m').strftime('%Y-%m')
    YY, MM = keyTime.split('-')
    LM = calendar.monthrange(int(YY), int(MM))[1]
    start = keyTime + '-01-00'
    end   = keyTime + '-' + str(LM) + '-23'
except ValueError:
    print('！！！ 請確認輸入格式 ！！！')
    sys.exit()
if (YY != '2019'):
    print("！！！模擬年份請輸入'2019'！！！")
    sys.exit()

nowTT = pd.Timestamp.now().strftime('%Y-%m-%d-%H-%M-%S')

rootDir = os.getcwd()
workDir = os.path.join(rootDir, 'Data', 'Evaluate', nowTT+ '_For' +keyTime)
try:
   os.makedirs(workDir)
except FileExistsError:
   pass


domain = {'EastAsia'  : ['首爾', '東京', '北京']}
allVars = ['T2', 'WS', 'WD']

for area in domain:
   ssList = domain[area]
   Data_out = pd.DataFrame()

   for var in allVars:

      ObsDir  = os.path.join(rootDir, 'Data', 'Obs', var)
      SimDir  = os.path.join(rootDir, 'Data', 'Sim', var)

      obsfile = obs_readhr(ObsDir, start, end , var)
      simfile = sim_readhr(SimDir, start, end , var)


      eva = pd.DataFrame.from_dict(evaluate(obsfile, simfile, ssList, var))
      Data_out = pd.concat([Data_out, eva], axis=1)


   csvfile = os.path.join(workDir, YY + MM + '_' + area + '.csv')
   pd.DataFrame.from_dict(data=Data_out).to_csv(csvfile, encoding ='utf-8-sig')

print('finish')

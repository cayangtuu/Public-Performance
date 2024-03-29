import pandas as pd
import os, sys, calendar
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


nowTT = pd.Timestamp.now().strftime('%Y-%m-%d-%H-%M-%S')

##資料夾配置
workDir = os.path.join(os.getcwd(), 'Data', 'Evaluate', nowTT+ '_For' +keyTime)
ObsDir  = os.path.join(os.getcwd(), 'Data', 'Obs')
SimDir  = os.path.join(os.getcwd(), 'Data', 'Sim')
gridFil = os.path.join(SimDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')
stFil   = os.path.join(SimDir, 'st.csv')

cmaqFilNm = input("請輸入欲計算性能評估之模擬檔案名稱，ex:v1.2019-01.conc.nc : ")
cmaqFil = os.path.join(SimDir, 'cctm', cmaqFilNm)
if os.path.isfile(cmaqFil):
  pass
else:
  print("檔案不存在，請確認輸入檔案名稱是否正確 ! ! !")
  sys.exit()


AirQ_Area = {'North':   ['基隆', '汐止', '萬里', '新店', '土城', '板橋', '新莊', 
                         '菜寮', '林口', '淡水', '士林', '中山', '萬華', '古亭', 
                         '松山', '桃園', '大園', '觀音', '平鎮', '龍潭', '湖口',
                         '竹東', '新竹', '頭份', '苗栗', '三義', '豐原', '陽明', 
                         '宜蘭', '冬山', '富貴角'],
             'Central': ['竹東', '新竹', '頭份', '苗栗', '三義', '豐原', '沙鹿',
                         '大里', '忠明', '西屯', '彰化', '線西', '二林', '南投', 
                         '斗六', '崙背', '新港', '朴子', '台西', '嘉義', '竹山', '埔里'],
             'YunChia': ['彰化', '線西', '二林', '南投', '斗六', '崙背', '新港', 
                         '朴子', '台西', '嘉義', '新營', '善化', '安南', '台南', 
                         '美濃', '竹山', '埔里', '麥寮'],
             'South':   ['朴子', '嘉義', '新營', '善化', '安南', '台南', '美濃', 
                         '橋頭', '仁武', '大寮', '林園', '楠梓', '左營', '前金',
                         '前鎮', '小港', '屏東', '潮州', '恆春'],
             'East':    ['台東', '花蓮', '埔里', '關山']}

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
            obs_PH = obs_PH.where(obs_PH >= ND, -999.)
            sim_PH = sim_PH.where(obs_PH >= ND, -999.)

            obs_DA, sim_DA = simobs_hr2day(obs_PH, sim_PH, RgTT)


            data_dict = Evaluate(obs_PH, sim_PH, obs_DA, sim_DA, sim_PH_o3MB, stons, cats, var)


            outputfile = os.path.join(workDir, area, cats)
            try:
               os.makedirs(outputfile)
            except FileExistsError:
               pass

            csvfile = os.path.join(outputfile, YY + MM + '_' + var +'.csv')
            pd.DataFrame.from_dict(data=data_dict).to_csv(csvfile, encoding ='utf-8-sig')

print('finish')

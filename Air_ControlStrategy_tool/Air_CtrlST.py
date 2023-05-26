import pandas as pd
import os, sys, calendar
from Lib import getData, calData

###時間格式設定
try:
    keyTime = input("請輸入'計算改善計畫模擬濃度差值'月份，ex:2019-01 : ")
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
ObsFil = os.path.join(os.getcwd(), 'Data', 'Obs', '2019'+'temp_var'+'_PerHour.csv')
SimDir = os.path.join(os.getcwd(), 'Data', 'Sim')
gridFil = os.path.join(SimDir, 'mcip', 'GRIDCRO2D_Taiwan.nc')
stFil = os.path.join(SimDir, 'st.csv')                           #測站經緯度檔案名稱(有再加入)
OutDirNm = os.path.join(os.getcwd(), 'Data', 'Evaluate', nowTT+'_For'+keyTime)

###使用者自行輸入Before及After 檔案名稱
def FileExists(Fil):
   if os.path.isfile(Fil):
     pass
   else:
     print("檔案不存在，請確認輸入檔案名稱是否正確 ! ! !")
     sys.exit()
   return
BaseFilNm = input("請輸入Base之背景模擬檔案名稱，ex:v1.2019-01.conc.nc : ")
BaseFil = os.path.join(SimDir, 'Base', BaseFilNm)       #Before檔案名稱
FileExists(BaseFil)
CaseFilNm = input("請輸入Case之改善計畫模擬檔案名稱，ex:c-v1.2019-01.conc.nc : ")
CaseFil = os.path.join(SimDir, 'Case', CaseFilNm)       #After 檔案名稱
FileExists(CaseFil)

###各地區測站名稱
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

Vars = {'O3':['HourMax', 'ETHourMax'], \
        'NO2':['HourMax'], 'SO2':['HourMax'], \
        'PM10':['DayMean'], 'PM25':['DayMean']}


###主程式
GetData = getData.getData(BaseFil, CaseFil, gridFil, stFil, RgTT)
CalData = calData.calData(RgTT) 
for var in Vars:
    Bdf, Cdf = GetData.getBCVar(var)
    Obsdf = GetData.getObs(ObsFil, var)
    for area in AirQ_Area:
        ssList = AirQ_Area[area]
        BData = GetData.getStHr('Bdf', Bdf, ssList)
        CData = GetData.getStHr('Cdf', Cdf, ssList)
        ObsData = Obsdf.loc[:, ssList]

        for calType in Vars[var]:
            print(var, area, calType)
            mnObs = CalData.mainCal(ObsData, calType)
            mnBD = CalData.mainCal(BData, calType)
            mnCD = CalData.mainCal(CData, calType)

            DVb = CalData.calDVb(mnObs, calType)
            CMb, CMf, RRF = CalData.calRRF(mnBD, mnCD)
            DVf = CalData.calDVf(DVb, RRF)

            outData = pd.concat([DVb, CMb, CMf, RRF, DVf], axis=1)
            outData.columns = ['DVb', 'CMb', 'CMf', 'RRF', 'DVf']
#           print(outData)

            ###創建輸出檔案之資料夾
            OutDir = os.path.join(OutDirNm, area)
            try:
               os.makedirs(OutDir)
            except FileExistsError:
               pass
            OutFil = os.path.join(OutDir, keyTime+'__ControlStrategy__'+var+'_'+calType+'.csv')
            outData.to_csv(OutFil, encoding='utf-8-sig')

print('finish')

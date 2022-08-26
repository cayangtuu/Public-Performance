import pandas as pd 
import numpy as np
import datetime
import os

class getStData():
    def __init__(self, st, tt_list, vars):
        self.st = st
        self.vars = vars
        self.start = tt_list[0].strftime('%Y-%m-%d-%H')
        self.end = tt_list[1].strftime('%Y-%m-%d-%H')


    def getData(self, dataDir, ddtype):
        filenm = pd.date_range(start=self.start, end=self.end, freq='1d')\
                               .strftime('%Y-%m-%d')

        Data = pd.DataFrame()
        for var in self.vars:
           varDir = os.path.join(dataDir, var)
           mnData = pd.DataFrame()
           for nm in filenm:
              df = pd.read_csv(varDir + '/' + nm + '_' + var + '_' + ddtype +'.csv',
                               encoding= 'utf-8-sig',index_col=0)
              mnser = pd.Series(data=df[self.st], name=self.st)
              mnData = pd.concat([mnData, mnser], axis=0, sort=False)

           Data = pd.concat([Data, mnData], axis=1, sort=False)

        Data = Data.replace(-999., np.nan)
        mask = (Data.index >= self.start) & (Data.index <= self.end)
        Data = Data.loc[mask]
        Data.columns = self.vars

        return Data


    def stInfo(self, stFil):
        stData = pd.read_csv(stFil, encoding='utf-8-sig', index_col='ch_name')
        st_info = {'st': self.st, 'stID':stData.loc[self.st, 'stID'], 
                   'enName':stData.loc[self.st, 'en_name'],
                   'lat':stData.loc[self.st, 'lat'], 
                   'lon':stData.loc[self.st, 'lon']}
        return st_info


def getWind(stFil, SimDir, tt_list):

    stData = pd.read_csv(stFil, encoding='utf-8-sig')
    stInfo = {'st': stData['ch_name'].to_list(),
              'lat': stData['lat'].to_numpy(),
              'lon': stData['lon'].to_numpy()}


    filenm = pd.date_range(start=tt_list[0]-pd.Timedelta(days=1), 
                           end=tt_list[1], freq='1d').strftime('%Y-%m-%d')

    WindData = {}
    for var in ['WS', 'WD']:
        WDir = os.path.join(SimDir, var)
        Data = pd.DataFrame()
        for nm in filenm:
            df = pd.read_csv(WDir + '/' + nm + '_' + var + '_sim.csv',
                             encoding= 'utf-8-sig',index_col=0)
            stData = pd.DataFrame()
            for st in stInfo['st']:
                stdf = pd.Series(df[st], name=st, index=df.index)
                stData = pd.concat([stData, stdf], axis=1, sort=False)
            Data = pd.concat([Data, stData], axis=0, sort=False)

        Data = Data.replace(-999., np.nan)
        Data.index = [datetime.datetime.strptime(tt, '%Y-%m-%d-%H') \
                      + pd.Timedelta(hours=8) for tt in Data.index]    #將UTC更改為LTS
        mask = (Data.index >= tt_list[0]) & (Data.index <= tt_list[1]) #並取一個月的資料
        Data = Data.loc[mask]

        WindData[var] = Data

    return WindData, stInfo


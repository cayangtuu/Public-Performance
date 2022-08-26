import pandas as pd 
import numpy as np
import datetime

def getEPA(st, tt_List, vars, obsDir):
    Data = pd.DataFrame()
    for var in vars:
       df = pd.read_csv(obsDir + '/' + str(tt_List[0])[:4] + var + '_PerHour.csv',
                        encoding= 'utf-8-sig', index_col=0)
       varser = pd.Series(data=df[st], name=st, index=df.index)
       Data = pd.concat([Data, varser], axis=1, sort=False)
    Data = Data.replace(-999, np.nan)
    Data.columns = vars
    Data.index = [datetime.datetime.strptime(tt, '%Y-%m-%d-%H') for tt in Data.index]

    print(Data)
    return Data


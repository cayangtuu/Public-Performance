import pandas as pd
import datetime

def obs_readhr(ObsDir, start, end, var):

    df = pd.DataFrame()
    filenm = pd.date_range(start=start, end=end, freq='1d').strftime('%Y-%m-%d')

    for nm in filenm:
        tmpData = pd.read_csv(ObsDir + '/' + str(nm) + '_' + var + '_obs.csv',
                              encoding = 'utf-8-sig', index_col = 0)
        df = pd.concat([df, tmpData], axis=0)
 
    df.index.name = 'time'

    return df

def sim_readhr(SimDir, start, end, var):

    df = pd.DataFrame()
    filenm = pd.date_range(start=start, end=end, freq='1d').strftime('%Y-%m-%d')

    for nm in filenm:
        tmpData = pd.read_csv(SimDir + '/' + str(nm) + '_' + var + '_sim.csv',
                              encoding = 'utf-8-sig', index_col = 0)
        df = pd.concat([df, tmpData], axis=0)

    df.index.name = 'time'

    return df

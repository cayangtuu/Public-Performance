import pandas as pd
import datetime, chardet
from pathlib import Path

def obs_readhr(ObsDir, start, end, var):

    df = pd.DataFrame()
    filenm = pd.date_range(start=start, end=end, freq='1d').strftime('%Y-%m-%d')

    for nm in filenm:
        Fil = ObsDir + '/' + str(nm) + '_' + var + '_obs.csv'
        encoding = chardet.detect(Path(Fil).read_bytes()).get("encoding")
        tmpData = pd.read_csv(Fil, encoding = encoding, index_col = 0)
        df = pd.concat([df, tmpData], axis=0)
 
    df.index.name = 'time'

    return df

def sim_readhr(SimDir, start, end, var):

    df = pd.DataFrame()
    filenm = pd.date_range(start=start, end=end, freq='1d').strftime('%Y-%m-%d')

    for nm in filenm:
        Fil = SimDir + '/' + str(nm) + '_' + var + '_sim.csv'
        encoding = chardet.detect(Path(Fil).read_bytes()).get("encoding")
        tmpData = pd.read_csv(Fil, encoding = encoding, index_col = 0)
        df = pd.concat([df, tmpData], axis=0)

    df.index.name = 'time'

    return df

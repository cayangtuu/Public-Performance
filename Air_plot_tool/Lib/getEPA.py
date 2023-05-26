import pandas as pd 
import numpy as np
import datetime, chardet
from pathlib import Path

def getEPA(st, tt_List, vars, obsDir):
    Data = pd.DataFrame()
    for var in vars:
       Fil = obsDir + '/' + str(tt_List[0])[:4] + var + '_PerHour.csv'
       encoding = chardet.detect(Path(Fil).read_bytes()).get("encoding")
       df = pd.read_csv(Fil, encoding=encoding, index_col=0)
       varser = pd.Series(data=df[st], name=st, index=df.index)
       Data = pd.concat([Data, varser], axis=1, sort=False)
    Data = Data.replace(-999, np.nan)
    Data.columns = vars
    Data.index = [datetime.datetime.strptime(tt, '%Y-%m-%d-%H') for tt in Data.index]

    return Data


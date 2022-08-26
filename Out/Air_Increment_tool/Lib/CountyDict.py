import pandas as pd
import numpy as np
import xarray as xr
import os


def CtyDict(LatLon, SimDir):
   CtyDir = os.path.join(SimDir, 'CountyDict')
   DictNm = {'01':'台北市', '31':'新北市', '32':'桃園市', '17':'台中市', '36':'台中市', 
             '21':'台南市', '41':'台南市', '02':'高雄市', '42':'高雄市', '11':'基隆市', 
             '12':'新竹市', '22':'嘉義市', '33':'新竹縣', '34':'宜蘭縣', '35':'苗栗縣',
             '37':'彰化縣', '38':'南投縣', '39':'雲林縣', '40':'嘉義縣', '43':'屏東縣', 
             '44':'澎湖縣', '45':'花蓮縣', '46':'台東縣', '50':'金門縣', '51':'連江縣'} 

   Data = pd.read_csv(CtyDir+'/TEDS11_AREA_WGS84.sdf', header=None, dtype=str, encoding='utf-8-sig')
   Data.columns = ['Index']
   Data['Lon'] = Data['Index'].map(lambda x:float(x[:9]))
   Data['Lat'] = Data['Index'].map(lambda x:float(x[9:17]))
   Data['Dict'] = Data['Index'].map(lambda x:x[24:28])
   Data = Data.drop(columns=['Index'])

   CtDict = np.empty([len(LatLon[0]), len(LatLon[0])], dtype=np.object)


   for ll in range(len(Data)):
      dis = np.sqrt((LatLon[0]-Data['Lat'][ll])**2 + \
                    (LatLon[1]-Data['Lon'][ll])**2).values    #尋找最接近的網格點
      ii, jj = divmod(np.argmin(dis), dis.shape[1])           #所在網格的位置
      CtDict[ii][jj] = DictNm[Data['Dict'][ll][:2]]           #建置每個網格所屬縣市
   print(CtDict)
   pd.DataFrame(CtDict).to_csv(CtyDir+'/CountyDict.csv', index=False, header=False, encoding='utf-8-sig')

   return np.array(CtyDict)




def CtyData(gridFil, stFil, CtyDict, CalDF): 
   def stData(LatLon, stLatLon):
      dis = np.sqrt((LatLon[0]-stLatLon[0])**2 + \
                    (LatLon[1]-stLatLon[1])**2)                #尋找最接近的網格點
      ii, jj = divmod(np.argmin(dis), dis.shape[1])            #所在網格的位置

      return ii, jj


   DictNm = ['台北市', '新北市', '桃園市', '台中市', '台南市', '高雄市', '基隆市', 
             '新竹市', '嘉義市', '新竹縣', '苗栗縣', '彰化縣', '南投縣', 
             '雲林縣', '嘉義縣', '屏東縣', '宜蘭縣', '花蓮縣', '台東縣'] 

   Grid = xr.open_dataset(gridFil).sel(TSTEP=0, LAY=0)
   LWMASK = Grid.LWMASK.values
   LAT = Grid.LAT.values
   LON = Grid.LON.values

   #縣市最大值
   Data = []
   for cty in DictNm:
      Ix, Iy = np.where((CtyDict==cty) & (LWMASK==1))
      vl = np.argmax([CalDF['Inc'][Ix[nm]][Iy[nm]] for nm in range(len(Ix))])
      ix, iy = Ix[vl], Iy[vl]
      Data.append([cty, LON[ix][iy], LAT[ix][iy], \
                   CalDF['Inc'][ix][iy], CalDF['Before'][ix][iy], CalDF['After'][ix][iy]])

   #測站數值
   if os.path.isfile(stFil):
     stInf = pd.read_csv(stFil, index_col=0, encoding='big5')
     for st in stInf.index:
        ix, iy = stData([LAT, LON], [stInf.loc[st,'緯度'], stInf.loc[st,'經度']])
        Data.append([st, round(stInf.loc[st,'經度'], 4), round(stInf.loc[st,'緯度'], 5), \
                     CalDF['Inc'][ix][iy], CalDF['Before'][ix][iy], CalDF['After'][ix][iy]])
   else:
     pass

   return Data

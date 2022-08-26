import pandas as pd
import xarray as xr
from monetio.models import cmaq
from monet.util import tools
 
def sim_readhr(cmaqFil, gridFil, stFil, ssList, var, RgTT):
 
   def cmaqData(cmaqFil, gridFil):
      # open the dataset using xarray
      dset = xr.open_dataset(cmaqFil)


      # get the grid information
      grid = cmaq.grid_from_dataset(dset, earth_radius=6370000)
      area_def = cmaq.get_ioapi_pyresample_area_def(dset, grid)

      # assign attributes for dataset and all DataArrays
      dset = dset.assign_attrs({'proj4_srs': grid})
      for i in dset.variables:
          dset[i] = dset[i].assign_attrs({'proj4_srs': grid})
          for j in dset[i].attrs:
              dset[i].attrs[j] = dset[i].attrs[j].strip()

      # get the times
      dset = cmaq._get_times(dset, drop_duplicates=False)

      # get the lat lon
      dset = cmaq._get_latlon(dset, area_def)

      # rename dimensions
      dset = dset.rename({'COL': 'x', 'ROW': 'y', 'LAY': 'z'})

      # convert all gas species to ppbv
      for i in dset.variables:
          if 'units' in dset[i].attrs:
             if 'ppmV' in dset[i].attrs['units']:
                dset[i] *= 1000.
                dset[i].attrs['units'] = 'ppbV'

      # convert 'micrograms to \mu g'
      for i in dset.variables:
          if 'units' in dset[i].attrs:
             if 'micrograms' in dset[i].attrs['units']:
                dset[i].attrs['units'] = '$\mu g m^{-3}$'


      CMAQData = dset.sel(z=0)
      if 'VOC' in CMAQData:
         CMAQData = CMAQData.rename({'VOC': 'NMHC'})  ##更改物種名稱
      if 'PM25_TOT' in CMAQData:
         CMAQData = CMAQData.rename({'PM25_TOT': 'PM25'})  ##更改物種名稱


      '''使用MCIP的LAT及LON替換掉CMAQData中的'''
      grid = xr.open_dataset(gridFil).sel(TSTEP=0, LAY=0)
      tmp = CMAQData.update({'latitude': grid.LAT,
                             'longitude': grid.LON})
      return CMAQData


   def stInfo(stFil, st):
#     stinfo = pd.read_csv(stFil, encoding ='utf-8-sig')
      stinfo = pd.read_csv(stFil, encoding ='big5')
      stData = stinfo.iloc[:, 2:]
      stData = stData.set_index('ch_name', drop=True)
      lat = stData.loc[st, 'lat']
      lon = stData.loc[st, 'lon']

      return lat, lon
    

   CMAQData = cmaqData(cmaqFil=cmaqFil, gridFil=gridFil)

   df = pd.DataFrame()
   for st in ssList:
       lat, lon = stInfo(stFil, st)
       xx, yy = CMAQData.monet.nearest_ij(lat=lat, lon=lon)
       cmd = 'CMAQData.' + var
       tmpData = eval(cmd)
       tmpData = tmpData.sel(x=xx, y=yy).to_dataframe()
       df = pd.concat([df, tmpData], axis=1)
   df.columns = ssList
   df.index = df.index + pd.Timedelta(hours=8)  ###UTC -> Local Time
   df.index.name = 'time'

   mask = (df.index >= RgTT[0]) & (df.index <= RgTT[1])
   df = df.loc[mask]

   return df

def obs_readhr(ObsDir, RgTT, ssList, var):
   EPAData = pd.read_csv(ObsDir + '/' + RgTT[0][:4] + var +'_PerHour.csv',
                         encoding='utf-8-sig', index_col=0)

   mask = (EPAData.index >= RgTT[0]) & (EPAData.index <= RgTT[1])
   EPAData = EPAData.loc[mask]

   df = pd.DataFrame()
   for st in ssList:
      stser = pd.Series(data=EPAData[st], name=st, index=EPAData.index)
      df = pd.concat([df, stser], axis=1)
   df.index.name = 'time'

   return df

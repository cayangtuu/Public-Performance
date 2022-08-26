import pandas as pd
import xarray as xr
from monetio.models import cmaq

class getData():
   def __init__(self, BaseFil, CaseFil, gridFil, RgTT):
      self.gridFil = gridFil
      self.RgTT = RgTT
      self.bset = self._open_dataset(BaseFil) 
      self.cset = self._open_dataset(CaseFil) 


   def _open_dataset(self, cmaqFil):
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
      dset.coords['time'] = dset.coords['time'] + pd.Timedelta('8h')

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
      if 'PM25_TOT' in CMAQData:
         CMAQData = CMAQData.rename({'PM25_TOT': 'PM25'})  ##更改物種名稱


      '''使用MCIP的LAT及LON替換掉CMAQData中的'''
      grid = xr.open_dataset(self.gridFil).sel(TSTEP=0, LAY=0)
      tmp = CMAQData.update({'latitude': grid.LAT,
                             'longitude': grid.LON})
      return CMAQData


   def LatLon(self):
       lat = eval('self.bset.' + 'latitude')
       lon = eval('self.bset.' + 'longitude')

       return lat, lon


   def EvyLLVl(self, var):
      Bdf = eval('self.bset.' + var)
      Cdf = eval('self.cset.' + var)
      Indf = Cdf - Bdf
      Indf = Indf.sel(time=slice(self.RgTT[0], self.RgTT[1]))
#     print(Indf)

      return Indf


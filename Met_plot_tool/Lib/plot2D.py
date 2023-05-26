import os
import warnings
import time as systime
import pandas as pd
import numpy as np
import monet
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from wrf import getvar, ALL_TIMES
from netCDF4 import Dataset

class plot2D():
    def __init__(self, wrfDir, latlon, stInfo, stWind, nowTT):
        self.U10, self.V10 = self._open_dataset(wrfDir)
        self.U10.attrs['units'] = 'm/s'  #更改單位形式 轉成metpy才不會出錯
        self.V10.attrs['units'] = 'm/s'  #更改單位形式 轉成metpy才不會出錯
        self.latlon = latlon
        self.stInfo = stInfo
        self.nowTT = nowTT
        self.stU, self.stV = self._wsd2uv(stWind)

    def _open_dataset(self, wrfDir):
        wrfFil = [Dataset(os.path.join(wrfDir, fnm)) for fnm in sorted(os.listdir(wrfDir))]
        u_join = getvar(wrfFil, "U10", timeidx=ALL_TIMES, method="cat") # 合併檔案
        v_join = getvar(wrfFil, "V10", timeidx=ALL_TIMES, method="cat")
        u_join = u_join.assign_coords(Time = u_join.Time + pd.Timedelta(hours=8)) # 由 UTC -> LT
        v_join = v_join.assign_coords(Time = v_join.Time + pd.Timedelta(hours=8)) # 由 UTC -> LT
        return u_join, v_join


    def _month_data(self):
        warnings.filterwarnings("ignore", category=FutureWarning)
        self.um = self.U10.resample(Time = '1M').mean()
        self.vm = self.V10.resample(Time = '1M').mean()
        return self.um, self.vm

    def _wsd2uv(self, stWind):
        WindU = pd.DataFrame()
        WindV = pd.DataFrame()
        m_wd = 270 - stWind['WD']
        p_wd = m_wd /180 *np.pi
        WindU = stWind['WS'] * np.cos(p_wd)
        WindV = stWind['WS'] * np.sin(p_wd)
        return WindU, WindV


    def plot2D(self, time, LstTime, type):
        if type == 'hour':
           uu = self.U10.isel(Time = time)
           vv = self.V10.isel(Time = time)
           stu = self.stU.loc[LstTime].to_numpy()
           stv = self.stV.loc[LstTime].to_numpy()
        elif type == 'month':
           uu = self.um.isel(Time = time)
           vv = self.vm.isel(Time = time)
           stu = self.stU.mean().to_numpy()
           stv = self.stV.mean().to_numpy()
#       print(uu.Time)
        proj = ccrs.LambertConformal(central_longitude=121,
                                     central_latitude=23.99,
                                     standard_parallels=(10,40))
        fig, ax = monet.plots.draw_map(crs=proj,
                                       figsize=(10, 11),
                                       extent=self.latlon,
                                       states=True, resolution='10m', return_fig=True)


        ####add wind arrow
        skip = (slice(None, None, 8), slice(None, None, 8))
        arr = ax.quiver(uu.XLONG.values[skip], uu.XLAT.values[skip],
                        uu.values[skip], vv.values[skip], transform=ccrs.PlateCarree(),
                        color='dimgrey', scale = 200, )
        ax.quiverkey(arr, 0.8, -0.02, 10, r'10m/s', labelpos='E',
                     coordinates='axes', fontproperties={'size':15})

        ####add station wind arrow
        ax.plot(self.stInfo['lon'], self.stInfo['lat'], 'k.',
                transform=ccrs.PlateCarree(), )
        ax.barbs(self.stInfo['lon'], self.stInfo['lat'], stu, stv, 
                 transform=ccrs.PlateCarree(), color='k', 
                 fill_empty=True, sizes={'emptybarb':0.1,'height':0.6})


        ###Print Time
        ts = pd.to_datetime(uu.Time.values)
        if type == 'hour':
           stime = ts.strftime('%Y/%m/%d %H')
        elif type == 'month':
           stime = ts.strftime('%Y/%m')


        if type == 'hour':
           ax.set_title('Wind Field at 10m \n' + stime + '(LST)')
        elif type == 'month':
           ax.set_title('Wind Field at 10m \n' + stime + ' Averaged')


        outDir = os.path.join('Output', 'output_2D', 
                              self.nowTT+ '_For' +ts.strftime('%Y%m'), type)
        try:
            os.makedirs(outDir)
        except FileExistsError:
            pass

        if type == 'hour':
           picFil = os.path.join(outDir,ts.strftime('%Y%m%d%H'))
        elif type == 'month':
           picFil = os.path.join(outDir, ts.strftime('%Y%m'))

        plt.savefig(picFil, bbox_inches='tight', pad_inches=0.3)
        plt.close()

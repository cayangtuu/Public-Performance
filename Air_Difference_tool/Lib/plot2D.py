import os, monet
import pandas as pd
import numpy as np
import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import cartopy.crs as ccrs
from matplotlib.font_manager import FontProperties
from pandas.plotting import register_matplotlib_converters

zhfont = FontProperties(fname='./Lib/NotoSansCJK-Regular.ttc', size=20)
register_matplotlib_converters()

class PLOT():
    def __init__(self, var, latlon, keyTime, gridFil, plotDir):
       self.Index = self.Index(var)
       self.var = var
       self.latlon = latlon
       self.keyTime = keyTime
       self.plotDir = plotDir
       self.LWMASK = xr.open_dataset(gridFil).sel(TSTEP=0, LAY=0).LWMASK


    def _maxmin(self, Data):
       dMM = Data.where((Data.lon >= self.latlon[0]) & (Data.lon <= self.latlon[1]) & \
                        (Data.lat >= self.latlon[2]) & (Data.lat <= self.latlon[3]) & \
                        (Data.LW == 1))

       if Data.name in ['PM25', 'PM10']:
         unit = r'ug/m^3'
       elif Data.name in ['NO2', 'SO2', 'O3']:
         unit = r'ppbV'

       TEXT = 'Land max, min = {:.2f}, {:.2f} ({})'.format(dMM.max().values, dMM.min().values, unit)

       return TEXT


    def Index(self, var):
#      bounds = [0.1, 0.3, 0.5, 0.8, 1, 1.5, 2]
       bounds = [0.01, 0.1, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8, 2]
       norm = colors.BoundaryNorm(boundaries=bounds, ncolors=11)

       colorsmap = ['deepskyblue','forestgreen','yellowgreen','gold','orange','red']
       cmap = colors.LinearSegmentedColormap.from_list('aaa', colorsmap) 
       cmap.set_over('purple')
       cmap.set_under('white')

       if var == 'SO2':
         title = r'SO$_{2}$ (ppbV)'
       elif var == 'NO2':
         title = r'NO$_{2}$ (ppbV)'
       elif var == 'PM25':
         title = r'PM$_{2.5}$ ($\mu$g/m$^3$)'
       elif var == 'PM10':
         title = r'PM$_{10}$ ($\mu$g/m$^3$)'
       elif var == 'O3':
         title = r'O$_{3}$ (ppbV)'

       return {'norm':norm, 'bounds':bounds, 'cmap':cmap, 'title':title}


    def plot2D(self, DF, lat, lon, Name):
       Data = xr.DataArray(data=DF, dims=["x", "y"],
                           coords=dict(lon=(["x", "y"], lon),
                                       lat=(["x", "y"], lat),
                                       LW =(["x", "y"], self.LWMASK)),
                           name=self.var)

       proj = ccrs.LambertConformal(central_longitude=120,
                                    central_latitude=25,
                                    standard_parallels=(10,40))

       fig, ax = monet.plots.draw_map(crs=proj, figsize=(10, 11),
                                      extent=self.latlon, states=True, 
                                      resolution='10m', return_fig=True)

       pax = Data.plot(x='lon', y='lat', ax=ax, cmap=self.Index['cmap'], \
                       norm=self.Index['norm'], extend='both', add_colorbar=False, \
                       transform=ccrs.PlateCarree(), infer_intervals=True)

       cax = fig.add_axes([ax.get_position().x1+0.01, \
                           ax.get_position().y0,0.02, \
                           ax.get_position().height])

       cbar = plt.colorbar(pax, cax=cax, ticks=self.Index['bounds'], \
                           extend='both', fraction=0.046, pad=0.04)
       cbar.ax.set_yticklabels(self.Index['bounds'], fontsize=16, weight='bold')

       ax.set_title(self.keyTime+' '+self.Index['title']+'\n'+Name[0], fontproperties=zhfont)
       ax.annotate(self._maxmin(Data), xy=(0,-25), xycoords='axes points', fontsize=15)

       picFil = os.path.join(self.plotDir, self.keyTime+'_'+self.var+'_'+Name[1]+'.png')
       plt.savefig(picFil, bbox_inches='tight', pad_inches=0.1)
#      plt.close()

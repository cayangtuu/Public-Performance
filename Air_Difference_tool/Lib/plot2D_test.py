import os, monet, math
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
       self.Title = self.Text(var)
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


    def Index(self, Data):

       DataMin = round(math.floor(Data.min()*100)/100., 2)
       DataMax = round(math.ceil(Data.max()*100)/100., 2)
       bounds = np.linspace(DataMin, DataMax, 200)
       norm = colors.BoundaryNorm(boundaries=bounds, ncolors=200)

       if (DataMin > 0):
          ticks = np.linspace(DataMin, DataMax, 9)
          colorlist = ['gold','red','purple']
          cmap = colors.LinearSegmentedColormap.from_list('LG', colorlist)
       elif (DataMin < 0):
          ticks = np.linspace(DataMin, DataMax, 9)
          colorlist = ['forestgreen','deepskyblue','darkblue']
          cmap = colors.LinearSegmentedColormap.from_list('LS', colorlist)

       return {'norm':norm, 'ticks':ticks, 'cmap':cmap, }



    def Text(self, var):
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

       return title



    def plot2D(self, DF, lat, lon, PerforCN):
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

       Index = self.Index(Data)
       pax = Data.plot(x='lon', y='lat', ax=ax, cmap=Index['cmap'],
                       norm=Index['norm'], add_colorbar=False, 
                       transform=ccrs.PlateCarree(), infer_intervals=True)

       cax = fig.add_axes([ax.get_position().x1+0.01, \
                           ax.get_position().y0,0.02, \
                           ax.get_position().height])

       cbar = plt.colorbar(pax, cax=cax, ticks=Index['ticks'], fraction=0.046, pad=0.04)
       cbar.ax.set_yticklabels(Index['ticks'], fontsize=16, weight='bold')

       ax.set_title(self.keyTime+' '+self.Title+'\n'+PerforCN, fontproperties=zhfont)
       ax.annotate(self._maxmin(Data), xy=(0,-25), xycoords='axes points', fontsize=15)

       picFil = os.path.join(self.plotDir, self.keyTime+'_'+self.var+PerforCN+'.png')
       plt.savefig(picFil, bbox_inches='tight', pad_inches=0.1)
#      plt.close()
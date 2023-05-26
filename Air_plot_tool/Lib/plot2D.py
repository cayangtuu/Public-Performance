import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import monet
import cartopy.crs as ccrs
import time as systime

class plot2D():
    def __init__(self,cmaqData, latlon, nowTT):
        self.cmaqData = cmaqData
        self.cmaqData['WSPD10'].attrs['units'] = 'm/s'  #更改單位形式 轉成metpy才不會出錯
        self.latlon = latlon
        self.nowTT = nowTT


    def _maxminText(self, dxr):
        dmaxmin = dxr.where((dxr.longitude >= self.latlon[0]) & (dxr.longitude <= self.latlon[1]) & \
                            (dxr.latitude  >= self.latlon[2]) & (dxr.latitude  <= self.latlon[3]))
        if dxr.name in ['PM25', 'PM10']:
            spctitle = r'$\mu$g/m$^3$'
        elif dxr.name in ['NO2', 'SO2', 'O3']:
            spctitle = r'ppbV'
        elif dxr.name in ['NMHC']:
            spctitle = r'ppbC'
        ss = 'max, min = {:.2f}, {:.2f} ({})'.format(dmaxmin.max().values,dmaxmin.min().values,spctitle)
        return ss

    def getUV(self,time):
        from metpy.calc import wind_components
        ws = self.cmaqData['WSPD10'].isel(time=time).metpy
        wd = self.cmaqData['WDIR10'].isel(time=time).metpy
        return wind_components(ws.unit_array, wd.unit_array)

    def plot2D(self,spc,time,type):
        cmd = 'self.cmaqData.' + spc
        dxr = eval(cmd)
        dxr = dxr.isel(time=time)

        proj = ccrs.LambertConformal(central_longitude=120,
                                     central_latitude=25,
                                     standard_parallels=(10, 40))

        fig, ax = monet.plots.draw_map(crs=proj,
                                       figsize=(10, 11),
                                       extent=self.latlon,
                                       states=True, resolution='10m', return_fig=True)


        vmax = {'SO2':30, 'NO2':60, 'O3':120, 'PM25':[40,120], 'NMHC':1200, 'PM10':160}
        vstep = {'SO2':2.5, 'NO2':5, 'O3':10, 'PM25':[5,10], 'NMHC':100, 'PM10':10}

        if (spc=='PM25'):
           bounds = np.hstack([np.arange(0, vmax[spc][0]+vstep[spc][0], vstep[spc][0]),\
                    np.arange(vmax[spc][0]+vstep[spc][1], vmax[spc][1]+vstep[spc][1], vstep[spc][1])])
           norm = colors.BoundaryNorm(boundaries=bounds, \
                  ncolors=(vmax[spc][0]/vstep[spc][0]+(vmax[spc][1]-vmax[spc][0])/vstep[spc][1]))
        else:
           bounds = np.arange(0, vmax[spc]+vstep[spc], vstep[spc])
           norm = colors.BoundaryNorm(boundaries=bounds, ncolors=vmax[spc]/vstep[spc])

        cmap = colors.LinearSegmentedColormap.from_list('aaa',\
               ['white','deepskyblue','forestgreen','yellowgreen','gold','orange','red','purple'])
        cmap.set_over('indigo')
        pax = dxr.plot(x='longitude', y='latitude', ax=ax,
                       cmap=cmap, norm=norm, add_colorbar=False,
                       transform=ccrs.PlateCarree(), infer_intervals=True)


        cax = fig.add_axes([ax.get_position().x1+0.01,\
                            ax.get_position().y0,0.02,
                            ax.get_position().height])


        cbar = plt.colorbar(pax, cax=cax, fraction=0.046, pad=0.04, extend='max', ticks=bounds)
        cbar.ax.set_yticklabels(bounds, fontsize=16, weight='bold')


        ###Print Time
        ts = pd.to_datetime(str(dxr.time.values))
        if type == 'hour':
           stime = ts.strftime('%Y/%m/%d %H')
        elif type == 'day':
           stime = ts.strftime('%Y/%m/%d')
        elif type == 'month':
           stime = ts.strftime('%Y/%m')


        if spc == 'SO2':
            spctitle = r'SO$_{2}$ (ppbV)'
        elif spc == 'NO2':
            spctitle = r'NO$_{2}$ (ppbV)'
        elif spc == 'NOX':
            spctitle = r'NO$_{x}$ (ppbV)'
        elif spc == 'CO':
            spctitle = r'CO (ppbV)'
        elif spc == 'PM25':
            spctitle = r'PM$_{2.5}$ ($\mu$g/m$^3$)'
        elif spc == 'PM10':
            spctitle = r'PM$_{10}$ ($\mu$g/m$^3$)'
        elif spc == 'O3':
            spctitle = r'O$_{3}$ (ppbV)'
        elif spc == 'NMHC':
            spctitle = r'NMHC (ppbC)'
        else:
            spctitle = spc
 
        if type == 'hour':
           ax.set_title(spctitle+' '+stime+'(LST)')
        else:
           ax.set_title(spctitle+' '+stime)

        ax.annotate(self._maxminText(dxr),xy=(0,-25),xycoords='axes points',fontsize=15)



        outDir = os.path.join('Output', 'output_2D', self.nowTT+ '_For' +ts.strftime('%Y-%m'), spc, type)
        try:
            os.makedirs(outDir)
        except FileExistsError:
            pass

        if type == 'hour':
           picFil = os.path.join(outDir,ts.strftime('%Y%m%d%H')+'_'+spc)
        elif type == 'day':
           picFil = os.path.join(outDir, ts.strftime('%Y%m%d')+'_'+spc)
        elif type == 'month':
           picFil = os.path.join(outDir, ts.strftime('%Y%m')+'_'+spc)

        plt.savefig(picFil, bbox_inches='tight', pad_inches=0.1)
        plt.close()

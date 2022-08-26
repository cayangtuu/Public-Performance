import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import monet
import cartopy.crs as ccrs
import time as systime

class plot2D():
    def __init__(self,cmaqData, latlon):
        self.cmaqData = cmaqData
        self.cmaqData['WSPD10'].attrs['units'] = 'm/s'  #更改單位形式 轉成metpy才不會出錯
        self.latlon = latlon


    def _maxminText(self,dxr):
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
                                     standard_parallels=(10,40))
        fig, ax = monet.plots.draw_map(crs=proj,
                                       figsize=(10, 11),
                                       extent=self.latlon,
                                       states=True, resolution='10m', return_fig=True)

        vmax = {'SO2':20, 'NO2':80, 'O3':120, 'PM25':140, 'NMHC':800, 'PM10':200}
        vstep = {'SO2':9, 'NO2':9, 'O3':9, 'PM25':9, 'NMHC':9, 'PM10':9}

        bounds = np.linspace(0, vmax[spc], 200)
        norm = colors.BoundaryNorm(boundaries=bounds, ncolors=200)

        cmap = colors.LinearSegmentedColormap.from_list('aaa',['white','deepskyblue','forestgreen','gold','red','purple'])
        pax = dxr.plot(x='longitude', y='latitude', ax=ax,
                       cmap=cmap,norm=norm,add_colorbar=False,
                       transform=ccrs.PlateCarree(), infer_intervals=True)

        cax = fig.add_axes([ax.get_position().x1+0.01,ax.get_position().y0,0.02,ax.get_position().height])


        cbar = plt.colorbar(pax, cax=cax, ticks=np.linspace(0, vmax[spc], vstep[spc]),
                            fraction=0.046, pad=0.04)
        cbar.ax.set_yticklabels(np.linspace(0, vmax[spc], vstep[spc]),
                                fontsize=16, weight='bold')
        ####add wind arrow
        #if type == 'hour':
        #   u,v = self.getUV(time)
        #   skip = (slice(None, None, 4), slice(None, None, 4))
        #   arr = ax.quiver(dxr.longitude.values[skip],dxr.latitude.values[skip],
        #                   u.m[skip],v.m[skip], transform=ccrs.PlateCarree(),
        #                   color='dimgrey', scale = 200, )
        #   ax.quiverkey(arr, 0.8, -0.03, 10, r'10ms$^{-1}$', labelpos='E',
        #                   coordinates='axes',fontproperties={'size':15})

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
           ax.set_title('WRF-CMAQ Simulation Ground \n'+spctitle+' '+stime+'(LT)')
        else:
           ax.set_title('WRF-CMAQ Simulation Ground \n'+spctitle+' '+stime)

        ax.annotate(self._maxminText(dxr),xy=(0,-25),xycoords='axes points',fontsize=15)

        # if True:   ###True(不要印出來)
        if False:  ###False(將檔案印出來)
            plt.show()
            systime.sleep(2)
        else:
            outDir = os.path.join('Output', 'output_2D', ts.strftime('%Y-%m'), spc, type)
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

            plt.savefig(picFil, bbox_inches='tight',
                        pad_inches=0.1)
            plt.close()

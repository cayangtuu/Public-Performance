import datetime as dt
import os
import time as systime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
from matplotlib.font_manager import FontProperties
from pandas.plotting import register_matplotlib_converters

zhfont = FontProperties(fname='./Lib/NotoSansCJK-Regular.ttc', size=20)
register_matplotlib_converters()


class plot_SimObs():
    def __init__(self, stInfo, obs, sim, dateRange):
        self.obsDf = obs
        self.simDf = sim
        self.stName = stInfo['st']
        self.area = stInfo['area']
        self.dateRange = dateRange


    def Ptimeseries(self, var):
        fig, ax = plt.subplots(figsize=(10, 5), constrained_layout = True)

        ax.set_xlim([np.datetime64(tt) for tt in self.dateRange])
        ax.scatter(self.obsDf[var].index, self.obsDf[var],
                   label='Obs', color='k', s=20)
        ax.plot(self.simDf.index, self.simDf[var],
                label='Sim', color='k', linestyle='-')

        ax.set_ylim([self.Clmin, self.Clmax])
        plt.yticks(range(int(self.Clmin), int(self.Clmax)+1, 5))

        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=15)
        ax.legend(fontsize=13, ncol=2, bbox_to_anchor=(1, 1), loc='lower right')
        ax.set_xlabel(u'日期', fontproperties=zhfont)
        ax.set_title(self.stName + '_' + self.spctitle + '_' + self.dateRange[0].strftime('%Y/%m'),
                     fontproperties=zhfont)
        return


    def Pscatter(self, var):

        fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)

        ax.set_xlim([self.Clmin, self.Clmax])
        ax.set_ylim([self.Clmin, self.Clmax])
        plt.xticks(range(int(self.Clmin), int(self.Clmax)+1, 5))
        plt.yticks(range(int(self.Clmin), int(self.Clmax)+1, 5))
        ax.plot(np.arange(self.Clmin, 3*self.Clmax),
                np.arange(self.Clmin, 3*self.Clmax), color='k', linestyle='-')

        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel(u'觀測', fontsize='medium', fontproperties=zhfont)
        ax.set_ylabel(u'模擬', fontsize='medium', fontproperties=zhfont)
        ax.scatter(self.obsDf[var], self.simDf[var], label=var, color='k', s=20)
        ax.set_title(self.stName + '_' + self.spctitle + '_' + self.dateRange[0].strftime('%Y/%m'),
                     fontproperties=zhfont)
        return


    def wsd2uv(self, winds):

        WindUV = pd.DataFrame()
        for time in winds.index:
           m_wd = 270 - winds.loc[time, 'WD']
           p_wd = m_wd /180 *np.pi
           WindUV.loc[time, 'u'] = winds.loc[time, 'WS'] * np.cos(p_wd)
           WindUV.loc[time, 'v'] = winds.loc[time, 'WS'] * np.sin(p_wd)
        return WindUV


    def PWindDir(self, sim_uv, obs_uv):

        fig, ax = plt.subplots(2, 1, figsize = (10, 8), constrained_layout=True)

        tlist = ['sim_uv','obs_uv']
        for ii in range(len(tlist)):
           data = eval(tlist[ii])
           arr = ax[ii].quiver(data.index, 0, data['u'], data['v'], 
                               color='k', scale=15, width=0.015, units='inches')
           ax[ii].set_xlim([np.datetime64(tt) for tt in self.dateRange])
           ax[ii].xaxis.set_major_locator(mdates.DayLocator(interval=5))
           ax[ii].xaxis.set_major_formatter(mdates.DateFormatter('%d'))
           ax[ii].tick_params(axis='x', labelsize=15)
           ax[ii].set_xlabel(u'日期', fontproperties=zhfont)
           ax[ii].yaxis.set_ticks([])
           ax[ii].set_ylabel(tlist[ii][:3], fontsize='medium', fontproperties=zhfont)
        ax[1].quiverkey(arr, 0.9, -0.2, 10, r'10m/s', labelpos='E',
                        coordinates='axes',fontproperties={'size':15})
        ax[0].set_title(self.stName + '_' + self.spctitle + '_' +
                        self.dateRange[0].strftime('%Y/%m'),
                        fontproperties=zhfont, fontsize=25)
        return


    def plotOut(self, var, type):

        # if True:  ###True(不要印出來)
        if False:  ###False(將檔案印出來)
            plt.show()
            systime.sleep(2)
        else:
            outDir = os.path.join('Output', 'output_' + type)
            outputfile = os.path.join(outDir, self.dateRange[0].strftime('%Y%m'), var, self.area)
            try:
                os.makedirs(outputfile)
            except FileExistsError:
                pass

            picFil = os.path.join(outputfile, self.stName + self.dateRange[0].strftime('%Y%m'))
            plt.savefig(picFil + '.png')
            plt.close()


    def plot(self, var):
        seaborn.set(font_scale=1.8)
        seaborn.set_style("whitegrid")
        seaborn.axes_style("whitegrid")
       
        mergeDF = pd.concat([self.obsDf[var], self.simDf[var]], axis=1)
        mergeDF.columns = ['obs','sim']
        maxVal = (mergeDF.max()).max()
        self.Clmax = (np.ceil(maxVal/5)+1)*5
        minVal = (mergeDF.min()).min()
        self.Clmin = (np.floor(minVal/5)-1)*5

        if var == 'T2':
           self.spctitle = r'Temperature ($^\circ$C)'
        elif var == 'WS':
           self.spctitle = r'Wind Speed (m/s)'
        elif var == 'WD':
           self.spctitle = r'Wind Direction'
  
        if (var == 'WD'):
           self.PWindDir(self.wsd2uv(self.simDf[['WS', 'WD']]), 
                         self.wsd2uv(self.obsDf[['WS', 'WD']])) 
           self.plotOut(var, 'timeseries')
        else:
           self.Ptimeseries(var)
           self.plotOut(var, 'timeseries')
           self.Pscatter(var)
           self.plotOut(var, 'scatter')



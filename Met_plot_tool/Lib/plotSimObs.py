import os
import time as systime
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn
from matplotlib.font_manager import FontProperties
from matplotlib.ticker import IndexLocator, MultipleLocator
from pandas.plotting import register_matplotlib_converters

zhfont = FontProperties(fname='./Lib/NotoSansCJK-Regular.ttc', size=20)
register_matplotlib_converters()


class plot_SimObs():
    def __init__(self, stInfo, obs, sim, dateRange, nowTT):
        self.obsDf = obs
        self.simDf = sim
        self.stInfo = stInfo
        self.dateRange = dateRange
        self.nowTT = nowTT


    def Ptimeseries(self, var):
        fig, ax = plt.subplots(figsize=(10, 5), constrained_layout = True)

        if (var == 'T2'):
           Clmin = (np.floor(self.minVal/5))*5
           Clmax = (np.ceil(self.maxVal/5))*5
           if (Clmax-Clmin) < 20:
              Clmax = Clmin + 20
        elif (var == 'WS'):
           Clmin = 0
           Clmax = (np.ceil(self.maxVal/5))*5

        ax.set_xlim([np.datetime64(tt) for tt in self.dateRange])
        ax.scatter(self.obsDf[var].index, self.obsDf[var],
                   label='Obs', color='k', s=20)
        ax.plot(self.simDf.index, self.simDf[var],
                label='Sim', color='k', linestyle='-')

        ax.set_ylim([Clmin, Clmax])
        plt.yticks(range(int(Clmin), int(Clmax)+1, 5))

        ax.xaxis.set_major_locator(IndexLocator(base=5, offset=-1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
        ax.tick_params(axis='x', labelsize=15)
        ax.tick_params(axis='y', labelsize=15)
        ax.legend(fontsize=13, ncol=2, bbox_to_anchor=(1, 1), loc='lower right')
        ax.set_xlabel(u'日期', fontproperties=zhfont)
        ax.set_title(self.stInfo['st'] + '_' + self.spctitle + '_' + self.dateRange[0].strftime('%Y/%m'),
                     fontproperties=zhfont)
        return


    def Pscatter(self, var):

        fig, ax = plt.subplots(figsize=(6, 6), constrained_layout=True)

        if (var == 'T2'):
           Clmin = (np.floor(self.minVal/5)-1)*5
        elif (var == 'WS'):
           Clmin = 0
        Clmax = (np.ceil(self.maxVal/5)+1)*5

        ax.scatter(self.obsDf[var], self.simDf[var], label=var, color='k', s=20)
        ax.set_xlim([Clmin, Clmax])
        ax.set_ylim([Clmin, Clmax])
        ax.plot(np.arange(Clmin, 3*Clmax),
                np.arange(Clmin, 3*Clmax), color='k', linestyle='-')

        ax.xaxis.set_major_locator(MultipleLocator(5))
        ax.yaxis.set_major_locator(MultipleLocator(5))
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlabel(u'觀測', fontsize='medium', fontproperties=zhfont)
        ax.set_ylabel(u'模擬', fontsize='medium', fontproperties=zhfont)
        ax.set_title(self.stInfo['st'] + '_' + self.spctitle + '_' + self.dateRange[0].strftime('%Y/%m'),
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

        fig, ax = plt.subplots(figsize = (10, 7), constrained_layout=True)

        arr_sim = ax.quiver(sim_uv.index, 1, sim_uv['u'], sim_uv['v'], 
                            color='k', scale=15, width=0.015, units='inches')
        arr_obs = ax.quiver(obs_uv.index, -1, obs_uv['u'], obs_uv['v'], 
                            color='k', scale=15, width=0.015, units='inches')
        ax.set_xlim([np.datetime64(tt) for tt in self.dateRange])
        ax.xaxis.set_major_locator(IndexLocator(base=5, offset=-1))
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d"))
        ax.tick_params(axis='x', labelsize=15)
        ax.set_xlabel(u'日期', fontproperties=zhfont)
        ax.set_ylim(-2,2)
        plt.yticks([-1, 1], [u'觀測', u'模擬'], fontsize='medium', font_properties=zhfont)
        ax.quiverkey(arr_obs, 0.9, -0.09, 10, r'10m/s', labelpos='E',
                        coordinates='axes',fontproperties={'size':15})
        ax.set_title(self.stInfo['st'] + '_' + self.spctitle + '_' +
                        self.dateRange[0].strftime('%Y/%m'),
                        fontproperties=zhfont, fontsize=25)
        return

    def plotOut(self, var, type):

        YYMM = self.dateRange[0].strftime('%Y%m')
        outDir = os.path.join('Output', 'output_' + type)
        outputfile = os.path.join(outDir, self.nowTT+ '_For' +YYMM, var, self.stInfo['area'])
        try:
            os.makedirs(outputfile)
        except FileExistsError:
            pass

        picFil = os.path.join(outputfile, str(self.stInfo['stID']) + self.stInfo['st'] + YYMM)
        plt.savefig(picFil + '.png')
        plt.close()


    def plot(self, var):
        seaborn.set(font_scale=1.8)
        seaborn.set_style("whitegrid", {'axes.edgecolor':'black'})
       
        mergeDF = pd.concat([self.obsDf[var], self.simDf[var]], axis=1)
        mergeDF.columns = ['obs','sim']
        self.maxVal = (mergeDF.max()).max()
        self.minVal = (mergeDF.min()).min()

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



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


class plotSimObs():
    def __init__(self, stInfo, obs, sim):
        self.obsDf = obs
        self.simDf = sim
        self.stName = stInfo['st']
        self.stID = stInfo['stID']
        self.enName = stInfo['enName']
        self.area = stInfo['area']

    def plot(self, spcs, dateRange, type):
        seaborn.set(font_scale=1.8)
        seaborn.set_style("whitegrid")
        seaborn.axes_style("whitegrid")


        if type == 'timeseries':
            fig, ax = plt.subplots(len(spcs), 1, 
                                   figsize=(8.27 * 2, 11.69 * 2), constrained_layout = True)
        elif type == 'scatter':
            fig, ax = plt.subplots(2, int(len(spcs)/2)+1,
                                   figsize=(11.69 * 2, 6.0 * 2), constrained_layout=True)
                                  #figsize=(11.69 * 2, 8.27 * 2), constrained_layout=True)
        else:
            raise KeyError

        for ii in range(len(spcs)):
            if spcs[ii] == 'SO2':
                spcnm = r'SO$_{2}$'
                spcun = r'(ppbV)'
            elif spcs[ii] == 'PM25':
                spcnm = r'PM$_{2.5}$'
                spcun = r'($\mu$g/m$^3$)'
            elif spcs[ii] == 'O3':
                spcnm = r'O$_{3}$'
                spcun = r'(ppbV)'
            elif spcs[ii] == 'NMHC':
                spcnm = r'NMHC'
                spcun = r'(ppbC)'
            elif spcs[ii] == 'PM10':
                spcnm = r'PM$_{10}$'
                spcun = r'($\mu$g/m$^3$)'
            else:
                spcnm = r'NO$_{2}$'
                spcun = r'(ppbV)'
           
            if (spcs[ii] == 'NMHC') or (spcs[ii] == 'O3') or (spcs[ii] == 'NO2_hr'):
               spctm = r'(小時平均)'
            else:
               spctm = r'(日平均)'

            mergeDF = pd.concat([self.obsDf[spcs[ii]], self.simDf[spcs[ii]]], axis=1)
            mergeDF.columns = ['obs','sim']
            maxVal = (mergeDF.max()).max()
            if (maxVal <= 20):
               Clmax = (np.ceil(maxVal/5)+1)*5
            else:
               Clmax = (np.ceil(maxVal/10)+1)*10

            if type == 'timeseries':
                slmark = np.isfinite(self.simDf[spcs[ii]])
                ax[ii].set_xlim([np.datetime64(dateRange[0]),
                                 np.datetime64(dateRange[1])-pd.Timedelta('1h')])
                ax[ii].scatter(self.obsDf.index, self.obsDf[spcs[ii]],
                               label='Obs', color='k', s=30)
                ax[ii].plot(self.simDf.index[slmark], self.simDf[spcs[ii]][slmark],
                            label='Sim', color='k', linestyle='-')
                ax[ii].set_ylim([0, Clmax])
                ax[ii].set_yticks(np.arange(0, Clmax*1.1, Clmax/5))
                ax[ii].xaxis.set_major_locator(mdates.DayLocator(interval=1))
                ax[ii].xaxis.set_major_formatter(mdates.DateFormatter('%d'))
                ax[ii].tick_params(axis='x', labelsize=20)
                ax[ii].legend(fontsize=13, ncol=2, bbox_to_anchor=(1, 1), loc='lower right')
                ax[ii].set_xlabel(u'日期', fontproperties=zhfont)
                ax[ii].set_title(self.stName + '_' + spcnm + ' ' + spcun + '_' + 
                                 dateRange[0].strftime('%Y/%m'),
                                 fontproperties=zhfont)

            elif type == 'scatter':
                ax[ii % 2, int(ii / 2)].set_xlim([0, Clmax])
                ax[ii % 2, int(ii / 2)].set_ylim([0, Clmax])
                ax[ii % 2, int(ii / 2)].set_aspect('equal', adjustable='box')
                ax[ii % 2, int(ii / 2)].set_xticks(np.arange(0, Clmax*1.1, Clmax/5))
                ax[ii % 2, int(ii / 2)].set_yticks(np.arange(0, Clmax*1.1, Clmax/5))
                ax[ii % 2, int(ii / 2)].set_xlabel(u'觀測 ' + spcun, fontsize='medium', fontproperties=zhfont)
                ax[ii % 2, int(ii / 2)].set_ylabel(u'模擬 ' + spcun, fontsize='medium', fontproperties=zhfont)

                ax[ii % 2, int(ii / 2)].scatter(mergeDF['obs'], mergeDF['sim'],
                                                label=spcs, color='k', s=20)
                ax[ii % 2, int(ii / 2)].plot(np.arange(3*maxVal), np.arange(3*maxVal),
                                             color='k', linestyle='-')
                ax[ii % 2, int(ii / 2)].set_title(self.stName + '_' + spcnm + ' ' + spctm + '_' +
                                                  dateRange[0].strftime('%Y/%m'),
                                                  fontproperties=zhfont)

            else:
                raise KeyError

        if type == 'scatter':
           ax[1, 3].remove()
           if (len(spcs) == 6):
             ax[0, 3].remove()

#           plt.tight_layout()



        # if True:  ###True(不要印出來)
        if False:  ###False(將檔案印出來)
            plt.show()
            systime.sleep(2)
        else:
            outDir = os.path.join('Output', 'output_'+type, 
                                      dateRange[0].strftime('%Y-%m'), self.area)
            try:
                os.makedirs(outDir)
            except FileExistsError:
                pass
            strStID = '{:03d}'.format(self.stID)
            picFil = os.path.join(outDir, strStID + self.stName + dateRange[0].strftime('%Y%m'))
            plt.savefig(picFil + '.png')
            plt.close()

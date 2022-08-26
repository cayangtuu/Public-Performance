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
zhfont2 = FontProperties(fname='./Lib/NotoSansCJK-Regular.ttc', size=15)
register_matplotlib_converters()


def plot(Data, AirQ_Area, allVar, Criteria, workDir):
    seaborn.set(font_scale=1.8)
    seaborn.set_style("whitegrid")
    seaborn.axes_style("whitegrid")

    spcnm = {'O3':r'O$_{3}$', 'NO2':r'NO$_{2}$', 'NMHC':r'NMHC', 'PM':r'PM', 
             'PM10':r'PM$_{10}$', 'PM25':r'PM$_{2.5}$', 'SO2':r'SO$_{2}$', 'NO2':r'NO$_{2}$'}
    marker = {'北部': 'o', '中部':'^', '雲嘉':'X', '南部':'s', '東部':'h'} 
    colors = {'北部': 'k', '中部':'darkred', '雲嘉':'darkblue', '南部':'orange', '東部':'darkgreen'} 


    for cats in allVar:
        for var in allVar[cats]:
            for ids in Criteria[cats][var]:
                DF = pd.DataFrame.from_dict(Data[cats][var][ids])
                DF.index = [MM+1 for MM in np.arange(12)]
                DF = DF.replace('--', np.nan)

                ##設定數值範圍
                CriVal = Criteria[cats][var][ids]
                if (ids != 'R'):
                   criTxt = f'Criteria: {CriVal[0]}~{CriVal[1]}'
                   if (ids == 'MNB'):
                      MinMax = [-1, 1, 0.2]
                   elif (ids == 'MNE'):
                      MinMax = [0, 1, 0.1]
                   elif (ids == 'MFB'):
                      MinMax = [-2, 2, 0.4]
                   elif (ids == 'MFE'):
                      MinMax = [0, 2, 0.2]
                   else:
                      minmin = DF.min(skipna=True).min(skipna=True)
                      maxmax = DF.max(skipna=True).max(skipna=True)
                      MinMax = [round(minmin, 1)-0.1, round(maxmax, 1)+0.1, 0.1]
                else:
                   criTxt = f'Criteria: >{CriVal}'
                   MinMax = [-1, 1, 0.2]
#               ##設定數值範圍[END]

#               ##設定數值範圍
#               maxmax = DF.max(skipna=True).max(skipna=True)
#               minmin = DF.min(skipna=True).min(skipna=True)
#               CriVal = Criteria[cats][var][ids]
#               if (ids != 'R'):
#                  minVal = round(minmin, 1)-dVal
#                  maxVal = round(maxmax, 1)+dVal
#                  criTxt = f'Criteria: {CriVal[0]}~{CriVal[1]}'
#                  if (maxVal-minVal)>1:
#                     dVal = 0.2
#               else:
#                  minVal = 0-dVal
#                  maxVal = round(maxmax, 1)+dVal
#                  criTxt = f'Criteria: >{CriVal}'
#               ##設定數值範圍[END]

                fig, ax = plt.subplots(figsize=(11.69, 8.27), constrained_layout = True)

                for area in AirQ_Area:
                    slmark = np.isfinite(DF[area])
                    ax.plot(DF.index[slmark], DF[area][slmark], color=colors[area])

                    ax.scatter(DF.index, DF[area], label=area,
                                marker=marker[area], color=colors[area], s=60)

                    if (ids != 'R'):
                       plt.hlines(CriVal[0], 1, 12, color='k', linestyle='--')
                       plt.hlines(CriVal[1], 1, 12, color='k', linestyle='--')
                    else:
                       plt.hlines(CriVal,1,12, color='k', linestyle='--')

                ax.set_xlim(1, 12)
#               ax.set_ylim(minVal, maxVal)
#               ax.set_yticks(np.arange(minVal, maxVal+dVal, dVal))
                ax.set_ylim(MinMax[0], MinMax[1])
                ax.set_yticks(np.arange(MinMax[0], MinMax[1]+MinMax[2], MinMax[2]))
                ax.set_xticks(DF.index)
                ax.set_xlabel(u'月份', fontproperties=zhfont)
                ax.set_ylabel(u'物種指標數值', fontproperties=zhfont)
                ax.annotate(criTxt, xy=(0.8, 1.0), xycoords='axes fraction', fontsize=15)
                ax.set_title('('+spcnm[cats]+')' + spcnm[var] + '_' + ids +
                             '\n全年各模擬區全部測站平均結果', fontproperties=zhfont)
                ax.legend(loc='upper right', prop=zhfont2, markerscale=1.5)



                # if True:  ###True(不要印出來)
                if False:  ###False(將檔案印出來)
                   plt.show()
                   systime.sleep(2)
                else:
                   outputfile = os.path.join(workDir, '圖檔', '全年各指標全部模擬區性能評估統計結果(固定值域)')
                   try:
                      os.makedirs(outputfile)
                   except FileExistsError:
                      pass
                   picFil = os.path.join(outputfile, '('+cats+') ' + var + '_' + ids +\
                                         ' 全年全部模擬區性能評估統計結果')
                   plt.savefig(picFil + '.png')
                   plt.close()

import os
import pandas as pd
import time as systime
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.font_manager import FontProperties

zhfont = FontProperties(fname='./Lib/NotoSansCJK-Regular.ttc', size=20)

### 圖例的參數設定 ###
def crsEE(CriteriaVl):
    colorsmap=['limegreen', 'green', 'orange', 'red']
    bounds = [CriteriaVl[0], 0.5*CriteriaVl[1], CriteriaVl[1], round(1.5*CriteriaVl[1],3)]
    cmap = mpl.colors.ListedColormap(colorsmap[:3])
    cmap.set_over(colorsmap[3])
    norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)
    return {'vcl':colorsmap, 'vb':bounds, 'vc':cmap, 'vn':norm}

def crsBB(CriteriaVl):
    colorsmap = ['orange', 'limegreen', 'green', 'red']
    bounds = [CriteriaVl[0], 0, CriteriaVl[1]]
    cmap = mpl.colors.ListedColormap(colorsmap[1:3])
    cmap.set_over(colorsmap[3])
    cmap.set_under(colorsmap[0])
    norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)
    return {'vcl':colorsmap, 'vb':bounds, 'vc':cmap, 'vn':norm}

def crsRR(CriteriaVl):
    colorsmap = ['red', 'darkorange', 'gold', 'green']
    bounds = [0, 0.5*CriteriaVl, CriteriaVl]
    cmap = mpl.colors.ListedColormap(colorsmap[1:3])
    cmap.set_over(colorsmap[3])
    cmap.set_under(colorsmap[0])
    norm = mpl.colors.BoundaryNorm(boundaries=bounds, ncolors=cmap.N)
    return {'vcl':colorsmap, 'vb':bounds, 'vc':cmap, 'vn':norm}


def plot2D(Data, Vars, Criteria, stFil, shpFil, workDir, FilNM):

    sitedf = pd.read_csv(stFil, encoding='big5')
    for iid in Data:
        CriteriaVl = Criteria[iid]

        ## 畫TW地圖
        fig, ax = plt.subplots(figsize = (16, 10.5))
        twmap = Basemap(llcrnrlon=119.3, llcrnrlat=21.82, urcrnrlon=122.1, urcrnrlat=25.43,
                        epsg=4326, resolution='f')
        twmap.readshapefile(shpFil, 'Taiwan', linewidth=1.0, drawbounds=True)
        im = twmap.drawcountries(linewidth=10.5)
        ## 畫TW地圖[END]

        ## 畫各測站點圖
        for sts in Data[iid]:
            stx = sitedf.loc[sitedf['ch_name']==sts, 'lon']
            sty = sitedf.loc[sitedf['ch_name']==sts, 'lat']
            stVl = Data[iid][sts]
            
            if (iid =='MNE') or (iid =='MFE'):
               criTxt = f'Criteria: {CriteriaVl[0]}~{CriteriaVl[1]}'
               Crs = eval('crsEE')(CriteriaVl)
               if (stVl != '--'):
                  if (stVl>=Crs['vb'][0]) and (stVl<Crs['vb'][1]):
                     twmap.plot(stx, sty, color=Crs['vcl'][0], marker='o', markersize=5)
                  elif (stVl>=Crs['vb'][1]) and (stVl<=Crs['vb'][2]):
                     twmap.plot(stx, sty, color=Crs['vcl'][1], marker='o', markersize=5)
                  elif (stVl>Crs['vb'][2]) and (stVl<=Crs['vb'][3]):
                     twmap.plot(stx, sty, color=Crs['vcl'][2], marker='o', markersize=5)
                  elif (stVl>Crs['vb'][3]):
                     twmap.plot(stx, sty, color=Crs['vcl'][3], marker='o', markersize=5)

            elif (iid =='R'):
               criTxt = f'Criteria: >{CriteriaVl}'
               Crs = eval('crsRR')(CriteriaVl)
               if (stVl != '--'):
                  if (stVl<Crs['vb'][0]):
                     twmap.plot(stx, sty, color=Crs['vcl'][0], marker='o', markersize=5)
                  elif (stVl>=Crs['vb'][0]) and (stVl<Crs['vb'][1]):
                     twmap.plot(stx, sty, color=Crs['vcl'][1], marker='o', markersize=5)
                  elif (stVl>=Crs['vb'][1]) and (stVl<Crs['vb'][2]):
                     twmap.plot(stx, sty, color=Crs['vcl'][2], marker='o', markersize=5)
                  elif (stVl>=Crs['vb'][2]):
                     twmap.plot(stx, sty, color=Crs['vcl'][3], marker='o', markersize=5)

            else:
               criTxt = f'Criteria: {CriteriaVl[0]}~{CriteriaVl[1]}'
               Crs = eval('crsBB')(CriteriaVl)
               if (stVl != '--'):
                  if (stVl<Crs['vb'][0]):
                     twmap.plot(stx, sty, color=Crs['vcl'][0], marker='o', markersize=5)
                  elif (stVl>=Crs['vb'][0]) and (stVl<Crs['vb'][1]):
                     twmap.plot(stx, sty, color=Crs['vcl'][1], marker='o', markersize=5)
                  elif (stVl>=Crs['vb'][1]) and (stVl<=Crs['vb'][2]):
                     twmap.plot(stx, sty, color=Crs['vcl'][2], marker='o', markersize=5)
                  elif (stVl>Crs['vb'][2]):
                     twmap.plot(stx, sty, color=Crs['vcl'][3], marker='o', markersize=5)
        ## 畫各測站點圖[END]


        ## 畫colorbar
        cax  = fig.add_axes([0.33, 0.8, 0.12, 0.023])
        if (iid == 'MNE') or (iid == 'MFE'):
           cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=Crs['vn'], cmap=Crs['vc']), 
                               cax=cax, ticks=Crs['vb'], orientation='horizontal',
                               extend='max', extendrect=True, extendfrac='auto', spacing='uniform')
        else:
           cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=Crs['vn'], cmap=Crs['vc']), 
                               cax=cax, ticks=Crs['vb'], orientation='horizontal',
                               extend='both', extendrect=True, extendfrac='auto', spacing='uniform')

        cbar.ax.set_xticklabels([str(txt) for txt in Crs['vb']])
        cbar.ax.tick_params(labelsize=12)

        ax.annotate(criTxt, xy=(0.03, 0.95), xycoords='axes fraction', fontsize=15)
        ax.set_title(FilNM+' ('+Vars[0]+')' + Vars[1] + '_' + iid +
                     '\各測站性能評估結果', fontproperties=zhfont)
        ## 畫colorbar[END]


        #if True:   ###True(不要印出來)
        if False:  ###False(將檔案印出來)
           plt.show()
           systime.sleep(2)
        else:
           outDir = outputfile = os.path.join(workDir, '圖檔', 
                                 '各指標全部測站性能評估結果', FilNM)
           try:
               os.makedirs(outDir)
           except FileExistsError:
               pass

           picFil = os.path.join(outDir, '('+FilNM+') ('+Vars[0]+')'+Vars[1]+'_'+iid+\
                                 ' 全部測站性能評估結果.png')
           plt.savefig(picFil, bbox_inches='tight')
           plt.close()


def plotBAD(Data, AirQ_Area, stFil, shpFil, workDir, FilNM):

    sitedf = pd.read_csv(stFil, encoding='big5')

    ## 畫TW地圖
    fig, ax = plt.subplots(figsize = (16, 10.5))
    twmap = Basemap(llcrnrlon=119.3, llcrnrlat=21.82, urcrnrlon=122.1, urcrnrlat=25.43,
                    epsg=4326, resolution='f')
    twmap.readshapefile(shpFil, 'Taiwan', linewidth=1.0, drawbounds=True)
    im = twmap.drawcountries(linewidth=10.5)
    ## 畫TW地圖[END]

    ## 畫各測站點圖
    for st in [sts for Area in AirQ_Area for sts in AirQ_Area[Area]]:
        stx = sitedf.loc[sitedf['ch_name']==st, 'lon']
        sty = sitedf.loc[sitedf['ch_name']==st, 'lat']
        try:
           stVl = Data[st]
        except KeyError:
           stVl = 0

        Crs_clr=['limegreen', 'green', 'orange', 'red']
        Crs_bounds = [0, 5, 10, 15, 22]
        Crs_cmap = mpl.colors.ListedColormap(Crs_clr)
        Crs_norm = mpl.colors.BoundaryNorm(boundaries=Crs_bounds, ncolors=Crs_cmap.N)

        for ii in range(1, len(Crs_bounds)):
           if (stVl == 0):
              twmap.plot(stx, sty, color='k', marker='+', markersize=5)
              break
           elif (stVl == Crs_bounds[ii]):
              twmap.plot(stx, sty, color=Crs_clr[ii-1], marker='o', markersize=5)
           elif (stVl>=Crs_bounds[ii-1] and stVl<Crs_bounds[ii]):
              twmap.plot(stx, sty, color=Crs_clr[ii-1], marker='o', markersize=5)
    ## 畫各測站點圖[END]

    ## 畫colorbar
    cax  = fig.add_axes([0.33, 0.83, 0.12, 0.023])
    cbar = fig.colorbar(mpl.cm.ScalarMappable(norm=Crs_norm, cmap=Crs_cmap),
                        cax=cax, ticks=Crs_bounds, orientation='horizontal')

    cbar.ax.set_xticklabels([str(txt) for txt in Crs_bounds])
    cbar.ax.tick_params(labelsize=12)

    ax.set_title(FilNM+' 各測站未通過性能評估指標數目', fontproperties=zhfont)
    ## 畫colorbar[END]


    #if True:   ###True(不要印出來)
    if False:  ###False(將檔案印出來)
       plt.show()
       systime.sleep(2)
    else:
       outDir = outputfile = os.path.join(workDir, '圖檔', '各測站未通過性能評估指標數目')
       try:
           os.makedirs(outDir)
       except FileExistsError:
           pass

       picFil = os.path.join(outDir, '('+FilNM+') 各測站未通過性能評估指標數目.png')
       plt.savefig(picFil, bbox_inches='tight')
       plt.close()

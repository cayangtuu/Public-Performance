import pandas as pd
import openpyxl
import os

def StsOut(Data, Criteria, AirQ_Area, allVar, workDir, FilNM):

    ##excel起始cols位置
    startcol = {'O3':{'O3':0, 'NO2':5, 'NMHC':9}, 
                'PM':{'PM10':13, 'PM25':17, 'SO2':21, 'NO2':25}}
    ##excel起始cols位置[END]

    for area in AirQ_Area:
        FilOut = os.path.join(workDir, '各月份各模擬區全部測站性能評估結果', 
                              '('+ FilNM +') ' +area +'模擬區全部測站性能評估結果.xlsx')
        writer = pd.ExcelWriter(FilOut)
        for cats in allVar:
            Vars = allVar[cats]
            for var in Vars:
                df = pd.DataFrame.from_dict(data=Data[area][cats][var])
                df.index.name = var

                df.to_excel(writer, sheet_name=FilNM, startcol=startcol[cats][var]) 
 
               
                ##依Criteria建立色階
                workbook = writer.book
                worksheet = writer.sheets[FilNM]
                format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                               'font_color': '#9C0006'})
                format2 = workbook.add_format({'bg_color': 'white', 
                                               'font_color': 'black'})


                crivl= list(Criteria[cats][var].values())
                for col in range(len(crivl)):
                    shcol = startcol[cats][var]+col+1
                    shrow = len(AirQ_Area[area])
                    if (col != len(crivl)-1):
                       worksheet.conditional_format(1, shcol, shrow+1, shcol, 
                                                    {'type': 'text',
                                                     'criteria': 'containing',
                                                     'value': '--', 
                                                     'format': format2})
                       worksheet.conditional_format(1, shcol, shrow+1, shcol, 
                                                    {'type': 'cell',
                                                     'criteria': 'not between',
                                                     'minimum': crivl[col][0],
                                                     'maximum': crivl[col][1], 
                                                     'format': format1})
                    else:
                       worksheet.conditional_format(1, shcol, shrow+1, shcol, 
                                                    {'type': 'cell',
                                                     'criteria': '<',
                                                     'value': crivl[col], 
                                                     'format': format1})
                    if (df.loc['合格率', str(df.columns[col])] != '--'):
                       if (int(df.loc['合格率', str(df.columns[col])].split('%')[0]) < 60):
                           worksheet.conditional_format(shrow+3, shcol, shrow+3, shcol,
                                                        {'type': 'formula',
                                                         'criteria': True,
                                                         'format': format1})
                ##依Criteria建立色階[END]

        worksheet.conditional_format(0, 0, shrow+6, 28,
                                     {'type':'no_blanks', 
                                      'format': workbook.add_format({'border':1})})
        worksheet.merge_range(shrow+8, 0, shrow+8, 11,
                              '註：部分測站由於環保署測站無資料可供比對或可用資料數不足，無法進行性能評估，故各指標之總站數有所差異') 
        writer.save()


def AreaOut(Data, Criteria, AirQ_Area, allVar, workDir, FilNM):
    FilOut = os.path.join(workDir, '各月份全部模擬區性能評估統計結果',
                          '('+ FilNM +') 全部模擬區性能評估統計結果'+'.xlsx')
    writer = pd.ExcelWriter(FilOut)
    for cats in allVar:
        Vars = allVar[cats]
        vldf = {area:{} for area in AirQ_Area}
        filcl = {area:{} for area in AirQ_Area}
        for area in AirQ_Area:
            for var in Vars:
                for iid in Data[area][cats][var].keys():
                    vl1 = Data[area][cats][var][iid]['overal']
                    vl2 = Data[area][cats][var][iid]['合格率']
                    vl = str(vl1)+'('+str(vl2)+')'
                    vldf[area][var+'_'+iid] = vl

                    ##依Criteria建立色階條件 
                    filcl[area][var+'_'+iid] = 'True'
                    if (iid != 'R'):
                       if (vl1 != '--') and (((vl1<Criteria[cats][var][iid][0]) \
                                         or  (vl1>Criteria[cats][var][iid][1])) \
                                         or (int(vl2.split('%')[0])<60)):
                          filcl[area][var+'_'+iid] = 'False'
                    else:
                       if (vl1 != '--') and ((vl1<Criteria[cats][var][iid]) \
                                         or (int(vl2.split('%')[0])<60)):
                          filcl[area][var+'_'+iid] = 'False'
                    ##依Criteria建立色階條件[END] 

        df = pd.DataFrame.from_dict(vldf).T
        df.index.name = cats

        if cats == 'O3':
           df.to_excel(writer, sheet_name=FilNM, startrow=0)
        elif cats == 'PM':
           df.to_excel(writer, sheet_name=FilNM, startrow=7)


        ##建立色階
        workbook = writer.book
        worksheet = writer.sheets[FilNM]
        format1 = workbook.add_format({'bg_color': '#FFC7CE',
                                       'font_color': '#9C0006'})


        for row in range(len(df.index)):
           for col in range(len(df.columns)):
               if (filcl[df.index[row]][df.columns[col]] == 'False'):
                  if cats == 'O3':
                     worksheet.conditional_format(row+1, col+1, row+1, col+1,
                                                  {'type': 'formula',
                                                   'criteria': True,
                                                   'format': format1}) 
                  elif cats == 'PM':
                     worksheet.conditional_format(row+8, col+1, row+8, col+1,
                                                  {'type': 'formula',
                                                   'criteria': True,
                                                   'format': format1}) 
        ##建立色階[END]

        worksheet.conditional_format('A1:K6',
                                     {'type':'no_blanks', 
                                      'format': workbook.add_format({'border':1})})
        worksheet.conditional_format('A8:M13',
                                     {'type':'no_blanks', 
                                      'format': workbook.add_format({'border':1})})

    worksheet.merge_range('A15:A15', "註：") 
    worksheet.merge_range('B15:G15', "1.表格內數值為該模擬區中全部測站平均結果(括弧內數值為測站合格率)") 
    worksheet.merge_range('B16:E16', "2. '--'符號表示該區域環保署測站無資料可供比對") 
    writer.save()


def BadOut(Data, Criteria, AirQ_Area, allVar):
    stnm = {area:0 for area in AirQ_Area}
    vldf = {area:0 for area in AirQ_Area}
    vlper = {area:0 for area in AirQ_Area}
    for area in AirQ_Area:
        for cats in allVar:
            Vars = allVar[cats]
            for var in Vars:
                for iid in Data[area][cats][var].keys():
                    ctvl = 0
                    for st in AirQ_Area[area]:
                        vl = Data[area][cats][var][iid][st]
                        if (iid != 'R'):
                           if (vl != '--') and ((vl<Criteria[cats][var][iid][0]) \
                                            or  (vl>Criteria[cats][var][iid][1])):
                              ctvl += 1
                        else:
                           if (vl != '--') and (vl<Criteria[cats][var][iid]):
                              ctvl += 1

                    vldf[area] += ctvl

                    if (Data[area][cats][var][iid]['總站數'] != '--'):
                       stnm[area] += Data[area][cats][var][iid]['總站數']
        if (stnm[area] != 0):
           vlper[area] = str(int(100*vldf[area]/stnm[area]) )+ '%'
        else: 
           vlper[area] = '--'

    return stnm, vldf, vlper

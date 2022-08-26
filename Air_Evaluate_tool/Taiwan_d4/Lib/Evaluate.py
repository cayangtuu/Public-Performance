import pandas as pd

def stonAvg(data, stons):
    hr_ = {ston: 0 for ston in stons}
    data_ = {ston: 0 for ston in stons}
    sumhr_ = 0
    sumdata_ = 0
    for ston in stons:
        for i in range(0, len(data)):
            if (float(data[ston][i]) != -999):
                hr_[ston] += 1  # 各個測站總共模擬的小時
                sumhr_ += 1     # 所有測站總共模擬的小時

                data_[ston] += data[ston][i]
                sumdata_ += data[ston][i]

        if hr_[ston] != 0:
            data_[ston] /= hr_[ston]
        else:
            data_[ston] = -999

    if sumhr_ != 0:
        sumdata_ /= sumhr_
    else:
        sumdata_ = -999


    return { 'each_stn' : data_ ,
             'sum_stn'  : sumdata_  }


def Evaluate(obs_PH, sim_PH, obs_DA, sim_DA, sim_PH_o3MB, stons, cats, var):

    all_vl = ['MNB', 'MNE', 'MFB', 'MFE', 'MB', 'Rph', 'Rda']

    # 計算Missing Value(-999)，若超過總資料95％則不顯示該測站計算資料
    def countnan(obsdata, simdata):
        countvl = {ston: True for ston in stons}
        for ston in stons:
           count = 0
           for obs in obsdata[ston]:
              if obs == -999:
                 count += 1
           if count > len(obsdata[ston])*0.95:
              countvl[ston] = False
              obsdata[ston] = -999    #將沒有納入計算的測站之觀測值全更改為-999
              simdata[ston] = -999    #將沒有納入計算的測站之模擬值全更改為-999
        return countvl

    if cats == 'O3':
       Cresult = countnan(obs_PH, sim_PH)
    elif cats == 'PM':
       Cresult = countnan(obs_DA, sim_DA)


    #訂定標準
    MNBCriteria = '--'
    MNECriteria = '--'
    MFBCriteria = '--'
    MFECriteria = '--'
    MBCriteria  = '--'
    RphCriteria = '--'
    RdaCriteria = '--'
   
    if var == 'O3':
       MNBCriteria = [-0.15, 0.15] #+-內
       MNECriteria = [0.0, 0.35]   #以下
       RphCriteria = 0.45          #以上
       MBCriteria  = [-0.1, 0.1]   #+-內
    if var == 'NO2':
       MNBCriteria = [-0.4, 0.5]   #+-內
       MNECriteria = [0.0, 0.80]   #以下
       MFECriteria = [0, 0.85]     #以下
       MFBCriteria = [-0.65, 0.65] #+-內
       RphCriteria = 0.35          #以上
       RdaCriteria = 0.45          #以上
    if var == 'NMHC':
       MNBCriteria = [-0.4, 0.5]   #+-內
       MNECriteria = [0, 0.80]     #以下
       RphCriteria = 0.35          #以上
    if var == 'PM10':
       MFECriteria = [0, 0.55]     #以下
       MFBCriteria = [-0.35, 0.35] #+-內
       RdaCriteria = 0.5           #以上
    if var == 'PM25':
       MFECriteria = [0, 0.55]     #以下
       MFBCriteria = [-0.35, 0.35] #+-內
       RdaCriteria = 0.5           #以上
    if var == 'SO2':
       MFECriteria = [0, 0.85]     #以下
       MFBCriteria = [-0.65, 0.65] #+-內
       RdaCriteria = 0.45          #以上



    # 創建性能評估指標的字典
    def IndexDict(vl, criteria):
       vl_Baby = {ston: 0 for ston in stons}
       vl_result = {ston: 0 for ston in stons}
       vl_result['overal'] = 0
       if (vl == 'Rph') or (vl == 'Rda'):
          vl_result['Criteria'] = criteria
       else:
          vl_result['Criteria'] = '/'.join('%s' % id for id in criteria) if isinstance(criteria, list) else '--'
       vl_result['合格率'] = '--'
       vl_result['合格站數'] = '--'

       return vl_Baby, vl_result

    MNB_Baby, MNB_result = IndexDict('MNB', MNBCriteria)
    MNE_Baby, MNE_result = IndexDict('MNE', MNECriteria)
    MFB_Baby, MFB_result = IndexDict('MFB', MFBCriteria)
    MFE_Baby, MFE_result = IndexDict('MFE', MFECriteria)
    MB_Baby,  MB_result  = IndexDict('MB',  MBCriteria)
    Rph_Baby, Rph_result = IndexDict('Rph', RphCriteria)
    Rda_Baby, Rda_result = IndexDict('Rda', RdaCriteria)
 

    # 性能評估指標計算 
    sim_overal_hr = 0
    sim_overal_day = 0
    sim_overal_day_MB = 0

    sim_hr = {ston: 0 for ston in stons}
    sim_day = {ston: 0 for ston in stons}
    sim_day_MB = {ston: 0 for ston in stons}

    Sp_PH_sum = 0
    So_PH_sum = 0
    Sp_DA_sum = 0
    So_DA_sum = 0

    Sp_PH = {ston: 0 for ston in stons}
    So_PH = {ston: 0 for ston in stons}
    Sp_DA = {ston: 0 for ston in stons}
    So_DA = {ston: 0 for ston in stons}

    P_PH = stonAvg(sim_PH, stons)
    O_PH = stonAvg(obs_PH, stons)
    P_DA = stonAvg(sim_DA, stons)
    O_DA = stonAvg(obs_DA, stons)


    for ston in stons:
        
        #(若為 MB 則使用 obs_PH 及 sim_PH_o3MB 資料)
        for i in range(0, len(sim_PH), 24):
            obsMax = obs_PH[ston][i:i+24].max()
            simMax = sim_PH_o3MB[ston][i:i+24].max()
            if obsMax > 0 and obsMax != -999:
               MB_Baby[ston] += (simMax - obsMax) / obsMax
               sim_day_MB[ston] += 1
               sim_overal_day_MB += 1



        #(若為 MNB, MNE, Rph 則使用 obs_PH 及 sim_PH 資料) 
        for i in range(0, len(sim_PH)):
            if (float(obs_PH[ston][i]) != -999) and (float(sim_PH[ston][i]) != -999):

               sim_hr[ston]   += 1  # 總共模擬的小時
               sim_overal_hr  += 1
               MNB_Baby[ston] += (float(sim_PH[ston][i]) - float(obs_PH[ston][i])) \
                                 / float(obs_PH[ston][i])
               MNE_Baby[ston] += abs(float(sim_PH[ston][i]) - float(obs_PH[ston][i])) \
                                 / float(obs_PH[ston][i])


               Sp_PH[ston] += (sim_PH[ston][i] - P_PH['each_stn'][ston])**2
               So_PH[ston] += (obs_PH[ston][i] - O_PH['each_stn'][ston])**2

               Sp_PH_sum += (sim_PH[ston][i] - P_PH['sum_stn'])**2
               So_PH_sum += (obs_PH[ston][i] - O_PH['sum_stn'])**2


               if (P_PH['each_stn'][ston] != -999) and (O_PH['each_stn'][ston] != -999):
                  Rph_Baby[ston] += ((sim_PH[ston][i]-P_PH['each_stn'][ston]) \
                                   * (obs_PH[ston][i]-O_PH['each_stn'][ston]))

               if (P_PH['sum_stn'] != -999) and (O_PH['sum_stn'] != -999):
                  Rph_result['overal'] += ((sim_PH[ston][i]-P_PH['sum_stn']) \
                                         * (obs_PH[ston][i]-O_PH['sum_stn']))



        #(若為 MFB, MFE, Rda 則使用 obs_DA 及 sim_DA 資料)
        for i in range(0, len(sim_DA)):
            if (float(obs_DA[ston][i]) != -999) and (float(sim_DA[ston][i]) != -999):

               sim_day[ston] += 1   # 各個測站總共模擬的天數
               sim_overal_day += 1  # 所有測站總共模擬的天數
               MFB_Baby[ston] += (float(sim_DA[ston][i])-float(obs_DA[ston][i])) / \
                                 (float(sim_DA[ston][i])+float(obs_DA[ston][i]))
               MFE_Baby[ston] += abs(float(sim_DA[ston][i])-float(obs_DA[ston][i])) / \
                                    (float(sim_DA[ston][i])+float(obs_DA[ston][i]))

               Sp_DA[ston] += (sim_DA[ston][i] - P_DA['each_stn'][ston])**2
               So_DA[ston] += (obs_DA[ston][i] - O_DA['each_stn'][ston])**2

               Sp_DA_sum += (sim_DA[ston][i] - P_DA['sum_stn'])**2
               So_DA_sum += (obs_DA[ston][i] - O_DA['sum_stn'])**2


               if (P_DA['each_stn'][ston] != -999) and (O_DA['each_stn'][ston] != -999):
                  Rda_Baby[ston] += ((sim_DA[ston][i]-P_DA['each_stn'][ston]) \
                                   * (obs_DA[ston][i]-O_DA['each_stn'][ston]))

               if (P_DA['sum_stn'] != -999) and (O_DA['sum_stn'] != -999):
                  Rda_result['overal'] += ((sim_DA[ston][i]-P_DA['sum_stn']) \
                                         * (obs_DA[ston][i]-O_DA['sum_stn']))




        if sim_hr[ston] != 0:
           MNB_result[ston] = round(MNB_Baby[ston] / sim_hr[ston], 3)
           MNE_result[ston] = round(MNE_Baby[ston] / sim_hr[ston], 3)
        if sim_day[ston] != 0:
           MFB_result[ston] = round((MFB_Baby[ston]*2) / sim_day[ston], 3)
           MFE_result[ston] = round((MFE_Baby[ston]*2) / sim_day[ston], 3)
        if sim_day_MB[ston] != 0:
           MB_result[ston]  = round(MB_Baby[ston]/sim_day_MB[ston], 3)

        if (Sp_PH[ston]**0.5 != 0) and (So_PH[ston]**0.5 != 0):
           Rph_result[ston] = round(Rph_Baby[ston] / ((Sp_PH[ston]**0.5) * (So_PH[ston]**0.5)), 3)

        if (Sp_DA[ston]**0.5 != 0) and (So_DA[ston]**0.5 != 0):
           Rda_result[ston] = round(Rda_Baby[ston] / ((Sp_DA[ston]**0.5) * (So_DA[ston]**0.5)), 3)



        MNB_result['overal'] += MNB_Baby[ston]
        MNE_result['overal'] += MNE_Baby[ston]
        MFB_result['overal'] += MFB_Baby[ston]
        MFE_result['overal'] += MFE_Baby[ston]
        MB_result['overal']  += MB_Baby[ston]
          



    if sim_overal_hr != 0:
       MNB_result['overal'] = round(MNB_result['overal'] / sim_overal_hr, 3)
       MNE_result['overal'] = round(MNE_result['overal'] / sim_overal_hr, 3)
    if sim_overal_day !=0 :
       MFB_result['overal'] = round((MFB_result['overal']*2) / sim_overal_day, 3)
       MFE_result['overal'] = round((MFE_result['overal']*2) / sim_overal_day, 3)
    if sim_overal_day_MB !=0 :
       MB_result['overal']  = round(MB_result['overal'] / sim_overal_day_MB, 3)

    if (Sp_PH_sum**0.5 != 0) and (So_PH_sum**0.5 != 0):
       Rph_result['overal'] = round(Rph_result['overal'] / ((Sp_PH_sum**0.5) * (So_PH_sum**0.5)), 3)

    if (Sp_DA_sum**0.5 != 0) and (So_DA_sum**0.5 != 0):
       Rda_result['overal'] = round(Rda_result['overal'] / ((Sp_DA_sum**0.5) * (So_DA_sum**0.5)), 3)
  

    #計算合格率與合格站數
    def Unify(vl, data, criteria):
        cal_vl = 0
        good_vl = 0
        if data['Criteria'] != '--':
           for ston in stons:
               if Cresult[ston] == False:
                  data[ston] = '--'
               else:
                  cal_vl += 1
                  if (vl == 'Rph') or (vl == 'Rda'):
                    if (data[ston] >= criteria):
                        good_vl += 1
                  else:
                     if (criteria[0] <= data[ston] <= criteria[1]):
                        good_vl += 1
           if (cal_vl) != 0:
              data['合格率'] = str(int((good_vl/cal_vl) * 100)) + '%'
              data['合格站數'] = good_vl
           else:
              data['overal'] = '--'
              data['合格率'] = '--'
              data['合格站數'] = '--'

    for vl in all_vl:
        Unify(vl, eval(vl+'_result'), eval(vl+'Criteria'))


    if (var == 'O3'):
       data_dict = {'MB': MB_result, 'MNB': MNB_result, 'MNE': MNE_result, 'R': Rph_result } 
    elif (var == 'NO2' and cats == 'O3'):
       data_dict = {'MNB': MNB_result, 'MNE': MNE_result, 'R': Rph_result }
    elif (var == 'NMHC'):
       data_dict = {'MNB': MNB_result, 'MNE': MNE_result, 'R': Rph_result } 
    else:
       data_dict = {'MFB': MFB_result, 'MFE': MFE_result, 'R': Rda_result } 

    return data_dict

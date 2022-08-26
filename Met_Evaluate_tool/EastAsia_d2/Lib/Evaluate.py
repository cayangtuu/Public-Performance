import pandas as pd

def evaluate(obsfile, simfile, ssList, var):

    sim_overal_hr = 0
    sim_hr = {ston: 0 for ston in ssList}

    for ston in ssList:
        for i in range(0, len(simfile)):
            if (float(obsfile[ston][i]) != -999) and (float(simfile[ston][i]) != -999):
               sim_hr[ston]  += 1  # 各測站總模擬小時
               sim_overal_hr += 1  # 所有測站總模擬小時



    if (var == 'T2') or (var == 'WS'):
       sim_obs = {ston: 0 for ston in ssList}
       abs_sim_obs = {ston: 0 for ston in ssList}
       square_sim_obs = {ston: 0 for ston in ssList}

       MBE = {ston: 0 for ston in ssList}
       MBE['overal'] = 0
       MAGE = {ston: 0 for ston in ssList}
       MAGE['overal'] = 0
       RMSE={ston: 0 for ston in ssList}
       RMSE['overal'] = 0

       good_MBE  = 0
       good_MAGE = 0
       good_RMSE = 0

       for ston in ssList:
           for i in range(0, len(simfile)):
               if (float(obsfile[ston][i]) != -999) and (float(simfile[ston][i]) != -999):
  
                  sim_obs[ston] += (float(simfile[ston][i])-float(obsfile[ston][i]))
                  abs_sim_obs[ston] += abs(float(simfile[ston][i])-float(obsfile[ston][i]))
                  square_sim_obs[ston] += (float(simfile[ston][i])-float(obsfile[ston][i]))**2


           if (sim_hr[ston] != 0):
              MBE[ston]  = round(sim_obs[ston]/sim_hr[ston], 2)
              MAGE[ston] = round(abs_sim_obs[ston]/sim_hr[ston], 2)
              RMSE[ston] = round((square_sim_obs[ston]/sim_hr[ston])**0.5, 2)

              MBE['overal']  += sim_obs[ston]
              MAGE['overal'] += abs_sim_obs[ston]
              RMSE['overal'] += square_sim_obs[ston]
           else:
              MBE[ston]  = None
              MAGE[ston] = None
              RMSE[ston] = None

           if abs(MBE[ston]) <= 1.5:
              good_MBE += 1
           if abs(MAGE[ston]) <= 3:
              good_MAGE += 1
           if abs(RMSE[ston])<= 3:
              good_RMSE += 1
         
       if (sim_overal_hr != 0):
          MBE['overal']  = round(MBE['overal']/(sim_overal_hr), 2)
          MAGE['overal'] = round(MAGE['overal']/(sim_overal_hr), 2)
          RMSE['overal'] = round((RMSE['overal']/(sim_overal_hr))**0.5, 2)


       if len(ssList) != 0:
          MBE['Criteria']  = '1.5/-1.5'
          MBE['合格率']    = str(round(good_MBE/len(ssList),2) * 100) + '%'
          MBE['合格站數']  = good_MBE
          MAGE['Criteria'] = '3'
          MAGE['合格率']   = str(round(good_MAGE/len(ssList),2) * 100) + '%'
          MAGE['合格站數'] = good_MAGE
          RMSE['Criteria'] = '3'
          RMSE['合格率']   = str(round(good_RMSE/len(ssList),2) * 100) + '%'
          RMSE['合格站數'] = good_RMSE



    if (var == 'WD'):
       sim_obs = {ston: 0 for ston in ssList}
       abs_sim_obs = {ston: 0 for ston in ssList}

       MNMB = {ston: 0 for ston in ssList}
       MNMB['overal'] = 0
       MNME = {ston: 0 for ston in ssList}
       MNME['overal'] = 0

       good_MNMB = 0
       good_MNME = 0

       for ston in ssList:
           for i in range(0, len(simfile)):
               if (float(obsfile[ston][i]) != -999) and (float(simfile[ston][i]) != -999):
  
                  if (float(simfile[ston][i])-float(obsfile[ston][i])) > 180.0:
                     sim_obs[ston] += (float(simfile[ston][i])-float(obsfile[ston][i])-360.0)
                     abs_sim_obs[ston] += abs((float(simfile[ston][i])-float(obsfile[ston][i])-360.0))

                  elif (float(simfile[ston][i])-float(obsfile[ston][i])) < -180.0:
                     sim_obs[ston] += (float(simfile[ston][i])-float(obsfile[ston][i])+360.0)
                     abs_sim_obs[ston] += abs((float(simfile[ston][i])-float(obsfile[ston][i])+360.0))

                  else:
                     sim_obs[ston] += (float(simfile[ston][i])-float(obsfile[ston][i]))
                     abs_sim_obs[ston] += abs(float(simfile[ston][i])-float(obsfile[ston][i]))


           if (sim_hr[ston] != 0):
              MNMB[ston] = round(sim_obs[ston]/(360*sim_hr[ston]), 4)
              MNME[ston] = round(abs_sim_obs[ston]/(360*sim_hr[ston]), 4) 

              MNMB['overal'] += sim_obs[ston]
              MNME['overal'] += abs_sim_obs[ston]
           else:
               MNMB[ston] = None
               MNME[ston] = None

           if abs(MNMB[ston]*100) <= 10:
              good_MNMB += 1
           if abs(MNME[ston]*100) <= 30:
              good_MNME += 1

           if (sim_hr[ston] != 0):
              MNMB[ston] = str(MNMB[ston] * 100) + '%'
              MNME[ston] = str(MNME[ston] * 100) + '%' 
           
       if (sim_overal_hr != 0):
          MNMB['overal'] = str(round((MNMB['overal']/(360*sim_overal_hr)), 4) * 100) + '%'
          MNME['overal'] = str(round((MNME['overal']/(360*sim_overal_hr)), 4) * 100) + '%'

       if len(ssList) != 0:
          MNMB['Criteria'] = '10.0%/-10.0%'
          MNMB['合格率']   = str(round(good_MNMB/len(ssList), 2) * 100) + '%'
          MNMB['合格站數'] = good_MNMB
          MNME['Criteria'] = '30%'
          MNME['合格率']   = str(round(good_MNME/len(ssList), 2) * 100) + '%'
          MNME['合格站數'] = good_MNME


    if (var == 'T2'):
       data_dict = {'T2_MBE': MBE, 'T2_MAGE': MAGE}
    elif (var == 'WS'):
       data_dict = {'WS_MBE': MBE, 'WS_RMSE': RMSE}
    elif (var == 'WD'):
       data_dict = {'WD_MNMB': MNMB, 'WD_MNME': MNME}

    return data_dict

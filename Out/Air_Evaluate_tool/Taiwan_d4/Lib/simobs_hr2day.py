import pandas as pd

def simobs_hr2day(obs_in, sim_in, RgTT):

    daytimes = [dd.strftime('%Y-%m-%d') for dd in pd.date_range(RgTT[0], RgTT[1])]

    obs_data={stn: {time:0 for time in range(0, len(daytimes))} for stn in obs_in.columns} 
    sim_data={stn: {time:0 for time in range(0, len(daytimes))} for stn in sim_in.columns} 


    for stn in obs_in.columns:   
       for time in range(0, len(daytimes)):
          hr = 0
          obs_sumdata = 0
          sim_sumdata = 0
          for i in range(0, 24):
             if (obs_in[stn][(time*24)+i] != -999):
                hr += 1
                obs_sumdata += float(obs_in[stn][(time*24)+i])
                sim_sumdata += float(sim_in[stn][(time*24)+i])
          if (hr >= 16) and (obs_sumdata > 0):
             obs_data[stn][time] = round(obs_sumdata/hr, 5)
             sim_data[stn][time] = round(sim_sumdata/hr, 5)
          else:
             obs_data[stn][time] = -999
             sim_data[stn][time] = -999


      
    obs_data = pd.DataFrame(data = obs_data, dtype = 'object')
    obs_data.index   = daytimes
    obs_data.index.name = 'time'

    sim_data = pd.DataFrame(data = sim_data, dtype = 'object')
    sim_data.index   = daytimes
    sim_data.index.name = 'time'

    return obs_data, sim_data

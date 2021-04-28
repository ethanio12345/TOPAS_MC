
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 10:54:48 2019

@author: ethan
"""

import topas2numpy as t2np
import numpy as np
import matplotlib.pyplot as plt

# Flip to match TOPAS order
data = (np.genfromtxt('10_average_beam_data.csv',delimiter=' '))

s_i = 0
e_i = 59

exp_depths = data[0,s_i:e_i]
beam_pdd = data[1,s_i:e_i]/data[1][np.where(exp_depths==10)]*100
beam_error = data[2,s_i:e_i]/data[1][np.where(exp_depths==10)]*100

exp_depths = np.flip(exp_depths)
beam_pdd = np.flip(beam_pdd)
beam_error = np.flip(beam_error)

cyl1 = t2np.BinnedResult('PDDCyl_6.0MV_tar_pcol_scol_ff_monchamb_40x40_10mil.csv')


depths = np.flip(cyl1.dimensions[2].get_bin_centers())
    
dose = np.squeeze(cyl1.data["Mean"])
percent_dose = dose/dose[np.where(depths==10.025)]*100
percent_error = np.squeeze(cyl1.data["Standard_Deviation"])/np.squeeze(cyl1.data["Count_in_Bin"])/dose[np.where(depths==10.025)]*100

#shift for data matching
depths -= 0.025

#set up empty lists
depths_sim = []
dose_sim = []
error_sim = []

#set up for stepped  data extraction
count = np.where(depths==exp_depths[0])[0][0]
for i in range(len(exp_depths)):
    depths_sim.append(depths[count])
    dose_sim.append(percent_dose[count])
    error_sim.append(percent_error[count])
    
    count += 10
#convert to numpy

depths_sim = np.asarray(depths_sim)    

dose_sim = np.asarray(dose_sim)
dose_sim = dose_sim.T

error_sim = np.asarray(error_sim)
error_sim = error_sim.T


total_measurement_error = np.sqrt(error_sim**2 + beam_error**2)




average_dmax = beam_pdd[np.where(exp_depths==1.5)[0]]
sim_dmax = dose_sim[np.where(depths_sim==1.5)]

dif_d_max = (average_dmax - sim_dmax )/ average_dmax * 100
error_dmax = total_measurement_error[np.where(exp_depths==1.5)]

average_d_ten = beam_pdd[np.where(exp_depths==20)]
sim_d_ten = dose_sim[np.where(depths_sim==20)]

dif_d_ten = (average_d_ten - sim_d_ten )/ average_d_ten * 100
error_d_ten = total_measurement_error[np.where(exp_depths==20)]


total_difference = (dose_sim - beam_pdd) / beam_pdd * 100
matching_error = np.abs(total_difference[:-1])



average_matching_error = np.mean(matching_error[:-1])

average_measurement_error = np.mean(total_measurement_error)


total_error = np.sqrt(error_sim**2 + beam_error**2)
average_error = np.average(total_error)



print('%% difference at dmax: %s +- %s \n' % (dif_d_max,error_dmax))
print('%% difference at dten: %s +- %s \n' % (dif_d_ten,error_d_ten))
print('Total Errors (matching +- measurement/simulation): %s \pm %s %% \n' % (average_matching_error, average_measurement_error))
print('Total Overall Error: %s %%' % average_matching_error)


fig, ax = plt.subplots()
ax.set_xlabel('Depth (cm)')
ax.set_ylabel('Dose (%)')

ax.plot(exp_depths,beam_pdd,label='Experimental')
ax.plot(depths,percent_dose,label='tar_pcol_scol_ff_monchamb')
ax.legend()
plt.tight_layout()

#plt.savefig('40x40_10mil_histories.png',dpi=1000)

#fig2, ax = plt.subplots()
#ax.bar(exp_depths,total_error)


plt.show()

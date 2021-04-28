
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 10:54:48 2019

@author: ethan
"""

import topas2numpy as t2np
import numpy as np
import matplotlib.pyplot as plt



data = np.genfromtxt('ChrisOBrien_Linac_Data.csv',delimiter=',')

equiv_square_size = 10

exp_depths = np.arange(0,30.5,0.5)
exp_pdd_10x10 = np.squeeze(data[1:,np.where(data[0]==equiv_square_size)[0]]/100)
exp_pdd_10x10_d10_norm = exp_pdd_10x10  / exp_pdd_10x10[np.where(exp_depths==10)]

#Energies
energies = [5.8,5.9,6.0,6.1,6.2,6.3,6.4,6.5,6.6,6.7]
#energies = [5.8,5.9,6.0,6.1]
#energies = [6.2,6.3,6.4,6.5,6.6,6.7]
#energies = [6.1]

#Field_Zises
#energies = ['10x10','20x20','30x30','40x40']
#energies = ['10x10']


#Historical
#energies = ['tar_pcol','tar_pcol_scol','tar_pcol_scol_ff','tar_pcol_scol_ff_monchamb']

depths = np.zeros([len(energies),600])
dose = np.zeros([len(energies),600])
percent_dose = np.zeros([len(energies),600])
error = np.zeros([len(energies),600])




for i in range(len(energies)):

#    cyl1 = t2np.BinnedResult("10x10_reuse10times/PDDCyl_%sMV.csv" % energies[i])
#    cyl1 = t2np.BinnedResult("10x10_reuse100times/PDDCyl_%sMV.csv" % energies[i])
#    cyl1 = t2np.BinnedResult("10x10_reuse5times_defaultcuts/PDDCyl_%sMV.csv" % energies[i])
#    cyl1 = t2np.BinnedResult("Historical_Model/PHSP_100_Times/PDDCyl_%sMV.csv" % energies[i])
#    cyl1 = t2np.BinnedResult("Historical_Model/PDDCyl_6.0MV_%s.csv" % energies[i])
#    cyl1 = t2np.BinnedResult("PDDCyl_6.0MV_%s.csv" % energies[i])
    cyl1 = t2np.BinnedResult("PDDCyl_%sMV.csv" % energies[i])

    depths[i] = np.flip(cyl1.dimensions[2].get_bin_centers())

    dose[i] = np.squeeze(cyl1.data["Mean"])
    percent_dose[i] = dose[i]/dose[i][np.where(depths[i]==10.025)]
#    error[i] = np.squeeze(cyl1.data["Standard_Deviation"])/cyl1.data["Count_in_Bin"]

#shift for data matching
depths -= 0.025

#set up empty lists
depths_sim = []
dose_sim = []
percent_error_sim = []

#set up for stepped  data extraction
count = 9
for i in range(59):
    depths_sim.append(depths[0][count])
    dose_sim.append(percent_dose[:,count])
    count += 10
#convert to numpy
dose_sim = np.asarray(dose_sim)
dose_sim = dose_sim.T


#flip to match TOPAS depth order
exp_d10 = np.flip(exp_pdd_10x10_d10_norm)
for i in range(len(dose_sim[0])):
    percent_error_sim.append((exp_d10[i]-dose_sim[:,i])/exp_d10[i]*100)
percent_error_sim = np.asarray(percent_error_sim)
percent_error_sim = percent_error_sim.T

#average error for each iteration
average_error = np.average(percent_error_sim,axis=1)

depths += 0.025

fig, ax = plt.subplots()
for i in range(len(depths)):
#    fig, ax = plt.subplots()

    ax.set_xlabel('Depth (cm)')
    ax.set_ylabel('Relative Dose (a.u.)')


    ax.plot(depths[i],percent_dose[i],label=energies[i])
#    print('Dmax position (%s MV): %.3f cm' % (energies[i], depths[0][np.where(percent_dose[i]==percent_dose[i].max())]))

ax.plot(exp_depths,exp_pdd_10x10_d10_norm,label="Experimental")

ax.legend()
fig.tight_layout()
# plt.savefig('10x10PDD_%sMV_5_reusephsp.png' % energies[i], dpi=1000)
#     plt.savefig('10x10PDD_%sMV_10_reusephsp_defaultcuts.png' % energies[i], dpi=1000)
#  plt.savefig('Dose_Comparison_10x10PDD_5.8-6.1_100reuse.png',dpi=1000)
#    plt.savefig('10x10PDD_%s.png' % energies[i],dpi=1000)
#    plt.savefig('6.1MV_%sPDD.png' % energies[i],dpi=1000)

plt.show()

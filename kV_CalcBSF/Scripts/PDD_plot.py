

import numpy as np
import matplotlib.pyplot as plt
import os, argparse


# =============================================================================
#  Parsing command line argument for directory 
# =============================================================================
parser = argparse.ArgumentParser()
parser.add_argument('--dir',
                    default='Results/Tests_for_our_kV/200kVp_30cm_3mmBeWindow_1.9mmCuFilter',
                    action='store',
                    dest='result')
args = parser.parse_args()
print(args.result)
pdd_direc = str(args.result)

######################

######################

#Set path to chosen folder for info


os.chdir("/home/ebutson/TOPAS/kV_CalcBSF/"+pdd_direc)

os.chdir('Combined_Results')
######################

planning = np.genfromtxt('/home/ebutson/TOPAS/kV_CalcBSF/Results/planning_30cmFSD_10cmCone.csv',delimiter=',')

sum_dose = np.genfromtxt("sum_dose.csv",delimiter=",")
pdd_combined = np.genfromtxt("pdd_combined.csv",delimiter=",")
smoothed_pdd = np.genfromtxt("smoothed_pdd.csv",delimiter=",")
cut_down_smoothed_pdd = np.genfromtxt("cut_down_smoothed_pdd.csv",delimiter=",")




plt.figure()

plt.xlabel('Depth (cm)')

plt.plot(planning[:,0],planning[:,1],label='Planning')
#plt.plot(sum_dose[:,0],sum_dose[:,1],label='Sum Dose')
plt.plot(pdd_combined[:,0],pdd_combined[:,1], label='PDD Combined')
plt.plot(smoothed_pdd[:,0],smoothed_pdd[:,1], label='Smoothed PDD')
#plt.plot(cut_down_smoothed_pdd[:,0],cut_down_smoothed_pdd[:,1], label = 'Smoothed Cut down pdd')
plt.legend()

plt.show()

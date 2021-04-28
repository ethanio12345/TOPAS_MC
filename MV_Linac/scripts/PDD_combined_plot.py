import topas2numpy as t2np
import numpy as np
import matplotlib.pyplot as plt
import os

# Set directory also for plot title
directory = 'Measured_FF'
#directory = 'Varian_FF'

energy = 6.0
energy_spread = 0

######################

#os.chdir("/home/ethanb/TOPAS/Linac_Model/output/PDD/"+directory)
os.chdir("/home/ethanb/TOPAS/Linac_Model/output/PDD/")

#os.chdir(str(energy)+"MeV_"+str(energy_spread)+'spread')
######################


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y,box,mode='same')
    return y_smooth

cyl1 = t2np.BinnedResult("/home/ethanb/TOPAS/Linac_Model/mac/PDDCyl.csv")
depth = np.flip(cyl1.dimensions[2].get_bin_centers())


files = {}
for filename in os.listdir():
    if filename.endswith('.csv') and os.stat(filename).st_size != 0:
        file_contents = t2np.BinnedResult(filename)
        files[filename] = file_contents



sum_dose = np.zeros(len(np.squeeze(cyl1.data["Mean"])))
counts_in_bin = np.zeros(len(np.squeeze(cyl1.data["Count_in_Bin"])))

count = 0
for file in files:
    sum_dose += np.squeeze(files[file].data["Sum"])
    counts_in_bin += np.squeeze(files[file].data["Count_in_Bin"])
    count +=1

#comb_array = np.asarray([depth,sum_dose,counts_in_bin])
#
#np.savetxt('pdd_combined.csv',comb_array,delimiter=',')

# Normalised to dmax
pdd = sum_dose/sum_dose.max()
smoothed_pdd = smooth(pdd,6)


tpr = 1.2661*pdd +0.0595
smoothed_tpr = 1.2661*smoothed_pdd +0.0595
tmr = tpr/tpr.max()
smoothed_tmr = smoothed_tpr/smoothed_tpr.max()

#close enough - can average if needed due to bad stats
#Points to depth z_step deeper in phanton

z_step = 30 / len(depth)

d_20_index  = int((30-20)/z_step)
d_10_index  = int((30-10)/z_step)

tpr_20 = (tpr[d_20_index-1]+tpr[d_20_index])/2
tpr_10 = (tpr[d_10_index-1]+tpr[d_10_index])/2


tpr_20_10 = tpr_20/tpr_10

print('d_max: %f' % depth[np.where(pdd==pdd.max())])
print('TPR_{20,10}: %f' % tpr_20_10)


plt.figure(1)


#plt.plot(depth, pdd,label = 'PDD ('+directory+')')
plt.plot(depth, tmr,label = 'TMR ('+directory+')')
#plt.plot(depth, smoothed_pdd, label = 'Smoothed PDD ('+directory+')')


plt.xlabel('Depth (cm)')
plt.legend()
plt.show()

import topas2numpy as t2np
import numpy as np
import matplotlib.pyplot as plt
import os

######################
os.chdir("/home/ethanb/TOPAS/Linac_Model/output/PDD/Measured_FF/6.0MeV")
######################


def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y,box,mode='same')
    return y_smooth


os

cyl1 = t2np.BinnedResult("/home/ethanb/TOPAS/Linac_Model/mac/PDDCyl.csv")
#cyl1 = t2np.BinnedResult("PDDCyl.csv")

depth = np.flip(cyl1.dimensions[2].get_bin_centers())
dose = np.squeeze(cyl1.data["Mean"])

pdd = dose / dose.max()
smoothed_pdd = smooth(pdd,10)
tpr = 1.2661*pdd +0.0595
tmr = tpr/tpr.max()

#close enough - can average if needed due to bad stats
#Points to depth z_step deeper in phanton
z_step = 0.05

d_max_index = int((30-1.5)/z_step)
d_20_index  = int((30-20)/z_step)
d_10_index  = int((30-10)/z_step)


tpr_20 = (tpr[d_20_index-1]+tpr[d_20_index])/2
tpr_10 = (tpr[d_10_index-1]+tpr[d_10_index])/2


tpr_20_10 = tpr_20/tpr_10

print('d_max: %f' % depth[np.where(smoothed_pdd==smoothed_pdd.max())])
print('TPR_{20,10}: %f' % tpr_20_10)

plt.figure(1)
#plt.plot(depth, pdd)
plt.plot(depth, tmr/0.96)
plt.plot(depth, smoothed_pdd)
plt.xlabel('Depth (cm)')

plt.show()

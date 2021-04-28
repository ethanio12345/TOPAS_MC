import topas2numpy as t2np
import numpy as np

import os

######################
os.chdir("/home/ethanb/TOPAS/Linac_Model/output/PDD")
######################


cyl1 = t2np.BinnedResult("../../mac/PDDCyl.csv")
depth = np.flip(cyl1.dimensions[2].get_bin_centers())


files = {}
for filename in os.listdir():
    print(filename,os.stat(filename        ))
    if filename.endswith('.csv') & os.stat(filename).st_size > 0:
        file_contents = t2np.BinnedResult(filename)
        files[filename] = file_contents
        print(filename)
    elif filename == 'pdd_combined.csv':
        pass



sum_dose = np.zeros(len(np.squeeze(cyl1.data["Mean"])))
counts_in_bin = np.zeros(len(np.squeeze(cyl1.data["Count_in_Bin"])))

count = 0
for file in files:
    sum_dose += np.squeeze(files[file].data["Sum"])
    counts_in_bin += np.squeeze(files[file].data["Count_in_Bin"])
    count +=1


comb_array = np.asarray([depth,sum_dose,counts_in_bin])


np.savetxt('pdd_combined.csv',comb_array,delimiter=',')

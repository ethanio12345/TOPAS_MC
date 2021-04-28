import numpy as np
import pandas as pd
import os

header_list = []


for filename in os.listdir():
    if filename.endswith('.header'):
        header_list.append(filename)
    elif "ASCIIOutput_combined.header" in header_list:
        header_list.remove('ASCIIOutput_combined.header')


interim_data = np.zeros([len(header_list),12])
final_data = np.zeros(12)
corresponding_rows = [0,1,2,32,33,34,35,36,37,38,39,40]

count = 0
for header_file in header_list:
    index = 0
    header = pd.DataFrame.to_numpy(pd.read_csv(header_file))
    
    for item in corresponding_rows[:6]:
        interim_data[count][index] = header[item][0].split()[-1]
        index += 1

    for item in corresponding_rows[6:]:
        interim_data[count][index] = header[item][0].split()[-2]
        index += 1
    
    count += 1

#Creating list of compared data
transp = interim_data.T

for item in range(0,6):
    final_data[item] = transp[item].sum()

for item in range(6,9):
    final_data[item] = transp[item].min()

for item in range(9,12):
    final_data[item] = transp[item].max()

#replacing and reconstructing header with final data    
index = 0
reconstruction = []

for row in range(len(header)):
    if row in corresponding_rows[0:5]:
        reconstruction.append(str.replace(header[row][0], 
                                          header[row][0].split()[-1], 
                                          str(int(final_data[index]))))
        index += 1

    elif item in corresponding_rows[5:]:
        reconstruction.append(str.replace(header[row][0], 
                                          header[row][0].split()[-2], 
                                          str(final_data[index])))
        index += 1
    else:
        reconstruction.append(header[row][0])

#Insert file type indicator
reconstruction.insert(0,'TOPAS ASCII Phase Space')

#Insert tab separation for blocks
for i in [1,5,35,39,43]:
    reconstruction.insert(i,"\t")

np.savetxt('ASCIIOutput_combined.header',reconstruction,fmt='%s')

#easiest to combine PHSP with bash; echo >> big_file.phsp


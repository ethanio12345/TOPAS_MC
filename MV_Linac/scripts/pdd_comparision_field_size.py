

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 10:54:48 2019

@author: ethan
"""

import topas2numpy as t2np
import numpy as np
import matplotlib.pyplot as plt


exp_dose = np.genfromtxt('ChrisOBrien_Linac_Data.csv',delimiter=',')


field_sizes = [5,20,30,40]



for field_size in field_sizes:
    
    energy = 6.0 #MV
    
    exp_depths = np.arange(0,30.5,0.5)
    exp_pdd = exp_dose[1:,np.where(exp_dose[0]==field_size)[0]]
    exp_pdd = exp_pdd/exp_pdd[np.where(exp_depths==10)]
    
    
    cyl1 = t2np.BinnedResult("Historical_Model/PHSP_100_Times/PDDCyl_%sx%sMV.csv" % (field_size,field_size))
#    cyl1 = t2np.BinnedResult("PDDCyl_%sx%sMV.csv" % (field_size,field_size))
    depth = np.flip(cyl1.dimensions[2].get_bin_centers())
    dose = np.squeeze(cyl1.data["Mean"])
    percent_dose = dose/dose[np.where(depth==10.025)]
    
    
    fig, ax = plt.subplots()
    ax.plot(depth, percent_dose,label='%s cm square - 6.0MV' %  field_size)
    
    ax.plot(exp_depths,exp_pdd,label="Experimental")
            
    ax.legend()
    ax.set_xlabel('Depth (cm)')
    ax.set_ylabel('Relative Dose (a.u.)')
    fig.tight_layout()
    fig.savefig('Dose_Comparison_6.0MV_%scm_square.png' % field_size,dpi=1000)
    fig.show()
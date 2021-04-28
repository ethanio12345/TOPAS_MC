#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 30 10:54:48 2019

@author: ethan
"""

import topas2numpy as t2np
import numpy as np
import matplotlib.pyplot as plt

#energies = [5.8,5.9,6.0,6.1,6.2,6.3,6.4,6.5,6.6,6.7]
#energies = [5.9]
#energies = [5,10,20,30,40]
energies = [30]

for energy in energies:
#    surface_data = np.genfromtxt('10x10_reuse100times/Voxel_top_1cm_6.0MV_%sx%sMV.csv' % (energy,energy),delimiter=',')
#    surface_data = np.genfromtxt('Voxel_top_1cm_6.0MV_%sx%sMV.csv' % (energy,energy),delimiter=',')
#    surface_data = np.genfromtxt('Historical_Model/PHSP_10_Times/Voxel_dmax_%sx%s.csv' % (energy,energy),delimiter=',')
    surface_data = np.genfromtxt('Voxel_dmax_%sx%s_d10.csv' % (energy,energy),delimiter=',')
#    
    #Split along y column, +1 to account for zero indexing
    
    split_data = np.split(surface_data,np.max(surface_data[:,1])+1)
    
    central_axis_index = (np.max(surface_data[:,1])+1)/2 - 1
    
#    print("Central axis is %s" % central_axis_index)
    
    central_axis_data = split_data[20].T
    
    fig, ax = plt.subplots()
#    ax.plot(central_axis_data[1],
#             central_axis_data[3]/max(central_axis_data[3]),
#             label='%s MV' % energy)    
    ax.plot(central_axis_data[1]-25,
             central_axis_data[3]/max(central_axis_data[3]),
             label='%s cm' % energy)

    ax.set_xlabel('Distance from central axis (cm)')
    ax.set_ylabel('Relative Dose (a.u.)')
    ax.legend()
    fig.tight_layout()
    plt.plot(axis_dist,axis_pdd_30x30/100)
#    fig.savefig('Voxel_top_1cm_6.0MV_%sx%s.png' % (energy,energy), dpi=1000)
#    fig.savefig('Voxel_top_1cm_%sMV.png' % energy, dpi=1000)
    fig.savefig('Voxel_d_max_%sx%s_d10.png' % (energy,energy), dpi=1000)
    

plt.show()

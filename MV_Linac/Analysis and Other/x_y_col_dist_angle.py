#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 11 16:22:00 2019

@author: ethan
"""
import numpy as np

x_ssd = 45
y_ssd = 55


field_sizes = np.array([5,10,20,30,40])


for field_size in field_sizes:
    x_dist = x_ssd * (field_size/2) / 100 + 10
    
    y_dist = y_ssd * (field_size/2) / 100 + 10
    
    col_angle = np.arctan(field_size/2 / 100) * 180/np.pi
    
    print("""
          
    
          Field size: %s cm square""" % field_size)
    
    print("""
          X Col Angle = %f deg \n
          X Col Distance = %s cm \n
          Y Col Distance = %s cm""" % (col_angle, x_dist, y_dist)
          )

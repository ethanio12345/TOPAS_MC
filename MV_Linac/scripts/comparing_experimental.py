#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 21:39:06 2019

@author: ethan
"""

import numpy as np
import matplotlib.pyplot as plt

experimental_labels=np.array(['TrueBeam','21IXS','6EX'])

ten_depths = np.array([1.5,5,10,20])
fourty_depths = np.array([1.2,5,10,20])

ten_by_ten_data = np.array(
        [
        [1,0.868577609518659,0.668469442942131,0.379989183342347],
        [1,0.868510867612718,0.67001975929585,0.383797377402551],
        [1,0.862175413110587,0.664063918648992,0.376429998184129]
        ]
        )

fourty_by_fourty_data = np.array(
        [
        [1,0.884145320609409,0.708354260840449,0.433484011384564],
        [1,0.881038448899113,0.707854091357213,0.437265856063096],
        [1,0.881038448899113,0.707854091357213,0.437265856063096]
        ]
        )

simulated_labels = np.array(['tar_pcol','tar_pcol_scol','tar_pcol_scol_ff','tar_pcol_scol_ff_monchamb'])

d_max_position = np.array([1.475,1.325,1.375,1.575])

d_max_dose_sim = np.array([2.85207223e-16,1.75498812e-16,1.48939649e-16,1.37002611e-16])


plt.plot(ten_depths,ten_by_ten_data[0])

plt.show()

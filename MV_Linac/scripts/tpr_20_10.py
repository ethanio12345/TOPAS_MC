#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 13:07:49 2020

@author: ethanb
"""

import topas2numpy as t2np
import numpy as np




def tpr_20_10(filename):
    cyl1 = t2np.BinnedResult(filename)

    depth = np.flip(cyl1.dimensions[2].get_bin_centers())
    dose = np.squeeze(cyl1.data['Mean'])

    d_max = depth[np.where(dose==dose.max())]
    z_step = 30 / len(depth)

    d_20_index  = int((30-20)/z_step)
    d_10_index  = int((30-10)/z_step)

    d_20 = (dose[d_20_index-1]+dose[d_20_index])/2
    d_10 = (dose[d_10_index-1]+dose[d_10_index])/2

    tpr_20_10 = 1.2661*d_20/d_10 + 0.0595
    return tpr_20_10

def print_tpr_20_10():
    print('d_max: %.3f cm' % d_max )
    print('TPR_{20,10}: %.3f' % tpr_20_10)

def main(filename):
    tpr_20_10(filename)
    print_tpr_20_10()

if __name__ == '__main__':
    main()

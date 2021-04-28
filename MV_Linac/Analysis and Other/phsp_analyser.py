#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 14:15:22 2019

@author: ethan
"""
import csv
import numpy as np

def generate_for_phsp(csv_file):
    with open(csv_file) as infile:

        e_energy = []
        gamma_energy = []
        particle_num_e = 0
        particle_num_g = 0

        for lines in infile:
            line = lines.split()
            
            p_energ = float(line[5])
            p_weight = float(line[6])
            
            if line[7] == '22':
                gamma_energy.append(float(p_energ*p_weight))
                particle_num_g += p_weight
            
            if line[7] == '11':
                e_energy.append(p_energ*p_weight)
                particle_num_e += p_weight
            

    return e_energy, gamma_energy, [particle_num_e,particle_num_g]


######################

#Set path to chosen folder for info

os.chdir("/home/ebutson/TOPAS/MV_Linac/output/Small_PDD_no_blob")


######################

                
e_energy, gamma_energy, particle_weights = generate_for_phsp('ASCIIOutput_5.9MV.phsp')

print('''
      Mean Elec energy: %.4s MeV \n
      Mean Gamma energy: %.4s MeV''' % 
      (sum(particle_energies[0])/particle_weights[0], 
       sum(particle_energies[1])/particle_weights[1])
      )

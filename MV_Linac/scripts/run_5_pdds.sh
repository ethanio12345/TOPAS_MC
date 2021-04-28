#!/bin/bash

cd ~/TOPAS/Linac_Model/output/PHSP

for run in {1..5}
do
  topas ~/TOPAS/Linac_Model/mac/linac_model_pdd.topas
done

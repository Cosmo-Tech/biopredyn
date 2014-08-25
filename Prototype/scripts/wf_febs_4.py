#!/usr/bin/env python
# coding=utf-8

import libsbml
from biopredyn import resources, result as res
import csv

# required data values
data_file = 'artificial_data.txt'
calibration_file = 'calibration_data.txt'
validation_file = 'validation_data.txt'

rm = resources.ResourceManager()
data = res.Result()
metabolites = data.import_from_csv_file(
  data_file, rm, separator=',', alignment='column')

cal = open(calibration_file, "w")
cal_writer = csv.writer(cal, delimiter=',')
cal_writer.writerow(metabolites)
val = open(validation_file, "w")
val_writer = csv.writer(val, delimiter=',')
val_writer.writerow(metabolites)

for l in range(len(data.get_time_steps())):
  row = []
  for m in metabolites:
    row.append(data.get_quantities_per_species(m)[l])
  if l%2 == 0: # even case
    cal_writer.writerow(row)
  else: # odd case
    val_writer.writerow(row)

cal.close()
val.close()

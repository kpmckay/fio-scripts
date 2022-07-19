#!/usr/bin/env python3

import sys
import os
import argparse
import csv
import subprocess
import json

if __name__ == '__main__':

   parser = argparse.ArgumentParser(
      description='Runs FIO jobs specified in a CSV file and parses the results.')

   parser.add_argument('out', metavar='<Output Directory>', 
      help='Output directory for FIO jobs')

   (args) = parser.parse_args()

   fiojobs = []   # Will hold lists of FIO jobs to run 

   os.chdir(args.out)

   for f in os.listdir(os.getcwd()):
       # checking if it is a file
       if f.endswith("summary.log"):
           fiojobs.append(f)

   # Put some basic results in a summary
   summary = open("fio_summary.csv", "w")

   modes = ['read', 'write', 'trim']
   stats = ['iops', 'iops_min', 'iops_max', 'iops_mean', 'iops_stddev',
            'bw', 'bw_min', 'bw_max', 'bw_mean', 'bw_dev']

   header = ['Test']
   for mode in modes:
      for stat in stats:
         header.append(mode + "_" + stat)
      header.append(mode + '_clat_ns_min')
      header.append(mode + '_clat_ns_max')
      header.append(mode + '_clat_ns_mean')
      header.append(mode + '_clat_ns_stddev')
      header.append('compress_pct')
   summary.write(','.join(header) + "\n")

   for logfile in fiojobs:
      with open(logfile, "r") as summaryfile:
         x = summaryfile.read()
         if len(x) > 0:
            j = json.loads(x)
            for job in j['jobs']:
               values = []
               values.append(job['jobname'])
               for mode in modes:
                  for stat in stats:
                     values.append(str(job[mode][stat]))
                  values.append(str(job[mode]['clat_ns']['min']))
                  values.append(str(job[mode]['clat_ns']['max']))
                  values.append(str(job[mode]['clat_ns']['mean']))
                  values.append(str(job[mode]['clat_ns']['stddev']))
               values.append(job['job options']['buffer_compress_percentage'])
               summary.write(','.join(values) + "\n")         
      summaryfile.close()
   summary.close()

print("\nComplete\n")
sys.exit()

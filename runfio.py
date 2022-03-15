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

   parser.add_argument('ssd', metavar='<NVMe Device>',
      help='NVMe device to test (/dev/...')
   parser.add_argument('csv', metavar='<CSV File>',
      help='CSV file containing FIO job parameters')
   parser.add_argument('out', metavar='<Output Directory>', 
      help='Output directory for FIO jobs')
   parser.add_argument('-p', '--parse-only', dest='parse_only', action='store_true',
      help='Parse CSV only')

   parser.set_defaults(parse_only='store_false')
   (args) = parser.parse_args()

   headers = []   # Will hold CSV header values 
   fiojobs = []   # Will hold lists of FIO jobs to run 

   with open(args.csv, newline='') as csvfile:
      csvdata_raw = csv.reader(csvfile, delimiter=',')

      # Remove comments and empty lines from the input CSV
      for row in csvdata_raw:
         if str(row[0]).startswith("#"):
            continue
         elif str(row[0]).isspace():
            continue
         elif not headers:
            headers = row   # Headers must come first 
         else:
            fiojobs.append(row)

      csvfile.close()

   # Create output path
   path = os.path.join(os.path.dirname(os.path.abspath(__file__)), str(args.out))
   if os.path.exists(path):
      print("Output path already exists. Please move it, rename it, or choose another path")
      sys.exit()
   else:
      os.makedirs(path)

   fiofiles = []   # Will hold set of FIO files to run

   for job in fiojobs:

      # The first column must be the filename, second column the testname, and third column whether to format
      if job[0] in fiofiles:   
         fiofile = open(os.path.join(args.out, str(job[0]).strip()), 'a')   # We are appending to an existing file
         fiofile.write("\n" + "[" + str(job[1]).strip() + "]\n") 
      else:
         fiofile = open(os.path.join(args.out, str(job[0]).strip()), 'w+')   # We are writing a new file
         if (str(job[2]).strip()).lower() == 'y' or (str(job[2]).strip()).lower() == 'yes':
            fiofile.write("#FORMAT: Device will be formatted before the test(s) below\n")
         fiofile.write("[" + str(job[1]).strip() + "]\n") 
         fiofiles.append(job[0])

      fiofile.write("filename=" + str(args.ssd) + "\n") 

      # Columns can be in any order after that...
      for i in range(len(headers)):
         if i < 3:   # We took care of these special cases above... 
            continue
         elif str(job[i]) == '' or str(job[i]).isspace():
            continue
         elif (str(job[i]).strip()).lower() == 'n' or (str(job[i]).strip()).lower() == 'no':
            continue
         elif (str(job[i]).strip()).lower() == 'y' or (str(job[i]).strip()).lower() == 'yes':
            fiofile.write(str(headers[i]).strip() + "\n")
         else:
            fiofile.write(str(headers[i]).strip() + "=" + str(job[i]).strip() + "\n")

      fiofile.close()

   if args.parse_only is True:
      sys.exit()

   os.chdir(args.out)

   # Run the FIO jobs
   for job in fiofiles:
      with open(str(job).strip()) as fiofile:
          if 'FORMAT' in fiofile.read():
             subprocess.run(["nvme", "format", str(args.ssd), "--ses=1", "-f"])
      fiofile.close()
      subprocess.run(["fio", str(job).strip(), "--output-format=json+",
         "--output=" + str(job).strip() + ".summary.log"]) 

   # Put some basic results in a summary
   summary = open("fio_summary.csv", "w+")

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
   summary.write(','.join(header) + "\n")

   for job in fiofiles:
      with open(str(job).strip() + ".summary.log") as summaryfile:
         j = json.loads(summaryfile.read())
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
         summary.write(','.join(values) + "\n")         
      summaryfile.close()
   summary.close()

print("\nComplete\n")
sys.exit()

#!/usr/bin/env python3

import sys
import os
import argparse
import csv
import subprocess

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

   headers  = []   # Will hold CSV header values 
   fiojobs  = []   # Will hold lists of FIO jobs to create
   fiofiles = []   # Will hold list if FIO files to run

   with open(args.csv, newline='') as csvfile:
      csvdata = csv.reader(csvfile, delimiter=',')
      # Remove comments and empty lines from the input CSV
      for row in csvdata:
         # Convert everything to lowercase and remove any leading/trailing spaces
         row = [(x.lower()).strip() for x in row]
         if str(row[0]).startswith("#"):
            continue
         if row == []:
            continue
         elif not headers:
            headers = row 
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

   # Build the job files
   for job in fiojobs:
      test = str(job[headers.index('file')])
      nvmf = str(job[headers.index('format')])
      name = str(job[headers.index('job')])
      # Check if a format is needed before running the job file 
      if nvmf.startswith("y") or nvmf.startswith("1") or nvmf.startswith("t"):
         test = "format-" + test 
      if test not in fiofiles and ("format-" + test) not in fiofiles:
         fiofiles.append(test)
      # Open FIO file to write
      fiofile = open(os.path.join(args.out, test), 'a')
      # Print the job name
      fiofile.write("\n" + "[" + name + "]\n")
      # Populate the drive to test
      fiofile.write("filename=" + str(args.ssd) + "\n") 
      # Fill in the rest of the values...
      for i in range(len(job)):
         # Special cases taken care of separately
         if i == headers.index('file'):
            continue
         elif i == headers.index('job'):
            continue
         elif i == headers.index('format'):
            continue
         # Everything else...
         elif str(job[i]) == '' or str(job[i]).isspace():
            continue
         elif (str(job[i]).startswith("n") or str(job[i]).startswith("0") or str(job[i]).startswith("f")):
            continue
         elif (str(job[i]).startswith("y") or str(job[i]).startswith("1") or str(job[i]).startswith("t")):
            fiofile.write(str(headers[i]) + "\n")
         else:
            fiofile.write(str(headers[i]) + "=" + str(job[i]) + "\n")
      fiofile.close()

   if args.parse_only is True:
      sys.exit()

   os.chdir(args.out)

   # Run the FIO jobs
   for fio in fiofiles:
      if fio.startswith("format-"):   
          subprocess.run(["nvme", "format", str(args.ssd), "--ses=1", "-f"])
      subprocess.run(["fio", fio, "--output-format=json+",
         "--output=" + fio + ".summary.log"]) 

print("\nComplete\n")
sys.exit()

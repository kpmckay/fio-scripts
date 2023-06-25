# fio-scripts
A collection of FIO scripts and canned test cases.

## runfio.py
This script takes a CSV file containing FIO test definitions and runs them. This allows a long sequence of tests to be configured and managed from a single file. The CSV file expects the first three columns to be (1) the filename for the FIO job file, (2) the job name that goes into the FIO job file, and (3) whether to format the drive prior to executing the FIO job file. After that, columns contain an arbitrary number of FIO parameter values in any order. The header contains the FIO parameter, and each row contains the value for that parameter. For FIO parameters that don't take a value, their inclusion in a test is indicated by adding a 'Y' or 'Yes' as the value (alternatively, a value of 1 can be used as well).

CSV files will generally take the following form:

| file          | test      | format | fio_option_1 | fio_option_2 | ... | fio_option_n |
| ------------- | --------- | ------ | ------------ | ------------ | --- | ------------ |
| filename1.fio | testname1 | yes    | option_value | option_value | ... | option_value |
| filename1.fio | testname2 | yes    | option_value | option_value | ... | option_value |
| filename2.fio | testname3 | yes    | option_value | option_value | ... | option_value |
| filename2.fio | testname4 | yes    | option_value | option_value | ... | option_value |

In the above example, two FIO control files would be generated, each with two tests.

Plugging in some actual FIO options, an example CSV may look something like the following: 

| file          | test             | format | rw       | bs   | ... | norandommap | time_based | ... |
| ------------- | ---------------- | ------ | -------- | ---- | --- | ----------- | ---------- | --- |
| 4k_random.fio | ran_precondition | yes    | ranwrite | 4k   | ... |             |            | ... |
| 4k_random.fio | ran_write        |        | ranwrite | 4k   | ... | Yes         | Yes        | ... |
| 4k_random.fio | ran_read         |        | ranread  | 4k   | ... | Yes         | Yes        | ... |
| 128k_seq.fio  | seq_precondition | yes    | write    | 128k | ... |             |            | ... |
| 128k_seq.fio  | seq_write        |        | write    | 128k | ... |             | Yes        | ... |
| 128k_seq.fio  | seq_read         |        | read     | 128k | ... |             | Yes        | ... |


As mentioned above, each test is added to the specified file. If more than one test is added to a file, then the flow of tests needs to be controlled with the stonewall option and the reporting groups setup as desired. Typically, one file per test is recommended unless the two tests run concurrently (e.g. mixed workloads using multiple jobs).

### Usage
`python3 runfio.py [-h] [-p] [-c] <Device> <CSV File> <Output Directory>`

The -p option will create the FIO control files without attempting to run them. When developing new test cases, it's best to review the FIO control files for correctness prior to running them.

THe -c option passes a "buffer_compress_percentage" option to the generated FIO control files (see section below).

## Compression Settings
ScaleFlux devices support transparent compression. By default, FIO injects a percentage of zeroes every 512-bytes when using the "buffer_compress_percentage" option (assuming default "buffer_compress_chunk" value). This is sufficient for testing performance with compressible data. The following table maps the "buffer_compress_percentage" setting to the achieved compression ratio on two generations of ScaleFlux devices:

| buffer_compress_percentage	| CSD 2000 CR | CSD 3000 CR |
|----------------------------|-------------|-------------|
| 0 | 1 | 1 |
| 1 | 1 | 1 |
| 2 | 1 | 1 |
| 3 | 1 | 1 |
| 4 | 1 | 1 |
| 5 | 1 | 1 |
| 6 | 1 | 1 |
| 7 | 1 | 1 |
| 8 | 1 | 1 |
| 9 | 1 | 1 |
| 10 | 1	| 1 |
| 11 | 1.04 | 1.07 |
| 12 | 1.07 | 1.08 |
| 13 | 1.08 | 1.1 |
| 14 | 1.09 | 1.11 |
| 15 | 1.1 |	1.12 |
| 16 | 1.12 | 1.13 |
| 17 | 1.13 | 1.15 |
| 18 | 1.14 | 1.16 |
| 19 | 1.15 | 1.18 |
| 20 | 1.17 | 1.19 |
| 21 | 1.18 | 1.2 |
| 22 | 1.19 | 1.22 |
| 23 | 1.2 |	1.23 |
| 24 | 1.22 | 1.25 |
| 25 | 1.23 | 1.26 |
| 26 | 1.25 | 1.28 |
| 27 | 1.27 | 1.3 |
| 28 | 1.28 | 1.32 |
| 29 | 1.3 |	1.33 |
| 30 | 1.31 | 1.35 |
| 31 | 1.33 | 1.37 |
| 32 | 1.34 | 1.39 |
| 33 | 1.37 | 1.41 |
| 34 | 1.39 | 1.43 |
| 35 | 1.4 |	1.45 |
| 36 | 1.42 | 1.47 |
| 37 | 1.45 | 1.49 |
| 38 | 1.46 | 1.52 |
| 39 | 1.48 | 1.54 |
| 40 | 1.5 |	1.57 |
| 41 | 1.53 | 1.59 |
| 42 | 1.56 | 1.62 |
| 43 | 1.58 | 1.64 |
| 44 | 1.6 |	1.67 |
| 45 | 1.63 | 1.7 |
| 46 | 1.66 | 1.73 |
| 47 | 1.68 | 1.76 |
| 48 | 1.7 |	1.79 |
| 49 | 1.74 | 1.8 |
| 50 | 1.77 | 1.82 |
| 51 | 1.79 | 1.9 |
| 52 | 1.82 | 1.94 |
| 53 | 1.86 | 1.97 |
| 54 | 1.91 | 2.02 |
| 55 | 1.94 | 2.05 |
| 56 | 1.98 | 2.07 |
| 57 | 2 | 2.15 |
| 58 | 2.05 | 2.19 |
| 59 | 2.1 | 2.23 |
| 60 | 2.15 | 2.29 |
| 61 | 2.17 | 2.31 |
| 62 | 2.22 | 2.36 |
| 63 | 2.26 | 2.47 |
| 64 | 2.31 | 2.54 |
| 65 | 2.34 | 2.6 |
| 66 | 2.46 | 2.67 |
| 67 | 2.53 | 2.71 |
| 68 | 2.58 | 2.78 |
| 69 | 2.62 | 2.85 |
| 70 | 2.7 | 2.99 |
| 71 | 2.77 | 3.04 |
| 72 | 2.88 | 3.13 |
| 73 | 2.9 | 3.24 |
| 74 | 3.03 | 3.33 |
| 75 | 3.09 | 3.41 |
| 76 | 3.19 | 3.68 |
| 77 | 3.25 | 3.81 |
| 78 | 3.39 | 3.95 |
| 79 | 3.65 | 4.1 |
| 80 | 3.76 | 4.25 |
| 81 | 3.89 | 4.43 |
| 82 | 4 | 4.72 |
| 83 | 4.26 | 4.9 |
| 84 | 4.41 | 5.13 |
| 85 | 4.65 | 5.44 |
| 86 | 4.77 | 5.61 |
| 87 | 5.04 | 5.92 |
| 88 | 5.33 | 6.75 |
| 89 | 5.61 | 7.21 |
| 90 | 5.85 | 7.72 |
| 91 | 6.46 | 8 |
| 92 | 7.12 | 8 |
| 93 | 7.61 | 8 |
| 94 | 8.23 | 8 |
| 95 | 9.5 | 8 |
| 96 | 10.36 | 8 |
| 97 | 12.05 | 8 |
| 98 | 13.53 | 8 |
| 99 | 18.47 | 8 |
| 100 | 28.44 | 8 |

## Terse Output Headers
Column headers for terse output. Depending on how many latency buckets are used in an FIO job, some latency percentile buckets may need to be deleted to aligne with the output data.

```Results Version,FIO Version,Job Name,Group ID,Error,Total KB Read,Read Bandwidth KB/s,Read IOPS,Read Runtime,Min Read Submission Latency,Max Read Submission Latency,Avg Read Submission Latency,Std Read Submission Latency,Min Read Completion Latency,Max Read Completion Latency,Avg Read Completion Latency,Std Read Completion Latency,Read Percentile Bucket 0,Read Percentile Bucket 1,Read Percentile Bucket 2,Read Percentile Bucket 3,Read Percentile Bucket 4,Read Percentile Bucket 5,Read Percentile Bucket 6,Read Percentile Bucket 7,Read Percentile Bucket 8,Read Percentile Bucket 9,Read Percentile Bucket 10,Read Percentile Bucket 11,Read Percentile Bucket 12,Read Percentile Bucket 13,Read Percentile Bucket 14,Read Percentile Bucket 15,Read Percentile Bucket 16,Read Percentile Bucket 17,Read Percentile Bucket 18,Read Percentile Bucket 19,Min Total Read Latency,Max Total Read Latency,Avg Total Read Latency,Std Total Read Latency,Minimum Read Bandwidth,Maximum Read Bandwidth,Aggregate Percentage Read Bandwidth,Mean Read Bandwidth,Read Bandwidth Standard Deviation,Total KB Written,Write Bandwidth KB/s,Write IOPS,Write Runtime,Min Write Submission Latency,Max Write Submission Latency,Avg Write Submission Latency,Std Write Submission Latency,Min Write Completion Latency,Max Write Completion Latency,Avg Write Completion Latency,Std Write Completion Latency,Write Percentile Bucket 0,Write Percentile Bucket 1,Write Percentile Bucket 2,Write Percentile Bucket 3,Write Percentile Bucket 4,Write Percentile Bucket 5,Write Percentile Bucket 6,Write Percentile Bucket 7,Write Percentile Bucket 8,Write Percentile Bucket 9,Write Percentile Bucket 10,Write Percentile Bucket 11,Write Percentile Bucket 12,Write Percentile Bucket 13,Write Percentile Bucket 14,Write Percentile Bucket 15,Write Percentile Bucket 16,Write Percentile Bucket 17,Write Percentile Bucket 18,Write Percentile Bucket 19,Min Total Write Latency,Max Total Write Latency,Avg Total Write Latency,Std Total Write Latency,Minimum Write Bandwidth,Maximum Write Bandwidth,Aggregate Percentage Write Bandwidth,Mean Write Bandwidth,Standard Deviation Write Bandwidth,CPU User,CPU Sys,Unused,Unused,Unused,1 IO Depth,2 IO Depth,4 IO Depth,8 IO Depth,16 IO Depth,32 IO Depth,64 IO Depth,2us Latency,4us Latency,10us Latency,20us Latency,50us Latency,100us Latency,250us Latency,500us Latency,750us Latency,1ms Latency,2ms Latency,4ms Latency,10ms Latency,20ms Latency,50ms Latency,100ms Latency,250ms Latency,500ms Latency,750ms Latency,1s Latency,2s Latency,>2s Latency,Device Name,Disk Read IOPS,Disk Write IOPS,Disk Read Merges,Disk Write Merges,Disk Read Ticks,Disk Write Ticks,Disk Queue Time,Disk Utilization```

# fio-scripts
A collection of FIO test cases and a Python script to run them.

## runfio.py
This script takes a CSV file of containing FIO test definitions and runs them. The CSV file expects the first three columns to be (1) the filename for the FIO job file, (2) the job name that goes into the FIO job file, and (3) whether to run an NVMe Format (with --ses=1) prior to executing the FIO job file. After that, columns contain FIO parameter values in any order. The header is the FIO parameter, and each row contains the value. To add FIO parameters that don't take a value, mark the desired row value with a 'Y' or 'Yes' to include it as a parameter for the job.

Example CSV Format:
| File    | Test             | Format | rw    | bs   | jobs | iodepth | direct | norandommap | ioengine | time_based | runtime | loops | new_group | group_reporting | stonewall |
| ------- | ---------------- | ------ | ----- | ---- | ---- | ------- | ------ | ----------- | -------- | ---------- | ------- | ----- | --------- | --------------- | --------- |
| ran.fio | ran_precondition | yes    | write | 4k   | 8    | 32      | 1      |             | io_uring |            |         | 5     |           | Yes             |           |
| ran.fio | random_write     |        | write | 4k   | 8    | 32      | 1      | Yes         | io_uring | Yes        | 3600    |       | Yes       | Yes             | Yes       |
| ran.fio | random_read      |        | read  | 4k   | 8    | 32      | 1      | Yes         | io_uring | Yes        | 3600    |       | Yes       | Yes             | Yes       |
| seq.fio | seq_precondition | yes    | write | 128k | 1    | 64      | 1      |             | io_uring |            |         | 2     |           | Yes             |           |
| seq.fio | seq_write        |        | write | 128k | 1    | 64      | 1      |             | io_uring | Yes        | 3600    |       | Yes       | Yes             | Yes       |
| seq.fio | seq_read         |        | read  | 128k | 1    | 64      | 1      |             | io_uring |            | 3600    |       | Yes       | Yes             | Yes       |

As mentioned above, each test is added to the specified file. If more than one test is added to a file, then the flow of tests needs to be controlled with the stonewall option and the reporting groups setup as desired. Typically, one file per test is recommended unless the two tests run concurrently (e.g. mixed workloads using multiple jobs).

### Usage
`python3 runfio.py [-h] [-p] <NVMe Device> <CSV File> <Output Directory>`

-p: Parse only - Just create the FIO job files, but don't run them.

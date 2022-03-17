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
`python3 runfio.py [-h] [-p] <Device> <CSV File> <Output Directory>`

The -p option will create the FIO control files without attempting to run them. When developing new test cases, it's best to review the FIO control files for correctness prior to running them.





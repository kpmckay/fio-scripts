import os
import json
import csv
import argparse

def parse_log_file_mode_based(file_path, mode='default'):
    with open(file_path, 'r') as f:
        lines = f.readlines()

    if not lines[0].strip().startswith('{'):
        lines = lines[1:]
    json_str = ''.join(lines)

    try:
        log_data = json.loads(json_str)
    except json.JSONDecodeError:
        print(f"Skipping file due to JSON decode error: {file_path}")
        return {}

    extracted_data = {}

    for job in log_data.get('jobs', []):
        extracted_data['jobname'] = job.get('jobname', 'Unknown')
        extracted_data['iodepth'] = job.get('job options', {}).get('iodepth', None)
        extracted_data['bs'] = job.get('job options', {}).get('bs', None)

        if mode == 'default':
            for rw_mode in ['read', 'write']:
                for key_metric in ['iops', 'bw']:
                    key = f"{rw_mode}_{key_metric}"
                    value = job.get(rw_mode, {}).get(key_metric, None)

                    # Convert read_bw and write_bw from KiB/s to MB/s
                    if key_metric == 'bw':
                        value = (value * 1024) / (1000 ** 2) if value else None

                    extracted_data[key] = value

                if rw_mode == 'read':
                    clat_ns_percentiles = job.get(rw_mode, {}).get('clat_ns', {}).get('percentile', {})
                    for percentile in ["99.000000", "99.900000", "99.990000", "99.999000", "99.999900"]:
                        key = f"{rw_mode}_clat_ns_{percentile}"
                        value = clat_ns_percentiles.get(percentile, None)

                        # Convert latency from ns to ms
                        value = value / 1_000_000 if value else None

                        extracted_data[key] = value

    return extracted_data

def write_to_csv(data_list, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = list(data_list[0].keys())
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for data in data_list:
            writer.writerow(data)

def main(input_dir):
    log_files = [f for f in os.listdir(input_dir) if f.endswith('summary.log')]

    # Sort files by modification time
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(input_dir, x)))

    all_extracted_data = []

    for log_file in log_files:
        log_file_path = os.path.join(input_dir, log_file)
        extracted_data = parse_log_file_mode_based(log_file_path, mode='default')
        if extracted_data:
            all_extracted_data.append(extracted_data)

    csv_file_path = os.path.join(input_dir, 'parsed_summary.csv')
    write_to_csv(all_extracted_data, csv_file_path)
    print(f"CSV file has been written to {csv_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Parse summary log files into a CSV.')
    parser.add_argument('input_dir', type=str, help='Path to the directory containing the summary log files.')

    args = parser.parse_args()
    main(args.input_dir)

#!/usr/bin/env python3
import os
import sys
import ast
import json
import csv


od_path = 'cfg/different_schedulers/no_miss_output_results'
scedulers = ['default', 'rr', 'lru', 'faint']
sched_info_dict = {}
for sched in scedulers:
    sched_od_path = f'{od_path}/{sched}'
    file_paths = os.listdir(sched_od_path)
    file_paths = [f for f in file_paths if 'statistics_dict' in f]
    # print(file_paths)
    for fp in file_paths:
        with open(f'{sched_od_path}/{fp}') as f:
            # Load the contents of the file as a Python dictionary
            run_data = json.load(f)
        # Extract relevant info:
        num_threads    = run_data['num_threads']
        single_threads_average_cpi = 0
        for key, value in run_data['threads'].items():
            single_threads_average_cpi += run_data['threads'][key]["CPI"]
        single_threads_average_cpi = single_threads_average_cpi / num_threads
        single_threads_average_ipc = 1 / single_threads_average_cpi
        cpi    = run_data['system'].get('System CPI',None)
        fairness = run_data['system'].get('Jain\'s fairness index',None)
        ipc    = 1/cpi if cpi else None
        util_d = run_data['system']['Units Utilization']
        util   = sum(util_d.values()) + util_d['unit alu utilization %'] + util_d['unit alu_st_ld utilization %']
        util   = util/11
        if len(util_d.values())!=9:
            print("ERR:")
            print(fp)
        data_tuple = (num_threads, ipc, fairness, util, single_threads_average_ipc)
        if sched not in sched_info_dict:
            sched_info_dict[sched] = []
        sched_info_dict[sched].append(data_tuple)

for v in sched_info_dict.values():
    v.sort(key=lambda x:x[0])
# print(sched_info_dict)
# sys.exit()
    
import time
cur_time_stamp = time.strftime('_%b_%d_%H%M', time.localtime(time.time()))
with open(f'cfg/different_schedulers/statistics/different_schedulers_stats{cur_time_stamp}.csv', 'w') as f:
    write = csv.writer(f)
    headers = []
    keys = list(sched_info_dict.keys())
    for k in keys:
        headers = headers + [k,'']
    write.writerow(headers)
    write.writerow(['Thread#','IPC', 'Fairness', 'Average Utilization', 'Single Thread Average IPC']*len(keys))

    maxl = max([len(v) for v in sched_info_dict.values()])
    for i in range(maxl):
        row = []
        for k in keys:
            if i < len(sched_info_dict[k]):
                row = row + [sched_info_dict[k][i][0],sched_info_dict[k][i][1],sched_info_dict[k][i][2],sched_info_dict[k][i][3],sched_info_dict[k][i][4]]
            else:
                row = row + ['','']
        write.writerow(row)


#!/usr/bin/env python3
import os
import sys
import ast
import json
import csv

od_path = 'cfg/increasing_threads/output_results/'
file_paths = os.listdir(od_path)
file_paths = [f for f in file_paths if 'statistics_dict' in f]

bench_dict_ipc = {}
bench_dict_util = {}
for fp in file_paths:
    with open(f'{od_path}{fp}') as f:
        run_data = ast.literal_eval(f.read())
    num    = run_data['num_threads']
    bench  = run_data['threads']['thread0']['Name']
    cpi    = run_data['system'].get('System CPI',None)
    ipc    = 1/cpi if cpi else None
    util_d = run_data['system']['Units Utilization']
    util   = sum(util_d.values()) + util_d['unit alu utilization %'] + util_d['unit alu_st_ld utilization %']
    util   = util/11
    if len(util_d.values())!=9:
        print("ERR:")
        print(fp)
    if bench not in bench_dict_ipc:
        bench_dict_ipc[bench] = []
    if bench not in bench_dict_util:
        bench_dict_util[bench] = []
    if ipc:
        bench_dict_ipc[bench].append((num , ipc ))
    bench_dict_util[bench].append((num  , util))
for v in bench_dict_ipc.values():
    v.sort(key=lambda x:x[0])
for v in bench_dict_util.values():
    v.sort(key=lambda x:x[0])


import time
cur_time_stamp = time.strftime('_%b_%d_%H%M', time.localtime(time.time()))
with open(f'increasing_threads{cur_time_stamp}_ipc.csv', 'w') as f:
    write = csv.writer(f)
    headers = []
    keys = list(bench_dict_ipc.keys())
    for k in keys:
        headers = headers + [k,'']
    write.writerow(headers)
    write.writerow(['Thread#','IPC']*len(keys))

    maxl = max([len(v) for v in bench_dict_ipc.values()])
    for i in range(maxl):
        row = []
        for k in keys:
            if i < len(bench_dict_ipc[k]):
                row = row + [bench_dict_ipc[k][i][0],bench_dict_ipc[k][i][1]]
            else:
                row = row + ['','']
        write.writerow(row)

with open(f'increasing_threads{cur_time_stamp}_util.csv', 'w') as f:
    write = csv.writer(f)
    headers = []
    keys = list(bench_dict_util.keys())
    for k in keys:
        headers = headers + [k,'']
    write.writerow(headers)
    write.writerow(['Thread#','Average Util']*len(keys))

    maxl = max([len(v) for v in bench_dict_util.values()])
    for i in range(maxl):
        row = []
        for k in keys:
            if i < len(bench_dict_util[k]):
                row = row + [bench_dict_util[k][i][0],bench_dict_util[k][i][1]]
            else:
                row = row + ['','']
        write.writerow(row)
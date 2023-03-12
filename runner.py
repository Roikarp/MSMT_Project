#!/usr/bin/env python3
import os
import sys
import ast
import argparse
sys.path.insert(1, f'{os.getcwd()}/classes')
from simulator import Simulator

parser = argparse.ArgumentParser()

# Add the argument for the file path
parser.add_argument("-t", "--threads_path", help="path to the threads traces file")
parser.add_argument("-c", "--config_path", help="path to the execution macro configuration file")
args = parser.parse_args()

# # Case of many traces files to check
# if os.path.isdir(args.threads_path):
#     files = os.listdir(args.threads_path)
#     num_of_simulators = len(files)
#     threads_traces_list = list()
#     for file_path in files:
#         with open(args.threads_path) as f:
#             threads_traces = ast.literal_eval(f.read())
#             threads_traces_list.append(threads_traces)
#
# with open(args.config_path) as f:
#     cfg_dct = ast.literal_eval(f.read())
#
# for k in range(num_of_simulators):
#     simulator = Simulator(threads_traces_list[k], cfg_dct)
#     simulator.simulate_on()
#     simulator.calc_statitstics(to_stdout=True)

# Case of simple case -  one file per each
with open(args.threads_path) as f:
    threads_traces = ast.literal_eval(f.read())

with open(args.config_path) as f:
    cfg_dct = ast.literal_eval(f.read())

simulator = Simulator(threads_traces, cfg_dct)
simulator.simulate_on()
simulator.calc_statitstics(to_stdout=True)



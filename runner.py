#!/usr/bin/env python3
import os
import sys
import ast
import argparse
import multiprocessing
sys.path.insert(1, f'{os.getcwd()}/classes')
from simulator import Simulator

def simulator_generator(thread_traces, cfg_dct, log_file):
    simulator = Simulator(thread_traces, cfg_dct, log_file)
    simulator.simulate_on()
    simulator.calc_statitstics(to_stdout=True)


parser = argparse.ArgumentParser()

# Add the argument for the file path
parser.add_argument("-t", "--threads_path", help="path to the threads traces file")
parser.add_argument("-c", "--config_path", help="path to the execution macro configuration file")
parser.add_argument("-od", "--output_dir", help="path to the dir for loggers")
args = parser.parse_args()

# Case of many traces files to check
if os.path.isdir(args.threads_path):
    files = os.listdir(args.threads_path)
    num_of_simulators = len(files)
    threads_traces_list = list()
    for file_path in files:
        with open(f'{args.threads_path}/{file_path}') as f:
            threads_traces = ast.literal_eval(f.read())
            threads_traces_list.append(threads_traces)
else:
    num_of_simulators = 1
    with open(args.threads_path) as f:
        threads_traces = ast.literal_eval(f.read())
        threads_traces_list = [threads_traces]

with open(args.config_path) as f:
    cfg_dct = ast.literal_eval(f.read())

processes = []
for k in range(num_of_simulators):
    p = multiprocessing.Process(target=simulator_generator,\
                            args=(threads_traces_list[k], cfg_dct, f'{args.output_dir}/logger_{k}.log'))
    processes.append(p)

for p in processes:
    p.start()


# Wait for all simulations to complete
for p in processes:
    p.join()



    # simulator = Simulator(threads_traces_list[k], cfg_dct, f'{args.output_dir}/logger_{k}.log')
    # simulator.simulate_on()
    # simulator.calc_statitstics(to_stdout=True)
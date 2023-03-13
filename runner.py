#!/usr/bin/env python3
import os
import sys
import ast
import argparse
import signal
import multiprocessing
import pdb
sys.path.insert(1, f'{os.getcwd()}/classes')
from simulator import Simulator

def handler(signum, frame):
    print("what do you want?")
    print("1 - abort (default)")
    print("2 - continue ")
    print("3 - debug ")
    user_choice = input()
    global stop_render
    if user_choice=="2":
        pass
    elif user_choice=="3":
        print("debugging!")
        pdb.set_trace()
    else:
        sys.exit()
signal.signal(signal.SIGINT, handler)

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

if num_of_simulators > 1:
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
else:
    simulator_generator(threads_traces_list[0], cfg_dct, f'{args.output_dir}/logger_0.log')

    
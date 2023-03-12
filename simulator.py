#!/usr/bin/env python3
import os
import sys
import ast
from time import sleep

sys.path.insert(1, f'{os.getcwd()}/classes')
from thread import thread
from execution_macro import execution_macro
from scheduler import Scheduler, RoundRobinScheduler, LRUScheduler
from cycle import *

with open(f'{os.getcwd()}/cfg/threads.cfg') as f:
    threads_traces = ast.literal_eval(f.read())

threads = []
for i,f in enumerate(threads_traces):
    cur_thread = thread(f'{os.getcwd()}/trace_files/{f}',i)
    threads.append(cur_thread)

with open(f'{os.getcwd()}/cfg/execution_macro.cfg') as f:
    cfg_dct = ast.literal_eval(f.read())
execution_macro = execution_macro(cfg_dct) 

if cfg_dct['scheduler']['outer_policy'] == 'LRU':
    scheduler = LRUScheduler("outer", threads)
elif cfg_dct['scheduler']['outer_policy'] == 'Round Robin':
    scheduler = RoundRobinScheduler("outer", threads)
else:
    scheduler = Scheduler("outer", threads)

while set([t.is_done() for t in threads]) != {True}:
    # run all parts for 1 cycle
    incr_cycle()
    # if get_cycle() > 130000:
    #     print(f'Cycle {get_cycle()}:')
    #     print(execution_macro)
    # if get_cycle() > 130000 :
    #     for t in threads:
    #         print(t)
    #         for c in t.cmds[:10]:
    #             print(c)
    #     sys.exit()
    # if get_cycle()%10000 == 0:
    #     print(get_cycle())

    if get_cycle()%30000 == 0:
        print(execution_macro)
        for t in threads:
            print (t)

    execution_macro.run()
    execution_macro.pop_done_threads()

    # handle communication between parts
    if execution_macro.has_stuck_threads():
        stuck_threads = execution_macro.pop_stuck_threads()
        # print("NEW THREADS IN SCHED:")
        # for t in stuck_threads:
        #     print(t)
        scheduler.add_thread(stuck_threads)

    if execution_macro.has_free_space():
        new_thread = scheduler.pop_thread()
        if new_thread:
            # print("NEW THREAD IN MACRO:")
            # print(new_thread)
            execution_macro.add_thread(new_thread)


cpi_per_thread = []
total_inst = 0
for t in threads:
    inst_cnt = t.get_inst_cnt()
    print(inst_cnt)
    cpi = get_cycle()/inst_cnt
    cpi_per_thread.append(cpi)

print(cpi_per_thread)


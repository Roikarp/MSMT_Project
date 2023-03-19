#!/usr/bin/env python3
import os
import sys
import ast
import math
from time import sleep
import pdb
import signal
import copy

from thread import thread
from execution_macro import execution_macro
from scheduler import Scheduler, RoundRobinScheduler, LRUScheduler, FaintScheduler
from logger import logger

def handler(signum, frame):
    print("what do you want?")
    print("1 - abort(default)")
    sys.exit()

class Simulator:
    def __init__(self, threads_traces, cfg_dct,logger_path):
        signal.signal(signal.SIGINT, handler)
        self.threads = []
        for i, f in enumerate(threads_traces):
            if f in [t.bench for t in self.threads]:
                print(f'copying data from previous thread: {f}')
                cur_thread = copy.deepcopy([t for t in self.threads if t.bench==f][0])
                print('copy finished')
                cur_thread.thread_id = i
            else:
                print(f'initiating: {os.getcwd()}/trace_files/{f}.trc')
                cur_thread     = thread(f'{os.getcwd()}/trace_files/{f}.trc', i)
                print('initialization finished')

            cur_thread.sim = self
            self.threads.append(cur_thread)

        self.cpi_per_thread = []
        self.usage_per_unit = []
        self.total_cpi = None
        self.fairness = None
        self.sim_done = False
        self.cycle = 0
        self.logger = logger(logger_path)
        self.calculated_mem_miss_rate = 1/(1+math.exp(math.log(9)-0.025*(len(self.threads)-1)**2))

        self.execution_macro = execution_macro(cfg_dct,self)
        self.cfg_dct = cfg_dct

        if cfg_dct['scheduler']['outer_policy'] == 'LRU':
            self.scheduler = LRUScheduler("outer", self.threads)
        elif cfg_dct['scheduler']['outer_policy'] == 'Round Robin':
            self.scheduler = RoundRobinScheduler("outer", self.threads)
        elif cfg_dct['scheduler']['outer_policy'] == 'Faint Pivot':
            self.scheduler = FaintScheduler("outer", self.threads)
        else:
            self.scheduler = Scheduler("outer", self.threads)
        self.scheduler.sim = self

    def get_mem_miss_rate(self):
        return self.calculated_mem_miss_rate

    def simulate_on(self):
        self.cycle = 0
        self.sim_done = False
        while set([t.is_done() for t in self.threads]) == {False}:
            # run all parts for 1 cycle
            self.cycle += 1
            # sleep(0.3)
            # if self.cycle > 130000:
            #     print(f'Cycle {self.cycle}:')
            #     print(self.execution_macro)
            # if self.cycle > 130000 :
            #     for t in self.threads:
            #         print(t)
            #         for c in t.cmds[:10]:
            #             print(c)
            #     sys.exit()

            if self.cycle % 20000 == 0:
                print(self.cycle)

            if self.cycle % 80000 == 0:
                print(self.execution_macro)
                for t in self.threads:
                    print(t)
                    if len(t.cmds) < 20:
                        for c in t.cmds:
                            print(c)
            # if self.cycle > 30:
            #     x = 5
            # for t in self.threads:
            #     print(t)
            #     for c in t.cmds[:10]:
            #         print(c)
            # print(f'Cycle {self.cycle}')
            # print(self.execution_macro)

            # if self.cycle > 1000:
            #     sys.exit()

            self.execution_macro.run()
            self.execution_macro.pop_done_threads()

            # handle communication between parts
            ready_threads = self.scheduler.cnt_pending_threads()
            if self.execution_macro.has_stuck_threads() and ready_threads:
                stuck_threads = self.execution_macro.pop_stuck_threads(ready_threads)
                # print("NEW THREADS IN SCHED:")
                # for t in stuck_threads:
                #     print(t)
                self.scheduler.add_thread(stuck_threads)

            if self.execution_macro.has_free_space():
                new_thread = self.scheduler.pop_thread()
                if new_thread:
                    # print("NEW THREAD IN MACRO:")
                    # print(new_thread)
                    self.execution_macro.add_thread(new_thread)

        self.sim_done = True
        # pdb.set_trace()

    def calc_statitstics(self, to_stdout=False):
        stats_dict = {
            'num_threads': len(self.threads),
            'threads': {},
            'system': {
                'Units Utilization': {},
                'System CPI': None,
                'Jain\'s fairness index': None
            },
            'cfg_dct':self.cfg_dct
        }
        for t in self.threads:
            cpi = t.get_cpi()
            self.cpi_per_thread.append(cpi)
            stats_dict['threads'][f'thread{t.thread_id}'] = {'Name': t.bench, 'CPI': cpi}
            # stats_dict['threads'][f'thread{t.thread_id} Name'] = t.bench
            # stats_dict['threads'][f'thread{t.thread_id} CPI'] = cpi

        for unit in self.execution_macro.execution_units:
            usage = round((unit.active_cycles / self.cycle)*100, 3)
            self.usage_per_unit.append(usage)
            stats_dict['system']['Units Utilization'][f'unit {unit.unit_type} utilization %'] = usage

        self.total_cpi = self.cycle / sum([t.get_inst_cnt() for t in self.threads])

        ipc_per_thread = [1 / cpi for cpi in self.cpi_per_thread]
        self.fairness = (sum(ipc_per_thread) ** 2) / (len(self.threads) * sum([ipc ** 2 for ipc in ipc_per_thread]))
        stats_dict['system']['System CPI'] = self.total_cpi
        stats_dict['system']['Jain\'s fairness index'] = self.fairness

        if to_stdout:
            self.logger.info('thread summary:')
            for i, t in enumerate(self.threads):
                self.logger.info(t)
                self.logger.info(self.cpi_per_thread[i])
            self.logger.info('execution unit summary:')
            for i, unit in enumerate(self.execution_macro.execution_units):
                self.logger.info(unit)
            self.logger.info(f'total cpi:{self.total_cpi}')
            self.logger.info(f'fairness:{self.fairness}')
            self.logger.info(self.cpi_per_thread)
        return stats_dict

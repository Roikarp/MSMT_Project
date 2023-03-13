#!/usr/bin/env python3
import os
import sys
import ast
import math
from time import sleep

from thread import thread
from execution_macro import execution_macro
from scheduler import Scheduler, RoundRobinScheduler, LRUScheduler, FaintScheduler
from logger import logger

class Simulator:
    def __init__(self, threads_traces, cfg_dct,logger_path):
        self.threads = []
        for i, f in enumerate(threads_traces):
            cur_thread     = thread(f'{os.getcwd()}/trace_files/{f}', i)
            cur_thread.sim = self
            self.threads.append(cur_thread)

        self.cpi_per_thread = []
        self.usage_per_unit = []
        self.total_cpi = None
        self.fairness = None
        self.sim_done = False
        self.cycle = 0
        self.logger = logger(logger_path)
        self.calculated_mem_miss_rate = 1/(1+math.exp(math.log(9)-0.25*(len(self.threads)-1)))

        self.execution_macro = execution_macro(cfg_dct,self)

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
        while set([t.is_done() for t in self.threads]) != {True}:
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

            if self.cycle % 10000 == 0:
                print(self.cycle)

            if self.cycle % 30000 == 0:
                print(self.execution_macro)
                for t in self.threads:
                    print(t)
            #         for c in t.cmds[:10]:
            #             print(c)
            if self.cycle > 30:
                x = 5
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
            if self.execution_macro.has_stuck_threads():
                stuck_threads = self.execution_macro.pop_stuck_threads()
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

    def calc_statitstics(self, to_stdout=False):
        for t in self.threads:
            cpi = t.get_cpi()
            self.cpi_per_thread.append(cpi)

        for unit in self.execution_macro.execution_units:
            usage = unit.active_cycles / self.cycle
            self.usage_per_unit.append(usage)

        self.total_cpi = self.cycle / sum([t.get_inst_cnt() for t in self.threads])

        ipc_per_thread = [1 / cpi for cpi in self.cpi_per_thread]
        self.fairness = (sum(ipc_per_thread) ** 2) / (len(self.threads) * sum([ipc ** 2 for ipc in ipc_per_thread]))

        if to_stdout:
            print('Thread summary:')
            for i, t in enumerate(self.threads):
                print(t)
            print('Execution unit summary:')
            for i, unit in enumerate(self.execution_macro.execution_units):
                print(unit)
            print(f'Total cpi:{self.total_cpi}')
            print(f'Fairness:{self.fairness}')
        print(f'Total simulation was {self.cycle} cycles')

        self.logger.info('Thread summary:')
        for i, t in enumerate(self.threads):
            self.logger.info(t)
        self.logger.info('Execution unit summary:')
        for i, unit in enumerate(self.execution_macro.execution_units):
            self.logger.info(unit)
        self.logger.info(f'Total cpi:{self.total_cpi}')
        self.logger.info(f'Fairness:{self.fairness}')
        self.logger.info(f'Total simulation was {self.cycle} cycles')

#!/usr/bin/env python3
from unit import unit
from scheduler import Scheduler, RoundRobinScheduler, LRUScheduler, FaintScheduler

class execution_macro:
    def __init__(self,cfg_dct,sim):
        macro_dict = cfg_dct['execution_macro']
        self.max_threads            = macro_dict['max_threads']
        self.context_switch_penalty = macro_dict['context_switch_penalty']
        self.inst_window_size       = macro_dict['inst_window_size']
        self.threads                = []
        self.sim                    = sim

        self.execution_units = []
        for unit_type in ['st_ld','alu','alu_st_ld','fp','fp_st_ld','br','br_st_ld','misc','misc_st_ld']:
            for i in range(macro_dict[f'{unit_type}_unit_num']):
                self.execution_units.append(unit(cfg_dct[f'{unit_type}_unit'],sim))

        if cfg_dct['scheduler']['inner_policy'] == 'LRU':
            self.sched = LRUScheduler("inner", self.threads)
        elif cfg_dct['scheduler']['inner_policy'] == 'Round Robin':
            self.sched = RoundRobinScheduler("inner", self.threads)
        elif cfg_dct['scheduler']['inner_policy'] == 'Faint Pivot':
            self.sched = FaintScheduler("inner", self.threads)
        else:
            self.sched = Scheduler("inner", self.threads)
        self.sched.sim = sim

    def run(self):
        for t in self.threads:
            if t.state == 'pending':
                t.state = 'running'
        for unit in self.execution_units:
            if not unit.is_active():
                inst = unit.pop_inst_output()
                if inst:
                    inst.add_to_thread()
            else:
                unit.run()

            if unit.free():
                inst = self._get_inst_by_type(unit.unit_type)
                # print(inst)
                if inst:
                    unit.add_inst(inst)


    def _get_inst_by_type(self,inst_type): #Scheduler
        t = self.sched.choose_thread(inst_type,self.inst_window_size)
        if t is None:
            return None
        return t.pop_by_type(inst_type,self.inst_window_size)

    def has_stuck_threads(self):
        for t in self.threads:
            if t.is_missed():
                return True
        return False

    def pop_stuck_threads(self,cnt):
        stuck_threads = []
        i = 0
        for t in self.threads:
            if t.is_missed():
                stuck_threads.append(t)
                i += 1
                if i >= cnt:
                    break
        for t in stuck_threads:
            self.sched.remove_thread(t)
        self.threads = [t for t in self.threads if t not in stuck_threads]
        return stuck_threads

    def has_free_space(self):
        return len(self.threads) < self.max_threads

    def add_thread(self,t):
        t.set_context_switch(self.context_switch_penalty)
        self.threads.append(t)
        self.sched.add_thread(t)
        if len(self.threads) > self.max_threads:
            print("ERROR")

    def pop_done_threads(self):
        for t in self.threads:
            if t.is_done():
                t.set_done()
                self.sched.remove_thread(t)
        self.threads = [t for t in self.threads if not t.is_done()]

    def __str__(self):
        s = ''
        s += '=== Execution Macro ===\n'
        s += 'Threads:\n'
        for t in self.threads:
            s += str(t).splitlines()[0]+ '\n'
        s += '\nUnits:\n==========\n'
        for i , u in enumerate(self.execution_units):
            us = ' '+'\n '.join(str(u).splitlines())
            s += f'{i}{(3-len(str(i)))*" "}: {us}\n'

        return s
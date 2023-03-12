#!/usr/bin/env python3
from unit import unit
from scheduler import Scheduler, RoundRobinScheduler, LRUScheduler

class execution_macro:
    def __init__(self,cfg_dct):
        macro_dict = cfg_dct['execution_macro']
        self.max_threads            = macro_dict['max_threads']
        self.context_switch_penalty = macro_dict['context_switch_penalty']
        self.inst_window_size       = macro_dict['inst_window_size']
        self.threads                = []

        self.store_load_units = []
        for i in range(macro_dict["store_load_unit_num"]):
            self.store_load_units.append(unit(cfg_dct["store_load_unit"]))

        self.alu_units = []
        for i in range(macro_dict["alu_unit_num"]):
            self.alu_units.append(unit(cfg_dct["alu_unit"]))

        self.fp_units = []
        for i in range(macro_dict["fp_unit_num"]):
            self.fp_units.append(unit(cfg_dct["fp_unit"]))

        self.br_units = []
        for i in range(macro_dict["br_unit_num"]):
            self.br_units.append(unit(cfg_dct["br_unit"]))

        self.misc_units = []
        for i in range(macro_dict["misc_unit_num"]):
            self.misc_units.append(unit(cfg_dct["misc_unit"]))


        self.sched                  = Scheduler('inner',[])

        self.execution_units = self.store_load_units \
                             + self.alu_units \
                             + self.fp_units \
                             + self.br_units \
                             + self.misc_units 
    def run(self):
        for unit in self.execution_units:
            if not unit.active():
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

    def pop_stuck_threads(self):
        stuck_threads = [t for t in self.threads if t.is_missed()]
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
                t.state = 'done'
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
            us = '    '+'\n    '.join(str(u).splitlines())
            s += f'{i}: {us}\n'

        return s
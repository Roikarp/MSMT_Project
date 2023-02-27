#!/usr/bin/env python3
from unit import unit
from scheduler import scheduler

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


        self.sched                  = scheduler()

    def run(self):
        execution_units = self.store_load_units \
                        + self.alu_units \
                        + self.fp_units \
                        + self.br_units \
                        + self.misc_units 

        for unit in execution_units:
            if not unit.active():
                inst = unit.pop_inst_output()
                if inst:
                    inst.add_to_thread()
            else:
                unit.run()

            if unit.free():
                inst = self._get_inst_by_type(unit.unit_type)
                if inst:
                    unit.add_inst(inst)


    def _get_inst_by_type(self,inst_type): #Scheduler
        t = self.sched.choose_thread(inst_type)
        if t is None:
            return None
        return t.pop_by_type(inst_type,self.inst_window_size)

    def has_stuck_threads(self):
        for t in self.threads:
            if t.stuck():
                return True
        return False

    def pop_stuck_threads(self):
        stuck_threads = [t for t in self.threads if t.stuck()]
        self.threads = [t for t in self.threads if t not in stuck_threads]
        return stuck_threads

    def has_free_space(self):
        return len(self.threads) < self.max_threads

    def add_thread(self,t):
        t.set_context_switch(self.context_switch_penalty)
        self.threads.append(t)
        if len(self.threads) > self.max_threads:
            print("ERROR")

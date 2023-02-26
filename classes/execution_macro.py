#!/usr/bin/env python3

class execution_macro:
    def __init__(self):
        self.max_threads            = 0
        self.threads                = []
        self.context_switch_penalty = 0

        self.store_load_units       = []
        self.alu_units              = []
        self.fp_units               = []
        self.br_units               = []
        self.misc_units             = []

        self.sched                  = None

    def run():
        execution_units = self.store_load_units 
                        + self.alu_units 
                        + self.fp_units 
                        + self.br_units 
                        + self.misc_units 

        for unit in execution_units:
            if not unit.active():
                inst = unit.pop_inst_output()
                if inst:
                    inst.add_to_thread()
            else:
                unit.run()

            if unit.free():
                inst = self._get_inst_by_type(unit.type)
                if inst:
                    unit.add_inst(inst)


    def _get_inst_by_type(self,inst_type): #Scheduler
        t = self.sched.choose_thread(inst_type)
        if t is None:
            return None
        return t.pop_by_type(inst_type)

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
